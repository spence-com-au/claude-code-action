# Claude Code Action

GitHub Actions built on [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action), one per
directory and each used as `spence-com-au/claude-code-action/<directory>@master`.

| Action                       | What it does                                                                    |
|------------------------------|---------------------------------------------------------------------------------|
| [`code-review`](code-review) | Reviews a pull request, then approves it or requests changes in a single review |
| [`mention`](mention)         | Answers a comment, review or issue that mentions `@claude`                      |

## The review as a workflow

[`claude.yaml`](.github/workflows/claude.yaml) is a reusable workflow that runs `code-review` on GitHub's runner, for a
caller that needs nothing of its own around it:

```yaml
---
name: 'Claude'

on:
  pull_request:
    types:
      - 'opened'
      - 'synchronize'
      - 'ready_for_review'
      - 'reopened'

permissions: {}

jobs:
  claude:
    uses: 'spence-com-au/claude-code-action/.github/workflows/claude.yaml@master'
    permissions:
      contents: 'read'
      id-token: 'write'
      pull-requests: 'write'
    secrets:
      CLAUDE_CODE_OAUTH_TOKEN: '${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}'
```

The check is named after the calling job, as `claude / Review`. Use the action directly for a different runner or
setup before Claude runs, and [`mention`](mention) from a workflow of its own.
