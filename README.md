# Claude Code Action

GitHub Actions built on [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action), one per
directory and each used as `spence-com-au/claude-code-action/<directory>@master`.

| Action                       | What it does                                                                    |
|------------------------------|---------------------------------------------------------------------------------|
| [`code-review`](code-review) | Reviews a pull request, then approves it or requests changes in a single review |
| [`mention`](mention)         | Answers a comment, review or issue that mentions `@claude`                      |

## Both in one workflow

[`claude.yaml`](.github/workflows/claude.yaml) is a reusable workflow that runs both on GitHub's runner, for a caller
that needs nothing of its own around them:

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
  pull_request:
    types:
      - 'opened'
      - 'synchronize'
      - 'ready_for_review'
      - 'reopened'
  pull_request_review:
    types:
      - 'submitted'
  pull_request_review_comment:
    types:
      - 'created'

permissions: {}

jobs:
  claude:
    uses: 'spence-com-au/claude-code-action/.github/workflows/claude.yaml@master'
    permissions:
      contents: 'write'
      id-token: 'write'
      issues: 'write'
      pull-requests: 'write'
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: '${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}'
```

The caller grants what the two jobs need between them, and the review job narrows it to read the code. Every event
starts a run in which the job it is not for is skipped, and the checks are named after the calling job, as
`claude / Review` and `claude / Mention`. Use the actions directly for a different runner, setup before Claude runs or
only one of the two.
