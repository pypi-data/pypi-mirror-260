'''
[![npm (scoped)](https://img.shields.io/npm/v/@catnekaise/actions-constructs?style=flat-square)](https://www.npmjs.com/package/@catnekaise/actions-constructs)
[![Nuget](https://img.shields.io/nuget/v/Catnekaise.CDK.ActionsConstructs?style=flat-square)](https://www.nuget.org/packages/Catnekaise.CDK.ActionsConstructs/)
[![PyPI](https://img.shields.io/pypi/v/catnekaise.cdk-actions-constructs?style=flat-square)](https://pypi.org/project/catnekaise.cdk-actions-constructs/)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/catnekaise/actions-constructs?sort=semver&style=flat-square)](https://github.com/catnekaise/actions-constructs/releases)

# Actions Constructs

AWS CDK Constructs for integrating GitHub Actions and AWS.

### Table of Contents

* ["Legacy" Constructs](#legacy-constructs)
* [ActionsIdentityPoolV2](#actionsidentitypoolv2)

  * [Usage](#usage)
  * [Usage - GitHub Actions](#usage---github-actions)
  * [OpenID Connect Provider](#openid-connect-provider)

    * [Audience](#audience)
  * [Mapped Claims](#mapped-claims)

    * [Custom Tag Names](#custom-tag-names)
    * [Library Tag Abbreviations](#library-tag-abbreviations)
  * [Enhanced AuthFlow](#enhanced-authflow)
* [ActionsIdentityPolicyUtility](#actionsidentitypolicyutility)

  * [Philosophy](#philosophy)
  * [Constraints](#constraints)

    * [Example](#example)

      * [Regular Usage](#regular-usage)
      * [With Policy Utility](#with-policy-utility)
  * [Policy Constraining](#policy-constraining)
  * [Policy Variable and PrincipalTagConditionKey](#policy-variable-and-principaltagconditionkey)
  * [ActionsIdentityConstraints](#actionsidentityconstraints)

    * [Constraints and CDK](#constraints-and-cdk)
  * [Resource Paths](#resource-paths)

    * [ToString](#tostring)
    * [More Examples](#more-examples)
  * [Role-Chaining (Cross Account)](#role-chaining-cross-account)
  * [Role Chaining in Workflows](#role-chaining-in-workflows)
  * [Passing Claims](#passing-claims)

    * [Trust Policy](#trust-policy)
* [Entrypoint Account](#entrypoint-account)

  * [Grant Organization Role Chain](#grant-organization-role-chain)

    * [Policy Statement](#policy-statement)
* [Additional Roles](#additional-roles)

  * [Same Stack](#same-stack-)
  * [Separate Stack](#separate-stack)

### "Legacy" Constructs

Will continue to be supported.

* [ActionsIdentityPool](./docs/actions-identity-pool/actions-identity-pool.md)
* [ActionsIdentityPoolBasic](./docs/actions-identity-pool/actions-identity-pool-basic.md)

# ActionsIdentityPoolV2

> Detailed explanation of the use-case can be found [here](https://catnekaise.github.io/github-actions-abac-aws/cognito-identity/).

Use this to create a Cognito Identity Pool that allows GitHub Actions to authenticate and receive temporary AWS credentials that has session/principal tags corresponding with the GitHub Actions claims. This enables attribute-based access control (ABAC) to AWS resources from GitHub Actions.

## Usage

```python
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cdk from 'aws-cdk-lib';
import {
  ActionsIdentityPoolV2,
  ActionsIdentityMappedClaims,
  GitHubActionsClaimConstraint,
} from '@catnekaise/actions-constructs';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'CatnekaiseActionsIdentityExampleStack');

// More details about OIDC Provider further below.
const openIdConnectProvider = iam.OpenIdConnectProvider
        .fromOpenIdConnectProviderArn(stack, 'Provider', `arn:aws:iam::${stack.account}:oidc-provider/token.actions.githubusercontent.com`);

const pool = new ActionsIdentityPoolV2(stack, 'Pool', {
  authenticatedRoleConstraints: [
    // change value to the name(s) of your GitHub organization(s) that shall be allowed to authenticate
    GitHubActionsClaimConstraint.repoOwners('catnekaise'),
  ],
  mappedClaims: ActionsIdentityMappedClaims.create(GhaClaim.REPOSITORY, GhaClaim.ACTOR, GhaClaim.RUNNER_ENVIRONMENT),
  authenticatedRoleName: 'GhaCognito', // Optional
  openIdConnectProvider,
});
```

## Usage - GitHub Actions

If having used the example above you can test it by using the workflow below. Make sure to update the values to match your environment.

Also, make sure the [OIDC Provider Audience](#audience) has been configured with whichever audience is used below.

```yaml
on:
  workflow_dispatch:
jobs:
  job1:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: "Get Credentials from Amazon Cognito Identity"
        uses: catnekaise/cognito-idpool-auth@v1
        with:
          # Change values below to match your setup
          auth-flow: "basic"
          cognito-identity-pool-id: "eu-west-1:11111111-example"
          aws-role-arn: "arn:aws:iam::111111111111:role/GhaCognito"
          aws-region: "eu-west-1"
          audience: "cognito-identity.amazonaws.com"
          aws-account-id: "111111111111"
          set-in-environment: true

      - name: "STS Get Caller Identity"
        run: |
          aws sts get-caller-identity
```

## OpenID Connect Provider

* If no OIDC Provider is defined in the props given to ActionsIdentityPoolV2 it will try to import the provider from the AWS Account where the pool is being created.
* If the OIDC Provider does not exist in the target account, the construct cannot be deployed.
* If using GitHub Enterprise with a customized issuer, then import/create that provider and explicitly define it in the props.

```python
const stack = new cdk.Stack(new cdk.App(), 'CatnekaiseActionsIdentityExampleStack');

// Example for creating the OIDC Provider in the same stack as the Identity Pool
const openIdConnectProvider = new iam.OpenIdConnectProvider(stack, 'Provider', {
  url: 'https://token.actions.githubusercontent.com',
  // Keep sts.amazonaws.com if also using account to assume roles directly via STS
  clientIds: ['cognito-identity.amazonaws.com', 'sts.amazonaws.com'],
});

const pool = new ActionsIdentityPoolV2(stack, 'Pool', {
  openIdConnectProvider,
  // ...
});
```

### Audience

If the provider already exist, go ahead and add the clientId (audience) `cognito-identity.amazonaws.com` to the existing provider. This is the audience used as default value for actions `catnekaise/cognito-idpool-auth` and `catnekaise/cognito-idpool-auth-basic`.

## Mapped Claims

Because there's a limit for how much data can be put into a session in AWS, not all existing GitHub Actions claims can be mapped by Cognito Identity. Attempting to map all (or too many) claims will result in failure when assuming a role.

`ActionsIdentityMappedClaims` is used for selecting which claims should be mapped in the identity pool. It can also be used to map claims using different tag names than the claim name. Using shorter tag names gives room for mapping additional claims and staying under the limit. Further details for how to manage the session limit can be found [here](https://catnekaise.github.io/github-actions-abac-aws/detailed-explanation/#session-limit).

A good starting point of which claims to map that should not affect these limits:

```python
const mappedClaims = ActionsIdentityMappedClaims.create(
        GhaClaim.REPOSITORY,
        GhaClaim.ACTOR,
        GhaClaim.RUN_ID,
        GhaClaim.SHA,
        GhaClaim.REF,
        GhaClaim.JOB_WORKFLOW_REF,
);
```

### Custom Tag Names

Claims can be mapped to a tag with a different name than the original claim. The key is the name of the claim and value will become name of the tag.

```python
const mappedClaims = ActionsIdentityMappedClaims.createCustom({
  repository: 'repo',
  job_workflow_ref: 'jWorkRef'
})
```

### Library Tag Abbreviations

This library has a set of abbreviations that can be used to shorten the tag names. Value of the abbreviation tag names can be found in [claims.ts](./src/identity-pool/claims.ts).

```python
const mappedClaims = ActionsIdentityMappedClaims.createWithAbbreviations(
        // becomes `repo` instead of `repository`
        GhaClaim.REPOSITORY,
        // becomes `jWorkRef` instead of `job_workflow_ref`
        GhaClaim.JOB_WORKFLOW_REF,
);
```

## Enhanced AuthFlow

> [!NOTE]
> Using the `basic` auth-flow will feel the most similar to how you have been using GitHub Actions OIDC with AWS STS today, so it may be a better starting point than the `enhanced` auth-flow.

By default the `ActionsIdentityPoolV2` uses the `Basic (Classic) AuthFlow` but it can also be configured to use the `Enhanced (Simplified) AuthFlow`.

Using the enhanced auth-flow requires an extra step where a role-assignment is made. More details about the differences of these auth-flows in the context of GitHub Actions can be found [here](https://catnekaise.github.io/github-actions-abac-aws/detailed-explanation/#authentication-flows).

```python
const pool = new ActionsIdentityPoolV2(stack, 'Pool', {
  useEnhancedAuthFlow: true,
  // other props
});

const role: iam.Role = pool.defaultAuthenticatedRole;

// The claims used in role assignment does not have to be claims that are mapped in the identity pool.
pool.enhancedFlowAssignRole(role, GhaClaim.REPOSITORY_OWNER, EnhancedFlowMatchType.EQUALS, 'catnekaise');
```

# ActionsIdentityPolicyUtility

Use the policy utility to:

* Create principals (trust policy) for additional IAM Roles assumed via Cognito Identity
* Create principals (trust policy) for IAM Roles assumed via the roles above (role-chaining)
* Build resource paths containing a mix of text and GitHub Actions claims
* Append grants with conditions based on claims from GitHub Actions
* Append policy statements with conditions based on claims from GitHub Actions

```python
import { ActionsIdentityPoolV2, ActionsIdentityPolicyUtility } from '@catnekaise/actions-constructs';

declare const pool: ActionsIdentityPoolV2;

// Available via ActionsIdentityPoolV2
let policyUtility = pool.policyUtility;

// Configure separately
policyUtility = ActionsIdentityPolicyUtility.create(scope, {
  mappedClaims: ActionsIdentityMappedClaims.create(GhaClaim.REPOSITORY /** additional claims **/),
  // Additional utility configuration
});
```

## Philosophy

The `ActionsIdentityPolicyUtility` aims to make it as easy as possible to work with the GitHub Actions claims while minimizing interference with how you work with AWS CDK today.

* The utility prevents you from using claims you have not mapped in your identity pool.
* The utility will select correct tag names if you have mapped a claim to a tag with a different name.
* Any changes to mapped claims configuration is reflected in any conditions or resource paths created via the policy utility

## Constraints

In the context of this library (and [catnekaise/cdk-iam-utilities](https://github.com/catnekaise/cdk-iam-utilities)), constraining is the act of appending existing `iam.PolicyStatement(s)` with conditions. One applied constraint may conditionally add `none`, `one` or `many` conditions to the provided policy statement(s).

The goal of constraints is to simplify working with the condition block of a policy statement when there are many conditions being used, and to help make working with the conditions "contextual" to the task at hand, such as creating policies for GitHub Actions attribute based access controls.

### Example

Using the existing functionality in CDK of granting a role the permissions to read and write in a S3 bucket, there are these example requirements:

* Can only read/write to an object prefix that matches `artifacts/workflow_run/${{ github.repository }}/${{ github.run_id }}/*`
* Can only read/write when workflow is running on a `self-hosted` runner
* Can only read/write when workflows running is a re-usable workflow on the `main` branch in repository `catnekaise/shared-workflows`

#### Regular Usage

```python
declare const bucket: s3.Bucket;

const grant = bucket.grantReadWrite(role,
        'artifacts/workflow_run/${aws:principalTag/repository}/${aws:principalTag/run_id}/*',
);

grant.principalStatements[0].addCondition('StringEquals', {
  'aws:principalTag/runner_environment': 'self-hosted',
});

grant.principalStatements[0].addCondition('StringLike', {
  'aws:principalTag/job_workflow_ref': 'catnekaise/shared-workflows/.github/workflows/*@refs/heads/main',
});
```

#### With Policy Utility

```python
declare const pool: ActionsIdentityPoolV2;
declare const bucket: s3.Bucket;

const grant = bucket.grantReadWrite(role,
        pool.policyUtility.util.resourcePath('artifacts/workflow_run', GhaClaim.REPOSITORY, GhaCLaim.RUN_ID, '*'),
);

pool.policyUtility.constrainGrant(grant)
        .whenSelfHosted()
        .jobWorkflowLike('catnekaise', 'shared-workflows', '*', 'refs/heads/main');
```

## Policy Constraining

A single policy statement can be constrained in the same way as a grant.

```python
declare const role: iam.Role;
declare const pool: ActionsIdentityPoolV2;

const policy = new iam.PolicyStatement({
  effect: iam.Effect.ALLOW,
  actions: ['ssm:GetParameter'],
  resources: ['*'],
});

pool.policyUtility.constrain(policy)
        .hasResourceTagEqualToClaim('repository', GhaClaim.REPOSITORY);

role.addToPolicy(policy);
```

## Policy Variable and PrincipalTagConditionKey

It's also possible to create individual policy variables and/or principal tags via the policy utility and use them in condition statements. Any changes made to the mapped claims configurations will be reflected in variables/tags created via the policy utility.

```python
import { ActionsIdentityPolicyUtility, GhaClaim } from '@catnekaise/actions-constructs';

const policyUtility = ActionsIdentityPolicyUtility.create(scope, {
  mappedClaims: ActionsIdentityMappedClaims.create(GhaClaim.REPOSITORY, GhaClaim.ACTOR),
});

const policyVariable = policyUtility.policyVar(GhaClaim.REPOSITORY);
const principalTag = policyUtility.principalTagConditionKey(GhaClaim.ACTOR);

const policy = new iam.PolicyStatement({
  conditions: {
    StringEquals: {
      [principalTag.toString()]: 'catnekaise/example-repo',
      'aws:ResourceTag/owner': policyVariable.toString(),
    },
  },
});
```

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Condition": {
        "StringEquals": {
          "aws:PrincipalTag/repository": "catnekaise/example-repo",
          "aws:ResourceTag/owner": "${aws:PrincipalTag/actor}"
        }
      }
    }
  ]
}
```

## ActionsIdentityConstraints

When working with constraints via the policy utility you will be using `ActionsIdentityConstraints` where convenience methods has been created for some common scenarios such as `whenSelfHosted()` and `repoOwners('catnekaise', 'additional-org')`.

These convenience methods do cover all possible scenarios. The following methods can be used for those scenarios.

```python
import { ConditionOperator } from '@catnekaise/cdk-iam-utilities';

pool.policyUtility.newPrincipalBuilder()
        .claimEquals(GhaClaim.REPOSITORY_VISIBILITY, 'public') // StringEquals
        .claimLike(GhaClaim.ENVIRONMENT, 'dev-*') // StringLike
        .claimCondition(ConditionOperator.STRING_NOT_EQUALS, GhaClaim.ENVIRONMENT, 'dev-custom');
```

### Constraints and CDK

Whether on a single policy statement or on several policy statements included in a grant, each condition is added to each policy statement via `policyStatement.addCondition()`. If the combination of `Operator` and `ConditionKey` already exists, existing value(s) gets replaced.

```python
declare const role: iam.Role;
declare const pool: ActionsIdentityPoolV2;

const policy = new iam.PolicyStatement({
  effect: iam.Effect.ALLOW,
  actions: [],
  resources: [],
  conditions: {
    StringEquals: {
      'aws:PrincipalTag/runner_environment': 'github-hosted',
    },
  },
});

// Condition value runner_environment is changed from github-hosted to self-hosted
pool.policyUtility.constrain(policy).whenSelfHosted();

// Condition value is changed from self-hosted to github-hosted
policy.addCondition('StringEquals', { 'aws:PrincipalTag/runner_environment': 'self-hosted' });

role.addToPolicy(policy);
```

## Resource Paths

Concatenate strings and claims to a resource path. All examples below results in the resource path: `items/${aws:principalTag/repository}/${aws:principalTag/environment}/*`.

```python
declare const pool: ActionsIdentityPoolV2;
declare const bucket: s3.Bucket;

let resourcePath: string;

resourcePath = policyUtility.resourcePath('items', GhaClaim.REPOSITORY, GhaCLaim.ENVIRONMENT, '*').toString();

resourcePath = policyUtility.resourcePath()
        .text('items')
        .claim(GhaClaim.REPOSITORY, GhaClaim.ENVIRONMENT)
        .text('*').toString();

resourcePath = policyUtility.resourcePath('items')
        .value(GhaClaim.REPOSITORY, GhaClaim.ENVIRONMENT, '*').toString();

const grant = bucket.grantReadWrite(role, resourcePath);
```

### ToString

While some CDK constructs allow passing in resource paths of `any` type and will implicitly invoke the toString() method, it's best to invoke toString() before passing the resource path to where it will be used.

### More Examples

```python
import { ActionsIdentityPoolV2 } from '@catnekaise/actions-constructs';

declare const pool: ActionsIdentityPoolV2;
declare const bucket: s3.Bucket;
declare const terraformStateTable: dynamodb.TableV2;

// Allow Github Actions to store cache to an S3 bucket in context of repository and the ref that is running
bucket.grantReadWrite(pool.defaultAuthenticatedRole,
        pool.policyUtility.resourcePath('cache', GhaClaim.REPOSITORY, GhaCLaim.REF, '*'));

// Allow Github Actions to upload/download artifacts in context of repository and the specific workflow run
bucket.grantReadWrite(pool.defaultAuthenticatedRole,
        pool.policyUtility.resourcePath('artifacts/workflow_run', GhaClaim.REPOSITORY, GhaCLaim.RUN_ID, '*'));


// Allow terraform running in GitHub Actions to to acquire state lock, but only on the combination of repository and environment running
const tableGrant = terraformStateTable.grant(pool.defaultAuthenticatedRole, 'dynamodb:DescribeTable', 'dynamodb:GetItem', 'dynamodb:PutItem', 'dynamodb:DeleteItem');
tableGrant.principalStatements.addCondition('ForAllValues:StringEquals', {
  'dynamodb:LeadingKeys': [
    pool.policyUtility.resourcePath(GhaClaim.REPOSITORY, GhaClaim.ENVIRONMENT, 'terraform.tfstate').toString(),
  ],
});
```

## Role-Chaining (Cross Account)

The example below can be split into separate CDK Apps.

```python
const poolStack = new cdk.Stack(app, 'PoolStack', {
  env: {
    region: 'eu-west-1',
    account: '111111111111',
  },
});

const workloadStack = new cdk.Stack(app, 'WorkloadStack', {
  env: {
    region: 'eu-west-1',
    account: '222222222222',
  },
});

workloadStack.addDependency(poolStack);

const mappedClaims = ActionsIdentityMappedClaims.create(GhaClaim.REPOSITORY, GhaClaim.ENVIRONMENT);

const pool = new ActionsIdentityPoolV2(poolStack, 'Pool', {
  authenticatedRoleConstraints: [
    // change value to the name(s) of your GitHub organization(s) or username(s) that shall be allowed to authenticate
    GitHubActionsClaimConstraint.repoOwners('catnekaise'),
  ],
  mappedClaims,
  authenticatedRoleName: 'GhaCognito',
});

pool.defaultAuthenticatedRole.grantAssumeRole(new iam.SessionTagsPrincipal(new iam.ArnPrincipal('arn:aws:iam::222222222222:role/github-actions/WorkloadDeploymentDev')));


new iam.Role(workloadStack, 'Role', {
  roleName: 'WorkloadDeploymentDev',
  path: '/github-actions/',
  assumedBy: util.newChainedPrincipalBuilder()
          .repositoryEquals('catnekaise/workload-repo')
          .environmentEquals('dev')
          .createPrincipalAssumedBy(workloadStack, new iam.AccountPrincipal('111111111111'), {
            // Read more about passing claims further below
            passClaims: mappedClaims.toPassClaims(),
          }),
});
```

## Role Chaining in Workflows

For more information, read documentation at [catnekaise/cognito-idpool-auth](https://github.com/catnekaise/cognito-idpool-auth)

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        required: true
        description: Environment

jobs:
  job1:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    permissions:
      id-token: write
      contents: read
    steps:
      - name: "Get Credentials from Amazon Cognito Identity"
        uses: catnekaise/cognito-idpool-auth@v1
        with:
          # Change values below to match your environment
          cognito-identity-pool-id: "eu-west-1:11111111-example"
          aws-role-arn: "arn:aws:iam::111111111111:role/GhaCognito"
          aws-region: "eu-west-1"
          audience: "cognito-identity.amazonaws.com"
          aws-account-id: "111111111111"
          set-in-environment: true
          role-chain-pass-claims: "repository,environment"
          role-chain-arn: "arn:aws:iam::222222222222:role/WorkloadDevDeployment"
```

## Passing Claims

In the context of this library, passing claims means tagging the next session with one or more of the GitHub Actions claims present in the current role session. Doing this is optional, but it makes it possible to use the GitHub Actions claims with policies inside the workload account.

In order to not allow the workflow to alter the value of claims during role chaining or setting any additional session tags, the trust policy in the workload account needs to be configured accordingly.

```python
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cdk from 'aws-cdk-lib';
import { ActionsIdentityPolicyUtility, ActionsIdentityMappedClaims, GhaClaim } from '@catnekaise/actions-constructs';

const stack = new cdk.Stack(new cdk.App(), 'WorkloadStack');

const mappedClaims = ActionsIdentityMappedClaims.create(GhaClaim.ACTOR, GhaClaim.REPOSITORY, GhaClaim.SHA, GhaClaim.REF, GhaClaim.ENVIRONMENT);

// All claims will have to be defined as session tags when using AssumeRole
const passAllClaims = mappedClaims.toPassClaims();

// Only the Repository and Environment claim has to be set when using AssumeRole
const passSomeClaims = mappedClaims.toPassClaims(GhaClaim.ENVIRONMENT, GhaClaim.REPOSITORY);

// Only Repository and Environment has to be set, but has to be set with customized tag names
const passCustomClaims = mappedClaims.toPassClaimsCustom({
  // claim: tagName
  repository: 'repo',
  environment: 'github_environment',
});

// Allows directly using the configure-aws-credentials action: https://github.com/aws-actions/configure-aws-credentials#session-tagging-and-name
// Note: The only real claims passable using this is: Repository, Actor, Sha and Ref
const passConfigureAwsCredentialsClaims = mappedClaims.toConfigureAwsCredentialsPassClaims();

const util = ActionsIdentityPolicyUtility.create(stack, {
  mappedClaims,
});

new iam.Role(workloadStack, 'Role', {
  roleName: 'WorkloadRole',
  assumedBy: util.newChainedPrincipalBuilder()
          .repositoryEquals('catnekaise/workload-repo')
          .environmentEquals('dev')
          .createPrincipalAssumedBy(workloadStack, new iam.AccountPrincipal('111111111111'), {
            // Set one of the examples above
            passClaims: passSomeClaims,
          }),
});
```

### Trust Policy

The example above would produce this trust policy:

```json5
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111111111111:root"
      },
      "Action": [
        "sts:AssumeRole",
        "sts:TagSession"
      ],
      "Condition": {
        "StringEquals": {
          // Requires role was assumed via Cognito Identity
          "aws:FederatedProvider": "cognito-identity.amazonaws.com",
          // Requires that value of current session tags equals the following environment and repository
          "aws:PrincipalTag/environment": "dev",
          "aws:PrincipalTag/repository": "catnekaise/workload-repo",
          // Requires setting session tags with same value as current session tags
          "aws:RequestTag/environment": "${aws:principalTag/environment}",
          "aws:RequestTag/repository": "${aws:principalTag/repository}"
        },
        "ForAllValues:StringEquals": {
          // Requires that only the two following session tags are set
          "aws:TagKeys": [
            "repository",
            "environment"
          ]
        }
      }
    }
  ]
}
```

# Entrypoint Account

In the context of this library (and its associated documentation), an `entrypoint` account is a production AWS account in an organization that is trusted to have correctly configured Cognito Identity, associated AWS IAM Roles and their permissions. This account is where GitHub Actions authentication starts.

The AWS credentials received from the Cognito Identity Pool in the entrypoint account is primarily used to perform role chaining into many workload accounts.

## Grant Organization Role Chain

When assuming a role cross-account, the role that performs `AssumeRole` needs permissions to do this (in addition to the cross-account role trust policy allowing the assumption to begin with). In order to not have to add permission for each individual workload role that an identity pool role shall be allowed to assume, and in order to not grant the same role the ability to assume any roles that have a weak trust policy, `grantOrganizationRoleChain` can be used.

`grantOrganizationRoleChain` provides an opinionated interface of granting the type of permissions required to meet the criteria above.

```python
import { ActionsIdentityPoolV2 } from '@catnekaise/actions-constructs';

declare const pool: ActionsIdentityPoolV2;

pool.policyUtility.grantOrganizationRoleChain(pool.defaultAuthenticatedRole, {
  // One of rolePath or roleHasResourceTags is required, or both.
  rolePath: '/github-actions/',
  roleHasResourceTags: {
    usedViaGitHubActions: '1',
  },
  // Optional
  resourceOrgPaths: ['o-example/r-ab12/ou-ab12-11111111/*'],
  // Optional
  // Identity Pool AWS Account ID is automatically excluded when using policyUtility via ActionsIdentityPoolV2
  excludeAccountIds: ['333333333333', '444444444444'],
});
```

### Policy Statement

The following permissions are granted to the role in the example above.

```json5
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "sts:TagSession",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "sts:AssumeRole",
      // Limited to assuming workload roles under path /github-actions/
      "Resource": "arn:aws:iam::*:role/github-actions/*",
      "Condition": {
        "StringEquals": {
          // Limited to assuming workload roles that have the following tag
          "aws:ResourceTag/usedViaGitHubActions": "1",
          // Limit to assuming roles within the same organization as the current role
          "aws:ResourceOrgID": "${aws:PrincipalOrgID}"
        },
        "StringNotEquals": {
          // Shall explicitly not be allowed to assume roles in identity pool account (111111111111)
          // Shall explicitly not be allowed to assume roles in accounts 333333333333, 444444444444
          "aws:ResourceAccount": ["111111111111", "333333333333", "444444444444"]
        },
        "ForAnyValue:StringLike": {
          // Shall only be allowed to assume roles under the following organization path
          "aws:ResourceOrgPaths": [
            "o-example/r-ab12/ou-ab12-11111111/*"
          ]
        }
      }
    }
  ]
}
```

# Additional Roles

More roles can be created and assumed via a Cognito Identity Pool. If using the `enhanced` auth-flow, these roles must exist in the same AWS account as the identity pool. If using the `basic` auth-flow, these roles can be created in any AWS Account and reference the ID of the identity pool.

Using the [ActionsIdentityPolicyUtility](#actionsidentitypolicyutility), the trust policies for these roles can be created that align with the configuration of an identity pool in any stack.

## Same Stack

```python
declare const pool: ActionsIdentityPoolV2;

const principal = pool.policyUtility.newPrincipalBuilder()
        .repositoryEquals('catnekaise/workload-repo')
        .createPrincipal(pool);

const role = new iam.Role(scope, 'AdditionalRole', {
  assumedBy: principal,
});

// If using the enhanced auth-flow, assignment must be configured
pool.enhancedFlowAssignRole(role, GhaClaim.REPOSITORY, EnhancedFlowMatchType.EQUALS, 'catnekaise/workload-repo');
```

## Separate Stack

```python
import { ActionsIdentityPolicyUtility } from '@catnekaise/actions-constructs';

const mappedClaims = ActionsIdentityMappedClaims.create(
        GhaClaim.REPOSITORY,
        // additional claims
);

const utility = ActionsIdentityPolicyUtility.create(stack, {
  mappedClaims,
  // identityPoolId is required when using the principalBuilder.
  identityPoolId: 'eu-west-1:11111111-example',
});

const principal = utility.newPrincipalBuilder()
        .repositoryEquals('catnekaise/workload-repo')
        .createPrincipal(pool);

new iam.Role(scope, 'AdditionalRole', {
  assumedBy: principal,
});
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import catnekaise_cdk_iam_utilities as _catnekaise_cdk_iam_utilities_ea41761b
import constructs as _constructs_77d1e7e8


class ActionsIdentityChainedPrincipalBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityChainedPrincipalBuilder",
):
    @jsii.member(jsii_name="fromClaimMapping")
    @builtins.classmethod
    def from_claim_mapping(
        cls,
        claim_mapping: "ClaimMapping",
    ) -> "ActionsIdentityChainedPrincipalBuilder":
        '''
        :param claim_mapping: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13d2f6a69939549b6114963e6f82632452f8e24348240d9ebf407b637bfb319e)
            check_type(argname="argument claim_mapping", value=claim_mapping, expected_type=type_hints["claim_mapping"])
        return typing.cast("ActionsIdentityChainedPrincipalBuilder", jsii.sinvoke(cls, "fromClaimMapping", [claim_mapping]))

    @jsii.member(jsii_name="claimEquals")
    def claim_equals(
        self,
        claim: "GhaClaim",
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "ActionsIdentityChainedPrincipalBuilder":
        '''
        :param claim: -
        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0e89a1594a29bd9bb0c116943007a4b22847182ecab397a88acfa03752f61a8)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityChainedPrincipalBuilder", jsii.invoke(self, "claimEquals", [claim, value, *additional_values]))

    @jsii.member(jsii_name="claimLike")
    def claim_like(
        self,
        claim: "GhaClaim",
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "ActionsIdentityChainedPrincipalBuilder":
        '''
        :param claim: -
        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37cb345b006cb452892a8b6bea35cf246546100f80c91b5ba896c0be4b8a351)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityChainedPrincipalBuilder", jsii.invoke(self, "claimLike", [claim, value, *additional_values]))

    @jsii.member(jsii_name="createConditions")
    def create_conditions(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "createConditions", []))

    @jsii.member(jsii_name="createPrincipalAssumedBy")
    def create_principal_assumed_by(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
    ) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''
        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8f537ac61404436bbe2a85a392c552386d6dd2041ee997183d838c522bfc601)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.invoke(self, "createPrincipalAssumedBy", [principal]))

    @jsii.member(jsii_name="passesClaim")
    def passes_claim(
        self,
        claim: "GhaClaim",
        *additional_claims: "GhaClaim",
    ) -> "ActionsIdentityChainedPrincipalBuilder":
        '''
        :param claim: -
        :param additional_claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__265d91cb006b7bb2c4b5d641d58336230fa4bb6c95e6471c6fc7f11d019c17c8)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument additional_claims", value=additional_claims, expected_type=typing.Tuple[type_hints["additional_claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityChainedPrincipalBuilder", jsii.invoke(self, "passesClaim", [claim, *additional_claims]))

    @jsii.member(jsii_name="requireExternalId")
    def require_external_id(
        self,
        external_id: builtins.str,
    ) -> "ActionsIdentityChainedPrincipalBuilder":
        '''
        :param external_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dceea15a13407bd99d3dd6c4c4677a064f25fe1da87757199848d8b2e3f2738)
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
        return typing.cast("ActionsIdentityChainedPrincipalBuilder", jsii.invoke(self, "requireExternalId", [external_id]))

    @jsii.member(jsii_name="requireIdentityPoolId")
    def require_identity_pool_id(
        self,
        identity_pool_id: builtins.str,
    ) -> "ActionsIdentityChainedPrincipalBuilder":
        '''
        :param identity_pool_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f31979e2d99f32c164c8e468743da8f082ed669110ef30d955b92303f76019)
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
        return typing.cast("ActionsIdentityChainedPrincipalBuilder", jsii.invoke(self, "requireIdentityPoolId", [identity_pool_id]))


class ActionsIdentityConstraints(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityConstraints",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addConstraint")
    @abc.abstractmethod
    def _add_constraint(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> None:
        '''
        :param constraint: -
        '''
        ...

    @jsii.member(jsii_name="approvedBy")
    def approved_by(self, *actors: builtins.str) -> "ActionsIdentityConstraints":
        '''
        :param actors: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01edf5097f67b8fb4ff08aa5fe0cfb3b3d2327eace11b2d466d383269530b149)
            check_type(argname="argument actors", value=actors, expected_type=typing.Tuple[type_hints["actors"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "approvedBy", [*actors]))

    @jsii.member(jsii_name="claimCondition")
    def claim_condition(
        self,
        operator: _catnekaise_cdk_iam_utilities_ea41761b.ConditionOperator,
        claim: "GhaClaim",
        *values: builtins.str,
    ) -> "ActionsIdentityConstraints":
        '''
        :param operator: -
        :param claim: -
        :param values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__496296eada68d4d4fa8fc5914f6d7ef4fa316cbe8e71abae90f86e0c4ca63697)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "claimCondition", [operator, claim, *values]))

    @jsii.member(jsii_name="claimEquals")
    def claim_equals(
        self,
        claim: "GhaClaim",
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "ActionsIdentityConstraints":
        '''
        :param claim: -
        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__307a58fef3f0f5c435143cdae8ad5a66a0c4e733ed80e09dfe01ad01109c4e42)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "claimEquals", [claim, value, *additional_values]))

    @jsii.member(jsii_name="claimLike")
    def claim_like(
        self,
        claim: "GhaClaim",
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "ActionsIdentityConstraints":
        '''
        :param claim: -
        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6277c0713efd5d7ade765d4482e45f0e66668eb77a3b63b949f75f8095ae9ce8)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "claimLike", [claim, value, *additional_values]))

    @jsii.member(jsii_name="environmentEquals")
    def environment_equals(
        self,
        environment: builtins.str,
        *additional_environments: builtins.str,
    ) -> "ActionsIdentityConstraints":
        '''
        :param environment: -
        :param additional_environments: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cee68bf00785268dfbb22092f0377038104aaf5d4a17b7f801baed5cff3bdea)
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument additional_environments", value=additional_environments, expected_type=typing.Tuple[type_hints["additional_environments"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "environmentEquals", [environment, *additional_environments]))

    @jsii.member(jsii_name="jobWorkflowLike")
    def job_workflow_like(
        self,
        organization: builtins.str,
        repository_name: typing.Optional[builtins.str] = None,
        filename: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> "ActionsIdentityConstraints":
        '''
        :param organization: Name of organization or user.
        :param repository_name: Name of repository.
        :param filename: Default value is '*'.
        :param ref: Default value is '*'.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca01ee0ba71bc3529d07b83396d08bbabc50d86292a362c38bf085e01d3bd1f7)
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "jobWorkflowLike", [organization, repository_name, filename, ref]))

    @jsii.member(jsii_name="refLike")
    def ref_like(self, *refs: builtins.str) -> "ActionsIdentityConstraints":
        '''
        :param refs: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4458c61cac6e6b461f7b730d952bd26e9b3b322129bf84bacdb522afd1b330)
            check_type(argname="argument refs", value=refs, expected_type=typing.Tuple[type_hints["refs"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "refLike", [*refs]))

    @jsii.member(jsii_name="repoOrganisations")
    def repo_organisations(
        self,
        organization: builtins.str,
        *additional_organizations: builtins.str,
    ) -> "ActionsIdentityConstraints":
        '''
        :param organization: -
        :param additional_organizations: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b6a894742320c5a2cab67931d7d69fbd3f352962392b3db5b6315347f3fa733)
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument additional_organizations", value=additional_organizations, expected_type=typing.Tuple[type_hints["additional_organizations"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "repoOrganisations", [organization, *additional_organizations]))

    @jsii.member(jsii_name="repositoryEquals")
    def repository_equals(
        self,
        repository: builtins.str,
        *additional_repositories: builtins.str,
    ) -> "ActionsIdentityConstraints":
        '''
        :param repository: -
        :param additional_repositories: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__060413733e65a3c2b43f10a8596687dd48d3ed370cfb8ff5ff7bddb8bfb511b9)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument additional_repositories", value=additional_repositories, expected_type=typing.Tuple[type_hints["additional_repositories"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "repositoryEquals", [repository, *additional_repositories]))

    @jsii.member(jsii_name="repositoryLike")
    def repository_like(
        self,
        repository: builtins.str,
        *additional_repositories: builtins.str,
    ) -> "ActionsIdentityConstraints":
        '''
        :param repository: -
        :param additional_repositories: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7128dfd8bfd9ba08eb68ac0ff55286372d5bd514adc76e59aa7e2943cd0e1f0e)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument additional_repositories", value=additional_repositories, expected_type=typing.Tuple[type_hints["additional_repositories"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "repositoryLike", [repository, *additional_repositories]))

    @jsii.member(jsii_name="whenSelfHosted")
    def when_self_hosted(self) -> "ActionsIdentityConstraints":
        return typing.cast("ActionsIdentityConstraints", jsii.invoke(self, "whenSelfHosted", []))


class _ActionsIdentityConstraintsProxy(ActionsIdentityConstraints):
    @jsii.member(jsii_name="addConstraint")
    def _add_constraint(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> None:
        '''
        :param constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab67385796fa2c1015170ae1cc9199b6ba5b5d321588ed849aded3e5133a06e)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
        return typing.cast(None, jsii.invoke(self, "addConstraint", [constraint]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ActionsIdentityConstraints).__jsii_proxy_class__ = lambda : _ActionsIdentityConstraintsProxy


class ActionsIdentityIamResourcePathBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityIamResourcePathBuilder",
):
    @jsii.member(jsii_name="fromClaimMapping")
    @builtins.classmethod
    def from_claim_mapping(
        cls,
        claim_mapping: "ClaimMapping",
    ) -> "ActionsIdentityIamResourcePathBuilder":
        '''
        :param claim_mapping: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28a0019179aec37d4a9f23b1a092ad6dcd14131b8a87f9a70d307cc818a24fc)
            check_type(argname="argument claim_mapping", value=claim_mapping, expected_type=type_hints["claim_mapping"])
        return typing.cast("ActionsIdentityIamResourcePathBuilder", jsii.sinvoke(cls, "fromClaimMapping", [claim_mapping]))

    @jsii.member(jsii_name="claim")
    def claim(
        self,
        value: "GhaClaim",
        *additional_values: "GhaClaim",
    ) -> "ActionsIdentityIamResourcePathBuilder":
        '''Value must be a mapped claim.

        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5feda193e60d764b32f6053c90438803b0950317330466a5eef2d0a7308dc0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityIamResourcePathBuilder", jsii.invoke(self, "claim", [value, *additional_values]))

    @jsii.member(jsii_name="text")
    def text(
        self,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "ActionsIdentityIamResourcePathBuilder":
        '''Value can be anything.

        Providing a GitHub Actions Claim will not render a principalTag context key.

        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d2bba97997cfcd0b948310fba3970ba1a76924ad4b470e2238aab84999bbbb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityIamResourcePathBuilder", jsii.invoke(self, "text", [value, *additional_values]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="toStringWithSeparator")
    def to_string_with_separator(self, separator: builtins.str) -> builtins.str:
        '''
        :param separator: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1deb7f20df4ed131f012c4bfb2245d26445b13fdd4ddc66a367e1e969951574)
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
        return typing.cast(builtins.str, jsii.invoke(self, "toStringWithSeparator", [separator]))

    @jsii.member(jsii_name="value")
    def value(
        self,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "ActionsIdentityIamResourcePathBuilder":
        '''Value can be anything.

        When value matches a known (mapped or not) GitHub Actions claim it will be treated as such.

        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a397d50ff87697bab21f682d500dda845ee5354f1bf973b2645b45028acdb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityIamResourcePathBuilder", jsii.invoke(self, "value", [value, *additional_values]))


class ActionsIdentityIamResourcePathBuilderV2(
    _catnekaise_cdk_iam_utilities_ea41761b.ClaimsIamResourcePathBuilder,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityIamResourcePathBuilderV2",
):
    @jsii.member(jsii_name="fromMappedClaims")
    @builtins.classmethod
    def from_mapped_claims(
        cls,
        mapped_claims: _catnekaise_cdk_iam_utilities_ea41761b.IMappedClaims,
    ) -> "ActionsIdentityIamResourcePathBuilderV2":
        '''
        :param mapped_claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__475622cd4e2a9ef991733bcbccee936cd93720e75714266b7113505d979a027a)
            check_type(argname="argument mapped_claims", value=mapped_claims, expected_type=type_hints["mapped_claims"])
        return typing.cast("ActionsIdentityIamResourcePathBuilderV2", jsii.sinvoke(cls, "fromMappedClaims", [mapped_claims]))

    @jsii.member(jsii_name="asStringWithSeparator")
    def as_string_with_separator(self, separator: builtins.str) -> builtins.str:
        '''
        :param separator: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__637971f317e75c80dca98cb517be41118c3a59e7459ef0194c34bf277a41419d)
            check_type(argname="argument separator", value=separator, expected_type=type_hints["separator"])
        return typing.cast(builtins.str, jsii.invoke(self, "asStringWithSeparator", [separator]))

    @jsii.member(jsii_name="claim")
    def claim(
        self,
        claim: "GhaClaim",
        *additional_claims: "GhaClaim",
    ) -> "ActionsIdentityIamResourcePathBuilderV2":
        '''
        :param claim: -
        :param additional_claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__246b1e1791c468aade25ef44d8f7785a95ee8dbacce77d38dbfa2c248e145b68)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument additional_claims", value=additional_claims, expected_type=typing.Tuple[type_hints["additional_claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityIamResourcePathBuilderV2", jsii.invoke(self, "claim", [claim, *additional_claims]))

    @jsii.member(jsii_name="policyVariable")
    def policy_variable(
        self,
        value: _catnekaise_cdk_iam_utilities_ea41761b.PolicyVariable,
    ) -> "ActionsIdentityIamResourcePathBuilderV2":
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc94873fb8aa6eb580ca5d67f2d07a5f653337340cf126ea23d3ed18e3b87746)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ActionsIdentityIamResourcePathBuilderV2", jsii.invoke(self, "policyVariable", [value]))

    @jsii.member(jsii_name="text")
    def text(
        self,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "ActionsIdentityIamResourcePathBuilderV2":
        '''
        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13200d0fe8e1c255d7d7839e879459d0d84e1489220d0b22bb5553a92cb3704d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityIamResourcePathBuilderV2", jsii.invoke(self, "text", [value, *additional_values]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="value")
    def value(
        self,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "ActionsIdentityIamResourcePathBuilderV2":
        '''
        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0141e9cc0ed371e2ea2669a6225b807f792d2522368fcebb7f9d54f7d1df59b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityIamResourcePathBuilderV2", jsii.invoke(self, "value", [value, *additional_values]))


@jsii.implements(_catnekaise_cdk_iam_utilities_ea41761b.IMappedClaims)
class ActionsIdentityMappedClaims(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityMappedClaims",
):
    def __init__(
        self,
        _claims: typing.Sequence[typing.Union[_catnekaise_cdk_iam_utilities_ea41761b.Claim, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''
        :param _claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697fff621d1282abf43672080318f318695cef2fa9b0be85c97f1efb4f5e25b7)
            check_type(argname="argument _claims", value=_claims, expected_type=type_hints["_claims"])
        jsii.create(self.__class__, self, [_claims])

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        claim: "GhaClaim",
        *additional_claims: "GhaClaim",
    ) -> "ActionsIdentityMappedClaims":
        '''
        :param claim: -
        :param additional_claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8e238634f7df7b66f826212cf4b72122026967b87a73edc7f0a356f0379dd1d)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument additional_claims", value=additional_claims, expected_type=typing.Tuple[type_hints["additional_claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityMappedClaims", jsii.sinvoke(cls, "create", [claim, *additional_claims]))

    @jsii.member(jsii_name="createCustom")
    @builtins.classmethod
    def create_custom(
        cls,
        claims: typing.Mapping[builtins.str, builtins.str],
    ) -> "ActionsIdentityMappedClaims":
        '''
        :param claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636e3b20261fec79fafe6b69ba7e947669029f6665bee31e9410601f9a2734f7)
            check_type(argname="argument claims", value=claims, expected_type=type_hints["claims"])
        return typing.cast("ActionsIdentityMappedClaims", jsii.sinvoke(cls, "createCustom", [claims]))

    @jsii.member(jsii_name="createWithAbbreviations")
    @builtins.classmethod
    def create_with_abbreviations(
        cls,
        claim: "GhaClaim",
        *additional_claims: "GhaClaim",
    ) -> "ActionsIdentityMappedClaims":
        '''
        :param claim: -
        :param additional_claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dcf8a0712800eb16f8170a2581a23616cd63db0eb3dc67d76c4ec8f383d15a2)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument additional_claims", value=additional_claims, expected_type=typing.Tuple[type_hints["additional_claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ActionsIdentityMappedClaims", jsii.sinvoke(cls, "createWithAbbreviations", [claim, *additional_claims]))

    @jsii.member(jsii_name="toClaimsContext")
    def to_claims_context(
        self,
    ) -> _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext:
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext, jsii.invoke(self, "toClaimsContext", []))

    @jsii.member(jsii_name="toConfigureAwsCredentialsPassClaims")
    def to_configure_aws_credentials_pass_claims(
        self,
    ) -> _catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings:
        '''Use this if you want to use https://github.com/aws-actions/configure-aws-credentials for performing role chaining.'''
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings, jsii.invoke(self, "toConfigureAwsCredentialsPassClaims", []))

    @jsii.member(jsii_name="toPassClaims")
    def to_pass_claims(
        self,
        *claims: "GhaClaim",
    ) -> _catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings:
        '''
        :param claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3772b475636084cf9b1ce97612996f9cbcf0c618a4e6b5f26207e791d2e1ed8f)
            check_type(argname="argument claims", value=claims, expected_type=typing.Tuple[type_hints["claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings, jsii.invoke(self, "toPassClaims", [*claims]))

    @jsii.member(jsii_name="toPassClaimsCustom")
    def to_pass_claims_custom(
        self,
        claims: typing.Mapping[builtins.str, builtins.str],
        allow_any_tags: typing.Optional[builtins.bool] = None,
        specifically_allowed_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings:
        '''
        :param claims: -
        :param allow_any_tags: -
        :param specifically_allowed_tags: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb5a65ddcb564b7cba1b842fccbfe6c18fe7219d63419ac6c23681e50d59bd2)
            check_type(argname="argument claims", value=claims, expected_type=type_hints["claims"])
            check_type(argname="argument allow_any_tags", value=allow_any_tags, expected_type=type_hints["allow_any_tags"])
            check_type(argname="argument specifically_allowed_tags", value=specifically_allowed_tags, expected_type=type_hints["specifically_allowed_tags"])
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings, jsii.invoke(self, "toPassClaimsCustom", [claims, allow_any_tags, specifically_allowed_tags]))

    @builtins.property
    @jsii.member(jsii_name="claims")
    def claims(self) -> typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Claim]:
        return typing.cast(typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Claim], jsii.get(self, "claims"))


