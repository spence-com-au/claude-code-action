# Code Review

An action in which Claude reviews a pull request with the [`code-review`][code-review] plugin and publishes the review
as a single pull request review: its findings as inline comments and its verdict as the event — `APPROVE` only when it
would change nothing, `REQUEST_CHANGES` for anything it would, and `COMMENT` when it cannot decide. A run that submits
no review comments on the pull request and fails, and the next run that submits one deletes that comment.

## Usage

```yaml
---
name: 'Claude Review'

on:
  pull_request:
    types:
      - 'opened'
      - 'synchronize'
      - 'ready_for_review'
      - 'reopened'

permissions: {}

jobs:
  review:
    name: 'Review'

    # A pull request from a fork is passed no secrets, so its review would be refused a token, and its `github.token`
    # can only read, so it could not post the comment that explains why either.
    if: |
      !github.event.pull_request.draft &&
      github.event.pull_request.head.repo.full_name == github.repository

    runs-on: 'ubuntu-latest'

    # A push supersedes the review running against the commit before it.
    concurrency:
      cancel-in-progress: true
      group: 'claude-review-${{ github.event.pull_request.number }}'

    permissions:
      contents: 'read'
      id-token: 'write'
      pull-requests: 'write'

    steps:
      - name: 'Checkout'
        uses: 'actions/checkout@v7'

      - name: 'Review the pull request'
        uses: 'spence-com-au/claude-code-action/code-review@master'
        with:
          claude_code_oauth_token: '${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}'
```

The action reads the pull request from `github.event`, so it runs only on a `pull_request` event, and it needs the
repository checked out and the three permissions above. The calling repository also needs the
[Claude GitHub app][app] installed and a `CLAUDE_CODE_OAUTH_TOKEN` secret.

## Gating merges on the verdict

The verdict only gates a merge where a ruleset on the default branch requires an approving review. Turn on
`dismiss_stale_reviews_on_push` with it, so an approval of one commit does not carry over to a push that changes the
diff. An administrator bypass is what lets a pull request that edits the calling workflow land, since the action is
refused a token for one.

[app]: https://github.com/apps/claude
[code-review]: https://github.com/anthropics/claude-code/tree/main/plugins/code-review
