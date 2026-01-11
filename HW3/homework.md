# HW 3: Automated Code Review

This assignment sets up automated tech debt analysis for your repository. An AI agent will review your codebase on a schedule and create GitHub issues with findings.

## Learning Goals

1. **Set up GitHub Actions** - Configure workflows that run on schedules or triggers
2. **Integrate an AI agent** - Connect automated code review to your repository
3. **Automate code quality checks** - Let AI find problems before they grow

## The Challenge

Configure your repository so an AI agent automatically reviews your codebase for tech debt every week and creates a GitHub issue with findings.

## What Success Looks Like

- An AI code review tool installed on your repository
- A workflow file that triggers the AI to analyze your code
- A GitHub issue created by the AI with tech debt findings

## Setup

> **Note:** This example uses Claude Code with GitHub Actions, but similar setups exist for other AI tools (Cursor, GitHub Copilot, etc.). The core concept—automating code review with AI—applies regardless of which tool you choose.

### Step 1: Install the Claude Code GitHub App

In Claude Code, run:

```
/install-github-app
```

Follow the instructions to connect Claude Code to your repository.

### Step 2: Add the Workflow File

Create `.github/workflows/tech-debt.yml` with this content:

```yaml
name: Claude Tech Debt Review

on:
  schedule:
    - cron: '0 18 * * 0'  # Runs every Sunday at 6 PM UTC
  workflow_dispatch:  # Allows manual triggering

jobs:
  tech-debt-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
      id-token: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 1

      - name: Run Claude Tech Debt Analysis
        id: claude-tech-debt
        uses: anthropics/claude-code-action@v1
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
          prompt: |
            REPO: ${{ github.repository }}
            DATE: ${{ github.event.schedule || 'manual' }}

            Please analyze the codebase for technical debt and create a GitHub issue with your findings grouped by severity and priority.

            Focus on:
            - Excessive try/except handling that hides errors (CRITICAL)
            - Code duplication and opportunities for refactoring (CRITICAL)
            - Outdated dependencies or deprecated patterns
            - Security vulnerabilities or concerns
            - Code complexity that could be simplified
            - Confusing or unclear naming, structure, or redirections

            Search the codebase thoroughly and provide specific examples with file paths and line numbers.

            Create a new GitHub issue with:
            - Title: "Tech Debt Review - [Current Date]"
            - Body containing:
              - Summary of findings
              - Prioritized list of tech debt items
              - Specific file locations and code references
              - Recommended actions

            Use `gh issue create` with your Bash tool to create the issue with labels "tech-debt" and "automated".

          claude_args: '--allowed-tools "Bash(gh issue create:*),Bash(gh issue list:*),Bash(gh label list:*)"'
```

### Step 3: Test It

Don't wait until Sunday. Trigger the workflow manually:

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Claude Tech Debt Review** from the left sidebar
4. Click **Run workflow** button
5. Watch it run and check the created issue

![Manual workflow trigger](https://isaacflath.s3.us-east-1.amazonaws.com/cb7ab823072eb9af42da3bf9c7ae603a.png)

## Customization

### Change the Schedule

The `cron: '0 18 * * 0'` line controls when the workflow runs. To customize it, ask an LLM: *"Give me a cron expression for [your preferred schedule] in UTC."*

### Modify the Prompt

Edit the `prompt` section to focus on what matters for your codebase:

- Add specific patterns you want to catch
- Remove checks that don't apply
- Adjust severity levels based on your priorities

### Create Multiple Workflows

Copy the file to create specialized reviewers:

- `security-review.yml` - Focus only on security concerns
- `dependency-check.yml` - Focus on outdated packages
- `style-review.yml` - Focus on code style and naming

## Deliverables

1. **Workflow file** committed to `.github/workflows/`
2. **Screenshot or link** to a successful workflow run
3. **GitHub issue** created by Claude with tech debt findings
4. **Brief notes** on any customizations you made to the prompt

## Tips

- Start with the default prompt, then customize based on what Claude finds
- If the workflow fails, check the Actions logs for error messages
- The `workflow_dispatch` trigger lets you test without waiting for the schedule