class ActionsIdentityPolicyUtility(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPolicyUtility",
):
    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        base_principal_constraints: typing.Optional[typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint]] = None,
        default_amr: typing.Optional["AuthenticatedMethodReference"] = None,
        identity_pool_account_id: typing.Optional[builtins.str] = None,
        identity_pool_id: typing.Optional[builtins.str] = None,
        identity_pool_uses_enhanced_flow: typing.Optional[builtins.bool] = None,
    ) -> "ActionsIdentityPolicyUtility":
        '''
        :param scope: -
        :param claims_context: 
        :param base_principal_constraints: 
        :param default_amr: 
        :param identity_pool_account_id: 
        :param identity_pool_id: 
        :param identity_pool_uses_enhanced_flow: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8baa62e7730ecbd78b1abeedc3267b3af2ab5bbbc00dc95ca61fb747bed6c5f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        settings = ActionsIdentityPolicyUtilitySettings(
            claims_context=claims_context,
            base_principal_constraints=base_principal_constraints,
            default_amr=default_amr,
            identity_pool_account_id=identity_pool_account_id,
            identity_pool_id=identity_pool_id,
            identity_pool_uses_enhanced_flow=identity_pool_uses_enhanced_flow,
        )

        return typing.cast("ActionsIdentityPolicyUtility", jsii.sinvoke(cls, "create", [scope, settings]))

    @jsii.member(jsii_name="constrain")
    def constrain(
        self,
        policy_statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
        scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    ) -> "PolicyStatementConstrainer":
        '''Append a policy with conditions contextual to GitHub Actions claims.

        :param policy_statement: -
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb0234daaa0038d5a647e481ffdc3faeed5a238b4458cfdd03a4e65f2c47123)
            check_type(argname="argument policy_statement", value=policy_statement, expected_type=type_hints["policy_statement"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("PolicyStatementConstrainer", jsii.invoke(self, "constrain", [policy_statement, scope]))

    @jsii.member(jsii_name="constrainGrant")
    def constrain_grant(
        self,
        grant: _aws_cdk_aws_iam_ceddda9d.Grant,
        scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    ) -> "GrantConstrainer":
        '''Append a grant with conditions contextual to GitHub Actions claims.

        :param grant: -
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e8bbb57c12bcf0063f5eb9b74245d1d02ab39d810d0bfc4310436a218a9bed9)
            check_type(argname="argument grant", value=grant, expected_type=type_hints["grant"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("GrantConstrainer", jsii.invoke(self, "constrainGrant", [grant, scope]))

    @jsii.member(jsii_name="grantOrganizationRoleChain")
    def grant_organization_role_chain(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *,
        exclude_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_org_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_org_path_string_equals: typing.Optional[builtins.bool] = None,
        role_has_resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        role_path: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grant role permissions to assume roles in any organization account.

        :param identity: -
        :param exclude_account_ids: Prevent assuming roles in these accounts.
        :param resource_org_paths: Require roles to exist under specified organization paths.
        :param resource_org_path_string_equals: Match resourcePaths using StringEquals instead of StringLike.
        :param role_has_resource_tags: Role has resource tags matching specified values. If tag value matches a known GitHub Actions claim, then value is changed to ``${aws:PrincipalTag/value}``
        :param role_path: Require that roles exist under this path for sts:AssumeRole.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9ec5bdf39de767f99eb114b74778be1b2079980cd26aa429d3215c4f14abe3)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        settings = GrantOrgRoleChainSettings(
            exclude_account_ids=exclude_account_ids,
            resource_org_paths=resource_org_paths,
            resource_org_path_string_equals=resource_org_path_string_equals,
            role_has_resource_tags=role_has_resource_tags,
            role_path=role_path,
        )

        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantOrganizationRoleChain", [identity, settings]))

    @jsii.member(jsii_name="newChainedPrincipalBuilder")
    def new_chained_principal_builder(self) -> "ChainedPrincipalBuilder":
        '''Use this to create principals that should be assumable by roles that have been assumed via a ActionsIdentityPoolV2.'''
        return typing.cast("ChainedPrincipalBuilder", jsii.invoke(self, "newChainedPrincipalBuilder", []))

    @jsii.member(jsii_name="newPrincipalBuilder")
    def new_principal_builder(
        self,
        amr: typing.Optional["AuthenticatedMethodReference"] = None,
    ) -> "PrincipalBuilder":
        '''Use this to create principals that should allow assumption via a Cognito Identity Pool.

        :param amr: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fe4e95fde4c5a93878d6f83841ff89cf334c339367e97a3ee15ae4112c36635)
            check_type(argname="argument amr", value=amr, expected_type=type_hints["amr"])
        return typing.cast("PrincipalBuilder", jsii.invoke(self, "newPrincipalBuilder", [amr]))

    @jsii.member(jsii_name="policyVar")
    def policy_var(
        self,
        claim: "GhaClaim",
    ) -> _catnekaise_cdk_iam_utilities_ea41761b.PolicyVariable:
        '''Create a policy variable.

        :param claim: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9144c2fb0c36a570bad142fdb0b2718cb42a090d0bdc76397f48a4c3ee7068d4)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.PolicyVariable, jsii.invoke(self, "policyVar", [claim]))

    @jsii.member(jsii_name="principalTagConditionKey")
    def principal_tag_condition_key(
        self,
        claim: "GhaClaim",
    ) -> _catnekaise_cdk_iam_utilities_ea41761b.AwsPrincipalTagConditionKey:
        '''Create a principal tag for claim.

        :param claim: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ce4a2fd57ea63d83eb7c48234cb7e469307bb8761cf646a564fb40451d0f98)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.AwsPrincipalTagConditionKey, jsii.invoke(self, "principalTagConditionKey", [claim]))

    @jsii.member(jsii_name="resourcePath")
    def resource_path(
        self,
        *value: builtins.str,
    ) -> ActionsIdentityIamResourcePathBuilderV2:
        '''Build a resource path for an IAM Policy.

        :param value: Mix of strings and claims.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69e909a1c997c0f92807685cf59b84ef239d95867a94ed44d581d52bf8a62e70)
            check_type(argname="argument value", value=value, expected_type=typing.Tuple[type_hints["value"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(ActionsIdentityIamResourcePathBuilderV2, jsii.invoke(self, "resourcePath", [*value]))

    @builtins.property
    @jsii.member(jsii_name="claimsContext")
    def claims_context(self) -> _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext:
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext, jsii.get(self, "claimsContext"))


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPolicyUtilitySettings",
    jsii_struct_bases=[],
    name_mapping={
        "claims_context": "claimsContext",
        "base_principal_constraints": "basePrincipalConstraints",
        "default_amr": "defaultAmr",
        "identity_pool_account_id": "identityPoolAccountId",
        "identity_pool_id": "identityPoolId",
        "identity_pool_uses_enhanced_flow": "identityPoolUsesEnhancedFlow",
    },
)
class ActionsIdentityPolicyUtilitySettings:
    def __init__(
        self,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        base_principal_constraints: typing.Optional[typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint]] = None,
        default_amr: typing.Optional["AuthenticatedMethodReference"] = None,
        identity_pool_account_id: typing.Optional[builtins.str] = None,
        identity_pool_id: typing.Optional[builtins.str] = None,
        identity_pool_uses_enhanced_flow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param claims_context: 
        :param base_principal_constraints: 
        :param default_amr: 
        :param identity_pool_account_id: 
        :param identity_pool_id: 
        :param identity_pool_uses_enhanced_flow: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf195a8bfb14ab23579c74fcdc4fc9b22231a3108676d905105d6b5a6e6f5dd)
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
            check_type(argname="argument base_principal_constraints", value=base_principal_constraints, expected_type=type_hints["base_principal_constraints"])
            check_type(argname="argument default_amr", value=default_amr, expected_type=type_hints["default_amr"])
            check_type(argname="argument identity_pool_account_id", value=identity_pool_account_id, expected_type=type_hints["identity_pool_account_id"])
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument identity_pool_uses_enhanced_flow", value=identity_pool_uses_enhanced_flow, expected_type=type_hints["identity_pool_uses_enhanced_flow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claims_context": claims_context,
        }
        if base_principal_constraints is not None:
            self._values["base_principal_constraints"] = base_principal_constraints
        if default_amr is not None:
            self._values["default_amr"] = default_amr
        if identity_pool_account_id is not None:
            self._values["identity_pool_account_id"] = identity_pool_account_id
        if identity_pool_id is not None:
            self._values["identity_pool_id"] = identity_pool_id
        if identity_pool_uses_enhanced_flow is not None:
            self._values["identity_pool_uses_enhanced_flow"] = identity_pool_uses_enhanced_flow

    @builtins.property
    def claims_context(self) -> _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext:
        result = self._values.get("claims_context")
        assert result is not None, "Required property 'claims_context' is missing"
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext, result)

    @builtins.property
    def base_principal_constraints(
        self,
    ) -> typing.Optional[typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Constraint]]:
        result = self._values.get("base_principal_constraints")
        return typing.cast(typing.Optional[typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Constraint]], result)

    @builtins.property
    def default_amr(self) -> typing.Optional["AuthenticatedMethodReference"]:
        result = self._values.get("default_amr")
        return typing.cast(typing.Optional["AuthenticatedMethodReference"], result)

    @builtins.property
    def identity_pool_account_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("identity_pool_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_pool_id(self) -> typing.Optional[builtins.str]:
        result = self._values.get("identity_pool_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_pool_uses_enhanced_flow(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("identity_pool_uses_enhanced_flow")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsIdentityPolicyUtilitySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolAuthenticatedRoleBehaviour"
)
class ActionsIdentityPoolAuthenticatedRoleBehaviour(enum.Enum):
    CREATE = "CREATE"
    USE_FIRST_ASSIGNED = "USE_FIRST_ASSIGNED"


class ActionsIdentityPoolBase(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        base_props: typing.Union["ActionsIdentityPoolBaseProps", typing.Dict[builtins.str, typing.Any]],
        allow_classic_flow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param base_props: -
        :param allow_classic_flow: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81531e8db6105fee95b24b0b55459a3541dee52b55db415a78afbf1a8a091975)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument base_props", value=base_props, expected_type=type_hints["base_props"])
            check_type(argname="argument allow_classic_flow", value=allow_classic_flow, expected_type=type_hints["allow_classic_flow"])
        jsii.create(self.__class__, self, [scope, id, base_props, allow_classic_flow])

    @jsii.member(jsii_name="createPrincipalForPool")
    def create_principal_for_pool(
        self,
        requirements: typing.Optional[typing.Union["PrincipalClaimRequirements", typing.Dict[builtins.str, typing.Any]]] = None,
        amr: typing.Optional["AuthenticatedMethodReference"] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''Create Principal with default Trust Policy for this Identity Pool.

        :param requirements: -
        :param amr: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a2771b558a1a9d752db8f44251adfff5df7c247de72336fceeabe7a233a131)
            check_type(argname="argument requirements", value=requirements, expected_type=type_hints["requirements"])
            check_type(argname="argument amr", value=amr, expected_type=type_hints["amr"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.invoke(self, "createPrincipalForPool", [requirements, amr]))

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityPoolId"))

    @builtins.property
    @jsii.member(jsii_name="mappedClaims")
    def mapped_claims(self) -> typing.List["MappedClaim"]:
        return typing.cast(typing.List["MappedClaim"], jsii.get(self, "mappedClaims"))

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProvider")
    def _open_id_connect_provider(
        self,
    ) -> _aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider, jsii.get(self, "openIdConnectProvider"))

    @builtins.property
    @jsii.member(jsii_name="util")
    def util(self) -> "ActionsIdentityPoolUtils":
        return typing.cast("ActionsIdentityPoolUtils", jsii.get(self, "util"))


class _ActionsIdentityPoolBaseProxy(ActionsIdentityPoolBase):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ActionsIdentityPoolBase).__jsii_proxy_class__ = lambda : _ActionsIdentityPoolBaseProxy


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "claim_mapping": "claimMapping",
        "principal_claim_requirements": "principalClaimRequirements",
        "authenticated_method_reference": "authenticatedMethodReference",
        "authenticated_role_name": "authenticatedRoleName",
        "identity_pool_name": "identityPoolName",
        "open_id_connect_provider": "openIdConnectProvider",
        "pool_id_export_name": "poolIdExportName",
    },
)
class ActionsIdentityPoolBaseProps:
    def __init__(
        self,
        *,
        claim_mapping: "ClaimMapping",
        principal_claim_requirements: typing.Union["PrincipalClaimRequirements", typing.Dict[builtins.str, typing.Any]],
        authenticated_method_reference: typing.Optional["AuthenticatedMethodReference"] = None,
        authenticated_role_name: typing.Optional[builtins.str] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
        pool_id_export_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param claim_mapping: 
        :param principal_claim_requirements: Required claims used when not passing any to this.createPrincipalForPool().
        :param authenticated_method_reference: Authenticated Method Reference. authenticated = authenticated host = token.actions.githubusercontent.com arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:*
        :param authenticated_role_name: Name of authenticated role when creating role.
        :param identity_pool_name: Name of the Identity Pool.
        :param open_id_connect_provider: Provide this or attempt will be made to import OpenIdConnectProvider using defaults.
        :param pool_id_export_name: Export name for the CfnOutput containing the Identity Pool ID.
        '''
        if isinstance(principal_claim_requirements, dict):
            principal_claim_requirements = PrincipalClaimRequirements(**principal_claim_requirements)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b916c54a25eaf320ffb40aa4a746d78ce4a2235fbc30f929c353cd325d7b1ed)
            check_type(argname="argument claim_mapping", value=claim_mapping, expected_type=type_hints["claim_mapping"])
            check_type(argname="argument principal_claim_requirements", value=principal_claim_requirements, expected_type=type_hints["principal_claim_requirements"])
            check_type(argname="argument authenticated_method_reference", value=authenticated_method_reference, expected_type=type_hints["authenticated_method_reference"])
            check_type(argname="argument authenticated_role_name", value=authenticated_role_name, expected_type=type_hints["authenticated_role_name"])
            check_type(argname="argument identity_pool_name", value=identity_pool_name, expected_type=type_hints["identity_pool_name"])
            check_type(argname="argument open_id_connect_provider", value=open_id_connect_provider, expected_type=type_hints["open_id_connect_provider"])
            check_type(argname="argument pool_id_export_name", value=pool_id_export_name, expected_type=type_hints["pool_id_export_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claim_mapping": claim_mapping,
            "principal_claim_requirements": principal_claim_requirements,
        }
        if authenticated_method_reference is not None:
            self._values["authenticated_method_reference"] = authenticated_method_reference
        if authenticated_role_name is not None:
            self._values["authenticated_role_name"] = authenticated_role_name
        if identity_pool_name is not None:
            self._values["identity_pool_name"] = identity_pool_name
        if open_id_connect_provider is not None:
            self._values["open_id_connect_provider"] = open_id_connect_provider
        if pool_id_export_name is not None:
            self._values["pool_id_export_name"] = pool_id_export_name

    @builtins.property
    def claim_mapping(self) -> "ClaimMapping":
        result = self._values.get("claim_mapping")
        assert result is not None, "Required property 'claim_mapping' is missing"
        return typing.cast("ClaimMapping", result)

    @builtins.property
    def principal_claim_requirements(self) -> "PrincipalClaimRequirements":
        '''Required claims used when not passing any to this.createPrincipalForPool().'''
        result = self._values.get("principal_claim_requirements")
        assert result is not None, "Required property 'principal_claim_requirements' is missing"
        return typing.cast("PrincipalClaimRequirements", result)

    @builtins.property
    def authenticated_method_reference(
        self,
    ) -> typing.Optional["AuthenticatedMethodReference"]:
        '''Authenticated Method Reference.

        authenticated = authenticated

        host = token.actions.githubusercontent.com

        arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:*
        '''
        result = self._values.get("authenticated_method_reference")
        return typing.cast(typing.Optional["AuthenticatedMethodReference"], result)

    @builtins.property
    def authenticated_role_name(self) -> typing.Optional[builtins.str]:
        '''Name of authenticated role when creating role.'''
        result = self._values.get("authenticated_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_pool_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Identity Pool.'''
        result = self._values.get("identity_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_id_connect_provider(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider]:
        '''Provide this or attempt will be made to import OpenIdConnectProvider using defaults.'''
        result = self._values.get("open_id_connect_provider")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider], result)

    @builtins.property
    def pool_id_export_name(self) -> typing.Optional[builtins.str]:
        '''Export name for the CfnOutput containing the Identity Pool ID.'''
        result = self._values.get("pool_id_export_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsIdentityPoolBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsIdentityPoolBasic(
    ActionsIdentityPoolBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolBasic",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        claim_mapping: "ClaimMapping",
        principal_claim_requirements: typing.Union["PrincipalClaimRequirements", typing.Dict[builtins.str, typing.Any]],
        authenticated_method_reference: typing.Optional["AuthenticatedMethodReference"] = None,
        authenticated_role_name: typing.Optional[builtins.str] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
        pool_id_export_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param claim_mapping: 
        :param principal_claim_requirements: Required claims used when not passing any to this.createPrincipalForPool().
        :param authenticated_method_reference: Authenticated Method Reference. authenticated = authenticated host = token.actions.githubusercontent.com arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:*
        :param authenticated_role_name: Name of authenticated role when creating role.
        :param identity_pool_name: Name of the Identity Pool.
        :param open_id_connect_provider: Provide this or attempt will be made to import OpenIdConnectProvider using defaults.
        :param pool_id_export_name: Export name for the CfnOutput containing the Identity Pool ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a13836398f9c0384e0d0715ff7dc7695c5ce908f8aedeb76a53696cadb53d21)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ActionsIdentityPoolBasicProps(
            claim_mapping=claim_mapping,
            principal_claim_requirements=principal_claim_requirements,
            authenticated_method_reference=authenticated_method_reference,
            authenticated_role_name=authenticated_role_name,
            identity_pool_name=identity_pool_name,
            open_id_connect_provider=open_id_connect_provider,
            pool_id_export_name=pool_id_export_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticatedRole")
    def default_authenticated_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "defaultAuthenticatedRole"))


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolBasicProps",
    jsii_struct_bases=[ActionsIdentityPoolBaseProps],
    name_mapping={
        "claim_mapping": "claimMapping",
        "principal_claim_requirements": "principalClaimRequirements",
        "authenticated_method_reference": "authenticatedMethodReference",
        "authenticated_role_name": "authenticatedRoleName",
        "identity_pool_name": "identityPoolName",
        "open_id_connect_provider": "openIdConnectProvider",
        "pool_id_export_name": "poolIdExportName",
    },
)
class ActionsIdentityPoolBasicProps(ActionsIdentityPoolBaseProps):
    def __init__(
        self,
        *,
        claim_mapping: "ClaimMapping",
        principal_claim_requirements: typing.Union["PrincipalClaimRequirements", typing.Dict[builtins.str, typing.Any]],
        authenticated_method_reference: typing.Optional["AuthenticatedMethodReference"] = None,
        authenticated_role_name: typing.Optional[builtins.str] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
        pool_id_export_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param claim_mapping: 
        :param principal_claim_requirements: Required claims used when not passing any to this.createPrincipalForPool().
        :param authenticated_method_reference: Authenticated Method Reference. authenticated = authenticated host = token.actions.githubusercontent.com arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:*
        :param authenticated_role_name: Name of authenticated role when creating role.
        :param identity_pool_name: Name of the Identity Pool.
        :param open_id_connect_provider: Provide this or attempt will be made to import OpenIdConnectProvider using defaults.
        :param pool_id_export_name: Export name for the CfnOutput containing the Identity Pool ID.
        '''
        if isinstance(principal_claim_requirements, dict):
            principal_claim_requirements = PrincipalClaimRequirements(**principal_claim_requirements)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ae82cb12a2d027c191eca4fe4c9e0eba97cba80d3d3312ea4386b370616f20)
            check_type(argname="argument claim_mapping", value=claim_mapping, expected_type=type_hints["claim_mapping"])
            check_type(argname="argument principal_claim_requirements", value=principal_claim_requirements, expected_type=type_hints["principal_claim_requirements"])
            check_type(argname="argument authenticated_method_reference", value=authenticated_method_reference, expected_type=type_hints["authenticated_method_reference"])
            check_type(argname="argument authenticated_role_name", value=authenticated_role_name, expected_type=type_hints["authenticated_role_name"])
            check_type(argname="argument identity_pool_name", value=identity_pool_name, expected_type=type_hints["identity_pool_name"])
            check_type(argname="argument open_id_connect_provider", value=open_id_connect_provider, expected_type=type_hints["open_id_connect_provider"])
            check_type(argname="argument pool_id_export_name", value=pool_id_export_name, expected_type=type_hints["pool_id_export_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claim_mapping": claim_mapping,
            "principal_claim_requirements": principal_claim_requirements,
        }
        if authenticated_method_reference is not None:
            self._values["authenticated_method_reference"] = authenticated_method_reference
        if authenticated_role_name is not None:
            self._values["authenticated_role_name"] = authenticated_role_name
        if identity_pool_name is not None:
            self._values["identity_pool_name"] = identity_pool_name
        if open_id_connect_provider is not None:
            self._values["open_id_connect_provider"] = open_id_connect_provider
        if pool_id_export_name is not None:
            self._values["pool_id_export_name"] = pool_id_export_name

    @builtins.property
    def claim_mapping(self) -> "ClaimMapping":
        result = self._values.get("claim_mapping")
        assert result is not None, "Required property 'claim_mapping' is missing"
        return typing.cast("ClaimMapping", result)

    @builtins.property
    def principal_claim_requirements(self) -> "PrincipalClaimRequirements":
        '''Required claims used when not passing any to this.createPrincipalForPool().'''
        result = self._values.get("principal_claim_requirements")
        assert result is not None, "Required property 'principal_claim_requirements' is missing"
        return typing.cast("PrincipalClaimRequirements", result)

    @builtins.property
    def authenticated_method_reference(
        self,
    ) -> typing.Optional["AuthenticatedMethodReference"]:
        '''Authenticated Method Reference.

        authenticated = authenticated

        host = token.actions.githubusercontent.com

        arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:*
        '''
        result = self._values.get("authenticated_method_reference")
        return typing.cast(typing.Optional["AuthenticatedMethodReference"], result)

    @builtins.property
    def authenticated_role_name(self) -> typing.Optional[builtins.str]:
        '''Name of authenticated role when creating role.'''
        result = self._values.get("authenticated_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_pool_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Identity Pool.'''
        result = self._values.get("identity_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_id_connect_provider(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider]:
        '''Provide this or attempt will be made to import OpenIdConnectProvider using defaults.'''
        result = self._values.get("open_id_connect_provider")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider], result)

    @builtins.property
    def pool_id_export_name(self) -> typing.Optional[builtins.str]:
        '''Export name for the CfnOutput containing the Identity Pool ID.'''
        result = self._values.get("pool_id_export_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsIdentityPoolBasicProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolPrincipalBuilderOptions",
    jsii_struct_bases=[],
    name_mapping={
        "claim_mapping": "claimMapping",
        "identity_pool_id": "identityPoolId",
        "amr": "amr",
        "open_id_connect_provider_arn": "openIdConnectProviderArn",
    },
)
class ActionsIdentityPoolPrincipalBuilderOptions:
    def __init__(
        self,
        *,
        claim_mapping: "ClaimMapping",
        identity_pool_id: builtins.str,
        amr: typing.Optional["AuthenticatedMethodReference"] = None,
        open_id_connect_provider_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param claim_mapping: 
        :param identity_pool_id: 
        :param amr: 
        :param open_id_connect_provider_arn: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d735f3b68305db539ab55eb1b375308a827a494150c1bdceb78a31a04db3c1da)
            check_type(argname="argument claim_mapping", value=claim_mapping, expected_type=type_hints["claim_mapping"])
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument amr", value=amr, expected_type=type_hints["amr"])
            check_type(argname="argument open_id_connect_provider_arn", value=open_id_connect_provider_arn, expected_type=type_hints["open_id_connect_provider_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claim_mapping": claim_mapping,
            "identity_pool_id": identity_pool_id,
        }
        if amr is not None:
            self._values["amr"] = amr
        if open_id_connect_provider_arn is not None:
            self._values["open_id_connect_provider_arn"] = open_id_connect_provider_arn

    @builtins.property
    def claim_mapping(self) -> "ClaimMapping":
        result = self._values.get("claim_mapping")
        assert result is not None, "Required property 'claim_mapping' is missing"
        return typing.cast("ClaimMapping", result)

    @builtins.property
    def identity_pool_id(self) -> builtins.str:
        result = self._values.get("identity_pool_id")
        assert result is not None, "Required property 'identity_pool_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def amr(self) -> typing.Optional["AuthenticatedMethodReference"]:
        result = self._values.get("amr")
        return typing.cast(typing.Optional["AuthenticatedMethodReference"], result)

    @builtins.property
    def open_id_connect_provider_arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("open_id_connect_provider_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsIdentityPoolPrincipalBuilderOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolProps",
    jsii_struct_bases=[ActionsIdentityPoolBaseProps],
    name_mapping={
        "claim_mapping": "claimMapping",
        "principal_claim_requirements": "principalClaimRequirements",
        "authenticated_method_reference": "authenticatedMethodReference",
        "authenticated_role_name": "authenticatedRoleName",
        "identity_pool_name": "identityPoolName",
        "open_id_connect_provider": "openIdConnectProvider",
        "pool_id_export_name": "poolIdExportName",
        "authenticated_role": "authenticatedRole",
        "role_resolution": "roleResolution",
    },
)
class ActionsIdentityPoolProps(ActionsIdentityPoolBaseProps):
    def __init__(
        self,
        *,
        claim_mapping: "ClaimMapping",
        principal_claim_requirements: typing.Union["PrincipalClaimRequirements", typing.Dict[builtins.str, typing.Any]],
        authenticated_method_reference: typing.Optional["AuthenticatedMethodReference"] = None,
        authenticated_role_name: typing.Optional[builtins.str] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
        pool_id_export_name: typing.Optional[builtins.str] = None,
        authenticated_role: ActionsIdentityPoolAuthenticatedRoleBehaviour,
        role_resolution: typing.Optional["EnhancedFlowRoleResolution"] = None,
    ) -> None:
        '''
        :param claim_mapping: 
        :param principal_claim_requirements: Required claims used when not passing any to this.createPrincipalForPool().
        :param authenticated_method_reference: Authenticated Method Reference. authenticated = authenticated host = token.actions.githubusercontent.com arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:*
        :param authenticated_role_name: Name of authenticated role when creating role.
        :param identity_pool_name: Name of the Identity Pool.
        :param open_id_connect_provider: Provide this or attempt will be made to import OpenIdConnectProvider using defaults.
        :param pool_id_export_name: Export name for the CfnOutput containing the Identity Pool ID.
        :param authenticated_role: Create authenticated role or use first role assigned in role mappings.
        :param role_resolution: When no rule matches, request should be denied or use default authenticated role.
        '''
        if isinstance(principal_claim_requirements, dict):
            principal_claim_requirements = PrincipalClaimRequirements(**principal_claim_requirements)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f017bde67aa4225c7c13bd73111eb0ce8241aeaaf233b2657daa0a1fe90dcaf7)
            check_type(argname="argument claim_mapping", value=claim_mapping, expected_type=type_hints["claim_mapping"])
            check_type(argname="argument principal_claim_requirements", value=principal_claim_requirements, expected_type=type_hints["principal_claim_requirements"])
            check_type(argname="argument authenticated_method_reference", value=authenticated_method_reference, expected_type=type_hints["authenticated_method_reference"])
            check_type(argname="argument authenticated_role_name", value=authenticated_role_name, expected_type=type_hints["authenticated_role_name"])
            check_type(argname="argument identity_pool_name", value=identity_pool_name, expected_type=type_hints["identity_pool_name"])
            check_type(argname="argument open_id_connect_provider", value=open_id_connect_provider, expected_type=type_hints["open_id_connect_provider"])
            check_type(argname="argument pool_id_export_name", value=pool_id_export_name, expected_type=type_hints["pool_id_export_name"])
            check_type(argname="argument authenticated_role", value=authenticated_role, expected_type=type_hints["authenticated_role"])
            check_type(argname="argument role_resolution", value=role_resolution, expected_type=type_hints["role_resolution"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claim_mapping": claim_mapping,
            "principal_claim_requirements": principal_claim_requirements,
            "authenticated_role": authenticated_role,
        }
        if authenticated_method_reference is not None:
            self._values["authenticated_method_reference"] = authenticated_method_reference
        if authenticated_role_name is not None:
            self._values["authenticated_role_name"] = authenticated_role_name
        if identity_pool_name is not None:
            self._values["identity_pool_name"] = identity_pool_name
        if open_id_connect_provider is not None:
            self._values["open_id_connect_provider"] = open_id_connect_provider
        if pool_id_export_name is not None:
            self._values["pool_id_export_name"] = pool_id_export_name
        if role_resolution is not None:
            self._values["role_resolution"] = role_resolution

    @builtins.property
    def claim_mapping(self) -> "ClaimMapping":
        result = self._values.get("claim_mapping")
        assert result is not None, "Required property 'claim_mapping' is missing"
        return typing.cast("ClaimMapping", result)

    @builtins.property
    def principal_claim_requirements(self) -> "PrincipalClaimRequirements":
        '''Required claims used when not passing any to this.createPrincipalForPool().'''
        result = self._values.get("principal_claim_requirements")
        assert result is not None, "Required property 'principal_claim_requirements' is missing"
        return typing.cast("PrincipalClaimRequirements", result)

    @builtins.property
    def authenticated_method_reference(
        self,
    ) -> typing.Optional["AuthenticatedMethodReference"]:
        '''Authenticated Method Reference.

        authenticated = authenticated

        host = token.actions.githubusercontent.com

        arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:*
        '''
        result = self._values.get("authenticated_method_reference")
        return typing.cast(typing.Optional["AuthenticatedMethodReference"], result)

    @builtins.property
    def authenticated_role_name(self) -> typing.Optional[builtins.str]:
        '''Name of authenticated role when creating role.'''
        result = self._values.get("authenticated_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity_pool_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Identity Pool.'''
        result = self._values.get("identity_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_id_connect_provider(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider]:
        '''Provide this or attempt will be made to import OpenIdConnectProvider using defaults.'''
        result = self._values.get("open_id_connect_provider")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider], result)

    @builtins.property
    def pool_id_export_name(self) -> typing.Optional[builtins.str]:
        '''Export name for the CfnOutput containing the Identity Pool ID.'''
        result = self._values.get("pool_id_export_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def authenticated_role(self) -> ActionsIdentityPoolAuthenticatedRoleBehaviour:
        '''Create authenticated role or use first role assigned in role mappings.'''
        result = self._values.get("authenticated_role")
        assert result is not None, "Required property 'authenticated_role' is missing"
        return typing.cast(ActionsIdentityPoolAuthenticatedRoleBehaviour, result)

    @builtins.property
    def role_resolution(self) -> typing.Optional["EnhancedFlowRoleResolution"]:
        '''When no rule matches, request should be denied or use default authenticated role.'''
        result = self._values.get("role_resolution")
        return typing.cast(typing.Optional["EnhancedFlowRoleResolution"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsIdentityPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsIdentityPoolUtils(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolUtils",
):
    def __init__(self, claim_mapping: "ClaimMapping") -> None:
        '''
        :param claim_mapping: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac9dff5284fda10eca7d3e912fdeb93011384c7d72ff00155fb50ca41b10235)
            check_type(argname="argument claim_mapping", value=claim_mapping, expected_type=type_hints["claim_mapping"])
        jsii.create(self.__class__, self, [claim_mapping])

    @builtins.property
    @jsii.member(jsii_name="chainedPrincipal")
    def chained_principal(self) -> ActionsIdentityChainedPrincipalBuilder:
        return typing.cast(ActionsIdentityChainedPrincipalBuilder, jsii.get(self, "chainedPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="iamResourcePath")
    def iam_resource_path(self) -> ActionsIdentityIamResourcePathBuilder:
        return typing.cast(ActionsIdentityIamResourcePathBuilder, jsii.get(self, "iamResourcePath"))


class ActionsIdentityPoolV2(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolV2",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        authenticated_role_constraints: typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint],
        mapped_claims: ActionsIdentityMappedClaims,
        authenticated_method_reference: typing.Optional["AuthenticatedMethodReference"] = None,
        authenticated_role_name: typing.Optional[builtins.str] = None,
        enhanced_flow_role_resolution: typing.Optional["EnhancedFlowRoleResolution"] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
        pool_id_export_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        use_enhanced_auth_flow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param authenticated_role_constraints: Constraints for the default authenticated role created in this pool. Example:: new ActionsIdentityPoolV2(this,'Pool', { authenticatedRoleConstraints: [ GitHubActionsClaimConstraint.repoOwners(`catnekaise`), // additional constraints ] });
        :param mapped_claims: Mapped Claims for this Identity Pool.
        :param authenticated_method_reference: Authenticated Method Reference. authenticated = authenticated (default) host = token.actions.githubusercontent.com arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:* Default: authenticated
        :param authenticated_role_name: Name of authenticated role when creating role.
        :param enhanced_flow_role_resolution: Only applicable when setting ``useEnhancedFlow`` to ``true``. Default: deny
        :param identity_pool_name: Name of the Identity Pool.
        :param open_id_connect_provider: Provide this or attempt will be made to import OpenIdConnectProvider using defaults. Default: Attempts to imports OIDC Provider from AWS Account
        :param pool_id_export_name: Export name for the CfnOutput containing the Identity Pool ID.
        :param removal_policy: Set removal policy.
        :param use_enhanced_auth_flow: Use Enhanced (Simplified) AuthFlow instead of Basic. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a6864ea4acd2021ed70d0fc40c133e643653d5c54a2afa2a317b2c4b4ca459a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ActionsIdentityPoolV2Props(
            authenticated_role_constraints=authenticated_role_constraints,
            mapped_claims=mapped_claims,
            authenticated_method_reference=authenticated_method_reference,
            authenticated_role_name=authenticated_role_name,
            enhanced_flow_role_resolution=enhanced_flow_role_resolution,
            identity_pool_name=identity_pool_name,
            open_id_connect_provider=open_id_connect_provider,
            pool_id_export_name=pool_id_export_name,
            removal_policy=removal_policy,
            use_enhanced_auth_flow=use_enhanced_auth_flow,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="enhancedFlowAssignRole")
    def enhanced_flow_assign_role(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.Role,
        claim: "GhaClaim",
        match_type: "EnhancedFlowMatchType",
        value: builtins.str,
    ) -> "ActionsIdentityPoolV2":
        '''
        :param role: -
        :param claim: -
        :param match_type: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ae0b0315cb4e8549bb550e46ce0fe03fda36a62833ec10ce6db0ffc14596795)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ActionsIdentityPoolV2", jsii.invoke(self, "enhancedFlowAssignRole", [role, claim, match_type, value]))

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticatedRole")
    def default_authenticated_role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "defaultAuthenticatedRole"))

    @builtins.property
    @jsii.member(jsii_name="identityPoolId")
    def identity_pool_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identityPoolId"))

    @builtins.property
    @jsii.member(jsii_name="policyUtility")
    def policy_utility(self) -> ActionsIdentityPolicyUtility:
        return typing.cast(ActionsIdentityPolicyUtility, jsii.get(self, "policyUtility"))


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPoolV2Props",
    jsii_struct_bases=[],
    name_mapping={
        "authenticated_role_constraints": "authenticatedRoleConstraints",
        "mapped_claims": "mappedClaims",
        "authenticated_method_reference": "authenticatedMethodReference",
        "authenticated_role_name": "authenticatedRoleName",
        "enhanced_flow_role_resolution": "enhancedFlowRoleResolution",
        "identity_pool_name": "identityPoolName",
        "open_id_connect_provider": "openIdConnectProvider",
        "pool_id_export_name": "poolIdExportName",
        "removal_policy": "removalPolicy",
        "use_enhanced_auth_flow": "useEnhancedAuthFlow",
    },
)
class ActionsIdentityPoolV2Props:
    def __init__(
        self,
        *,
        authenticated_role_constraints: typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint],
        mapped_claims: ActionsIdentityMappedClaims,
        authenticated_method_reference: typing.Optional["AuthenticatedMethodReference"] = None,
        authenticated_role_name: typing.Optional[builtins.str] = None,
        enhanced_flow_role_resolution: typing.Optional["EnhancedFlowRoleResolution"] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
        pool_id_export_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        use_enhanced_auth_flow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param authenticated_role_constraints: Constraints for the default authenticated role created in this pool. Example:: new ActionsIdentityPoolV2(this,'Pool', { authenticatedRoleConstraints: [ GitHubActionsClaimConstraint.repoOwners(`catnekaise`), // additional constraints ] });
        :param mapped_claims: Mapped Claims for this Identity Pool.
        :param authenticated_method_reference: Authenticated Method Reference. authenticated = authenticated (default) host = token.actions.githubusercontent.com arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:* Default: authenticated
        :param authenticated_role_name: Name of authenticated role when creating role.
        :param enhanced_flow_role_resolution: Only applicable when setting ``useEnhancedFlow`` to ``true``. Default: deny
        :param identity_pool_name: Name of the Identity Pool.
        :param open_id_connect_provider: Provide this or attempt will be made to import OpenIdConnectProvider using defaults. Default: Attempts to imports OIDC Provider from AWS Account
        :param pool_id_export_name: Export name for the CfnOutput containing the Identity Pool ID.
        :param removal_policy: Set removal policy.
        :param use_enhanced_auth_flow: Use Enhanced (Simplified) AuthFlow instead of Basic. Default: false
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab6d184bff5984ac3fe5e6feff9bf0be2bd30dd5725fa6e36add7efc0413eeb)
            check_type(argname="argument authenticated_role_constraints", value=authenticated_role_constraints, expected_type=type_hints["authenticated_role_constraints"])
            check_type(argname="argument mapped_claims", value=mapped_claims, expected_type=type_hints["mapped_claims"])
            check_type(argname="argument authenticated_method_reference", value=authenticated_method_reference, expected_type=type_hints["authenticated_method_reference"])
            check_type(argname="argument authenticated_role_name", value=authenticated_role_name, expected_type=type_hints["authenticated_role_name"])
            check_type(argname="argument enhanced_flow_role_resolution", value=enhanced_flow_role_resolution, expected_type=type_hints["enhanced_flow_role_resolution"])
            check_type(argname="argument identity_pool_name", value=identity_pool_name, expected_type=type_hints["identity_pool_name"])
            check_type(argname="argument open_id_connect_provider", value=open_id_connect_provider, expected_type=type_hints["open_id_connect_provider"])
            check_type(argname="argument pool_id_export_name", value=pool_id_export_name, expected_type=type_hints["pool_id_export_name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument use_enhanced_auth_flow", value=use_enhanced_auth_flow, expected_type=type_hints["use_enhanced_auth_flow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "authenticated_role_constraints": authenticated_role_constraints,
            "mapped_claims": mapped_claims,
        }
        if authenticated_method_reference is not None:
            self._values["authenticated_method_reference"] = authenticated_method_reference
        if authenticated_role_name is not None:
            self._values["authenticated_role_name"] = authenticated_role_name
        if enhanced_flow_role_resolution is not None:
            self._values["enhanced_flow_role_resolution"] = enhanced_flow_role_resolution
        if identity_pool_name is not None:
            self._values["identity_pool_name"] = identity_pool_name
        if open_id_connect_provider is not None:
            self._values["open_id_connect_provider"] = open_id_connect_provider
        if pool_id_export_name is not None:
            self._values["pool_id_export_name"] = pool_id_export_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if use_enhanced_auth_flow is not None:
            self._values["use_enhanced_auth_flow"] = use_enhanced_auth_flow

    @builtins.property
    def authenticated_role_constraints(
        self,
    ) -> typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Constraint]:
        '''Constraints for the default authenticated role created in this pool.

        Example::

           new ActionsIdentityPoolV2(this,'Pool', {
             authenticatedRoleConstraints: [
              GitHubActionsClaimConstraint.repoOwners(`catnekaise`),
              // additional constraints
             ]
           });
        '''
        result = self._values.get("authenticated_role_constraints")
        assert result is not None, "Required property 'authenticated_role_constraints' is missing"
        return typing.cast(typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Constraint], result)

    @builtins.property
    def mapped_claims(self) -> ActionsIdentityMappedClaims:
        '''Mapped Claims for this Identity Pool.'''
        result = self._values.get("mapped_claims")
        assert result is not None, "Required property 'mapped_claims' is missing"
        return typing.cast(ActionsIdentityMappedClaims, result)

    @builtins.property
    def authenticated_method_reference(
        self,
    ) -> typing.Optional["AuthenticatedMethodReference"]:
        '''Authenticated Method Reference.

        authenticated = authenticated (default)

        host = token.actions.githubusercontent.com

        arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:*

        :default: authenticated
        '''
        result = self._values.get("authenticated_method_reference")
        return typing.cast(typing.Optional["AuthenticatedMethodReference"], result)

    @builtins.property
    def authenticated_role_name(self) -> typing.Optional[builtins.str]:
        '''Name of authenticated role when creating role.'''
        result = self._values.get("authenticated_role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enhanced_flow_role_resolution(
        self,
    ) -> typing.Optional["EnhancedFlowRoleResolution"]:
        '''Only applicable when setting ``useEnhancedFlow`` to ``true``.

        :default: deny
        '''
        result = self._values.get("enhanced_flow_role_resolution")
        return typing.cast(typing.Optional["EnhancedFlowRoleResolution"], result)

    @builtins.property
    def identity_pool_name(self) -> typing.Optional[builtins.str]:
        '''Name of the Identity Pool.'''
        result = self._values.get("identity_pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def open_id_connect_provider(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider]:
        '''Provide this or attempt will be made to import OpenIdConnectProvider using defaults.

        :default: Attempts to imports OIDC Provider from AWS Account
        '''
        result = self._values.get("open_id_connect_provider")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider], result)

    @builtins.property
    def pool_id_export_name(self) -> typing.Optional[builtins.str]:
        '''Export name for the CfnOutput containing the Identity Pool ID.'''
        result = self._values.get("pool_id_export_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Set removal policy.'''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def use_enhanced_auth_flow(self) -> typing.Optional[builtins.bool]:
        '''Use Enhanced (Simplified) AuthFlow instead of Basic.

        :default: false
        '''
        result = self._values.get("use_enhanced_auth_flow")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ActionsIdentityPoolV2Props(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsIdentityPrincipalBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPrincipalBuilder",
):
    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        claim_mapping: "ClaimMapping",
        identity_pool_id: builtins.str,
        amr: typing.Optional["AuthenticatedMethodReference"] = None,
        open_id_connect_provider_arn: typing.Optional[builtins.str] = None,
    ) -> "ActionsIdentityPrincipalBuilder":
        '''
        :param claim_mapping: -
        :param identity_pool_id: -
        :param amr: -
        :param open_id_connect_provider_arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__679e0bb5ac87a280cafc36d03be1415105e14bedd3569c5847a1effd7c869f32)
            check_type(argname="argument claim_mapping", value=claim_mapping, expected_type=type_hints["claim_mapping"])
            check_type(argname="argument identity_pool_id", value=identity_pool_id, expected_type=type_hints["identity_pool_id"])
            check_type(argname="argument amr", value=amr, expected_type=type_hints["amr"])
            check_type(argname="argument open_id_connect_provider_arn", value=open_id_connect_provider_arn, expected_type=type_hints["open_id_connect_provider_arn"])
        return typing.cast("ActionsIdentityPrincipalBuilder", jsii.sinvoke(cls, "create", [claim_mapping, identity_pool_id, amr, open_id_connect_provider_arn]))

    @jsii.member(jsii_name="createPrincipal")
    def create_principal(
        self,
        requirements: typing.Union["PrincipalClaimRequirements", typing.Dict[builtins.str, typing.Any]],
        amr: typing.Optional["AuthenticatedMethodReference"] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''
        :param requirements: -
        :param amr: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d443405ca9b4ec72aa2b406c044dd5cffd34d4d979f541c81ec0d91bc9243cc1)
            check_type(argname="argument requirements", value=requirements, expected_type=type_hints["requirements"])
            check_type(argname="argument amr", value=amr, expected_type=type_hints["amr"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.invoke(self, "createPrincipal", [requirements, amr]))

    @jsii.member(jsii_name="getAmrValue")
    def _get_amr_value(
        self,
        amr: typing.Optional["AuthenticatedMethodReference"] = None,
    ) -> builtins.str:
        '''
        :param amr: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2777106f59990cccece4b56f7f8343f8e7f1ad454db77e45484242472065976d)
            check_type(argname="argument amr", value=amr, expected_type=type_hints["amr"])
        return typing.cast(builtins.str, jsii.invoke(self, "getAmrValue", [amr]))


