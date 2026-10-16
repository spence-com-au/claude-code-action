# Claude Code Action

GitHub Actions built on [anthropics/claude-code-action](https://github.com/anthropics/claude-code-action), one per
directory and each used as `joshuaspence/claude-code-action/<directory>@master`.

| Action                       | What it does                                                                    |
|------------------------------|---------------------------------------------------------------------------------|
| [`code-review`](code-review) | Reviews a pull request, then approves it or requests changes in a single review |
| [`mention`](mention)         | Answers a comment, review or issue that mentions `@claude`                      |
