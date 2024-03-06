'''
[![npm (scoped)](https://img.shields.io/npm/v/@catnekaise/ghrawel?style=flat-square)](https://www.npmjs.com/package/@catnekaise/ghrawel)
[![Nuget](https://img.shields.io/nuget/v/Catnekaise.CDK.Ghrawel?style=flat-square)](https://www.nuget.org/packages/Catnekaise.CDK.Ghrawel/)
[![PyPI](https://img.shields.io/pypi/v/catnekaise.ghrawel?style=flat-square)](https://pypi.org/project/catnekaise.ghrawel/)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/catnekaise/ghrawel?sort=semver&style=flat-square)](https://github.com/catnekaise/ghrawel/releases)

# ghrawel

`gh`r`aw`el will aim to provide components that help integrate GitHub and AWS using primarily AWS CDK and minimal application code.

# Token Provider

Use this to deploy an AWS API Gateway RestAPI capable of returning GitHub App installation access tokens and use AWS IAM to control access to this API.

## Table of Contents

* [Use Case](#use-case)
* [When not to use this](#when-not-to-use-this)
* [How it Works](#how-it-works)
* [Setup](#setup)

  * [Costs](#costs)
  * [1. GitHub](#1-github)
  * [2. AWS CDK](#2-aws-cdk)
  * [3. Add Private Key in Parameter Store](#3-add-private-key-in-parameter-store)
  * [4. Request a token](#4-request-a-token)
  * [5. Use the token](#5-use-the-token)
  * [6. Test limits of the token](#6-test-limits-of-the-token)
  * [7. Cleanup](#7-cleanup)
* [Granting Access](#granting-access)
* [Get Token - cURL](#get-token---curl)
* [Get Token - GitHub Actions](#get-token---github-actions)
* [Customize RestAPI and Lambda](#customize-restapi-and-lambda)
* [Next Steps](#next-steps)

  * [Token Providers](#next-steps)
  * [AWS IAM](#next-steps)
  * [Application](#next-steps)
  * [Usage](#next-steps)
  * [GitHub Actions Attribute-based Access Control](#next-steps)
  * [Infrastructure](#next-steps)
  * [Logging](#next-steps)
* [Contributions](#contributions)

## Use case

The private key belonging to a [GitHub App](https://docs.github.com/en/apps/overview) can be used to [create installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app) that only contains a [selection of the permissions](https://docs.github.com/en/rest/apps/apps?apiVersion=2022-11-28#create-an-installation-access-token-for-an-app) that the GitHub App has been granted and also for a limited number of repositories that the GitHub App has been installed in. This installation access token has a maximum lifetime of an hour and can [revoke](https://docs.github.com/en/rest/apps/installations?apiVersion=2022-11-28#revoke-an-installation-access-token) itself.

Use ghrawel to control access to sensitive GitHub API credentials within an AWS and GitHub Actions environments, when such requirements exist.

## When not to use this

Creating PATs or GitHub App Private keys is easy and they are simple to use whether stored in AWS or as a GitHub secret. Using this solution introduces new components and complexity that has to be managed and such a thing is not always worth it.

## How it works

An application or a GitHub Actions workflow with access to AWS IAM Credentials initiates the sequence of events by signing a HTTP request with those credentials.

```mermaid
sequenceDiagram
    autonumber
    participant HTTP as HTTP Request
    participant App as Application/GHA
    note over App: Has AWS IAM Credentials
    participant API as API Gateway
    participant Authorizer as IAM Authorizer
    participant Lambda as Lambda
    participant GitHub as GitHub API
    App->>HTTP: Create and Sign
    App->>API: Send Request
    API->>Authorizer: Authorization
    alt if not authorized
        API-->>App: 401
    end
    API->>Lambda: Forward Authorized Request
    Lambda->>Lambda: Additional validation
    alt if validation fails
        Lambda-->>API: 400 Bad Request
        API-->>App: 400 Bad Request
    end
    Lambda->>GitHub: Request Token
    Lambda->>API: Token Response
    API->>App: Token Response
    App->>GitHub: Uses token
```

# Setup

> [!NOTE]
> The machine deploying will require docker as [catnekaise/ghrawel-tokenprovider-lambda-go](https://github.com/catnekaise/ghrawel-tokenprovider-lambda-go) will be built to run in the lambda function. See [Dockerfile](./lambda/default/Dockerfile) and [application](./docs/token-provider/application.md) for more.

> [!NOTE]
> This guide assumes some familiarity with AWS CDK.

This test setup can be tested with a GitHub App that only has access to a single test repository in GitHub and this repository (and app) can be on your user instead of in your organization.

## Costs

Assuming that you make `10 000` requests using this test setup, the cost of lambda and cloudwatch is covered under the free tier. The cost of the API Gateway RestApi will be between free and 0.035$ depending on how old the AWS Account is. Depending on your AWS Environment there could be charges for CloudTrail, Config, other tools and any custom automations that might create additional resources based on the resources deployed. It's best to test this is a sandbox account.

There are no charges related to GitHub.

## 1. GitHub

> https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app

For our testing purposes we need to create a test `repository` and a `GitHub App`. The app being created shall be considered a test app and should not be granted unnecessary permissions or installed anywhere but in repositories used for testing this. The link above provides additional information about working with GitHub Apps.

1. Create a new empty repository in your organization or on your user which can be used for testing.

   * When creating this repository, initialize the repository so that a default branch with a README.md file is created.
2. Create a GitHub App in the same organization or user and grant `read & write` on the repository level permissions `contents` and `issues`.

   * Do not add configuration under `Identifying and authorizing users` as this app is not for users
   * Put any url under `Homepage URL` as its a required field
   * Deselect `active` under webhook as no webhook shall be configured for this use-case
   * Keep `only on this account` selected
3. Note down the `id` of the GitHub App as it will be used later.
4. Create a new private key for this GitHub App and keep it around as it will be used later.
5. Install the GitHub App in the single test repository that was created further above

## 2.1 Installation

> [!NOTE]
> CDK for .NET can also be used to test this but examples below has to be translated.

```shell
cdk init --language typescript
npm install -s @catnekaise/ghrawel
```

## 2.2 AWS CDK

1. Change the value of `defaultAppId` in the example below to match your newly created GitHub App.
2. Synthesis the stack and review what changes will be made before finally deploying the stack into a sandbox account.

```python
import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import { ManagedGitHubApps, GitHubAppSecretsStorage, TokenProviderApi, PermissionLevel } from '@catnekaise/ghrawel';

const app = new cdk.App();
const stack = new cdk.Stack(app, 'TokenProviderStack');

const apps = new ManagedGitHubApps(stack, 'Apps', {
  // Change this value
  defaultAppId: 1234,
  storage: GitHubAppSecretsStorage.PARAMETER_STORE,
});

const tokenProviderApi = new TokenProviderApi(stack, 'TokenProviderApi', {
  apps,
});

const provider = tokenProviderApi.newTokenProvider('example-provider', {
  permissions: {
    contents: PermissionLevel.READ,
    issues: PermissionLevel.WRITE,
  },
});
```

## 3. Add Private Key in Parameter Store

When the stack has completed its deployment a secure string parameter will have been initialized at path `/catnekaise/github-apps/default` in `Systems Manager Parameter Store` with value `placeholder`. Go there and enter the full text value of GitHub App Private Key created earlier inside the value field of this parameter.

## 4. Request a token

The easiest way to see that this is now working and to request an access token is to head over to the API Gateway in the AWS Console. Examples on how to request a token with [cURL](#get-token---curl) or [GitHub Actions](#get-token---github-actions) can be seen further down, and more in additional [usage docs](./docs/token-provider/usage.md).

1. Open the API that was created.
2. Find the single `GET` method created and select it.
3. Click on the `Test` tab.
4. Enter the name of the organization or user where the test repository is located in the form field labeled `owner`.
5. Enter the name of the test repository in the form field labeled `repo`.
6. Click on the Test button.
7. If everything was done correctly, the response should look similar to below.

![](./docs/images/apigw-console.png)

## 5. Use the token

In this example cURL is used to create an issue in your test repository. Either use this example or use a tool of your choice with the same input. After Successfully performing this test there should be a new issue in your test repository.

```shell
#!/usr/bin/env bash

OWNER="Enter name of organization or user"
REPO="Enter name of repo"
TOKEN="Enter token"

curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Token ${TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/${OWNER}/${REPO}/issues" \
  -d '{"title":"Testing using app installation token","body":"Testing using app installation token"}'
```

## 6. Test limits of the token

If a GitHub App was created with the example permissions further above and the token provider was configured the with access `read` or the permission `contents`, then the token shall be able to read contents in the repository but not write content to the repository.

### 6.1 Read README.md

The following cURL command will fetch the contents of `README.md` and print out body the full JSON body and decode the value of `content` in the body.

```shell
#!/usr/bin/env bash

OWNER="Enter name of organization or user"
REPO="Enter name of repo"
MY_TOKEN="Enter token Value"

README_MD=$(curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Token ${MY_TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/${OWNER}/${REPO}/contents/README.md")

echo "$README_MD"

echo "$README_MD" | jq -r '.content' | base64 -d
```

### 6.2 Write TEST.md

Again, assuming setup have been done as example above, the following cURL command shall **fail** to create the file `TEST.md` in the test repositories default branch.

```shell
#!/usr/bin/env bash

OWNER="Enter name of organization or user"
REPO="Enter name of repo"
MTOKEN="Enter token Value"

curl --fail-with-body -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Token ${TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/${OWNER}/${REPO}/contents/TEST.md" \
  -d '{"message":"my commit message","content":"SGVsbG8gZnJvbSBjYXRuZWthaXNlCg=="}'
```

### 6.3 Create a second token provider

Update the stack by creating a second token provider that is granted `write` for the `contents` permission and re-deploy the stack.

```python
tokenProviderApi.newTokenProvider('example-provider-2', {
  permissions: {
    contents: PermissionLevel.WRITE,
  },
});
```

### 6.4 Retry Creating TEST.md

After deployment, refresh the page in the web browser where you previously generated a token and find the second `GET` method available under the path `/x/example-provider-2/{owner}/{repo}`. Use this token provider to generate a new token for the same repository and re-run the example below. After successfully performing this test there should be a file named `TEST.md` in the root of your test repository on the default branch.

```shell
#!/usr/bin/env bash

OWNER="Enter name of organization or user"
REPO="Enter name of repo"
MY_TOKEN="Enter token Value"

curl --fail-with-body  -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Token ${MY_TOKEN}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/repos/${OWNER}/${REPO}/contents/TEST.md" \
  -d '{"message":"my commit message","content":"SGVsbG8gZnJvbSBjYXRuZWthaXNlCg=="}'
```

## 7. Cleanup

Either clean up now or test this out some more using `cURL` or `GitHub Actions` before cleaning up. The steps to remove everything that was created.

1. In GitHub, find the GitHub App and either uninstall, suspend or delete this GitHub App

   * If wanting to test this again at a later date, suspend the installation and next time re-enable and rotate the private key to resume testing.
   * If done, delete the GitHub App
2. In AWS Console go to CloudFormation and find the Stack that was created and delete it.

# Granting Access

Continue reading [here](./docs/token-provider/aws-iam.md) for more detailed examples.

```python
declare const principal: iam.IPrincipal;

const role = new iam.Role(stack, 'Role', {
  assumedBy: principal,
});

const provider = tokenProviderApi.newTokenProvider('example-provider', {
  permissions: {
    contents: PermissionLevel.READ,
    issues: PermissionLevel.WRITE,
  },
});

provider.grantExecute(role);
```

# Get Token - cURL

This example shows how to use cURL to sign the request with the AWS IAM credentials. The example assumes the existence of `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` and `AWS_SESSION_TOKEN` in the environment.

For more usage examples, check out [usage docs](./docs/token-provider/usage.md).

```shell
AWS_REGION="eu-west-1"
BASE_URL="https://abcd1234.execute-api.${AWS_REGION}.amazonaws.com/dev"
PROVIDER="example-provider"

RESPONSE=$(curl "${BASE_URL}/x/${PROVIDER}/catnekaise/example-repo" \
	--user "${AWS_ACCESS_KEY_ID}":"${AWS_SECRET_ACCESS_KEY}" \
	-H "x-amz-security-token: ${AWS_SESSION_TOKEN}" \
	--aws-sigv4 "aws:amz:${AWS_REGION}:execute-api")

TOKEN=$(echo "$RESPONSE" | jq -r '.token')

## Use Token...
```

# Get Token - GitHub Actions

For more usage examples in GitHub Actions and a re-usable action, check out [GitHub Actions usage docs](./docs/token-provider/github-actions-usage.md).

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
      - name: "Authenticate"
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-region: "eu-west-1"
          role-to-assume: "arn:aws:iam::111111111111:role/role-name"

      - name: "Get Token"
        uses: catnekaise/ghrawel-token@v1
        id: token
        with:
          base-url: "https://abc123d4.execute-api.eu-west-1.amazonaws.com/dev"
          provider-name: "example-provider"
          aws-region: "eu-west-1"
      - name: "Use Token"
        env:
          TOKEN: "${{ steps.token.outputs.token }}"
        run: |
          echo "Utilize the token"
```

# Customize RestAPI and Lambda

Read more in [infrastructure](./docs/token-provider/infrastructure.md) and [application](./docs/token-provider/application.md).

```python
import { ManagedGitHubApps, TokenProviderApi } from '@catnekaise/ghrawel';

const managedLambda = new lambda.Function(stack, 'Function', {
  code: lambda.Code.fromDockerBuild(path.join(process.cwd(), 'node_modules/@catnekaise/ghrawel/lambda/default/Dockerfile'), {
    buildArgs: {
      GIT_REPO: 'https://github.com/catnekaise/example-fork.git',
      GIT_CHECKOUT: 'main',
    },
  }),
  handler: 'bootstrap',
  runtime: lambda.Runtime.PROVIDED_AL2023,
  // Add name, vpc, etc
});

const managedApi = new apigateway.RestApi(stack, 'TokenProviderApi', {
  // Add domain, vpc, etc
});

const apps = new ManagedGitHubApps(stack, 'Apps', {
  defaultAppId: 1234,
  storage: GitHubAppSecretsStorage.PARAMETER_STORE,
  additionalApps: [
    GitHubApp.create('another-app', 1111),
    GitHubApp.create('yet-another-app', 2222),
  ],
});

const tokenProviderApi = new TokenProviderApi(stack, 'TokenProviderApi', {
  apps,
  lambda: managedLambda,
  api: managedApi,
});

tokenProviderApi.newTokenProvider('example-provider', {
  permissions: {
    contents: PermissionLevel.READ,
  },
});
```

# Next Steps

Here're some additional documentation on various topics:

* [Token Providers](./docs/token-provider/README.md)
* [AWS IAM](./docs/token-provider/aws-iam.md)
* [Application](./docs/token-provider/application.md)
* [Usage](./docs/token-provider/usage.md)

  * [cURL](./docs/token-provider/usage.md)
  * [Go](./docs/token-provider/usage.md)
  * [.NET](./docs/token-provider/usage.md)
  * [TypeScript](./docs/token-provider/usage.md)
* [GitHub Actions Attribute-based Access Control](./docs/token-provider/github-actions-abac.md)
* [Infrastructure](./docs/token-provider/infrastructure.md)

  * [Custom Setup](./docs/token-provider/infrastructure.md#custom-setup)
  * [GitHub Apps](./docs/token-provider/infrastructure.md#github-apps)
  * [Lambda](./docs/token-provider/infrastructure.md#lambda)
* [Logging](./docs/token-provider/logging.md)
* [Troubleshooting](./docs/token-provider/README.md#internal-server-error)

# Contributions

Please open issues if having general feedback or if getting stuck on something that was not covered by any documentation. PR's are welcome for bugfixes. For any feature additions, please open an issue for discussion first.
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
import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import catnekaise_cdk_iam_utilities as _catnekaise_cdk_iam_utilities_ea41761b
import constructs as _constructs_77d1e7e8


class GitHubApp(metaclass=jsii.JSIIMeta, jsii_type="@catnekaise/ghrawel.GitHubApp"):
    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(cls, name: builtins.str, app_id: jsii.Number) -> "GitHubApp":
        '''
        :param name: -
        :param app_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b8b58cfbf31d20c1a3f2dbdd99873aeeaa79ca05b9edb00bbfa6c79318414b2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
        return typing.cast("GitHubApp", jsii.sinvoke(cls, "create", [name, app_id]))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appId"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.GitHubAppPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "administration": "administration",
        "checks": "checks",
        "codespaces": "codespaces",
        "contents": "contents",
        "dependabot_secrets": "dependabotSecrets",
        "deployments": "deployments",
        "email_addresses": "emailAddresses",
        "environments": "environments",
        "followers": "followers",
        "git_ssh_keys": "gitSshKeys",
        "gpg_keys": "gpgKeys",
        "interaction_limits": "interactionLimits",
        "issues": "issues",
        "members": "members",
        "metadata": "metadata",
        "organization_administration": "organizationAdministration",
        "organization_announcement_banners": "organizationAnnouncementBanners",
        "organization_copilot_seat_management": "organizationCopilotSeatManagement",
        "organization_custom_org_roles": "organizationCustomOrgRoles",
        "organization_custom_properties": "organizationCustomProperties",
        "organization_custom_roles": "organizationCustomRoles",
        "organization_events": "organizationEvents",
        "organization_hooks": "organizationHooks",
        "organization_packages": "organizationPackages",
        "organization_personal_access_token_requests": "organizationPersonalAccessTokenRequests",
        "organization_personal_access_tokens": "organizationPersonalAccessTokens",
        "organization_plan": "organizationPlan",
        "organization_projects": "organizationProjects",
        "organization_secrets": "organizationSecrets",
        "organization_self_hosted_runners": "organizationSelfHostedRunners",
        "organization_user_blocking": "organizationUserBlocking",
        "packages": "packages",
        "pages": "pages",
        "profile": "profile",
        "pull_requests": "pullRequests",
        "repository_custom_properties": "repositoryCustomProperties",
        "repository_hooks": "repositoryHooks",
        "repository_projects": "repositoryProjects",
        "secrets": "secrets",
        "secret_scanning_alerts": "secretScanningAlerts",
        "security_events": "securityEvents",
        "single_file": "singleFile",
        "starring": "starring",
        "statuses": "statuses",
        "team_discussions": "teamDiscussions",
        "vulnerability_alerts": "vulnerabilityAlerts",
        "workflows": "workflows",
    },
)
class GitHubAppPermissions:
    def __init__(
        self,
        *,
        actions: typing.Optional["PermissionLevel"] = None,
        administration: typing.Optional["PermissionLevel"] = None,
        checks: typing.Optional["PermissionLevel"] = None,
        codespaces: typing.Optional["PermissionLevel"] = None,
        contents: typing.Optional["PermissionLevel"] = None,
        dependabot_secrets: typing.Optional["PermissionLevel"] = None,
        deployments: typing.Optional["PermissionLevel"] = None,
        email_addresses: typing.Optional["PermissionLevel"] = None,
        environments: typing.Optional["PermissionLevel"] = None,
        followers: typing.Optional["PermissionLevel"] = None,
        git_ssh_keys: typing.Optional["PermissionLevel"] = None,
        gpg_keys: typing.Optional["PermissionLevel"] = None,
        interaction_limits: typing.Optional["PermissionLevel"] = None,
        issues: typing.Optional["PermissionLevel"] = None,
        members: typing.Optional["PermissionLevel"] = None,
        metadata: typing.Optional["PermissionLevel"] = None,
        organization_administration: typing.Optional["PermissionLevel"] = None,
        organization_announcement_banners: typing.Optional["PermissionLevel"] = None,
        organization_copilot_seat_management: typing.Optional["PermissionLevel"] = None,
        organization_custom_org_roles: typing.Optional["PermissionLevel"] = None,
        organization_custom_properties: typing.Optional["PermissionLevel"] = None,
        organization_custom_roles: typing.Optional["PermissionLevel"] = None,
        organization_events: typing.Optional["PermissionLevel"] = None,
        organization_hooks: typing.Optional["PermissionLevel"] = None,
        organization_packages: typing.Optional["PermissionLevel"] = None,
        organization_personal_access_token_requests: typing.Optional["PermissionLevel"] = None,
        organization_personal_access_tokens: typing.Optional["PermissionLevel"] = None,
        organization_plan: typing.Optional["PermissionLevel"] = None,
        organization_projects: typing.Optional["PermissionLevel"] = None,
        organization_secrets: typing.Optional["PermissionLevel"] = None,
        organization_self_hosted_runners: typing.Optional["PermissionLevel"] = None,
        organization_user_blocking: typing.Optional["PermissionLevel"] = None,
        packages: typing.Optional["PermissionLevel"] = None,
        pages: typing.Optional["PermissionLevel"] = None,
        profile: typing.Optional["PermissionLevel"] = None,
        pull_requests: typing.Optional["PermissionLevel"] = None,
        repository_custom_properties: typing.Optional["PermissionLevel"] = None,
        repository_hooks: typing.Optional["PermissionLevel"] = None,
        repository_projects: typing.Optional["PermissionLevel"] = None,
        secrets: typing.Optional["PermissionLevel"] = None,
        secret_scanning_alerts: typing.Optional["PermissionLevel"] = None,
        security_events: typing.Optional["PermissionLevel"] = None,
        single_file: typing.Optional["PermissionLevel"] = None,
        starring: typing.Optional["PermissionLevel"] = None,
        statuses: typing.Optional["PermissionLevel"] = None,
        team_discussions: typing.Optional["PermissionLevel"] = None,
        vulnerability_alerts: typing.Optional["PermissionLevel"] = None,
        workflows: typing.Optional["PermissionLevel"] = None,
    ) -> None:
        '''
        :param actions: 
        :param administration: 
        :param checks: 
        :param codespaces: 
        :param contents: 
        :param dependabot_secrets: 
        :param deployments: 
        :param email_addresses: 
        :param environments: 
        :param followers: 
        :param git_ssh_keys: 
        :param gpg_keys: 
        :param interaction_limits: 
        :param issues: 
        :param members: 
        :param metadata: 
        :param organization_administration: 
        :param organization_announcement_banners: 
        :param organization_copilot_seat_management: 
        :param organization_custom_org_roles: 
        :param organization_custom_properties: 
        :param organization_custom_roles: 
        :param organization_events: 
        :param organization_hooks: 
        :param organization_packages: 
        :param organization_personal_access_token_requests: 
        :param organization_personal_access_tokens: 
        :param organization_plan: 
        :param organization_projects: 
        :param organization_secrets: 
        :param organization_self_hosted_runners: 
        :param organization_user_blocking: 
        :param packages: 
        :param pages: 
        :param profile: 
        :param pull_requests: 
        :param repository_custom_properties: 
        :param repository_hooks: 
        :param repository_projects: 
        :param secrets: 
        :param secret_scanning_alerts: 
        :param security_events: 
        :param single_file: 
        :param starring: 
        :param statuses: 
        :param team_discussions: 
        :param vulnerability_alerts: 
        :param workflows: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae7544ad6702ec73277e1729d8a5a1e716ff1633f500f3c4388e5033f7adc364)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument administration", value=administration, expected_type=type_hints["administration"])
            check_type(argname="argument checks", value=checks, expected_type=type_hints["checks"])
            check_type(argname="argument codespaces", value=codespaces, expected_type=type_hints["codespaces"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument dependabot_secrets", value=dependabot_secrets, expected_type=type_hints["dependabot_secrets"])
            check_type(argname="argument deployments", value=deployments, expected_type=type_hints["deployments"])
            check_type(argname="argument email_addresses", value=email_addresses, expected_type=type_hints["email_addresses"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
            check_type(argname="argument followers", value=followers, expected_type=type_hints["followers"])
            check_type(argname="argument git_ssh_keys", value=git_ssh_keys, expected_type=type_hints["git_ssh_keys"])
            check_type(argname="argument gpg_keys", value=gpg_keys, expected_type=type_hints["gpg_keys"])
            check_type(argname="argument interaction_limits", value=interaction_limits, expected_type=type_hints["interaction_limits"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument members", value=members, expected_type=type_hints["members"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument organization_administration", value=organization_administration, expected_type=type_hints["organization_administration"])
            check_type(argname="argument organization_announcement_banners", value=organization_announcement_banners, expected_type=type_hints["organization_announcement_banners"])
            check_type(argname="argument organization_copilot_seat_management", value=organization_copilot_seat_management, expected_type=type_hints["organization_copilot_seat_management"])
            check_type(argname="argument organization_custom_org_roles", value=organization_custom_org_roles, expected_type=type_hints["organization_custom_org_roles"])
            check_type(argname="argument organization_custom_properties", value=organization_custom_properties, expected_type=type_hints["organization_custom_properties"])
            check_type(argname="argument organization_custom_roles", value=organization_custom_roles, expected_type=type_hints["organization_custom_roles"])
            check_type(argname="argument organization_events", value=organization_events, expected_type=type_hints["organization_events"])
            check_type(argname="argument organization_hooks", value=organization_hooks, expected_type=type_hints["organization_hooks"])
            check_type(argname="argument organization_packages", value=organization_packages, expected_type=type_hints["organization_packages"])
            check_type(argname="argument organization_personal_access_token_requests", value=organization_personal_access_token_requests, expected_type=type_hints["organization_personal_access_token_requests"])
            check_type(argname="argument organization_personal_access_tokens", value=organization_personal_access_tokens, expected_type=type_hints["organization_personal_access_tokens"])
            check_type(argname="argument organization_plan", value=organization_plan, expected_type=type_hints["organization_plan"])
            check_type(argname="argument organization_projects", value=organization_projects, expected_type=type_hints["organization_projects"])
            check_type(argname="argument organization_secrets", value=organization_secrets, expected_type=type_hints["organization_secrets"])
            check_type(argname="argument organization_self_hosted_runners", value=organization_self_hosted_runners, expected_type=type_hints["organization_self_hosted_runners"])
            check_type(argname="argument organization_user_blocking", value=organization_user_blocking, expected_type=type_hints["organization_user_blocking"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument pages", value=pages, expected_type=type_hints["pages"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument pull_requests", value=pull_requests, expected_type=type_hints["pull_requests"])
            check_type(argname="argument repository_custom_properties", value=repository_custom_properties, expected_type=type_hints["repository_custom_properties"])
            check_type(argname="argument repository_hooks", value=repository_hooks, expected_type=type_hints["repository_hooks"])
            check_type(argname="argument repository_projects", value=repository_projects, expected_type=type_hints["repository_projects"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument secret_scanning_alerts", value=secret_scanning_alerts, expected_type=type_hints["secret_scanning_alerts"])
            check_type(argname="argument security_events", value=security_events, expected_type=type_hints["security_events"])
            check_type(argname="argument single_file", value=single_file, expected_type=type_hints["single_file"])
            check_type(argname="argument starring", value=starring, expected_type=type_hints["starring"])
            check_type(argname="argument statuses", value=statuses, expected_type=type_hints["statuses"])
            check_type(argname="argument team_discussions", value=team_discussions, expected_type=type_hints["team_discussions"])
            check_type(argname="argument vulnerability_alerts", value=vulnerability_alerts, expected_type=type_hints["vulnerability_alerts"])
            check_type(argname="argument workflows", value=workflows, expected_type=type_hints["workflows"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if administration is not None:
            self._values["administration"] = administration
        if checks is not None:
            self._values["checks"] = checks
        if codespaces is not None:
            self._values["codespaces"] = codespaces
        if contents is not None:
            self._values["contents"] = contents
        if dependabot_secrets is not None:
            self._values["dependabot_secrets"] = dependabot_secrets
        if deployments is not None:
            self._values["deployments"] = deployments
        if email_addresses is not None:
            self._values["email_addresses"] = email_addresses
        if environments is not None:
            self._values["environments"] = environments
        if followers is not None:
            self._values["followers"] = followers
        if git_ssh_keys is not None:
            self._values["git_ssh_keys"] = git_ssh_keys
        if gpg_keys is not None:
            self._values["gpg_keys"] = gpg_keys
        if interaction_limits is not None:
            self._values["interaction_limits"] = interaction_limits
        if issues is not None:
            self._values["issues"] = issues
        if members is not None:
            self._values["members"] = members
        if metadata is not None:
            self._values["metadata"] = metadata
        if organization_administration is not None:
            self._values["organization_administration"] = organization_administration
        if organization_announcement_banners is not None:
            self._values["organization_announcement_banners"] = organization_announcement_banners
        if organization_copilot_seat_management is not None:
            self._values["organization_copilot_seat_management"] = organization_copilot_seat_management
        if organization_custom_org_roles is not None:
            self._values["organization_custom_org_roles"] = organization_custom_org_roles
        if organization_custom_properties is not None:
            self._values["organization_custom_properties"] = organization_custom_properties
        if organization_custom_roles is not None:
            self._values["organization_custom_roles"] = organization_custom_roles
        if organization_events is not None:
            self._values["organization_events"] = organization_events
        if organization_hooks is not None:
            self._values["organization_hooks"] = organization_hooks
        if organization_packages is not None:
            self._values["organization_packages"] = organization_packages
        if organization_personal_access_token_requests is not None:
            self._values["organization_personal_access_token_requests"] = organization_personal_access_token_requests
        if organization_personal_access_tokens is not None:
            self._values["organization_personal_access_tokens"] = organization_personal_access_tokens
        if organization_plan is not None:
            self._values["organization_plan"] = organization_plan
        if organization_projects is not None:
            self._values["organization_projects"] = organization_projects
        if organization_secrets is not None:
            self._values["organization_secrets"] = organization_secrets
        if organization_self_hosted_runners is not None:
            self._values["organization_self_hosted_runners"] = organization_self_hosted_runners
        if organization_user_blocking is not None:
            self._values["organization_user_blocking"] = organization_user_blocking
        if packages is not None:
            self._values["packages"] = packages
        if pages is not None:
            self._values["pages"] = pages
        if profile is not None:
            self._values["profile"] = profile
        if pull_requests is not None:
            self._values["pull_requests"] = pull_requests
        if repository_custom_properties is not None:
            self._values["repository_custom_properties"] = repository_custom_properties
        if repository_hooks is not None:
            self._values["repository_hooks"] = repository_hooks
        if repository_projects is not None:
            self._values["repository_projects"] = repository_projects
        if secrets is not None:
            self._values["secrets"] = secrets
        if secret_scanning_alerts is not None:
            self._values["secret_scanning_alerts"] = secret_scanning_alerts
        if security_events is not None:
            self._values["security_events"] = security_events
        if single_file is not None:
            self._values["single_file"] = single_file
        if starring is not None:
            self._values["starring"] = starring
        if statuses is not None:
            self._values["statuses"] = statuses
        if team_discussions is not None:
            self._values["team_discussions"] = team_discussions
        if vulnerability_alerts is not None:
            self._values["vulnerability_alerts"] = vulnerability_alerts
        if workflows is not None:
            self._values["workflows"] = workflows

    @builtins.property
    def actions(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("actions")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def administration(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("administration")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def checks(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("checks")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def codespaces(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("codespaces")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def contents(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("contents")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def dependabot_secrets(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("dependabot_secrets")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def deployments(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("deployments")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def email_addresses(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("email_addresses")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def environments(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("environments")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def followers(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("followers")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def git_ssh_keys(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("git_ssh_keys")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def gpg_keys(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("gpg_keys")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def interaction_limits(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("interaction_limits")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def issues(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("issues")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def members(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("members")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def metadata(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("metadata")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_administration(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_administration")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_announcement_banners(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_announcement_banners")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_copilot_seat_management(
        self,
    ) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_copilot_seat_management")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_custom_org_roles(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_custom_org_roles")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_custom_properties(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_custom_properties")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_custom_roles(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_custom_roles")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_events(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_events")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_hooks(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_hooks")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_packages(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_packages")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_personal_access_token_requests(
        self,
    ) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_personal_access_token_requests")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_personal_access_tokens(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_personal_access_tokens")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_plan(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_plan")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_projects(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_projects")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_secrets(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_secrets")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_self_hosted_runners(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_self_hosted_runners")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def organization_user_blocking(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("organization_user_blocking")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def packages(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("packages")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def pages(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("pages")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def profile(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("profile")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def pull_requests(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("pull_requests")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def repository_custom_properties(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("repository_custom_properties")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def repository_hooks(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("repository_hooks")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def repository_projects(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("repository_projects")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def secrets(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("secrets")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def secret_scanning_alerts(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("secret_scanning_alerts")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def security_events(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("security_events")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def single_file(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("single_file")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def starring(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("starring")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def statuses(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("statuses")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def team_discussions(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("team_discussions")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def vulnerability_alerts(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("vulnerability_alerts")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    @builtins.property
    def workflows(self) -> typing.Optional["PermissionLevel"]:
        result = self._values.get("workflows")
        return typing.cast(typing.Optional["PermissionLevel"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubAppPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@catnekaise/ghrawel.GitHubAppSecretsStorage")
class GitHubAppSecretsStorage(enum.Enum):
    PARAMETER_STORE = "PARAMETER_STORE"
    SECRETS_MANAGER = "SECRETS_MANAGER"


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.GitHubAppsProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_app_id": "defaultAppId",
        "storage": "storage",
        "additional_apps": "additionalApps",
        "prefix": "prefix",
    },
)
class GitHubAppsProps:
    def __init__(
        self,
        *,
        default_app_id: jsii.Number,
        storage: GitHubAppSecretsStorage,
        additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param default_app_id: 
        :param storage: 
        :param additional_apps: 
        :param prefix: Default: /catnekaise/github-apps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2ffb7d2678ffbad6c0c3782621cdf2f494f16350855d8910531dfa9469fd7f)
            check_type(argname="argument default_app_id", value=default_app_id, expected_type=type_hints["default_app_id"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument additional_apps", value=additional_apps, expected_type=type_hints["additional_apps"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_app_id": default_app_id,
            "storage": storage,
        }
        if additional_apps is not None:
            self._values["additional_apps"] = additional_apps
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def default_app_id(self) -> jsii.Number:
        result = self._values.get("default_app_id")
        assert result is not None, "Required property 'default_app_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage(self) -> GitHubAppSecretsStorage:
        result = self._values.get("storage")
        assert result is not None, "Required property 'storage' is missing"
        return typing.cast(GitHubAppSecretsStorage, result)

    @builtins.property
    def additional_apps(self) -> typing.Optional[typing.List[GitHubApp]]:
        result = self._values.get("additional_apps")
        return typing.cast(typing.Optional[typing.List[GitHubApp]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''
        :default: /catnekaise/github-apps
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubAppsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@catnekaise/ghrawel.IGitHubApps")
class IGitHubApps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="secretsPrefix")
    def secrets_prefix(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="secretsStorage")
    def secrets_storage(self) -> GitHubAppSecretsStorage:
        ...

    @jsii.member(jsii_name="getAppIdForAppName")
    def get_app_id_for_app_name(
        self,
        name: typing.Optional[builtins.str] = None,
    ) -> jsii.Number:
        '''
        :param name: -
        '''
        ...

    @jsii.member(jsii_name="grantAccess")
    def grant_access(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''
        :param principal: -
        '''
        ...