@jsii.enum(jsii_type="@catnekaise/actions-constructs.AuthenticatedMethodReference")
class AuthenticatedMethodReference(enum.Enum):
    AUTHENTICATED = "AUTHENTICATED"
    HOST = "HOST"
    ARN = "ARN"
    '''
    :deprecated: Use ``AuthenticatedMethodReference.HOST`` if needing more specificity than ``authenticated``

    :stability: deprecated
    '''


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.BuilderSettings",
    jsii_struct_bases=[],
    name_mapping={"claims_context": "claimsContext"},
)
class BuilderSettings:
    def __init__(
        self,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    ) -> None:
        '''
        :param claims_context: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0952284c95d32e5881acf9617b6fe33bf4894ae75b332125376d7af016a6c5c)
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claims_context": claims_context,
        }

    @builtins.property
    def claims_context(self) -> _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext:
        result = self._values.get("claims_context")
        assert result is not None, "Required property 'claims_context' is missing"
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuilderSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ChainedPrincipal(
    _aws_cdk_aws_iam_ceddda9d.PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ChainedPrincipal",
):
    def __init__(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.PrincipalWithConditions,
        session_tags: builtins.bool,
        external_ids: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param principal: -
        :param session_tags: -
        :param external_ids: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f63dee69b08feab59b87db48d5b94bcf39ba7533ed2ebaa389e5f86f868c6e8b)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument session_tags", value=session_tags, expected_type=type_hints["session_tags"])
            check_type(argname="argument external_ids", value=external_ids, expected_type=type_hints["external_ids"])
        jsii.create(self.__class__, self, [principal, session_tags, external_ids])

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(
        self,
        doc: _aws_cdk_aws_iam_ceddda9d.PolicyDocument,
    ) -> None:
        '''Add the principal to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param doc: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__117d187f37cdd2cd5f312c5f8e4b3a3d9b9ea102c7ce585c06d2e95f2558e2b0)
            check_type(argname="argument doc", value=doc, expected_type=type_hints["doc"])
        return typing.cast(None, jsii.invoke(self, "addToAssumeRolePolicy", [doc]))

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''Return whether or not this principal is equal to the given principal.'''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> _aws_cdk_aws_iam_ceddda9d.PrincipalPolicyFragment:
        '''Return the policy fragment that identifies this principal in a Policy.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.ChainedPrincipalCreateOptions",
    jsii_struct_bases=[],
    name_mapping={"pass_claims": "passClaims"},
)
class ChainedPrincipalCreateOptions:
    def __init__(
        self,
        *,
        pass_claims: typing.Optional[typing.Union[_catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param pass_claims: 
        '''
        if isinstance(pass_claims, dict):
            pass_claims = _catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings(**pass_claims)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22d58ba04d620f703d369425bf6cf64fe109534ab2f217c0724dc36782ef23b)
            check_type(argname="argument pass_claims", value=pass_claims, expected_type=type_hints["pass_claims"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pass_claims is not None:
            self._values["pass_claims"] = pass_claims

    @builtins.property
    def pass_claims(
        self,
    ) -> typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings]:
        result = self._values.get("pass_claims")
        return typing.cast(typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChainedPrincipalCreateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ClaimMapping(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ClaimMapping",
):
    @jsii.member(jsii_name="fromClaimsAsTagNames")
    @builtins.classmethod
    def from_claims_as_tag_names(
        cls,
        claim: "GhaClaim",
        *additional_claims: "GhaClaim",
    ) -> "ClaimMapping":
        '''
        :param claim: -
        :param additional_claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9c68e9d9006d0e1e55d005b123a2fcd06cc56515401eab0c9db25670ead7246)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument additional_claims", value=additional_claims, expected_type=typing.Tuple[type_hints["additional_claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ClaimMapping", jsii.sinvoke(cls, "fromClaimsAsTagNames", [claim, *additional_claims]))

    @jsii.member(jsii_name="fromCustomTagNames")
    @builtins.classmethod
    def from_custom_tag_names(
        cls,
        claims: typing.Mapping[builtins.str, builtins.str],
    ) -> "ClaimMapping":
        '''
        :param claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4db1daa4f859f221973de296b83426a0a9d47e1cca4e0ad6f619166502ce19)
            check_type(argname="argument claims", value=claims, expected_type=type_hints["claims"])
        return typing.cast("ClaimMapping", jsii.sinvoke(cls, "fromCustomTagNames", [claims]))

    @jsii.member(jsii_name="fromDefaults")
    @builtins.classmethod
    def from_defaults(
        cls,
        claim: "GhaClaim",
        *additional_claims: "GhaClaim",
    ) -> "ClaimMapping":
        '''
        :param claim: -
        :param additional_claims: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6415c258123522e4d9a23e153b00a1a01359457f24da0dc318e077d2ae74561)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument additional_claims", value=additional_claims, expected_type=typing.Tuple[type_hints["additional_claims"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ClaimMapping", jsii.sinvoke(cls, "fromDefaults", [claim, *additional_claims]))

    @builtins.property
    @jsii.member(jsii_name="claims")
    def claims(self) -> typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Claim]:
        return typing.cast(typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Claim], jsii.get(self, "claims"))

    @builtins.property
    @jsii.member(jsii_name="mappedClaims")
    def mapped_claims(self) -> typing.List["MappedClaim"]:
        return typing.cast(typing.List["MappedClaim"], jsii.get(self, "mappedClaims"))


