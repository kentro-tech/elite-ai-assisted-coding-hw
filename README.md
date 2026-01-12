# Elite AI Assisted Coding Homework

We're building a SaaS app to help writers outline short stories using Orson Scott Card's "MICE Quotient" structure.

## Quick Start

1. Install Python 3.13+ and [uv](https://docs.astral.sh/uv/getting-started/installation/)
2. Start with [HW1: Context-Driven Development](./HW1/ASSIGNMENT_OVERVIEW.md)
3. See the reference implementation: `HW1/demo/3. BetterContext/`

## Repository Structure

| Directory | Description |
|-----------|-------------|
| [`HW1/`](./HW1/ASSIGNMENT_OVERVIEW.md) | Context-Driven Development - Build a story outliner |
| [`HW2/`](./HW2/ASSIGNMENT.md) | Create Your Own Tool - Build a personal project |
| [`HW3/`](./HW3/ASSIGNMENT.md) | Automated Code Review - Set up CI/CD with AI |

## Homework Assignments

### HW1: Context-Driven Development
Build a web app that helps writers outline stories using the MICE Quotient structure. Learn to provide effective context to AI assistants and set up verification tools.

**Demos showing progressive context quality:**
- `demo/1. NoContext/` - Minimal context (intentionally incomplete)
- `demo/2. Requirements/` - Good requirements, manual verification
- `demo/3. BetterContext/` - Full context with MCP servers (reference implementation)

### HW2: Create Your Own Tool
Build a personal tool you've wanted but never had time to create. Apply the Specflow process to go from idea to implementation.

### HW3: Automated Code Review
Set up GitHub Actions for AI-powered code review and tech debt analysis.

## Why Short Stories?

We wanted to replicate what it's like to code an actual product:

1. Real products have complexity that isn't solved 10,000 times before
2. This is part of a real product I'm building (you're free to do anything with this!)
3. Like a real product, you might have to learn how it works while you create it

## Why Air?

Air is a FastAPI-based web framework by Daniel and Audrey Roy Greenfeld.

Why I'm using it:

1. Built on FastAPI - proven foundation
2. New - minimal training data. You'll work with context, not memorization
3. I like it. Use what works for you. If Air doesn't work for you, do the assignments in your framework of choice

**Current version:** Air 0.43.0+ (Python 3.13+)

## Why Something New?

Real work involves internal libraries, private repos, and code that's not in training data.

Learning with tools that don't have significant representation in the training data builds those skills.

## Resources

- [Air Documentation](https://github.com/feldroy/air)
- [Specflow Templates](https://github.com/specstoryai/specflow)
- [MICE Quotient Explanation](./HW1/demo/3.%20BetterContext/mice.md)
