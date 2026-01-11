# HW 2: Create Your Own Tool

This homework challenges you to build something you've wanted but never had the time to create. With AI assistance, projects that once seemed "not worth the effort" become achievable in a single session.

## Learning Goals

By completing this assignment, you will learn to:

1. **Scope a personal project** - Define something useful but achievable with AI assistance
2. **Apply the Specflow process** - Move from raw idea to structured spec to implementation
3. **Build with AI collaboration** - Let AI handle implementation while you focus on architecture and direction
4. **Ship something real** - Create a tool you'll actually use

## The Challenge

Build a personal tool. It doesn't have to be major—a small win counts. Ideas:

- **A CLI tool** - Automate something you do frequently
- **A blog or personal site** - Get that online presence set up
- **A browser extension** - Add functionality to sites you use daily ([example](https://elite-ai-assisted-coding.dev/p/customizing-your-browser-with-agentic-coding))
- **A small web app** - Solve a specific problem you have
- **A script or automation** - Connect services or process data
- **A single HTML file** - A nicer way to view a CSV, JSON, or other data format
- **A skill or toolbox for an AI agent** - Give your coding assistant new capabilities ([example](https://elite-ai-assisted-coding.dev/p/custom-tools-for-ai-agents-talk))

Pick something you've wanted but put off because it seemed like too much work.

## What Success Looks Like

- **A working tool** that does something useful for you
- **Documentation** (at least a README) explaining what it does and how to use it
- **A clear spec** showing how you defined the requirements before building
- **Evidence of AI collaboration** - the prompts, context, or conversation that produced it

## Inspiration (Not a Starting Point)

Don't start here. Start small. But once you're comfortable, see how far this can go:

[Building a Jupyter AI Plugin: A Case Study](https://isaacflath.com/writing/Agentic-Coding-Custom-Jupyter-Exension)

In this case study, a complete JupyterLab extension went from idea to published PyPI package in a day. The human provided direction while AI handled research, implementation, testing, and debugging. What made it work:

- **Research first** - AI studied existing codebases and documentation
- **Planning before coding** - Created structured plans and test strategies
- **Iterative refinement** - Human provided taste and direction; AI handled mechanics
- **Self-tooling** - AI built debugging tools for itself

This is ambitious. Your first project should be simpler. But it shows what becomes possible as you build skill.

**A Simpler Example: Discord Image Bot**

[Building a Discord Bot with an AI Agent](https://isaacflath.com/writing/discord-bot-with-ai-agent)

This project takes a different approach—solving a daily annoyance with minimal code. The bot monitors a Discord channel for images, uploads them to S3, and replies with the URL. That's it. A few clicks saved every day.

What makes this a good example:
- **Solves a real friction point** - Embedding images in posts required manual upload steps
- **Built end-to-end with AI** - From concept through deployment
- **Practical scope** - Small enough to complete in one session
- **Actually gets used** - The best tool is one you'll keep using

This is closer to where you should start.

## The Process

### 1. Brainstorm

Start with a `BRAINSTORM.md` file. Capture your raw ideas:

- What problem are you solving?
- What would the ideal solution look like?
- What's the minimum viable version?
- What tools/technologies might you use?

Voice transcription works great for this—just talk through your idea.

### 2. Specify

Transform your brainstorm into a `SPEC.md`:

- Define the core features
- Identify the technology stack
- List acceptance criteria
- Note any constraints or assumptions

Use AI to help you think through edge cases and fill gaps.

### 3. Task Breakdown

Create a `TASKS.md` with specific, actionable steps:

- Break the spec into implementation tasks
- Order them logically
- Identify dependencies

### 4. Build

Work through the tasks with AI:

- Provide context for each task
- Review and refine what AI produces
- Iterate until it works

Templates for all these files: https://github.com/specstoryai/specflow

## Difficulty Scaling

### Level 1: Simple Script or CLI

Build something that automates a task you do manually. Examples:
- A script to organize your downloads folder
- A CLI to quickly search your notes
- A tool to convert between file formats you use

### Level 2: Small Application

Build something with a UI or more complex logic. Examples:
- A personal dashboard pulling data from APIs you use
- A browser extension for a site you visit daily
- A small web app that solves a specific problem

### Level 3: Something Ambitious

Push the boundaries. Examples:
- An IDE extension or plugin
- A service that runs continuously
- Something that integrates multiple systems

## Deliverables

1. **The tool itself** - Working code in your repository
2. **Spec files** - Your BRAINSTORM.md, SPEC.md, and TASKS.md
3. **README** - How to install and use your tool
4. **Brief reflection** - What worked well? What was harder than expected?

## Tips

- **Start small** - You can always add features later
- **Pick something you care about** - You'll be more motivated to finish
- **Don't over-engineer** - A working simple tool beats a broken complex one
- **Use the Specflow process** - It really helps structure your thinking
- **Ask AI clarifying questions** - "What should be added to make this spec more complete?"