class Constrainer(
    ActionsIdentityConstraints,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/actions-constructs.Constrainer",
):
    def __init__(
        self,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
    ) -> None:
        '''
        :param claims_context: 
        :param policy_type: 
        '''
        settings = ConstrainerSettings(
            claims_context=claims_context, policy_type=policy_type
        )

        jsii.create(self.__class__, self, [settings])

    @jsii.member(jsii_name="hasResourceTagEqualToClaim")
    def has_resource_tag_equal_to_claim(
        self,
        resource_tag_name: builtins.str,
        claim: "GhaClaim",
    ) -> "Constrainer":
        '''
        :param resource_tag_name: -
        :param claim: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02cabc566f868f06b7ad3f2444822c138bb4926a37f48f0d87f94718e5fa4c2b)
            check_type(argname="argument resource_tag_name", value=resource_tag_name, expected_type=type_hints["resource_tag_name"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
        return typing.cast("Constrainer", jsii.invoke(self, "hasResourceTagEqualToClaim", [resource_tag_name, claim]))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def _settings(self) -> "ConstrainerSettings":
        return typing.cast("ConstrainerSettings", jsii.get(self, "settings"))


class _ConstrainerProxy(
    Constrainer,
    jsii.proxy_for(ActionsIdentityConstraints), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Constrainer).__jsii_proxy_class__ = lambda : _ConstrainerProxy


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.ConstrainerSettings",
    jsii_struct_bases=[],
    name_mapping={"claims_context": "claimsContext", "policy_type": "policyType"},
)
class ConstrainerSettings:
    def __init__(
        self,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
    ) -> None:
        '''
        :param claims_context: 
        :param policy_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9748bb7fb446bcb539119e1f1b23837d5652f0b5e6d702a01b570c5476c207a1)
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claims_context": claims_context,
        }
        if policy_type is not None:
            self._values["policy_type"] = policy_type

    @builtins.property
    def claims_context(self) -> _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext:
        result = self._values.get("claims_context")
        assert result is not None, "Required property 'claims_context' is missing"
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext, result)

    @builtins.property
    def policy_type(
        self,
    ) -> typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType]:
        result = self._values.get("policy_type")
        return typing.cast(typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConstrainerSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_catnekaise_cdk_iam_utilities_ea41761b.IConstraintsBuilder)
