# Claude Code Action

A reusable workflow in which Claude reviews a pull request with the [`code-review`][code-review] plugin and publishes
the review as a single pull request review: its findings as inline comments and its verdict as the event —
`APPROVE` only when it would change nothing, `REQUEST_CHANGES` for anything it would, and `COMMENT` when it cannot
decide. A run that submits no review comments on the pull request and fails.

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
    uses: 'joshuaspence/claude-code-action/.github/workflows/claude-review.yaml@master'
    permissions:
      contents: 'read'
      id-token: 'write'
      pull-requests: 'write'
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: '${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}'
```

The calling repository needs the [Claude GitHub app][app] installed and a `CLAUDE_CODE_OAUTH_TOKEN` secret.

## Gating merges on the verdict

The verdict only gates a merge where a ruleset on the default branch requires an approving review. Turn on
`dismiss_stale_reviews_on_push` with it, so an approval of one commit does not carry over to a push that changes the
diff. An administrator bypass is what lets a pull request that edits the calling workflow land, since the action is
refused a token for one.

[app]: https://github.com/apps/claude
[code-review]: https://github.com/anthropics/claude-code/tree/main/plugins/code-review