class _IGitHubAppsProxy:
    __jsii_type__: typing.ClassVar[str] = "@catnekaise/ghrawel.IGitHubApps"

    @builtins.property
    @jsii.member(jsii_name="secretsPrefix")
    def secrets_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsPrefix"))

    @builtins.property
    @jsii.member(jsii_name="secretsStorage")
    def secrets_storage(self) -> GitHubAppSecretsStorage:
        return typing.cast(GitHubAppSecretsStorage, jsii.get(self, "secretsStorage"))

    @jsii.member(jsii_name="getAppIdForAppName")
    def get_app_id_for_app_name(
        self,
        name: typing.Optional[builtins.str] = None,
    ) -> jsii.Number:
        '''
        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93065fc1a73507023cd84becd96fbd7613ba014c83d24cb0aa1871140ddff6c0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getAppIdForAppName", [name]))

    @jsii.member(jsii_name="grantAccess")
    def grant_access(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''
        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6317f8b4c7d726827a7160e640d328ed0cb6540889f2786903f016ea5cac8506)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant], jsii.invoke(self, "grantAccess", [principal]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGitHubApps).__jsii_proxy_class__ = lambda : _IGitHubAppsProxy


@jsii.interface(jsii_type="@catnekaise/ghrawel.ITokenProvider")
class ITokenProvider(typing_extensions.Protocol):
    @jsii.member(jsii_name="grantExecute")
    def grant_execute(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        owner: typing.Optional[builtins.str] = None,
        *repo: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Use this to grant access to the token provider.

        :param role: -
        :param owner: -
        :param repo: -
        '''
        ...

    @jsii.member(jsii_name="grantExecuteGitHubActionsAbac")
    def grant_execute_git_hub_actions_abac(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        path_strategy: typing.Optional["TokenProviderPathStrategy"] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''use this to grant access to the token provider when the role is assumed via Cognito Identity.

        :param role: -
        :param claims_context: 
        :param path_strategy: 
        '''
        ...


class _ITokenProviderProxy:
    __jsii_type__: typing.ClassVar[str] = "@catnekaise/ghrawel.ITokenProvider"

    @jsii.member(jsii_name="grantExecute")
    def grant_execute(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        owner: typing.Optional[builtins.str] = None,
        *repo: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Use this to grant access to the token provider.

        :param role: -
        :param owner: -
        :param repo: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff92f177cf21f77bb26e71233de3d0b41b212c731621b5bfc1c71796faa2458)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repo", value=repo, expected_type=typing.Tuple[type_hints["repo"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantExecute", [role, owner, *repo]))

    @jsii.member(jsii_name="grantExecuteGitHubActionsAbac")
    def grant_execute_git_hub_actions_abac(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        path_strategy: typing.Optional["TokenProviderPathStrategy"] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''use this to grant access to the token provider when the role is assumed via Cognito Identity.

        :param role: -
        :param claims_context: 
        :param path_strategy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__107060e3b9ef192c6f3645dcf54ce3c7fda51f51e74c2c0534c6a6d60216d1a7)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        settings = TokenProviderActionsIdentitySettings(
            claims_context=claims_context, path_strategy=path_strategy
        )

        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantExecuteGitHubActionsAbac", [role, settings]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITokenProvider).__jsii_proxy_class__ = lambda : _ITokenProviderProxy


@jsii.interface(jsii_type="@catnekaise/ghrawel.ITokenProviderApi")
class ITokenProviderApi(typing_extensions.Protocol):
    @jsii.member(jsii_name="newTokenProvider")
    def new_token_provider(
        self,
        name: builtins.str,
        *,
        permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
        app: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional["TokenProviderEndpoint"] = None,
        target_rule: typing.Optional["TokenProviderTargetRule"] = None,
    ) -> ITokenProvider:
        '''
        :param name: -
        :param permissions: Permissions.
        :param app: Default: default
        :param endpoint: Default: DEFAULT
        :param target_rule: Default: AT_LEAST_ONE
        '''
        ...


class _ITokenProviderApiProxy:
    __jsii_type__: typing.ClassVar[str] = "@catnekaise/ghrawel.ITokenProviderApi"

    @jsii.member(jsii_name="newTokenProvider")
    def new_token_provider(
        self,
        name: builtins.str,
        *,
        permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
        app: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional["TokenProviderEndpoint"] = None,
        target_rule: typing.Optional["TokenProviderTargetRule"] = None,
    ) -> ITokenProvider:
        '''
        :param name: -
        :param permissions: Permissions.
        :param app: Default: default
        :param endpoint: Default: DEFAULT
        :param target_rule: Default: AT_LEAST_ONE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6efd91b3b22e294cb3ea209964f69f2c75291cd5076dab68165dc014f4445cba)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        configuration = NewTokenProviderConfiguration(
            permissions=permissions,
            app=app,
            endpoint=endpoint,
            target_rule=target_rule,
        )

        return typing.cast(ITokenProvider, jsii.invoke(self, "newTokenProvider", [name, configuration]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITokenProviderApi).__jsii_proxy_class__ = lambda : _ITokenProviderApiProxy


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.ManagedGitHubAppsProps",
    jsii_struct_bases=[GitHubAppsProps],
    name_mapping={
        "default_app_id": "defaultAppId",
        "storage": "storage",
        "additional_apps": "additionalApps",
        "prefix": "prefix",
        "kms_key": "kmsKey",
        "removal_policy": "removalPolicy",
    },
)
class ManagedGitHubAppsProps(GitHubAppsProps):
    def __init__(
        self,
        *,
        default_app_id: jsii.Number,
        storage: GitHubAppSecretsStorage,
        additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
        prefix: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param default_app_id: 
        :param storage: 
        :param additional_apps: 
        :param prefix: Default: /catnekaise/github-apps
        :param kms_key: Default: AWS_MANAGED
        :param removal_policy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bebb70c3fdb800811e05fdca4f145b17995d6b66268ee8c12556b14ce8176de4)
            check_type(argname="argument default_app_id", value=default_app_id, expected_type=type_hints["default_app_id"])
            check_type(argname="argument storage", value=storage, expected_type=type_hints["storage"])
            check_type(argname="argument additional_apps", value=additional_apps, expected_type=type_hints["additional_apps"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_app_id": default_app_id,
            "storage": storage,
        }
        if additional_apps is not None:
            self._values["additional_apps"] = additional_apps
        if prefix is not None:
            self._values["prefix"] = prefix
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def default_app_id(self) -> jsii.Number:
        result = self._values.get("default_app_id")
        assert result is not None, "Required property 'default_app_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def storage(self) -> GitHubAppSecretsStorage:
        result = self._values.get("storage")
        assert result is not None, "Required property 'storage' is missing"
        return typing.cast(GitHubAppSecretsStorage, result)

    @builtins.property
    def additional_apps(self) -> typing.Optional[typing.List[GitHubApp]]:
        result = self._values.get("additional_apps")
        return typing.cast(typing.Optional[typing.List[GitHubApp]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''
        :default: /catnekaise/github-apps
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''
        :default: AWS_MANAGED
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedGitHubAppsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.NewTokenProviderConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "permissions": "permissions",
        "app": "app",
        "endpoint": "endpoint",
        "target_rule": "targetRule",
    },
)
class NewTokenProviderConfiguration:
    def __init__(
        self,
        *,
        permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
        app: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional["TokenProviderEndpoint"] = None,
        target_rule: typing.Optional["TokenProviderTargetRule"] = None,
    ) -> None:
        '''
        :param permissions: Permissions.
        :param app: Default: default
        :param endpoint: Default: DEFAULT
        :param target_rule: Default: AT_LEAST_ONE
        '''
        if isinstance(permissions, dict):
            permissions = GitHubAppPermissions(**permissions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222a766e2b57364cf9f0ce77e00ad40e2f806fcf6ac3f1a758987802a2251ba4)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument target_rule", value=target_rule, expected_type=type_hints["target_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "permissions": permissions,
        }
        if app is not None:
            self._values["app"] = app
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if target_rule is not None:
            self._values["target_rule"] = target_rule

    @builtins.property
    def permissions(self) -> GitHubAppPermissions:
        '''Permissions.'''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast(GitHubAppPermissions, result)

    @builtins.property
    def app(self) -> typing.Optional[builtins.str]:
        '''
        :default: default
        '''
        result = self._values.get("app")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional["TokenProviderEndpoint"]:
        '''
        :default: DEFAULT
        '''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional["TokenProviderEndpoint"], result)

    @builtins.property
    def target_rule(self) -> typing.Optional["TokenProviderTargetRule"]:
        '''
        :default: AT_LEAST_ONE
        '''
        result = self._values.get("target_rule")
        return typing.cast(typing.Optional["TokenProviderTargetRule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NewTokenProviderConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@catnekaise/ghrawel.PermissionLevel")
class PermissionLevel(enum.Enum):
    READ = "READ"
    WRITE = "WRITE"
    ADMIN = "ADMIN"


@jsii.enum(jsii_type="@catnekaise/ghrawel.RepositorySelectionMode")
class RepositorySelectionMode(enum.Enum):
    AT_LEAST_ONE = "AT_LEAST_ONE"
    '''Allows targeting of any individual or multiple repos, but NOT the organization.'''
    ALLOW_OWNER = "ALLOW_OWNER"
    '''Allows targeting of any individual or multiple repos and the organization/user.'''


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.TargetRuleSettings",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class TargetRuleSettings:
    def __init__(self, *, mode: RepositorySelectionMode) -> None:
        '''
        :param mode: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b704a2551113104895eeb05c4cdbd2cf7bc1695f4ed86ec2429e0eea9c42b1e7)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }

    @builtins.property
    def mode(self) -> RepositorySelectionMode:
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(RepositorySelectionMode, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetRuleSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITokenProvider)
class TokenProvider(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/ghrawel.TokenProvider",
):
    '''This construct may receive some changes before constructor is made public.

    Until then use static create method.
    '''

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api: _aws_cdk_aws_apigateway_ceddda9d.IRestApi,
        app: builtins.str,
        app_id: jsii.Number,
        configurator: "TokenProviderConfigurator",
        endpoint: "TokenProviderEndpoint",
        lambda_: _aws_cdk_aws_lambda_ceddda9d.Function,
        method_options: typing.Union["TokenProviderMethodOptions", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
        target_rule: "TokenProviderTargetRule",
    ) -> "TokenProvider":
        '''
        :param scope: -
        :param id: -
        :param api: 
        :param app: 
        :param app_id: 
        :param configurator: 
        :param endpoint: 
        :param lambda_: 
        :param method_options: 
        :param name: 
        :param permissions: 
        :param target_rule: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47da14983d315f770cb9b49258cbc42dedecdde7f9cfcaa1128629120b5c67ca)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        settings = TokenProviderSettings(
            api=api,
            app=app,
            app_id=app_id,
            configurator=configurator,
            endpoint=endpoint,
            lambda_=lambda_,
            method_options=method_options,
            name=name,
            permissions=permissions,
            target_rule=target_rule,
        )

        return typing.cast("TokenProvider", jsii.sinvoke(cls, "create", [scope, id, settings]))

    @jsii.member(jsii_name="grantExecute")
    def grant_execute(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        owner: typing.Optional[builtins.str] = None,
        *repo: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Use this to grant access to the token provider.

        :param role: -
        :param owner: -
        :param repo: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b4f69eb50f8ef45c03e843ee6071a4517fd7ac801d14b710c8e21f196082f3)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repo", value=repo, expected_type=typing.Tuple[type_hints["repo"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantExecute", [role, owner, *repo]))

    @jsii.member(jsii_name="grantExecuteGitHubActionsAbac")
    def grant_execute_git_hub_actions_abac(
        self,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        path_strategy: typing.Optional["TokenProviderPathStrategy"] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''use this to grant access to the token provider when the role is assumed via Cognito Identity.

        :param role: -
        :param claims_context: 
        :param path_strategy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462c5ac83e1dd36c07945f3eb3c8edae77bd1e2f6bbc72e59e89bc02e4211dc0)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        settings = TokenProviderActionsIdentitySettings(
            claims_context=claims_context, path_strategy=path_strategy
        )

        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantExecuteGitHubActionsAbac", [role, settings]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''
        :param metric_name: -
        :param stage: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cb028368768599a36c4cd7674f28aa6e8617839b5ea5a560c6b518e24c9435d)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, stage, props]))

    @jsii.member(jsii_name="metricCacheHitCount")
    def metric_cache_hit_count(
        self,
        stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''
        :param stage: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee92cd394d7c5e60a3a6d6d6085b2bd220443dce44821cdf0297e344332eea82)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricCacheHitCount", [stage, props]))

    @jsii.member(jsii_name="metricCacheMissCount")
    def metric_cache_miss_count(
        self,
        stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''
        :param stage: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37867ee6c92c75b5e203b36fa548e1595763285e5079c5e17f06eaa136a5d85)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricCacheMissCount", [stage, props]))

    @jsii.member(jsii_name="metricClientError")
    def metric_client_error(
        self,
        stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''
        :param stage: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b71ddd65c8933685e07c859f54c170824a3be4f14fc757206727f3d88374c3)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricClientError", [stage, props]))

    @jsii.member(jsii_name="metricCount")
    def metric_count(
        self,
        stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''
        :param stage: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5050afe9ba4d1e3083eb566d8a24e8bb4f5c7e7bf49d73d8fab3f06e685cd89)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricCount", [stage, props]))

    @jsii.member(jsii_name="metricServerError")
    def metric_server_error(
        self,
        stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''
        :param stage: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b316e21cc306460bf236437740b400c22ee427198e6233e14064cfa18fbbdfe4)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricServerError", [stage, props]))

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def http_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpMethod"))

    @builtins.property
    @jsii.member(jsii_name="methodArn")
    def method_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "methodArn"))

    @builtins.property
    @jsii.member(jsii_name="methodId")
    def method_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "methodId"))


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.TokenProviderActionsIdentitySettings",
    jsii_struct_bases=[],
    name_mapping={"claims_context": "claimsContext", "path_strategy": "pathStrategy"},
)
class TokenProviderActionsIdentitySettings:
    def __init__(
        self,
        *,
        claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
        path_strategy: typing.Optional["TokenProviderPathStrategy"] = None,
    ) -> None:
        '''
        :param claims_context: 
        :param path_strategy: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7548c7b1a9a3bc552cfeb35d3873c2c9c68dc2707998a33a2f1e762c78260484)
            check_type(argname="argument claims_context", value=claims_context, expected_type=type_hints["claims_context"])
            check_type(argname="argument path_strategy", value=path_strategy, expected_type=type_hints["path_strategy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "claims_context": claims_context,
        }
        if path_strategy is not None:
            self._values["path_strategy"] = path_strategy

    @builtins.property
    def claims_context(self) -> _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext:
        result = self._values.get("claims_context")
        assert result is not None, "Required property 'claims_context' is missing"
        return typing.cast(_catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext, result)

    @builtins.property
    def path_strategy(self) -> typing.Optional["TokenProviderPathStrategy"]:
        result = self._values.get("path_strategy")
        return typing.cast(typing.Optional["TokenProviderPathStrategy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TokenProviderActionsIdentitySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITokenProviderApi)
class TokenProviderApi(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/ghrawel.TokenProviderApi",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        apps: IGitHubApps,
        api: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.RestApi] = None,
        lambda_: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param apps: GitHub Apps configuration.
        :param api: Use this to provide the API Gateway RestApi configured to your requirements.
        :param lambda_: Use this to provide the Lambda Function configured to your requirements.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__447181897fd65ed027681dd6ae55f3617b7987814a20d194d8f72359dddd2e1a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TokenProviderApiProps(apps=apps, api=api, lambda_=lambda_)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="newTokenProvider")
    def new_token_provider(
        self,
        name: builtins.str,
        *,
        permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
        app: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional["TokenProviderEndpoint"] = None,
        target_rule: typing.Optional["TokenProviderTargetRule"] = None,
    ) -> ITokenProvider:
        '''
        :param name: -
        :param permissions: Permissions.
        :param app: Default: default
        :param endpoint: Default: DEFAULT
        :param target_rule: Default: AT_LEAST_ONE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c8c4edca56b96907bb6a3d0352cf11ed13cc9261a825014e2d722ce7a80793)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        configuration = NewTokenProviderConfiguration(
            permissions=permissions,
            app=app,
            endpoint=endpoint,
            target_rule=target_rule,
        )

        return typing.cast(ITokenProvider, jsii.invoke(self, "newTokenProvider", [name, configuration]))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "lambdaFunction"))

    @builtins.property
    @jsii.member(jsii_name="restApi")
    def rest_api(self) -> _aws_cdk_aws_apigateway_ceddda9d.RestApi:
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.RestApi, jsii.get(self, "restApi"))


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.TokenProviderApiProps",
    jsii_struct_bases=[],
    name_mapping={"apps": "apps", "api": "api", "lambda_": "lambda"},
)
class TokenProviderApiProps:
    def __init__(
        self,
        *,
        apps: IGitHubApps,
        api: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.RestApi] = None,
        lambda_: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
    ) -> None:
        '''
        :param apps: GitHub Apps configuration.
        :param api: Use this to provide the API Gateway RestApi configured to your requirements.
        :param lambda_: Use this to provide the Lambda Function configured to your requirements.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5c0ccca61c2f54b020376534f7552111a23464932c1bedd4424de39f457b4b3)
            check_type(argname="argument apps", value=apps, expected_type=type_hints["apps"])
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "apps": apps,
        }
        if api is not None:
            self._values["api"] = api
        if lambda_ is not None:
            self._values["lambda_"] = lambda_

    @builtins.property
    def apps(self) -> IGitHubApps:
        '''GitHub Apps configuration.'''
        result = self._values.get("apps")
        assert result is not None, "Required property 'apps' is missing"
        return typing.cast(IGitHubApps, result)

    @builtins.property
    def api(self) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.RestApi]:
        '''Use this to provide the API Gateway RestApi configured to your requirements.'''
        result = self._values.get("api")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.RestApi], result)

    @builtins.property
    def lambda_(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function]:
        '''Use this to provide the Lambda Function configured to your requirements.'''
        result = self._values.get("lambda_")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TokenProviderApiProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TokenProviderConfigurator(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/ghrawel.TokenProviderConfigurator",
):
    '''This class may see some breaking changes but the intent is to stabilize, be made abstract and available as input on ``TokenProviderConfiguration``.'''

    @jsii.member(jsii_name="create")
    @builtins.classmethod
    def create(cls) -> "TokenProviderConfigurator":
        return typing.cast("TokenProviderConfigurator", jsii.sinvoke(cls, "create", []))

    @jsii.member(jsii_name="createApiResource")
    def create_api_resource(
        self,
        api: _aws_cdk_aws_apigateway_ceddda9d.IRestApi,
        name: builtins.str,
        endpoint: "TokenProviderEndpoint",
    ) -> _aws_cdk_aws_apigateway_ceddda9d.Resource:
        '''
        :param api: -
        :param name: -
        :param endpoint: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbd4856310dc9f8ff7221de72e178cde01b590eadf25d1132cde57b50f9d52c)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.Resource, jsii.invoke(self, "createApiResource", [api, name, endpoint]))

    @jsii.member(jsii_name="createIntegrationOptions")
    def create_integration_options(
        self,
        *,
        app_id: jsii.Number,
        app_name: builtins.str,
        endpoint: "TokenProviderEndpoint",
        name: builtins.str,
        permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
        target_rule: typing.Union[TargetRuleSettings, typing.Dict[builtins.str, typing.Any]],
    ) -> _aws_cdk_aws_apigateway_ceddda9d.LambdaIntegrationOptions:
        '''
        :param app_id: 
        :param app_name: 
        :param endpoint: 
        :param name: 
        :param permissions: 
        :param target_rule: 
        '''
        settings = TokenProviderConfiguratorIntegrationOptionsContext(
            app_id=app_id,
            app_name=app_name,
            endpoint=endpoint,
            name=name,
            permissions=permissions,
            target_rule=target_rule,
        )

        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.LambdaIntegrationOptions, jsii.invoke(self, "createIntegrationOptions", [settings]))

    @jsii.member(jsii_name="createMethodOptions")
    def create_method_options(
        self,
        *,
        endpoint_type: "TokenProviderEndpointType",
        error_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
        operation_name: builtins.str,
        repository_selection_mode: RepositorySelectionMode,
        token_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
        request_validator: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRequestValidator] = None,
    ) -> _aws_cdk_aws_apigateway_ceddda9d.MethodOptions:
        '''
        :param endpoint_type: 
        :param error_response_model: 
        :param operation_name: 
        :param repository_selection_mode: 
        :param token_response_model: 
        :param request_validator: 
        '''
        input = TokenProviderConfiguratorMethodOptionsContext(
            endpoint_type=endpoint_type,
            error_response_model=error_response_model,
            operation_name=operation_name,
            repository_selection_mode=repository_selection_mode,
            token_response_model=token_response_model,
            request_validator=request_validator,
        )

        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, jsii.invoke(self, "createMethodOptions", [input]))

    @builtins.property
    @jsii.member(jsii_name="integrationResponses")
    def integration_responses(
        self,
    ) -> typing.List[_aws_cdk_aws_apigateway_ceddda9d.IntegrationResponse]:
        return typing.cast(typing.List[_aws_cdk_aws_apigateway_ceddda9d.IntegrationResponse], jsii.get(self, "integrationResponses"))


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.TokenProviderConfiguratorIntegrationOptionsContext",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "app_name": "appName",
        "endpoint": "endpoint",
        "name": "name",
        "permissions": "permissions",
        "target_rule": "targetRule",
    },
)
class TokenProviderConfiguratorIntegrationOptionsContext:
    def __init__(
        self,
        *,
        app_id: jsii.Number,
        app_name: builtins.str,
        endpoint: "TokenProviderEndpoint",
        name: builtins.str,
        permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
        target_rule: typing.Union[TargetRuleSettings, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param app_id: 
        :param app_name: 
        :param endpoint: 
        :param name: 
        :param permissions: 
        :param target_rule: 
        '''
        if isinstance(permissions, dict):
            permissions = GitHubAppPermissions(**permissions)
        if isinstance(target_rule, dict):
            target_rule = TargetRuleSettings(**target_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8c55c93ce5b6beab389dc743e3ea3bd35cb5b9ed46cdaa6c5aca4fa01f678d5)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument app_name", value=app_name, expected_type=type_hints["app_name"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument target_rule", value=target_rule, expected_type=type_hints["target_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
            "app_name": app_name,
            "endpoint": endpoint,
            "name": name,
            "permissions": permissions,
            "target_rule": target_rule,
        }

    @builtins.property
    def app_id(self) -> jsii.Number:
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def app_name(self) -> builtins.str:
        result = self._values.get("app_name")
        assert result is not None, "Required property 'app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def endpoint(self) -> "TokenProviderEndpoint":
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast("TokenProviderEndpoint", result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permissions(self) -> GitHubAppPermissions:
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast(GitHubAppPermissions, result)

    @builtins.property
    def target_rule(self) -> TargetRuleSettings:
        result = self._values.get("target_rule")
        assert result is not None, "Required property 'target_rule' is missing"
        return typing.cast(TargetRuleSettings, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TokenProviderConfiguratorIntegrationOptionsContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.TokenProviderConfiguratorMethodOptionsContext",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_type": "endpointType",
        "error_response_model": "errorResponseModel",
        "operation_name": "operationName",
        "repository_selection_mode": "repositorySelectionMode",
        "token_response_model": "tokenResponseModel",
        "request_validator": "requestValidator",
    },
)
class TokenProviderConfiguratorMethodOptionsContext:
    def __init__(
        self,
        *,
        endpoint_type: "TokenProviderEndpointType",
        error_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
        operation_name: builtins.str,
        repository_selection_mode: RepositorySelectionMode,
        token_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
        request_validator: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRequestValidator] = None,
    ) -> None:
        '''
        :param endpoint_type: 
        :param error_response_model: 
        :param operation_name: 
        :param repository_selection_mode: 
        :param token_response_model: 
        :param request_validator: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cab4e27fc7db0d13d7cd3871bbe773dd647644e979f731a2be04f5772269d5f)
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument error_response_model", value=error_response_model, expected_type=type_hints["error_response_model"])
            check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
            check_type(argname="argument repository_selection_mode", value=repository_selection_mode, expected_type=type_hints["repository_selection_mode"])
            check_type(argname="argument token_response_model", value=token_response_model, expected_type=type_hints["token_response_model"])
            check_type(argname="argument request_validator", value=request_validator, expected_type=type_hints["request_validator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_type": endpoint_type,
            "error_response_model": error_response_model,
            "operation_name": operation_name,
            "repository_selection_mode": repository_selection_mode,
            "token_response_model": token_response_model,
        }
        if request_validator is not None:
            self._values["request_validator"] = request_validator

    @builtins.property
    def endpoint_type(self) -> "TokenProviderEndpointType":
        result = self._values.get("endpoint_type")
        assert result is not None, "Required property 'endpoint_type' is missing"
        return typing.cast("TokenProviderEndpointType", result)

    @builtins.property
    def error_response_model(self) -> _aws_cdk_aws_apigateway_ceddda9d.Model:
        result = self._values.get("error_response_model")
        assert result is not None, "Required property 'error_response_model' is missing"
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.Model, result)

    @builtins.property
    def operation_name(self) -> builtins.str:
        result = self._values.get("operation_name")
        assert result is not None, "Required property 'operation_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_selection_mode(self) -> RepositorySelectionMode:
        result = self._values.get("repository_selection_mode")
        assert result is not None, "Required property 'repository_selection_mode' is missing"
        return typing.cast(RepositorySelectionMode, result)

    @builtins.property
    def token_response_model(self) -> _aws_cdk_aws_apigateway_ceddda9d.Model:
        result = self._values.get("token_response_model")
        assert result is not None, "Required property 'token_response_model' is missing"
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.Model, result)

    @builtins.property
    def request_validator(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRequestValidator]:
        result = self._values.get("request_validator")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRequestValidator], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TokenProviderConfiguratorMethodOptionsContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TokenProviderEndpoint(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/ghrawel.TokenProviderEndpoint",
):
    @jsii.member(jsii_name="useDefault")
    @builtins.classmethod
    def use_default(cls) -> "TokenProviderEndpoint":
        '''Use this to configure a token provider at ``/x/<provider-name>/{owner}/{repo}``.'''
        return typing.cast("TokenProviderEndpoint", jsii.sinvoke(cls, "useDefault", []))

    @jsii.member(jsii_name="useOwner")
    @builtins.classmethod
    def use_owner(
        cls,
        owner: typing.Optional[builtins.str] = None,
    ) -> "TokenProviderEndpoint":
        '''Use this to configure a token provider at ``/x/<provider-name>/{owner}`` or ``/x/<provider-name>/<owner>``.

        :param owner: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dfff464a70314acdf214d8d395eea7820fb7c46866eddb34aadcb58b8114abd)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
        return typing.cast("TokenProviderEndpoint", jsii.sinvoke(cls, "useOwner", [owner]))

    @builtins.property
    @jsii.member(jsii_name="isOwnerEndpoint")
    def is_owner_endpoint(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "isOwnerEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "TokenProviderEndpointType":
        return typing.cast("TokenProviderEndpointType", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repo"))


@jsii.enum(jsii_type="@catnekaise/ghrawel.TokenProviderEndpointType")
class TokenProviderEndpointType(enum.Enum):
    DEFAULT = "DEFAULT"
    DYNAMIC_OWNER = "DYNAMIC_OWNER"
    STATIC_OWNER = "STATIC_OWNER"


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.TokenProviderMethodOptions",
    jsii_struct_bases=[],
    name_mapping={
        "endpoint_type": "endpointType",
        "error_response_model": "errorResponseModel",
        "operation_name": "operationName",
        "request_validator": "requestValidator",
        "token_response_model": "tokenResponseModel",
    },
)
class TokenProviderMethodOptions:
    def __init__(
        self,
        *,
        endpoint_type: TokenProviderEndpointType,
        error_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
        operation_name: builtins.str,
        request_validator: _aws_cdk_aws_apigateway_ceddda9d.RequestValidator,
        token_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
    ) -> None:
        '''
        :param endpoint_type: 
        :param error_response_model: 
        :param operation_name: 
        :param request_validator: 
        :param token_response_model: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7289d88a63a29e2063dcc14e5944e9bd86ab9d8092085773bc0a4dff54a40c)
            check_type(argname="argument endpoint_type", value=endpoint_type, expected_type=type_hints["endpoint_type"])
            check_type(argname="argument error_response_model", value=error_response_model, expected_type=type_hints["error_response_model"])
            check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
            check_type(argname="argument request_validator", value=request_validator, expected_type=type_hints["request_validator"])
            check_type(argname="argument token_response_model", value=token_response_model, expected_type=type_hints["token_response_model"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_type": endpoint_type,
            "error_response_model": error_response_model,
            "operation_name": operation_name,
            "request_validator": request_validator,
            "token_response_model": token_response_model,
        }

    @builtins.property
    def endpoint_type(self) -> TokenProviderEndpointType:
        result = self._values.get("endpoint_type")
        assert result is not None, "Required property 'endpoint_type' is missing"
        return typing.cast(TokenProviderEndpointType, result)

    @builtins.property
    def error_response_model(self) -> _aws_cdk_aws_apigateway_ceddda9d.Model:
        result = self._values.get("error_response_model")
        assert result is not None, "Required property 'error_response_model' is missing"
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.Model, result)

    @builtins.property
    def operation_name(self) -> builtins.str:
        result = self._values.get("operation_name")
        assert result is not None, "Required property 'operation_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def request_validator(self) -> _aws_cdk_aws_apigateway_ceddda9d.RequestValidator:
        result = self._values.get("request_validator")
        assert result is not None, "Required property 'request_validator' is missing"
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.RequestValidator, result)

    @builtins.property
    def token_response_model(self) -> _aws_cdk_aws_apigateway_ceddda9d.Model:
        result = self._values.get("token_response_model")
        assert result is not None, "Required property 'token_response_model' is missing"
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.Model, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TokenProviderMethodOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@catnekaise/ghrawel.TokenProviderPathPolicyVariable")
class TokenProviderPathPolicyVariable(enum.Enum):
    REPOSITORY = "REPOSITORY"
    REPOSITORY_OWNER = "REPOSITORY_OWNER"


