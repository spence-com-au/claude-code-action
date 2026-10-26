# Mention

An action in which Claude answers a comment, review or issue that mentions `@claude`: it replies on the pull request
or issue and, where the mention asks for a change, makes it.

## Usage

```yaml
---
name: 'Claude'

on:
  issue_comment:
    types:
      - 'created'
  issues:
    types:
      - 'opened'
  pull_request_review:
    types:
      - 'submitted'
  pull_request_review_comment:
    types:
      - 'created'

permissions: {}

jobs:
  mention:
    name: 'Mention'
    if: |
      contains(github.event.comment.body, '@claude') ||
      contains(github.event.review.body, '@claude') ||
      (github.event_name == 'issues' && (
        contains(github.event.issue.title, '@claude') || contains(github.event.issue.body, '@claude')
      ))
    runs-on: 'ubuntu-latest'

    permissions:
      actions: 'read'
      contents: 'write'
      id-token: 'write'
      issues: 'write'
      pull-requests: 'write'

    steps:
      - name: 'Checkout'
        uses: 'actions/checkout@v7'

      - name: 'Answer the mention'
        uses: 'spence-com-au/claude-code-action/mention@master'
        with:
          claude_code_oauth_token: '${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}'
```

The `if` keeps a comment that does not mention Claude from starting a runner; the action would find no mention and
stop anyway. The job's `permissions` govern `GITHUB_TOKEN`, not the [Claude GitHub app][app]'s installation token that
Claude commits, pushes and comments with, so trimming them does not keep Claude to replies: it can push a branch
whenever a mention asks, including when steered by text in an issue or comment that someone else wrote. The calling
repository also needs that app installed and a `CLAUDE_CODE_OAUTH_TOKEN` secret.

Claude itself uses `GITHUB_TOKEN` only to read a pull request's workflow runs and job logs, so that a mention can ask
why CI failed, and `actions: 'read'` is what that needs; without it the action skips those tools with a warning. Job
logs hold whatever a workflow prints, and GitHub masks only what it knows to be a secret.

On a pull request from a fork, GitHub passes no secrets to `pull_request_review` and `pull_request_review_comment` and
makes their token read-only, so a mention in a review or an inline comment there fails without a reply. Mention Claude
in a comment on the pull request's conversation instead: `issue_comment` runs in the base repository, secrets and all.

Run it from a workflow of its own rather than alongside [`code-review`](../code-review): that action sets a prompt,
which keeps a mention from being answered, and it ends every run in a review verdict, which a mention should never
produce.

[app]: https://github.com/apps/claude