class ConstraintsBuilder(
    ActionsIdentityConstraints,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/actions-constructs.ConstraintsBuilder",
):
    def __init__(
        self,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    ) -> None:
        '''
        :param claims_context: 
        '''
        settings = BuilderSettings(claims_context=claims_context)

        jsii.create(self.__class__, self, [settings])

    @jsii.member(jsii_name="applyToPolicyOfType")
    def _apply_to_policy_of_type(
        self,
        scope: _constructs_77d1e7e8.Construct,
        statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
        policy_type: _catnekaise_cdk_iam_utilities_ea41761b.PolicyType,
        additional_constraints: typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint],
    ) -> None:
        '''
        :param scope: -
        :param statement: -
        :param policy_type: -
        :param additional_constraints: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e9063700e3a35f2d882d08775b0bdf4976c14a6d9d61ef6c0af8b53b9dd99b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
            check_type(argname="argument policy_type", value=policy_type, expected_type=type_hints["policy_type"])
            check_type(argname="argument additional_constraints", value=additional_constraints, expected_type=type_hints["additional_constraints"])
        return typing.cast(None, jsii.invoke(self, "applyToPolicyOfType", [scope, statement, policy_type, additional_constraints]))

    @builtins.property
    @jsii.member(jsii_name="addedConstraints")
    def _added_constraints(
        self,
    ) -> typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Constraint]:
        return typing.cast(typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Constraint], jsii.get(self, "addedConstraints"))

    @builtins.property
    @jsii.member(jsii_name="constraints")
    def constraints(
        self,
    ) -> typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Constraint]:
        return typing.cast(typing.List[_catnekaise_cdk_iam_utilities_ea41761b.Constraint], jsii.get(self, "constraints"))

    @builtins.property
    @jsii.member(jsii_name="settings")
    def _settings(self) -> BuilderSettings:
        return typing.cast(BuilderSettings, jsii.get(self, "settings"))


class _ConstraintsBuilderProxy(
    ConstraintsBuilder,
    jsii.proxy_for(ActionsIdentityConstraints), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ConstraintsBuilder).__jsii_proxy_class__ = lambda : _ConstraintsBuilderProxy


@jsii.enum(jsii_type="@catnekaise/actions-constructs.EnhancedFlowMatchType")
class EnhancedFlowMatchType(enum.Enum):
    EQUALS = "EQUALS"
    CONTAINS = "CONTAINS"
    STARTS_WITH = "STARTS_WITH"
    NOT_EQUALS = "NOT_EQUALS"


@jsii.enum(jsii_type="@catnekaise/actions-constructs.EnhancedFlowRoleResolution")
class EnhancedFlowRoleResolution(enum.Enum):
    DENY = "DENY"
    USE_DEFAULT_AUTHENTICATED_ROLE = "USE_DEFAULT_AUTHENTICATED_ROLE"


@jsii.enum(jsii_type="@catnekaise/actions-constructs.GhaClaim")
class GhaClaim(enum.Enum):
    JTI = "JTI"
    SUB = "SUB"
    ENVIRONMENT = "ENVIRONMENT"
    AUD = "AUD"
    REF = "REF"
    SHA = "SHA"
    REPOSITORY = "REPOSITORY"
    REPOSITORY_OWNER = "REPOSITORY_OWNER"
    ACTOR_ID = "ACTOR_ID"
    REPOSITORY_VISIBILITY = "REPOSITORY_VISIBILITY"
    REPOSITORY_ID = "REPOSITORY_ID"
    REPOSITORY_OWNER_ID = "REPOSITORY_OWNER_ID"
    RUN_ID = "RUN_ID"
    RUN_NUMBER = "RUN_NUMBER"
    RUN_ATTEMPT = "RUN_ATTEMPT"
    RUNNER_ENVIRONMENT = "RUNNER_ENVIRONMENT"
    ACTOR = "ACTOR"
    WORKFLOW = "WORKFLOW"
    HEAD_REF = "HEAD_REF"
    BASE_REF = "BASE_REF"
    EVENT_NAME = "EVENT_NAME"
    REF_TYPE = "REF_TYPE"
    JOB_WORKFLOW_REF = "JOB_WORKFLOW_REF"
    WORKFLOW_REF = "WORKFLOW_REF"
    ISS = "ISS"
    ENTERPRISE = "ENTERPRISE"


class GitHubActionsClaimConstraint(
    _catnekaise_cdk_iam_utilities_ea41761b.ClaimConstraint,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.GitHubActionsClaimConstraint",
):
    def __init__(
        self,
        operator: _catnekaise_cdk_iam_utilities_ea41761b.ConditionOperator,
        claim: GhaClaim,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: -
        :param claim: -
        :param values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15684106be45daeb7387c00c3e9adf982113d157f6d159e6b6905fab7f1ad557)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        jsii.create(self.__class__, self, [operator, claim, values])

    @jsii.member(jsii_name="actorEquals")
    @builtins.classmethod
    def actor_equals(cls, *actors: builtins.str) -> "GitHubActionsClaimConstraint":
        '''
        :param actors: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bdd5915407010a4d6acf58a43fe7b8d358fa972d21c70d6eea10345eadad477)
            check_type(argname="argument actors", value=actors, expected_type=typing.Tuple[type_hints["actors"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GitHubActionsClaimConstraint", jsii.sinvoke(cls, "actorEquals", [*actors]))

    @jsii.member(jsii_name="claimCondition")
    @builtins.classmethod
    def claim_condition(
        cls,
        operator: _catnekaise_cdk_iam_utilities_ea41761b.ConditionOperator,
        claim: GhaClaim,
        *values: builtins.str,
    ) -> "GitHubActionsClaimConstraint":
        '''
        :param operator: -
        :param claim: -
        :param values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51e29daca092cc79f2da95502bc637e2aab0beb38ef6e790a5fb286748985f1b)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GitHubActionsClaimConstraint", jsii.sinvoke(cls, "claimCondition", [operator, claim, *values]))

    @jsii.member(jsii_name="claimEquals")
    @builtins.classmethod
    def claim_equals(
        cls,
        claim: GhaClaim,
        value: builtins.str,
        *additional_values: builtins.str,
    ) -> "GitHubActionsClaimConstraint":
        '''
        :param claim: -
        :param value: -
        :param additional_values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__532d4dd4e80c75e877d7388e4915bc96a257ae4b35f90f9b2e71e90ed31f2f3b)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument additional_values", value=additional_values, expected_type=typing.Tuple[type_hints["additional_values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GitHubActionsClaimConstraint", jsii.sinvoke(cls, "claimEquals", [claim, value, *additional_values]))

    @jsii.member(jsii_name="claimLike")
    @builtins.classmethod
    def claim_like(
        cls,
        claim: GhaClaim,
        *values: builtins.str,
    ) -> "GitHubActionsClaimConstraint":
        '''
        :param claim: -
        :param values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6991d35e747b57260de068a2b3550aea1f4d922314de888e29778c5537e91d)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GitHubActionsClaimConstraint", jsii.sinvoke(cls, "claimLike", [claim, *values]))

    @jsii.member(jsii_name="environmentEquals")
    @builtins.classmethod
    def environment_equals(
        cls,
        *environments: builtins.str,
    ) -> "GitHubActionsClaimConstraint":
        '''
        :param environments: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffabbd6ce152d98b0d51716b50fd853a7bfcc192c90b4b307bd3a2b6d19ca4b9)
            check_type(argname="argument environments", value=environments, expected_type=typing.Tuple[type_hints["environments"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GitHubActionsClaimConstraint", jsii.sinvoke(cls, "environmentEquals", [*environments]))

    @jsii.member(jsii_name="jobWorkflowLike")
    @builtins.classmethod
    def job_workflow_like(
        cls,
        organization: builtins.str,
        repository_name: builtins.str,
        filename: typing.Optional[builtins.str] = None,
        ref: typing.Optional[builtins.str] = None,
    ) -> "GitHubActionsClaimConstraint":
        '''
        :param organization: Name of organization or user.
        :param repository_name: Name of repository.
        :param filename: Default value is '*'.
        :param ref: Default value is '*'.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f0037c488a893fe53ff034616de5f6e2dff649e238d326d3861176369ae1f55)
            check_type(argname="argument organization", value=organization, expected_type=type_hints["organization"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument filename", value=filename, expected_type=type_hints["filename"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        return typing.cast("GitHubActionsClaimConstraint", jsii.sinvoke(cls, "jobWorkflowLike", [organization, repository_name, filename, ref]))

    @jsii.member(jsii_name="repoOwners")
    @builtins.classmethod
    def repo_owners(cls, *owners: builtins.str) -> "GitHubActionsClaimConstraint":
        '''Value(s) of GitHub organizations or users running GitHub Actions.

        :param owners: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f870195d8fdbbbcacd789dea8d0c7df318ac6a02c4581023d523825d653dd233)
            check_type(argname="argument owners", value=owners, expected_type=typing.Tuple[type_hints["owners"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GitHubActionsClaimConstraint", jsii.sinvoke(cls, "repoOwners", [*owners]))

    @jsii.member(jsii_name="repositoryLike")
    @builtins.classmethod
    def repository_like(
        cls,
        *repositories: builtins.str,
    ) -> "GitHubActionsClaimConstraint":
        '''
        :param repositories: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f6163e6b28225ce046d5a435967b6bbfa3a7225c7b8aba020612cd93936c990)
            check_type(argname="argument repositories", value=repositories, expected_type=typing.Tuple[type_hints["repositories"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("GitHubActionsClaimConstraint", jsii.sinvoke(cls, "repositoryLike", [*repositories]))

    @jsii.member(jsii_name="assemble")
    def assemble(
        self,
        scope: _constructs_77d1e7e8.Construct,
        *,
        effect: _aws_cdk_aws_iam_ceddda9d.Effect,
        policy_type: _catnekaise_cdk_iam_utilities_ea41761b.PolicyType,
        claims_context: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext] = None,
    ) -> typing.List[_catnekaise_cdk_iam_utilities_ea41761b.ConstraintPolicyMutation]:
        '''
        :param scope: -
        :param effect: 
        :param policy_type: 
        :param claims_context: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1276897667e491a02dd623a8008c8094cd253292557a962fa7589e79bdc62425)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        context = _catnekaise_cdk_iam_utilities_ea41761b.ConstraintAssembleContext(
            effect=effect, policy_type=policy_type, claims_context=claims_context
        )

        return typing.cast(typing.List[_catnekaise_cdk_iam_utilities_ea41761b.ConstraintPolicyMutation], jsii.invoke(self, "assemble", [scope, context]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SelfHosted")
    def SELF_HOSTED(cls) -> "GitHubActionsClaimConstraint":
        return typing.cast("GitHubActionsClaimConstraint", jsii.sget(cls, "SelfHosted"))


class GrantConstrainer(
    Constrainer,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.GrantConstrainer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        grant: _aws_cdk_aws_iam_ceddda9d.Grant,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
    ) -> None:
        '''
        :param scope: -
        :param grant: -
        :param claims_context: 
        :param policy_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2427e10f71bcba9e0199eb31fc284d233c67b2aecf3aabd56f14e459fa77c2c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument grant", value=grant, expected_type=type_hints["grant"])
        settings = ConstrainerSettings(
            claims_context=claims_context, policy_type=policy_type
        )

        jsii.create(self.__class__, self, [scope, grant, settings])

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        grant: _aws_cdk_aws_iam_ceddda9d.Grant,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
    ) -> "GrantConstrainer":
        '''
        :param scope: -
        :param grant: -
        :param claims_context: 
        :param policy_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9304dd5192bbbec291ceb0ba042fc6aeb20a1aa084eef4831b70d1e81044d0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument grant", value=grant, expected_type=type_hints["grant"])
        settings = ConstrainerSettings(
            claims_context=claims_context, policy_type=policy_type
        )

        return typing.cast("GrantConstrainer", jsii.sinvoke(cls, "create", [scope, grant, settings]))

    @jsii.member(jsii_name="add")
    def add(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> "GrantConstrainer":
        '''
        :param constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0b697055b38468475ae534970f99db33e0d35b7bdfee93b1c8a89cdaf7e0769)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
        return typing.cast("GrantConstrainer", jsii.invoke(self, "add", [constraint]))

    @jsii.member(jsii_name="addConstraint")
    def _add_constraint(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> None:
        '''
        :param constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1a2cee3e398216b1b9746ce3bed9ad334a148d9d09ea8a5ecbffee481a4cff4)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
        return typing.cast(None, jsii.invoke(self, "addConstraint", [constraint]))


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.GrantOrgRoleChainSettings",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_account_ids": "excludeAccountIds",
        "resource_org_paths": "resourceOrgPaths",
        "resource_org_path_string_equals": "resourceOrgPathStringEquals",
        "role_has_resource_tags": "roleHasResourceTags",
        "role_path": "rolePath",
    },
)
class GrantOrgRoleChainSettings:
    def __init__(
        self,
        *,
        exclude_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_org_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_org_path_string_equals: typing.Optional[builtins.bool] = None,
        role_has_resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        role_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param exclude_account_ids: Prevent assuming roles in these accounts.
        :param resource_org_paths: Require roles to exist under specified organization paths.
        :param resource_org_path_string_equals: Match resourcePaths using StringEquals instead of StringLike.
        :param role_has_resource_tags: Role has resource tags matching specified values. If tag value matches a known GitHub Actions claim, then value is changed to ``${aws:PrincipalTag/value}``
        :param role_path: Require that roles exist under this path for sts:AssumeRole.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d9af6dd533c2425eaf1c7baf9fe646da833c82ea089fed8b91f414f0739d61e)
            check_type(argname="argument exclude_account_ids", value=exclude_account_ids, expected_type=type_hints["exclude_account_ids"])
            check_type(argname="argument resource_org_paths", value=resource_org_paths, expected_type=type_hints["resource_org_paths"])
            check_type(argname="argument resource_org_path_string_equals", value=resource_org_path_string_equals, expected_type=type_hints["resource_org_path_string_equals"])
            check_type(argname="argument role_has_resource_tags", value=role_has_resource_tags, expected_type=type_hints["role_has_resource_tags"])
            check_type(argname="argument role_path", value=role_path, expected_type=type_hints["role_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if exclude_account_ids is not None:
            self._values["exclude_account_ids"] = exclude_account_ids
        if resource_org_paths is not None:
            self._values["resource_org_paths"] = resource_org_paths
        if resource_org_path_string_equals is not None:
            self._values["resource_org_path_string_equals"] = resource_org_path_string_equals
        if role_has_resource_tags is not None:
            self._values["role_has_resource_tags"] = role_has_resource_tags
        if role_path is not None:
            self._values["role_path"] = role_path

    @builtins.property
    def exclude_account_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Prevent assuming roles in these accounts.'''
        result = self._values.get("exclude_account_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_org_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Require roles to exist under specified organization paths.'''
        result = self._values.get("resource_org_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_org_path_string_equals(self) -> typing.Optional[builtins.bool]:
        '''Match resourcePaths using StringEquals instead of StringLike.'''
        result = self._values.get("resource_org_path_string_equals")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def role_has_resource_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Role has resource tags matching specified values.

        If tag value matches a known GitHub Actions claim, then value is changed to ``${aws:PrincipalTag/value}``
        '''
        result = self._values.get("role_has_resource_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def role_path(self) -> typing.Optional[builtins.str]:
        '''Require that roles exist under this path for sts:AssumeRole.'''
        result = self._values.get("role_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantOrgRoleChainSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.MappedClaim",
    jsii_struct_bases=[],
    name_mapping={"claim": "claim", "tag_name": "tagName"},
)
class MappedClaim:
    def __init__(self, *, claim: GhaClaim, tag_name: builtins.str) -> None:
        '''
        :param claim: 
        :param tag_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c20a3f1a8d7b9cacb9303d02f3b72bab71f809dce4c1d6bcffcf49e0df434a25)
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument tag_name", value=tag_name, expected_type=type_hints["tag_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claim": claim,
            "tag_name": tag_name,
        }

    @builtins.property
    def claim(self) -> GhaClaim:
        result = self._values.get("claim")
        assert result is not None, "Required property 'claim' is missing"
        return typing.cast(GhaClaim, result)

    @builtins.property
    def tag_name(self) -> builtins.str:
        result = self._values.get("tag_name")
        assert result is not None, "Required property 'tag_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MappedClaim(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyStatementConstrainer(
    Constrainer,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.PolicyStatementConstrainer",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        policy_statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
    ) -> None:
        '''
        :param scope: -
        :param policy_statement: -
        :param claims_context: 
        :param policy_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5132d75a32adc2ba58dcb05b3b3526523560f4ef20a0c19107bdc8f500d9f2f7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument policy_statement", value=policy_statement, expected_type=type_hints["policy_statement"])
        settings = ConstrainerSettings(
            claims_context=claims_context, policy_type=policy_type
        )

        jsii.create(self.__class__, self, [scope, policy_statement, settings])

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        policy_statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
    ) -> "PolicyStatementConstrainer":
        '''
        :param scope: -
        :param policy_statement: -
        :param claims_context: 
        :param policy_type: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80843efeb4dc3dab35d645be06a0ff92bb852e4fec022d6934b1911ab4571ea)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument policy_statement", value=policy_statement, expected_type=type_hints["policy_statement"])
        settings = ConstrainerSettings(
            claims_context=claims_context, policy_type=policy_type
        )

        return typing.cast("PolicyStatementConstrainer", jsii.sinvoke(cls, "create", [scope, policy_statement, settings]))

    @jsii.member(jsii_name="add")
    def add(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> "PolicyStatementConstrainer":
        '''
        :param constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7f0230ad60c8ee8fa55d4c8340ad3fb40f711052e547aa13808740a810b66c)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
        return typing.cast("PolicyStatementConstrainer", jsii.invoke(self, "add", [constraint]))

    @jsii.member(jsii_name="addConstraint")
    def _add_constraint(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> None:
        '''
        :param constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a92fa439e039b4ce005ba578cf2f986f040a0dc545c5a44498236b8c6adbe35)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
        return typing.cast(None, jsii.invoke(self, "addConstraint", [constraint]))


class PrincipalBuilder(
    ConstraintsBuilder,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.PrincipalBuilder",
):
    def __init__(
        self,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    ) -> None:
        '''
        :param claims_context: 
        '''
        settings = BuilderSettings(claims_context=claims_context)

        jsii.create(self.__class__, self, [settings])

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        constraints: typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint],
    ) -> "PrincipalBuilder":
        '''
        :param claims_context: -
        :param constraints: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4b8a79699304f7a2c5cb36e1aa41615a1c40523c487eae05b3138ba460aae3)
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
            check_type(argname="argument constraints", value=constraints, expected_type=type_hints["constraints"])
        return typing.cast("PrincipalBuilder", jsii.sinvoke(cls, "create", [claims_context, constraints]))

    @jsii.member(jsii_name="add")
    def add(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
        *additional_constraints: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> "PrincipalBuilder":
        '''
        :param constraint: -
        :param additional_constraints: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904ed409cf0212a7f05e5d140fd2106e0f3bb96d9303218a8d0fe53289be60e7)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
            check_type(argname="argument additional_constraints", value=additional_constraints, expected_type=typing.Tuple[type_hints["additional_constraints"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("PrincipalBuilder", jsii.invoke(self, "add", [constraint, *additional_constraints]))

    @jsii.member(jsii_name="addConstraint")
    def _add_constraint(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> None:
        '''
        :param constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b903cf2bb92f84919bcc8f5aef243f4064caf8b812a0932f6528d327da0eb7e)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
        return typing.cast(None, jsii.invoke(self, "addConstraint", [constraint]))

    @jsii.member(jsii_name="createPrincipal")
    def create_principal(
        self,
        scope: _constructs_77d1e7e8.Construct,
    ) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''
        :param scope: Any construct will do. Is used for annotating warnings
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523ea782ea81b0512c8c540f5a8d624acb1bd4f74e5b90405f413069f29ca965)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.invoke(self, "createPrincipal", [scope]))


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.PrincipalClaimRequirementCondition",
    jsii_struct_bases=[],
    name_mapping={"condition": "condition", "values": "values"},
)
class PrincipalClaimRequirementCondition:
    def __init__(
        self,
        *,
        condition: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param condition: 
        :param values: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79bc2489cc848f5f026af5e8aee8c9cdf684c1725627340a0334522c0474545d)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition": condition,
            "values": values,
        }

    @builtins.property
    def condition(self) -> builtins.str:
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrincipalClaimRequirementCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@catnekaise/actions-constructs.PrincipalClaimRequirements",
    jsii_struct_bases=[],
    name_mapping={
        "actor": "actor",
        "actor_id": "actorId",
        "environment": "environment",
        "job_workflow_ref": "jobWorkflowRef",
        "repository": "repository",
        "repository_owner": "repositoryOwner",
        "runner_environment": "runnerEnvironment",
        "workflow_ref": "workflowRef",
    },
)
class PrincipalClaimRequirements:
    def __init__(
        self,
        *,
        actor: typing.Optional[typing.Sequence[builtins.str]] = None,
        actor_id: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[PrincipalClaimRequirementCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        job_workflow_ref: typing.Optional[typing.Union[PrincipalClaimRequirementCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        repository: typing.Optional[typing.Union[PrincipalClaimRequirementCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        repository_owner: typing.Optional[typing.Sequence[builtins.str]] = None,
        runner_environment: typing.Optional[builtins.str] = None,
        workflow_ref: typing.Optional[typing.Union[PrincipalClaimRequirementCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param actor: 
        :param actor_id: 
        :param environment: 
        :param job_workflow_ref: 
        :param repository: 
        :param repository_owner: 
        :param runner_environment: 
        :param workflow_ref: 
        '''
        if isinstance(environment, dict):
            environment = PrincipalClaimRequirementCondition(**environment)
        if isinstance(job_workflow_ref, dict):
            job_workflow_ref = PrincipalClaimRequirementCondition(**job_workflow_ref)
        if isinstance(repository, dict):
            repository = PrincipalClaimRequirementCondition(**repository)
        if isinstance(workflow_ref, dict):
            workflow_ref = PrincipalClaimRequirementCondition(**workflow_ref)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f1ba7b678372452dfb3677704ea459b21d7cdce81416c96172f41e835128fbe)
            check_type(argname="argument actor", value=actor, expected_type=type_hints["actor"])
            check_type(argname="argument actor_id", value=actor_id, expected_type=type_hints["actor_id"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument job_workflow_ref", value=job_workflow_ref, expected_type=type_hints["job_workflow_ref"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument repository_owner", value=repository_owner, expected_type=type_hints["repository_owner"])
            check_type(argname="argument runner_environment", value=runner_environment, expected_type=type_hints["runner_environment"])
            check_type(argname="argument workflow_ref", value=workflow_ref, expected_type=type_hints["workflow_ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actor is not None:
            self._values["actor"] = actor
        if actor_id is not None:
            self._values["actor_id"] = actor_id
        if environment is not None:
            self._values["environment"] = environment
        if job_workflow_ref is not None:
            self._values["job_workflow_ref"] = job_workflow_ref
        if repository is not None:
            self._values["repository"] = repository
        if repository_owner is not None:
            self._values["repository_owner"] = repository_owner
        if runner_environment is not None:
            self._values["runner_environment"] = runner_environment
        if workflow_ref is not None:
            self._values["workflow_ref"] = workflow_ref

    @builtins.property
    def actor(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("actor")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def actor_id(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("actor_id")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[PrincipalClaimRequirementCondition]:
        result = self._values.get("environment")
        return typing.cast(typing.Optional[PrincipalClaimRequirementCondition], result)

    @builtins.property
    def job_workflow_ref(self) -> typing.Optional[PrincipalClaimRequirementCondition]:
        result = self._values.get("job_workflow_ref")
        return typing.cast(typing.Optional[PrincipalClaimRequirementCondition], result)

    @builtins.property
    def repository(self) -> typing.Optional[PrincipalClaimRequirementCondition]:
        result = self._values.get("repository")
        return typing.cast(typing.Optional[PrincipalClaimRequirementCondition], result)

    @builtins.property
    def repository_owner(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("repository_owner")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def runner_environment(self) -> typing.Optional[builtins.str]:
        result = self._values.get("runner_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_ref(self) -> typing.Optional[PrincipalClaimRequirementCondition]:
        result = self._values.get("workflow_ref")
        return typing.cast(typing.Optional[PrincipalClaimRequirementCondition], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrincipalClaimRequirements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ActionsIdentityPool(
    ActionsIdentityPoolBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ActionsIdentityPool",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        authenticated_role: ActionsIdentityPoolAuthenticatedRoleBehaviour,
        role_resolution: typing.Optional[EnhancedFlowRoleResolution] = None,
        claim_mapping: ClaimMapping,
        principal_claim_requirements: typing.Union[PrincipalClaimRequirements, typing.Dict[builtins.str, typing.Any]],
        authenticated_method_reference: typing.Optional[AuthenticatedMethodReference] = None,
        authenticated_role_name: typing.Optional[builtins.str] = None,
        identity_pool_name: typing.Optional[builtins.str] = None,
        open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
        pool_id_export_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param authenticated_role: Create authenticated role or use first role assigned in role mappings.
        :param role_resolution: When no rule matches, request should be denied or use default authenticated role.
        :param claim_mapping: 
        :param principal_claim_requirements: Required claims used when not passing any to this.createPrincipalForPool().
        :param authenticated_method_reference: Authenticated Method Reference. authenticated = authenticated host = token.actions.githubusercontent.com arn = arn:aws:iam::111111111111:oidc-provider/token.actions.githubusercontent.com:OIDC:*
        :param authenticated_role_name: Name of authenticated role when creating role.
        :param identity_pool_name: Name of the Identity Pool.
        :param open_id_connect_provider: Provide this or attempt will be made to import OpenIdConnectProvider using defaults.
        :param pool_id_export_name: Export name for the CfnOutput containing the Identity Pool ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71198c71a7b2a7043a022fd40414cfe9b6d75385b93d7b7561a88d4ee74f9a99)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ActionsIdentityPoolProps(
            authenticated_role=authenticated_role,
            role_resolution=role_resolution,
            claim_mapping=claim_mapping,
            principal_claim_requirements=principal_claim_requirements,
            authenticated_method_reference=authenticated_method_reference,
            authenticated_role_name=authenticated_role_name,
            identity_pool_name=identity_pool_name,
            open_id_connect_provider=open_id_connect_provider,
            pool_id_export_name=pool_id_export_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="assignRoleWhenClaimContains")
    def assign_role_when_claim_contains(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.Role,
        claim: GhaClaim,
        value: builtins.str,
    ) -> "ActionsIdentityPool":
        '''
        :param role: -
        :param claim: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6db2e94e740428e61655c877c1df44c850eeb196f0a29dab176c12a9f8d7a02e)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ActionsIdentityPool", jsii.invoke(self, "assignRoleWhenClaimContains", [role, claim, value]))

    @jsii.member(jsii_name="assignRoleWhenClaimEquals")
    def assign_role_when_claim_equals(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.Role,
        claim: GhaClaim,
        value: builtins.str,
    ) -> "ActionsIdentityPool":
        '''Assign role when claim equals value.

        :param role: -
        :param claim: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b05d1abf2ebd3b69cc37cfa613cfe3f49d2e3d8273ed8ad65db733974b5232e)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ActionsIdentityPool", jsii.invoke(self, "assignRoleWhenClaimEquals", [role, claim, value]))

    @jsii.member(jsii_name="assignRoleWhenClaimStartsWith")
    def assign_role_when_claim_starts_with(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.Role,
        claim: GhaClaim,
        value: builtins.str,
    ) -> "ActionsIdentityPool":
        '''Assign role when "sub" claim starts with value.

        :param role: -
        :param claim: -
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdde2ffc5d9a453eac0e57fb099f4b592ef0e20f494f3940fb5450a6e691bdf3)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument claim", value=claim, expected_type=type_hints["claim"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("ActionsIdentityPool", jsii.invoke(self, "assignRoleWhenClaimStartsWith", [role, claim, value]))

    @builtins.property
    @jsii.member(jsii_name="defaultAuthenticatedRole")
    def default_authenticated_role(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role]:
        '''When using ``useFirstAssigned`` authenticatedRole, this is undefined until first assignment.'''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Role], jsii.get(self, "defaultAuthenticatedRole"))


class ChainedPrincipalBuilder(
    ConstraintsBuilder,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/actions-constructs.ChainedPrincipalBuilder",
):
    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    ) -> "ChainedPrincipalBuilder":
        '''
        :param claims_context: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15524385f1edff042c739cc6ada95952660d59c31ab80cf94496783cdf5bb823)
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
        return typing.cast("ChainedPrincipalBuilder", jsii.sinvoke(cls, "create", [claims_context]))

    @jsii.member(jsii_name="add")
    def add(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
        *additional_constraints: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> "ChainedPrincipalBuilder":
        '''
        :param constraint: -
        :param additional_constraints: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__368e5def6d4b4bd858d5403a62c3735607487aad613228f7244f0c9ad3ea407f)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
            check_type(argname="argument additional_constraints", value=additional_constraints, expected_type=typing.Tuple[type_hints["additional_constraints"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("ChainedPrincipalBuilder", jsii.invoke(self, "add", [constraint, *additional_constraints]))

    @jsii.member(jsii_name="addConstraint")
    def _add_constraint(
        self,
        constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    ) -> None:
        '''
        :param constraint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93a40b9e97171ec3f3a975be50274f7c1f3c2d79baa1d86772abee828fc86a6)
            check_type(argname="argument constraint", value=constraint, expected_type=type_hints["constraint"])
        return typing.cast(None, jsii.invoke(self, "addConstraint", [constraint]))

    @jsii.member(jsii_name="createPrincipalAssumedBy")
    def create_principal_assumed_by(
        self,
        scope: _constructs_77d1e7e8.Construct,
        principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
        *,
        pass_claims: typing.Optional[typing.Union[_catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''
        :param scope: -
        :param principal: -
        :param pass_claims: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f94027dbc7e81f2ab29368fa297158c65d6a33c67f702fae710ea99393183b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        options = ChainedPrincipalCreateOptions(pass_claims=pass_claims)

        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.invoke(self, "createPrincipalAssumedBy", [scope, principal, options]))


__all__ = [
    "ActionsIdentityChainedPrincipalBuilder",
    "ActionsIdentityConstraints",
    "ActionsIdentityIamResourcePathBuilder",
    "ActionsIdentityIamResourcePathBuilderV2",
    "ActionsIdentityMappedClaims",
    "ActionsIdentityPolicyUtility",
    "ActionsIdentityPolicyUtilitySettings",
    "ActionsIdentityPool",
    "ActionsIdentityPoolAuthenticatedRoleBehaviour",
    "ActionsIdentityPoolBase",
    "ActionsIdentityPoolBaseProps",
    "ActionsIdentityPoolBasic",
    "ActionsIdentityPoolBasicProps",
    "ActionsIdentityPoolPrincipalBuilderOptions",
    "ActionsIdentityPoolProps",
    "ActionsIdentityPoolUtils",
    "ActionsIdentityPoolV2",
    "ActionsIdentityPoolV2Props",
    "ActionsIdentityPrincipalBuilder",
    "AuthenticatedMethodReference",
    "BuilderSettings",
    "ChainedPrincipal",
    "ChainedPrincipalBuilder",
    "ChainedPrincipalCreateOptions",
    "ClaimMapping",
    "Constrainer",
    "ConstrainerSettings",
    "ConstraintsBuilder",
    "EnhancedFlowMatchType",
    "EnhancedFlowRoleResolution",
    "GhaClaim",
    "GitHubActionsClaimConstraint",
    "GrantConstrainer",
    "GrantOrgRoleChainSettings",
    "MappedClaim",
    "PolicyStatementConstrainer",
    "PrincipalBuilder",
    "PrincipalClaimRequirementCondition",
    "PrincipalClaimRequirements",
]

publication.publish()

def _typecheckingstub__13d2f6a69939549b6114963e6f82632452f8e24348240d9ebf407b637bfb319e(
    claim_mapping: ClaimMapping,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e89a1594a29bd9bb0c116943007a4b22847182ecab397a88acfa03752f61a8(
    claim: GhaClaim,
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37cb345b006cb452892a8b6bea35cf246546100f80c91b5ba896c0be4b8a351(
    claim: GhaClaim,
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8f537ac61404436bbe2a85a392c552386d6dd2041ee997183d838c522bfc601(
    principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__265d91cb006b7bb2c4b5d641d58336230fa4bb6c95e6471c6fc7f11d019c17c8(
    claim: GhaClaim,
    *additional_claims: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dceea15a13407bd99d3dd6c4c4677a064f25fe1da87757199848d8b2e3f2738(
    external_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f31979e2d99f32c164c8e468743da8f082ed669110ef30d955b92303f76019(
    identity_pool_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01edf5097f67b8fb4ff08aa5fe0cfb3b3d2327eace11b2d466d383269530b149(
    *actors: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__496296eada68d4d4fa8fc5914f6d7ef4fa316cbe8e71abae90f86e0c4ca63697(
    operator: _catnekaise_cdk_iam_utilities_ea41761b.ConditionOperator,
    claim: GhaClaim,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__307a58fef3f0f5c435143cdae8ad5a66a0c4e733ed80e09dfe01ad01109c4e42(
    claim: GhaClaim,
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6277c0713efd5d7ade765d4482e45f0e66668eb77a3b63b949f75f8095ae9ce8(
    claim: GhaClaim,
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cee68bf00785268dfbb22092f0377038104aaf5d4a17b7f801baed5cff3bdea(
    environment: builtins.str,
    *additional_environments: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca01ee0ba71bc3529d07b83396d08bbabc50d86292a362c38bf085e01d3bd1f7(
    organization: builtins.str,
    repository_name: typing.Optional[builtins.str] = None,
    filename: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4458c61cac6e6b461f7b730d952bd26e9b3b322129bf84bacdb522afd1b330(
    *refs: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b6a894742320c5a2cab67931d7d69fbd3f352962392b3db5b6315347f3fa733(
    organization: builtins.str,
    *additional_organizations: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060413733e65a3c2b43f10a8596687dd48d3ed370cfb8ff5ff7bddb8bfb511b9(
    repository: builtins.str,
    *additional_repositories: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7128dfd8bfd9ba08eb68ac0ff55286372d5bd514adc76e59aa7e2943cd0e1f0e(
    repository: builtins.str,
    *additional_repositories: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab67385796fa2c1015170ae1cc9199b6ba5b5d321588ed849aded3e5133a06e(
    constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28a0019179aec37d4a9f23b1a092ad6dcd14131b8a87f9a70d307cc818a24fc(
    claim_mapping: ClaimMapping,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5feda193e60d764b32f6053c90438803b0950317330466a5eef2d0a7308dc0ef(
    value: GhaClaim,
    *additional_values: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2bba97997cfcd0b948310fba3970ba1a76924ad4b470e2238aab84999bbbb7(
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1deb7f20df4ed131f012c4bfb2245d26445b13fdd4ddc66a367e1e969951574(
    separator: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a397d50ff87697bab21f682d500dda845ee5354f1bf973b2645b45028acdb52(
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475622cd4e2a9ef991733bcbccee936cd93720e75714266b7113505d979a027a(
    mapped_claims: _catnekaise_cdk_iam_utilities_ea41761b.IMappedClaims,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__637971f317e75c80dca98cb517be41118c3a59e7459ef0194c34bf277a41419d(
    separator: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__246b1e1791c468aade25ef44d8f7785a95ee8dbacce77d38dbfa2c248e145b68(
    claim: GhaClaim,
    *additional_claims: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc94873fb8aa6eb580ca5d67f2d07a5f653337340cf126ea23d3ed18e3b87746(
    value: _catnekaise_cdk_iam_utilities_ea41761b.PolicyVariable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13200d0fe8e1c255d7d7839e879459d0d84e1489220d0b22bb5553a92cb3704d(
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0141e9cc0ed371e2ea2669a6225b807f792d2522368fcebb7f9d54f7d1df59b3(
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697fff621d1282abf43672080318f318695cef2fa9b0be85c97f1efb4f5e25b7(
    _claims: typing.Sequence[typing.Union[_catnekaise_cdk_iam_utilities_ea41761b.Claim, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8e238634f7df7b66f826212cf4b72122026967b87a73edc7f0a356f0379dd1d(
    claim: GhaClaim,
    *additional_claims: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636e3b20261fec79fafe6b69ba7e947669029f6665bee31e9410601f9a2734f7(
    claims: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dcf8a0712800eb16f8170a2581a23616cd63db0eb3dc67d76c4ec8f383d15a2(
    claim: GhaClaim,
    *additional_claims: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3772b475636084cf9b1ce97612996f9cbcf0c618a4e6b5f26207e791d2e1ed8f(
    *claims: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb5a65ddcb564b7cba1b842fccbfe6c18fe7219d63419ac6c23681e50d59bd2(
    claims: typing.Mapping[builtins.str, builtins.str],
    allow_any_tags: typing.Optional[builtins.bool] = None,
    specifically_allowed_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8baa62e7730ecbd78b1abeedc3267b3af2ab5bbbc00dc95ca61fb747bed6c5f6(
    scope: _constructs_77d1e7e8.Construct,
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    base_principal_constraints: typing.Optional[typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint]] = None,
    default_amr: typing.Optional[AuthenticatedMethodReference] = None,
    identity_pool_account_id: typing.Optional[builtins.str] = None,
    identity_pool_id: typing.Optional[builtins.str] = None,
    identity_pool_uses_enhanced_flow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb0234daaa0038d5a647e481ffdc3faeed5a238b4458cfdd03a4e65f2c47123(
    policy_statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e8bbb57c12bcf0063f5eb9b74245d1d02ab39d810d0bfc4310436a218a9bed9(
    grant: _aws_cdk_aws_iam_ceddda9d.Grant,
    scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9ec5bdf39de767f99eb114b74778be1b2079980cd26aa429d3215c4f14abe3(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *,
    exclude_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_org_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_org_path_string_equals: typing.Optional[builtins.bool] = None,
    role_has_resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    role_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fe4e95fde4c5a93878d6f83841ff89cf334c339367e97a3ee15ae4112c36635(
    amr: typing.Optional[AuthenticatedMethodReference] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9144c2fb0c36a570bad142fdb0b2718cb42a090d0bdc76397f48a4c3ee7068d4(
    claim: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ce4a2fd57ea63d83eb7c48234cb7e469307bb8761cf646a564fb40451d0f98(
    claim: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e909a1c997c0f92807685cf59b84ef239d95867a94ed44d581d52bf8a62e70(
    *value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf195a8bfb14ab23579c74fcdc4fc9b22231a3108676d905105d6b5a6e6f5dd(
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    base_principal_constraints: typing.Optional[typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint]] = None,
    default_amr: typing.Optional[AuthenticatedMethodReference] = None,
    identity_pool_account_id: typing.Optional[builtins.str] = None,
    identity_pool_id: typing.Optional[builtins.str] = None,
    identity_pool_uses_enhanced_flow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81531e8db6105fee95b24b0b55459a3541dee52b55db415a78afbf1a8a091975(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    base_props: typing.Union[ActionsIdentityPoolBaseProps, typing.Dict[builtins.str, typing.Any]],
    allow_classic_flow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a2771b558a1a9d752db8f44251adfff5df7c247de72336fceeabe7a233a131(
    requirements: typing.Optional[typing.Union[PrincipalClaimRequirements, typing.Dict[builtins.str, typing.Any]]] = None,
    amr: typing.Optional[AuthenticatedMethodReference] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b916c54a25eaf320ffb40aa4a746d78ce4a2235fbc30f929c353cd325d7b1ed(
    *,
    claim_mapping: ClaimMapping,
    principal_claim_requirements: typing.Union[PrincipalClaimRequirements, typing.Dict[builtins.str, typing.Any]],
    authenticated_method_reference: typing.Optional[AuthenticatedMethodReference] = None,
    authenticated_role_name: typing.Optional[builtins.str] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
    pool_id_export_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a13836398f9c0384e0d0715ff7dc7695c5ce908f8aedeb76a53696cadb53d21(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    claim_mapping: ClaimMapping,
    principal_claim_requirements: typing.Union[PrincipalClaimRequirements, typing.Dict[builtins.str, typing.Any]],
    authenticated_method_reference: typing.Optional[AuthenticatedMethodReference] = None,
    authenticated_role_name: typing.Optional[builtins.str] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
    pool_id_export_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ae82cb12a2d027c191eca4fe4c9e0eba97cba80d3d3312ea4386b370616f20(
    *,
    claim_mapping: ClaimMapping,
    principal_claim_requirements: typing.Union[PrincipalClaimRequirements, typing.Dict[builtins.str, typing.Any]],
    authenticated_method_reference: typing.Optional[AuthenticatedMethodReference] = None,
    authenticated_role_name: typing.Optional[builtins.str] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
    pool_id_export_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d735f3b68305db539ab55eb1b375308a827a494150c1bdceb78a31a04db3c1da(
    *,
    claim_mapping: ClaimMapping,
    identity_pool_id: builtins.str,
    amr: typing.Optional[AuthenticatedMethodReference] = None,
    open_id_connect_provider_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f017bde67aa4225c7c13bd73111eb0ce8241aeaaf233b2657daa0a1fe90dcaf7(
    *,
    claim_mapping: ClaimMapping,
    principal_claim_requirements: typing.Union[PrincipalClaimRequirements, typing.Dict[builtins.str, typing.Any]],
    authenticated_method_reference: typing.Optional[AuthenticatedMethodReference] = None,
    authenticated_role_name: typing.Optional[builtins.str] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
    pool_id_export_name: typing.Optional[builtins.str] = None,
    authenticated_role: ActionsIdentityPoolAuthenticatedRoleBehaviour,
    role_resolution: typing.Optional[EnhancedFlowRoleResolution] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac9dff5284fda10eca7d3e912fdeb93011384c7d72ff00155fb50ca41b10235(
    claim_mapping: ClaimMapping,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a6864ea4acd2021ed70d0fc40c133e643653d5c54a2afa2a317b2c4b4ca459a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    authenticated_role_constraints: typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint],
    mapped_claims: ActionsIdentityMappedClaims,
    authenticated_method_reference: typing.Optional[AuthenticatedMethodReference] = None,
    authenticated_role_name: typing.Optional[builtins.str] = None,
    enhanced_flow_role_resolution: typing.Optional[EnhancedFlowRoleResolution] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
    pool_id_export_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    use_enhanced_auth_flow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ae0b0315cb4e8549bb550e46ce0fe03fda36a62833ec10ce6db0ffc14596795(
    role: _aws_cdk_aws_iam_ceddda9d.Role,
    claim: GhaClaim,
    match_type: EnhancedFlowMatchType,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab6d184bff5984ac3fe5e6feff9bf0be2bd30dd5725fa6e36add7efc0413eeb(
    *,
    authenticated_role_constraints: typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint],
    mapped_claims: ActionsIdentityMappedClaims,
    authenticated_method_reference: typing.Optional[AuthenticatedMethodReference] = None,
    authenticated_role_name: typing.Optional[builtins.str] = None,
    enhanced_flow_role_resolution: typing.Optional[EnhancedFlowRoleResolution] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
    pool_id_export_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    use_enhanced_auth_flow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__679e0bb5ac87a280cafc36d03be1415105e14bedd3569c5847a1effd7c869f32(
    claim_mapping: ClaimMapping,
    identity_pool_id: builtins.str,
    amr: typing.Optional[AuthenticatedMethodReference] = None,
    open_id_connect_provider_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d443405ca9b4ec72aa2b406c044dd5cffd34d4d979f541c81ec0d91bc9243cc1(
    requirements: typing.Union[PrincipalClaimRequirements, typing.Dict[builtins.str, typing.Any]],
    amr: typing.Optional[AuthenticatedMethodReference] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2777106f59990cccece4b56f7f8343f8e7f1ad454db77e45484242472065976d(
    amr: typing.Optional[AuthenticatedMethodReference] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0952284c95d32e5881acf9617b6fe33bf4894ae75b332125376d7af016a6c5c(
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f63dee69b08feab59b87db48d5b94bcf39ba7533ed2ebaa389e5f86f868c6e8b(
    principal: _aws_cdk_aws_iam_ceddda9d.PrincipalWithConditions,
    session_tags: builtins.bool,
    external_ids: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__117d187f37cdd2cd5f312c5f8e4b3a3d9b9ea102c7ce585c06d2e95f2558e2b0(
    doc: _aws_cdk_aws_iam_ceddda9d.PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22d58ba04d620f703d369425bf6cf64fe109534ab2f217c0724dc36782ef23b(
    *,
    pass_claims: typing.Optional[typing.Union[_catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9c68e9d9006d0e1e55d005b123a2fcd06cc56515401eab0c9db25670ead7246(
    claim: GhaClaim,
    *additional_claims: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4db1daa4f859f221973de296b83426a0a9d47e1cca4e0ad6f619166502ce19(
    claims: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6415c258123522e4d9a23e153b00a1a01359457f24da0dc318e077d2ae74561(
    claim: GhaClaim,
    *additional_claims: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02cabc566f868f06b7ad3f2444822c138bb4926a37f48f0d87f94718e5fa4c2b(
    resource_tag_name: builtins.str,
    claim: GhaClaim,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9748bb7fb446bcb539119e1f1b23837d5652f0b5e6d702a01b570c5476c207a1(
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e9063700e3a35f2d882d08775b0bdf4976c14a6d9d61ef6c0af8b53b9dd99b(
    scope: _constructs_77d1e7e8.Construct,
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    policy_type: _catnekaise_cdk_iam_utilities_ea41761b.PolicyType,
    additional_constraints: typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15684106be45daeb7387c00c3e9adf982113d157f6d159e6b6905fab7f1ad557(
    operator: _catnekaise_cdk_iam_utilities_ea41761b.ConditionOperator,
    claim: GhaClaim,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdd5915407010a4d6acf58a43fe7b8d358fa972d21c70d6eea10345eadad477(
    *actors: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51e29daca092cc79f2da95502bc637e2aab0beb38ef6e790a5fb286748985f1b(
    operator: _catnekaise_cdk_iam_utilities_ea41761b.ConditionOperator,
    claim: GhaClaim,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532d4dd4e80c75e877d7388e4915bc96a257ae4b35f90f9b2e71e90ed31f2f3b(
    claim: GhaClaim,
    value: builtins.str,
    *additional_values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6991d35e747b57260de068a2b3550aea1f4d922314de888e29778c5537e91d(
    claim: GhaClaim,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffabbd6ce152d98b0d51716b50fd853a7bfcc192c90b4b307bd3a2b6d19ca4b9(
    *environments: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f0037c488a893fe53ff034616de5f6e2dff649e238d326d3861176369ae1f55(
    organization: builtins.str,
    repository_name: builtins.str,
    filename: typing.Optional[builtins.str] = None,
    ref: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f870195d8fdbbbcacd789dea8d0c7df318ac6a02c4581023d523825d653dd233(
    *owners: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f6163e6b28225ce046d5a435967b6bbfa3a7225c7b8aba020612cd93936c990(
    *repositories: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1276897667e491a02dd623a8008c8094cd253292557a962fa7589e79bdc62425(
    scope: _constructs_77d1e7e8.Construct,
    *,
    effect: _aws_cdk_aws_iam_ceddda9d.Effect,
    policy_type: _catnekaise_cdk_iam_utilities_ea41761b.PolicyType,
    claims_context: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2427e10f71bcba9e0199eb31fc284d233c67b2aecf3aabd56f14e459fa77c2c6(
    scope: _constructs_77d1e7e8.Construct,
    grant: _aws_cdk_aws_iam_ceddda9d.Grant,
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9304dd5192bbbec291ceb0ba042fc6aeb20a1aa084eef4831b70d1e81044d0e(
    scope: _constructs_77d1e7e8.Construct,
    grant: _aws_cdk_aws_iam_ceddda9d.Grant,
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0b697055b38468475ae534970f99db33e0d35b7bdfee93b1c8a89cdaf7e0769(
    constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a2cee3e398216b1b9746ce3bed9ad334a148d9d09ea8a5ecbffee481a4cff4(
    constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9af6dd533c2425eaf1c7baf9fe646da833c82ea089fed8b91f414f0739d61e(
    *,
    exclude_account_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_org_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_org_path_string_equals: typing.Optional[builtins.bool] = None,
    role_has_resource_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    role_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20a3f1a8d7b9cacb9303d02f3b72bab71f809dce4c1d6bcffcf49e0df434a25(
    *,
    claim: GhaClaim,
    tag_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5132d75a32adc2ba58dcb05b3b3526523560f4ef20a0c19107bdc8f500d9f2f7(
    scope: _constructs_77d1e7e8.Construct,
    policy_statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80843efeb4dc3dab35d645be06a0ff92bb852e4fec022d6934b1911ab4571ea(
    scope: _constructs_77d1e7e8.Construct,
    policy_statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    policy_type: typing.Optional[_catnekaise_cdk_iam_utilities_ea41761b.PolicyType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7f0230ad60c8ee8fa55d4c8340ad3fb40f711052e547aa13808740a810b66c(
    constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a92fa439e039b4ce005ba578cf2f986f040a0dc545c5a44498236b8c6adbe35(
    constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4b8a79699304f7a2c5cb36e1aa41615a1c40523c487eae05b3138ba460aae3(
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    constraints: typing.Sequence[_catnekaise_cdk_iam_utilities_ea41761b.Constraint],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904ed409cf0212a7f05e5d140fd2106e0f3bb96d9303218a8d0fe53289be60e7(
    constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    *additional_constraints: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b903cf2bb92f84919bcc8f5aef243f4064caf8b812a0932f6528d327da0eb7e(
    constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523ea782ea81b0512c8c540f5a8d624acb1bd4f74e5b90405f413069f29ca965(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79bc2489cc848f5f026af5e8aee8c9cdf684c1725627340a0334522c0474545d(
    *,
    condition: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f1ba7b678372452dfb3677704ea459b21d7cdce81416c96172f41e835128fbe(
    *,
    actor: typing.Optional[typing.Sequence[builtins.str]] = None,
    actor_id: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[PrincipalClaimRequirementCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    job_workflow_ref: typing.Optional[typing.Union[PrincipalClaimRequirementCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    repository: typing.Optional[typing.Union[PrincipalClaimRequirementCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    repository_owner: typing.Optional[typing.Sequence[builtins.str]] = None,
    runner_environment: typing.Optional[builtins.str] = None,
    workflow_ref: typing.Optional[typing.Union[PrincipalClaimRequirementCondition, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71198c71a7b2a7043a022fd40414cfe9b6d75385b93d7b7561a88d4ee74f9a99(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    authenticated_role: ActionsIdentityPoolAuthenticatedRoleBehaviour,
    role_resolution: typing.Optional[EnhancedFlowRoleResolution] = None,
    claim_mapping: ClaimMapping,
    principal_claim_requirements: typing.Union[PrincipalClaimRequirements, typing.Dict[builtins.str, typing.Any]],
    authenticated_method_reference: typing.Optional[AuthenticatedMethodReference] = None,
    authenticated_role_name: typing.Optional[builtins.str] = None,
    identity_pool_name: typing.Optional[builtins.str] = None,
    open_id_connect_provider: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IOpenIdConnectProvider] = None,
    pool_id_export_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6db2e94e740428e61655c877c1df44c850eeb196f0a29dab176c12a9f8d7a02e(
    role: _aws_cdk_aws_iam_ceddda9d.Role,
    claim: GhaClaim,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b05d1abf2ebd3b69cc37cfa613cfe3f49d2e3d8273ed8ad65db733974b5232e(
    role: _aws_cdk_aws_iam_ceddda9d.Role,
    claim: GhaClaim,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdde2ffc5d9a453eac0e57fb099f4b592ef0e20f494f3940fb5450a6e691bdf3(
    role: _aws_cdk_aws_iam_ceddda9d.Role,
    claim: GhaClaim,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15524385f1edff042c739cc6ada95952660d59c31ab80cf94496783cdf5bb823(
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368e5def6d4b4bd858d5403a62c3735607487aad613228f7244f0c9ad3ea407f(
    constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
    *additional_constraints: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93a40b9e97171ec3f3a975be50274f7c1f3c2d79baa1d86772abee828fc86a6(
    constraint: _catnekaise_cdk_iam_utilities_ea41761b.Constraint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f94027dbc7e81f2ab29368fa297158c65d6a33c67f702fae710ea99393183b(
    scope: _constructs_77d1e7e8.Construct,
    principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
    *,
    pass_claims: typing.Optional[typing.Union[_catnekaise_cdk_iam_utilities_ea41761b.PassClaimsConstraintSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