class TokenProviderPathStrategy(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/ghrawel.TokenProviderPathStrategy",
):
    @jsii.member(jsii_name="anyRepository")
    @builtins.classmethod
    def any_repository(cls) -> "TokenProviderPathStrategy":
        '''Grants permission to ``/x/<provider-name>/*``.'''
        return typing.cast("TokenProviderPathStrategy", jsii.sinvoke(cls, "anyRepository", []))

    @jsii.member(jsii_name="policyVarRepository")
    @builtins.classmethod
    def policy_var_repository(cls) -> "TokenProviderPathStrategy":
        '''Grants permission to ``/x/<provider-name>/${aws:PrincipalTag/repository}``.'''
        return typing.cast("TokenProviderPathStrategy", jsii.sinvoke(cls, "policyVarRepository", []))

    @jsii.member(jsii_name="policyVarRepositoryOwner")
    @builtins.classmethod
    def policy_var_repository_owner(
        cls,
        *repositories: builtins.str,
    ) -> "TokenProviderPathStrategy":
        '''Grants permission to ``/x/<provider-name>/${aws:PrincipalTag/repository_owner}`` or ``/x/<provider-name>/${aws:PrincipalTag/repository_owner}/<repo>``.

        :param repositories: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__711170ee6ec315efc6274e3c4bf4a19333e645345a5d63663a8ad84a5d1446a6)
            check_type(argname="argument repositories", value=repositories, expected_type=typing.Tuple[type_hints["repositories"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("TokenProviderPathStrategy", jsii.sinvoke(cls, "policyVarRepositoryOwner", [*repositories]))

    @jsii.member(jsii_name="selectOwner")
    @builtins.classmethod
    def select_owner(cls, owner: builtins.str) -> "TokenProviderPathStrategy":
        '''Grants permission to ``/x/<provider-name>/<owner>``.

        :param owner: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__751d68b1211241b423a94adb8c95ce481e7ae72795c4f23fed73d9fba682c189)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
        return typing.cast("TokenProviderPathStrategy", jsii.sinvoke(cls, "selectOwner", [owner]))

    @jsii.member(jsii_name="selectRepositories")
    @builtins.classmethod
    def select_repositories(
        cls,
        owner: builtins.str,
        *repositories: builtins.str,
    ) -> "TokenProviderPathStrategy":
        '''Grants permission for each specified repo ``/x/<provider-name>/<owner>/<repo>``.

        :param owner: -
        :param repositories: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9454746a1597183761c9d3392e3e5072e5d4272f4009d1db2c34272f5808e3)
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repositories", value=repositories, expected_type=typing.Tuple[type_hints["repositories"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("TokenProviderPathStrategy", jsii.sinvoke(cls, "selectRepositories", [owner, *repositories]))

    @builtins.property
    @jsii.member(jsii_name="pathTargetsRepositories")
    def path_targets_repositories(self) -> builtins.bool:
        return typing.cast(builtins.bool, jsii.get(self, "pathTargetsRepositories"))

    @builtins.property
    @jsii.member(jsii_name="repositories")
    def repositories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "repositories"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "TokenProviderPathStrategyType":
        return typing.cast("TokenProviderPathStrategyType", jsii.get(self, "type"))

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "owner"))

    @builtins.property
    @jsii.member(jsii_name="policyVar")
    def policy_var(self) -> typing.Optional[TokenProviderPathPolicyVariable]:
        return typing.cast(typing.Optional[TokenProviderPathPolicyVariable], jsii.get(self, "policyVar"))


@jsii.enum(jsii_type="@catnekaise/ghrawel.TokenProviderPathStrategyType")
class TokenProviderPathStrategyType(enum.Enum):
    POLICY_VAR = "POLICY_VAR"
    ANY_REPOSITORY = "ANY_REPOSITORY"
    OWNER = "OWNER"
    REPOSITORIES = "REPOSITORIES"


@jsii.data_type(
    jsii_type="@catnekaise/ghrawel.TokenProviderSettings",
    jsii_struct_bases=[],
    name_mapping={
        "api": "api",
        "app": "app",
        "app_id": "appId",
        "configurator": "configurator",
        "endpoint": "endpoint",
        "lambda_": "lambda",
        "method_options": "methodOptions",
        "name": "name",
        "permissions": "permissions",
        "target_rule": "targetRule",
    },
)
class TokenProviderSettings:
    def __init__(
        self,
        *,
        api: _aws_cdk_aws_apigateway_ceddda9d.IRestApi,
        app: builtins.str,
        app_id: jsii.Number,
        configurator: TokenProviderConfigurator,
        endpoint: TokenProviderEndpoint,
        lambda_: _aws_cdk_aws_lambda_ceddda9d.Function,
        method_options: typing.Union[TokenProviderMethodOptions, typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
        target_rule: "TokenProviderTargetRule",
    ) -> None:
        '''
        :param api: 
        :param app: 
        :param app_id: 
        :param configurator: 
        :param endpoint: 
        :param lambda_: 
        :param method_options: 
        :param name: 
        :param permissions: 
        :param target_rule: 
        '''
        if isinstance(method_options, dict):
            method_options = TokenProviderMethodOptions(**method_options)
        if isinstance(permissions, dict):
            permissions = GitHubAppPermissions(**permissions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df343b45d0e38600b0deb1a3f53edaf9ed4bb9de01ef8e0bb0706ce7a71c9424)
            check_type(argname="argument api", value=api, expected_type=type_hints["api"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument configurator", value=configurator, expected_type=type_hints["configurator"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument lambda_", value=lambda_, expected_type=type_hints["lambda_"])
            check_type(argname="argument method_options", value=method_options, expected_type=type_hints["method_options"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument target_rule", value=target_rule, expected_type=type_hints["target_rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api": api,
            "app": app,
            "app_id": app_id,
            "configurator": configurator,
            "endpoint": endpoint,
            "lambda_": lambda_,
            "method_options": method_options,
            "name": name,
            "permissions": permissions,
            "target_rule": target_rule,
        }

    @builtins.property
    def api(self) -> _aws_cdk_aws_apigateway_ceddda9d.IRestApi:
        result = self._values.get("api")
        assert result is not None, "Required property 'api' is missing"
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.IRestApi, result)

    @builtins.property
    def app(self) -> builtins.str:
        result = self._values.get("app")
        assert result is not None, "Required property 'app' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_id(self) -> jsii.Number:
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def configurator(self) -> TokenProviderConfigurator:
        result = self._values.get("configurator")
        assert result is not None, "Required property 'configurator' is missing"
        return typing.cast(TokenProviderConfigurator, result)

    @builtins.property
    def endpoint(self) -> TokenProviderEndpoint:
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(TokenProviderEndpoint, result)

    @builtins.property
    def lambda_(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        result = self._values.get("lambda_")
        assert result is not None, "Required property 'lambda_' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, result)

    @builtins.property
    def method_options(self) -> TokenProviderMethodOptions:
        result = self._values.get("method_options")
        assert result is not None, "Required property 'method_options' is missing"
        return typing.cast(TokenProviderMethodOptions, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def permissions(self) -> GitHubAppPermissions:
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast(GitHubAppPermissions, result)

    @builtins.property
    def target_rule(self) -> "TokenProviderTargetRule":
        result = self._values.get("target_rule")
        assert result is not None, "Required property 'target_rule' is missing"
        return typing.cast("TokenProviderTargetRule", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TokenProviderSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TokenProviderTargetRule(
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/ghrawel.TokenProviderTargetRule",
):
    @jsii.member(jsii_name="allowOwner")
    @builtins.classmethod
    def allow_owner(cls) -> "TokenProviderTargetRule":
        return typing.cast("TokenProviderTargetRule", jsii.sinvoke(cls, "allowOwner", []))

    @jsii.member(jsii_name="atLeastOne")
    @builtins.classmethod
    def at_least_one(cls) -> "TokenProviderTargetRule":
        return typing.cast("TokenProviderTargetRule", jsii.sinvoke(cls, "atLeastOne", []))

    @builtins.property
    @jsii.member(jsii_name="repositorySelectionMode")
    def repository_selection_mode(self) -> RepositorySelectionMode:
        return typing.cast(RepositorySelectionMode, jsii.get(self, "repositorySelectionMode"))


@jsii.implements(IGitHubApps)
class BaseGitHubApps(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@catnekaise/ghrawel.BaseGitHubApps",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        default_app_id: jsii.Number,
        storage: GitHubAppSecretsStorage,
        additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param default_app_id: 
        :param storage: 
        :param additional_apps: 
        :param prefix: Default: /catnekaise/github-apps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27f1979774303d0c2c01e555f4c4c0a1762b4eda02f48012eba143682a19f30e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        base_props = GitHubAppsProps(
            default_app_id=default_app_id,
            storage=storage,
            additional_apps=additional_apps,
            prefix=prefix,
        )

        jsii.create(self.__class__, self, [scope, id, base_props])

    @jsii.member(jsii_name="getAppIdForAppName")
    def get_app_id_for_app_name(
        self,
        name: typing.Optional[builtins.str] = None,
    ) -> jsii.Number:
        '''
        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad019f9459017cf2cddaf31a8a53227ee2baef1e41357434e10683b65ebe6707)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(jsii.Number, jsii.invoke(self, "getAppIdForAppName", [name]))

    @jsii.member(jsii_name="grantAccess")
    @abc.abstractmethod
    def grant_access(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''
        :param principal: -
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secretsPrefix")
    def secrets_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "secretsPrefix"))

    @builtins.property
    @jsii.member(jsii_name="secretsStorage")
    def secrets_storage(self) -> GitHubAppSecretsStorage:
        return typing.cast(GitHubAppSecretsStorage, jsii.get(self, "secretsStorage"))


