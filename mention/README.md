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
      contents: 'write'
      id-token: 'write'
      issues: 'write'
      pull-requests: 'write'

    steps:
      - name: 'Checkout'
        uses: 'actions/checkout@v7'

      - name: 'Answer the mention'
        uses: 'joshuaspence/claude-code-action/mention@master'
        with:
          claude_code_oauth_token: '${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}'
```

The `if` keeps a comment that does not mention Claude from starting a runner; the action would find no mention and
stop anyway. `contents: 'write'` is what lets Claude push a change it was asked for, so drop it to keep it to replies.
The calling repository also needs the [Claude GitHub app][app] installed and a `CLAUDE_CODE_OAUTH_TOKEN` secret.

Run it from a workflow of its own rather than alongside [`code-review`](../code-review): that action sets a prompt,
which keeps a mention from being answered, and it ends every run in a review verdict, which a mention should never
produce.

[app]: https://github.com/apps/claude
