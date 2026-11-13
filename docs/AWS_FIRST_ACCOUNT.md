# First personal AWS account

Verified against AWS documentation on 2026-11-13. AWS currently has both a new project-based sign-up experience and an advanced account setup. Screens can differ; use the branch matching the account you actually create. No AWS credentials are needed in chat or GitHub.

## First step: create and open the account

Start at [AWS](https://aws.amazon.com/) and choose Create an AWS account. Complete email/identity/billing verification yourself and review any paid-plan terms. Choose Basic Support when a support-plan choice is offered. Account creation and any upgrade/financial commitment remain your actions.

The [new experience](https://docs.aws.amazon.com/accounts/latest/reference/sign-in-new.html) organizes resources into projects and can support Google/GitHub sign-in. A Builder ID alone is not the same as a provisioned AWS account. The [advanced flow](https://docs.aws.amazon.com/accounts/latest/reference/getting-started.html) offers full account configuration and is relevant if the project's networking/compute requirements are unavailable in the new plan. Compare [supported services](https://docs.aws.amazon.com/accounts/latest/reference/supported-services-sign-up-new.html) before changing plans. Do not upgrade merely to follow an older tutorial.

For an advanced account, protect the root login with MFA and use a separate temporary-credential identity for daily work. Do not create root access keys. For a new-experience account, use the account's supported identity and project-access flow. We should inspect which flow you have before creating permissions.

## Choose cost controls before launch

Pick a small monthly pilot amount you are comfortable paying and confirm the deployment region. `us-east-1` is our current planning assumption, not a configured account setting.

In Billing and Cost Management, create a monthly cost budget with email notifications, for example at 50%, 80% and 100% of your chosen amount. [AWS budget setup](https://docs.aws.amazon.com/cost-management/latest/userguide/create-cost-budget.html). A normal budget is an alert; it does not automatically cap spending. If the new paid project experience offers a spend limit, that is separate: review its scope and behavior in AWS Settings before relying on it. Free-tier credits do not imply that all services or future usage are free.

## Connect this Mac with temporary credentials

1. Install the current official **AWS CLI v2 for macOS** using [AWS's installer instructions](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html). The browser-login command requires v2.32.0 or newer. `pip install awscli` is not the v2 installation path.
2. Open Terminal and run `aws --version`.
3. For supported console credentials, run:

```sh
aws login --profile book-revival
```

Choose the intended account/project in the browser and approve the sign-in yourself. Set the selected region when prompted. An IAM user/role may need the `SignInLocalDevelopmentAccess` managed policy for this login flow; this permits local sign-in, not all deployment operations. Do not use root for project deployment.

If the account instead uses IAM Identity Center, use its own flow with your start URL and account assignment:

```sh
aws configure sso --profile book-revival
aws sso login --profile book-revival
```

If the new AWS experience presents Connect an AI coding tool for the project, follow that project-specific route and inspect the permissions it grants. Do not invent a start URL or access key to make a generic tutorial work.

4. Verify the session locally:

```sh
aws sts get-caller-identity --profile book-revival
```

This is a read-only identity check and does not deploy anything. Its output includes account/identity identifiers; there is no need to paste tokens or keys into chat. We can inspect the configured profile locally once it is available.

When done:

```sh
aws logout --profile book-revival
```

Identity Center sessions use `aws sso logout` instead.

## What happens next

Confirm that the AWS console opens, identify the account experience, and choose a pilot budget. Then we can verify local login, scope a deployment identity to the planned resources, finish the upload service, and review an infrastructure change set. There is no deployed Book Revival endpoint yet.

References: [console-based CLI login](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html), [AWS sign-in options](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html), [sign-up comparison](https://docs.aws.amazon.com/accounts/latest/reference/sign-up-for-aws.html).