class _BaseGitHubAppsProxy(BaseGitHubApps):
    @jsii.member(jsii_name="grantAccess")
    def grant_access(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''
        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c7528b5339ac187841708f3d23e74a3549d79d818c32bedd6f7be955412848)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant], jsii.invoke(self, "grantAccess", [principal]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, BaseGitHubApps).__jsii_proxy_class__ = lambda : _BaseGitHubAppsProxy


@jsii.implements(IGitHubApps)
class ManagedGitHubApps(
    BaseGitHubApps,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/ghrawel.ManagedGitHubApps",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        default_app_id: jsii.Number,
        storage: GitHubAppSecretsStorage,
        additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param kms_key: Default: AWS_MANAGED
        :param removal_policy: 
        :param default_app_id: 
        :param storage: 
        :param additional_apps: 
        :param prefix: Default: /catnekaise/github-apps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cb1c73287d45be4f5b69a9432034aa182ac35ae8c794b2df147a28493044204)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ManagedGitHubAppsProps(
            kms_key=kms_key,
            removal_policy=removal_policy,
            default_app_id=default_app_id,
            storage=storage,
            additional_apps=additional_apps,
            prefix=prefix,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantAccess")
    def grant_access(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''
        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f10ee4429bad1059239a053c84aaafabde43268615c43e39ee72d305df06bc)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant], jsii.invoke(self, "grantAccess", [principal]))


