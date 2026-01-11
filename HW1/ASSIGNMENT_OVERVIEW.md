# HW1: Context-Driven Development with AI

## Learning Goals

By completing this assignment, you will learn to:

1. **Provide effective context to AI assistants** - Structure information so AI can understand your goals, constraints, and technical requirements without constant clarification
2. **Equip AI with the right tools** - Set up capabilities like browser automation, documentation access, and testing so AI can verify its work autonomously
3. **Design iterative workflows** - Break complex features into manageable steps where AI handles implementation while you focus on architecture and review
4. **Work with unfamiliar codebases** - Practice giving context about libraries, frameworks, or patterns that may not be in AI training data

## The Challenge

Build a web application that helps writers outline short stories using Orson Scott Card's "MICE Quotient" structure (Milieu, Idea, Character, Event).

Video Introduction: https://youtu.be/KsZwxlUF3vs

### What Success Looks Like

A successful solution will:

- **Display the four MICE sections** with clear visual organization
- **Allow adding story elements** to each section with a title and description
- **Enable editing and deleting** elements after creation
- **Persist data** so outlines survive page refreshes
- **Provide a clean, usable interface** that writers can actually use

### Core Functionality Requirements

Your application needs to support this workflow:

1. Writer opens the app and sees their cards and the overview
2. Writer can add cards to any section
3. Writer can edit existing cards to refine their outline
4. Writer can delete cards that don't fit
5. Work is saved automatically or explicitly (your choice)
6. Writer can return later and continue working

## Context is Key

This assignment isn't about writing every line of code yourself. It's about:

- **Documenting requirements** clearly enough that AI understands what to build
- **Providing technical context** like framework documentation, coding standards, and architecture decisions
- **Setting up verification tools** so AI can test its own work (browser automation, running the app, checking for errors)
- **Reviewing and refining** what AI produces rather than writing from scratch

## Approach Options

### Extend the Example
- Start with the provided implementation
- Add features like:
  - Mobile-responsive design
  - Drag-and-drop reordering within sections
  - Database migrations (Alembic)
  - Multi-user support with authentication
  - AI-powered outline generation
  - Export and sharing capabilities

### Use Provided Scaffolding
- Review the example implementation in `/demo`
- Study the context files (requirements, plan, agent instructions)
- Observe how MCP servers provide tools for verification
- Use or adapt these patterns for your implementation

### Start From Scratch
- Choose any tech stack (PHP, Next.js, Django, FastHTML, Rails, etc.)
- Create your own requirements document
- Set up your own context files and tools
- Build the complete application with AI assistance

## Key Concepts to Explore

### Context Files
- Requirements documents that explain WHAT to build and WHY
- Technical plans that outline HOW to build it
- Agent instructions that define coding standards and workflows

### AI Tools (MCP Servers)
- **Browser automation** (Playwright) - Let AI click buttons and verify UI
- **Documentation access** (framework docs) - Give AI reference materials
- **Code execution** - Allow AI to run and test code

### Iterative Development
- Break work into small, verifiable steps
- Have AI implement one piece at a time
- Review and commit incrementally
- Refactor when a feature is complete

## The Specflow Process

For larger features, consider using the **Specflow** methodology—a structured approach to going from idea to implementation:

1. **Brainstorm** (`BRAINSTORM.md`) - Capture raw, unstructured ideas. Voice transcription works great here.

2. **Specify** (`SPEC.md`) - Transform your brainstorm into a formal specification. Think through:
   - Who are the users and what do they need?
   - What are the important features?
   - What technology stack will you use?
   - What assumptions are being made?

3. **Task** (`TASKS.md`) - Break the spec into a list of development tasks that AI can execute one at a time.

The key insight: **you are the architect**. AI handles implementation, but you provide direction through clear specifications.

Templates and more details: https://github.com/specstoryai/specflow

## Getting Started

1. **Understand the domain** - Read about the MICE Quotient structure for story outlining
2. **Define your requirements** - What exactly should this app do?
3. **Choose your tools** - What framework and AI assistant will you use?
4. **Set up verification** - How will you (and AI) know if something works?
5. **Plan your approach** - What order will you build features? Consider using Specflow.
6. **Start building** - Begin with the simplest functional version

## Resources

- Example implementation: `/demo/3. BetterContext/`
- Context examples: See `CLAUDE.md`, `plan.md`, `todos.md` in demo
- Process documentation: `README.md` in demo directory
- Specflow templates: https://github.com/specstoryai/specflow