@jsii.implements(IGitHubApps)
class SelfManagedGitHubApps(
    BaseGitHubApps,
    metaclass=jsii.JSIIMeta,
    jsii_type="@catnekaise/ghrawel.SelfManagedGitHubApps",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        default_app_id: jsii.Number,
        storage: GitHubAppSecretsStorage,
        additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param default_app_id: 
        :param storage: 
        :param additional_apps: 
        :param prefix: Default: /catnekaise/github-apps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbe394f36e36b2141bc186e96cce5e41b0d34930a7e0ee7d8ce090bc4606f95)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubAppsProps(
            default_app_id=default_app_id,
            storage=storage,
            additional_apps=additional_apps,
            prefix=prefix,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantAccess")
    def grant_access(
        self,
        principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant]:
        '''
        :param principal: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41de57ad1f319b3bc402c07c093da5c87ef6c98a5b7f67c06ee4ccc0e1311ff3)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.Grant], jsii.invoke(self, "grantAccess", [principal]))


__all__ = [
    "BaseGitHubApps",
    "GitHubApp",
    "GitHubAppPermissions",
    "GitHubAppSecretsStorage",
    "GitHubAppsProps",
    "IGitHubApps",
    "ITokenProvider",
    "ITokenProviderApi",
    "ManagedGitHubApps",
    "ManagedGitHubAppsProps",
    "NewTokenProviderConfiguration",
    "PermissionLevel",
    "RepositorySelectionMode",
    "SelfManagedGitHubApps",
    "TargetRuleSettings",
    "TokenProvider",
    "TokenProviderActionsIdentitySettings",
    "TokenProviderApi",
    "TokenProviderApiProps",
    "TokenProviderConfigurator",
    "TokenProviderConfiguratorIntegrationOptionsContext",
    "TokenProviderConfiguratorMethodOptionsContext",
    "TokenProviderEndpoint",
    "TokenProviderEndpointType",
    "TokenProviderMethodOptions",
    "TokenProviderPathPolicyVariable",
    "TokenProviderPathStrategy",
    "TokenProviderPathStrategyType",
    "TokenProviderSettings",
    "TokenProviderTargetRule",
]

publication.publish()

def _typecheckingstub__5b8b58cfbf31d20c1a3f2dbdd99873aeeaa79ca05b9edb00bbfa6c79318414b2(
    name: builtins.str,
    app_id: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae7544ad6702ec73277e1729d8a5a1e716ff1633f500f3c4388e5033f7adc364(
    *,
    actions: typing.Optional[PermissionLevel] = None,
    administration: typing.Optional[PermissionLevel] = None,
    checks: typing.Optional[PermissionLevel] = None,
    codespaces: typing.Optional[PermissionLevel] = None,
    contents: typing.Optional[PermissionLevel] = None,
    dependabot_secrets: typing.Optional[PermissionLevel] = None,
    deployments: typing.Optional[PermissionLevel] = None,
    email_addresses: typing.Optional[PermissionLevel] = None,
    environments: typing.Optional[PermissionLevel] = None,
    followers: typing.Optional[PermissionLevel] = None,
    git_ssh_keys: typing.Optional[PermissionLevel] = None,
    gpg_keys: typing.Optional[PermissionLevel] = None,
    interaction_limits: typing.Optional[PermissionLevel] = None,
    issues: typing.Optional[PermissionLevel] = None,
    members: typing.Optional[PermissionLevel] = None,
    metadata: typing.Optional[PermissionLevel] = None,
    organization_administration: typing.Optional[PermissionLevel] = None,
    organization_announcement_banners: typing.Optional[PermissionLevel] = None,
    organization_copilot_seat_management: typing.Optional[PermissionLevel] = None,
    organization_custom_org_roles: typing.Optional[PermissionLevel] = None,
    organization_custom_properties: typing.Optional[PermissionLevel] = None,
    organization_custom_roles: typing.Optional[PermissionLevel] = None,
    organization_events: typing.Optional[PermissionLevel] = None,
    organization_hooks: typing.Optional[PermissionLevel] = None,
    organization_packages: typing.Optional[PermissionLevel] = None,
    organization_personal_access_token_requests: typing.Optional[PermissionLevel] = None,
    organization_personal_access_tokens: typing.Optional[PermissionLevel] = None,
    organization_plan: typing.Optional[PermissionLevel] = None,
    organization_projects: typing.Optional[PermissionLevel] = None,
    organization_secrets: typing.Optional[PermissionLevel] = None,
    organization_self_hosted_runners: typing.Optional[PermissionLevel] = None,
    organization_user_blocking: typing.Optional[PermissionLevel] = None,
    packages: typing.Optional[PermissionLevel] = None,
    pages: typing.Optional[PermissionLevel] = None,
    profile: typing.Optional[PermissionLevel] = None,
    pull_requests: typing.Optional[PermissionLevel] = None,
    repository_custom_properties: typing.Optional[PermissionLevel] = None,
    repository_hooks: typing.Optional[PermissionLevel] = None,
    repository_projects: typing.Optional[PermissionLevel] = None,
    secrets: typing.Optional[PermissionLevel] = None,
    secret_scanning_alerts: typing.Optional[PermissionLevel] = None,
    security_events: typing.Optional[PermissionLevel] = None,
    single_file: typing.Optional[PermissionLevel] = None,
    starring: typing.Optional[PermissionLevel] = None,
    statuses: typing.Optional[PermissionLevel] = None,
    team_discussions: typing.Optional[PermissionLevel] = None,
    vulnerability_alerts: typing.Optional[PermissionLevel] = None,
    workflows: typing.Optional[PermissionLevel] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2ffb7d2678ffbad6c0c3782621cdf2f494f16350855d8910531dfa9469fd7f(
    *,
    default_app_id: jsii.Number,
    storage: GitHubAppSecretsStorage,
    additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93065fc1a73507023cd84becd96fbd7613ba014c83d24cb0aa1871140ddff6c0(
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6317f8b4c7d726827a7160e640d328ed0cb6540889f2786903f016ea5cac8506(
    principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff92f177cf21f77bb26e71233de3d0b41b212c731621b5bfc1c71796faa2458(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
    owner: typing.Optional[builtins.str] = None,
    *repo: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__107060e3b9ef192c6f3645dcf54ce3c7fda51f51e74c2c0534c6a6d60216d1a7(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    path_strategy: typing.Optional[TokenProviderPathStrategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6efd91b3b22e294cb3ea209964f69f2c75291cd5076dab68165dc014f4445cba(
    name: builtins.str,
    *,
    permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
    app: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[TokenProviderEndpoint] = None,
    target_rule: typing.Optional[TokenProviderTargetRule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bebb70c3fdb800811e05fdca4f145b17995d6b66268ee8c12556b14ce8176de4(
    *,
    default_app_id: jsii.Number,
    storage: GitHubAppSecretsStorage,
    additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
    prefix: typing.Optional[builtins.str] = None,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222a766e2b57364cf9f0ce77e00ad40e2f806fcf6ac3f1a758987802a2251ba4(
    *,
    permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
    app: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[TokenProviderEndpoint] = None,
    target_rule: typing.Optional[TokenProviderTargetRule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b704a2551113104895eeb05c4cdbd2cf7bc1695f4ed86ec2429e0eea9c42b1e7(
    *,
    mode: RepositorySelectionMode,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47da14983d315f770cb9b49258cbc42dedecdde7f9cfcaa1128629120b5c67ca(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api: _aws_cdk_aws_apigateway_ceddda9d.IRestApi,
    app: builtins.str,
    app_id: jsii.Number,
    configurator: TokenProviderConfigurator,
    endpoint: TokenProviderEndpoint,
    lambda_: _aws_cdk_aws_lambda_ceddda9d.Function,
    method_options: typing.Union[TokenProviderMethodOptions, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
    target_rule: TokenProviderTargetRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b4f69eb50f8ef45c03e843ee6071a4517fd7ac801d14b710c8e21f196082f3(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
    owner: typing.Optional[builtins.str] = None,
    *repo: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462c5ac83e1dd36c07945f3eb3c8edae77bd1e2f6bbc72e59e89bc02e4211dc0(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    path_strategy: typing.Optional[TokenProviderPathStrategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cb028368768599a36c4cd7674f28aa6e8617839b5ea5a560c6b518e24c9435d(
    metric_name: builtins.str,
    stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee92cd394d7c5e60a3a6d6d6085b2bd220443dce44821cdf0297e344332eea82(
    stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37867ee6c92c75b5e203b36fa548e1595763285e5079c5e17f06eaa136a5d85(
    stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b71ddd65c8933685e07c859f54c170824a3be4f14fc757206727f3d88374c3(
    stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5050afe9ba4d1e3083eb566d8a24e8bb4f5c7e7bf49d73d8fab3f06e685cd89(
    stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b316e21cc306460bf236437740b400c22ee427198e6233e14064cfa18fbbdfe4(
    stage: _aws_cdk_aws_apigateway_ceddda9d.IStage,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7548c7b1a9a3bc552cfeb35d3873c2c9c68dc2707998a33a2f1e762c78260484(
    *,
    claims_context: _catnekaise_cdk_iam_utilities_ea41761b.IClaimsContext,
    path_strategy: typing.Optional[TokenProviderPathStrategy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__447181897fd65ed027681dd6ae55f3617b7987814a20d194d8f72359dddd2e1a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    apps: IGitHubApps,
    api: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.RestApi] = None,
    lambda_: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c8c4edca56b96907bb6a3d0352cf11ed13cc9261a825014e2d722ce7a80793(
    name: builtins.str,
    *,
    permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
    app: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[TokenProviderEndpoint] = None,
    target_rule: typing.Optional[TokenProviderTargetRule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5c0ccca61c2f54b020376534f7552111a23464932c1bedd4424de39f457b4b3(
    *,
    apps: IGitHubApps,
    api: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.RestApi] = None,
    lambda_: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Function] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbd4856310dc9f8ff7221de72e178cde01b590eadf25d1132cde57b50f9d52c(
    api: _aws_cdk_aws_apigateway_ceddda9d.IRestApi,
    name: builtins.str,
    endpoint: TokenProviderEndpoint,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8c55c93ce5b6beab389dc743e3ea3bd35cb5b9ed46cdaa6c5aca4fa01f678d5(
    *,
    app_id: jsii.Number,
    app_name: builtins.str,
    endpoint: TokenProviderEndpoint,
    name: builtins.str,
    permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
    target_rule: typing.Union[TargetRuleSettings, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cab4e27fc7db0d13d7cd3871bbe773dd647644e979f731a2be04f5772269d5f(
    *,
    endpoint_type: TokenProviderEndpointType,
    error_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
    operation_name: builtins.str,
    repository_selection_mode: RepositorySelectionMode,
    token_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
    request_validator: typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.IRequestValidator] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dfff464a70314acdf214d8d395eea7820fb7c46866eddb34aadcb58b8114abd(
    owner: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7289d88a63a29e2063dcc14e5944e9bd86ab9d8092085773bc0a4dff54a40c(
    *,
    endpoint_type: TokenProviderEndpointType,
    error_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
    operation_name: builtins.str,
    request_validator: _aws_cdk_aws_apigateway_ceddda9d.RequestValidator,
    token_response_model: _aws_cdk_aws_apigateway_ceddda9d.Model,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__711170ee6ec315efc6274e3c4bf4a19333e645345a5d63663a8ad84a5d1446a6(
    *repositories: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__751d68b1211241b423a94adb8c95ce481e7ae72795c4f23fed73d9fba682c189(
    owner: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9454746a1597183761c9d3392e3e5072e5d4272f4009d1db2c34272f5808e3(
    owner: builtins.str,
    *repositories: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df343b45d0e38600b0deb1a3f53edaf9ed4bb9de01ef8e0bb0706ce7a71c9424(
    *,
    api: _aws_cdk_aws_apigateway_ceddda9d.IRestApi,
    app: builtins.str,
    app_id: jsii.Number,
    configurator: TokenProviderConfigurator,
    endpoint: TokenProviderEndpoint,
    lambda_: _aws_cdk_aws_lambda_ceddda9d.Function,
    method_options: typing.Union[TokenProviderMethodOptions, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    permissions: typing.Union[GitHubAppPermissions, typing.Dict[builtins.str, typing.Any]],
    target_rule: TokenProviderTargetRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27f1979774303d0c2c01e555f4c4c0a1762b4eda02f48012eba143682a19f30e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    default_app_id: jsii.Number,
    storage: GitHubAppSecretsStorage,
    additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad019f9459017cf2cddaf31a8a53227ee2baef1e41357434e10683b65ebe6707(
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c7528b5339ac187841708f3d23e74a3549d79d818c32bedd6f7be955412848(
    principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb1c73287d45be4f5b69a9432034aa182ac35ae8c794b2df147a28493044204(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    default_app_id: jsii.Number,
    storage: GitHubAppSecretsStorage,
    additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f10ee4429bad1059239a053c84aaafabde43268615c43e39ee72d305df06bc(
    principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbe394f36e36b2141bc186e96cce5e41b0d34930a7e0ee7d8ce090bc4606f95(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    default_app_id: jsii.Number,
    storage: GitHubAppSecretsStorage,
    additional_apps: typing.Optional[typing.Sequence[GitHubApp]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41de57ad1f319b3bc402c07c093da5c87ef6c98a5b7f67c06ee4ccc0e1311ff3(
    principal: _aws_cdk_aws_iam_ceddda9d.IPrincipal,
) -> None:
    """Type checking stubs"""
    pass
