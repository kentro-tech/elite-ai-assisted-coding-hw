# Code Quality Guidelines

When generating or modifying code, please adhere to these principles:

## Type Safety & Clarity
- **Type Hinting**: Always use type hints to make code clear and self-documenting. Every function parameter and return value should have explicit type annotations.

## Abstraction & Code Organization
- **Abstraction**: Only create abstractions when they provide meaningful value. Evaluate each abstraction by:
    - How thick vs. thin it is (avoid thin wrappers that just call another function).
    - How many times the pattern is duplicated (don't abstract until there's clear duplication several times)
    - The cost of adding indirection to readability (complexity should be justified)
- **Duplication**: Some duplication is acceptable. If it's just a couple lines of code refactor on the third occurrence, not the second.  But if duplication is likely to lead to a bug that negatively effects functionality in a significant way the future, refactor more aggressively.
- **File Structure**: Maintain proper separation of concerns by file type. Python code belongs in `.py` files, CSS in `.css` files, JavaScript in `.js` files. Never embed large blocks of CSS or JavaScript as strings in Python or templates - import them instead.
- **Function Size**: Functions can be longer if they represent a single, cohesive task. Prioritize clarity over line limits.

## Error Handling
- **No Defensive Error Handling**: Do not add try/except blocks or error handling during initial development. Let the application fail with full stack traces so bugs can be identified and fixed at their source. Error handling should only be added surgically in specific cases where graceful degradation is truly needed.

## Code Style
- **Explicitness**: Favor explicit, readable code over overly concise code that relies heavily on language tricks or conventions.
- **Readability**: Prioritize readability over performance optimizations unless performance is explicitly a concern.
- **Comments**: Use comments to explain *why* (intent and business logic), not *how* (implementation details should be self-evident from clear code).

## Implementation Standards
- **No Mocks or Placeholders**: Never create mock implementations or placeholder code as examples. If you cannot implement something properly, stop and ask what information or resources are needed to do it correctly. All code should be realistic.
- **Dependencies**: Prefer adding well-maintained third-party libraries over writing complex functionality from scratch.  But never add a dependency without providing options and alternatives first for me to consider carefully.
- **Design Patterns**: Use the simplest solution that works. Only apply formal design patterns when they meaningfully simplify the code.  I do not care about design patterns, I care about simple solutions and readable code.
- **Paradigm**: Favor functional programming patterns where appropriate (pure functions, immutability for data transformations) wherever possible. In general, if state needs to be managed do so in a database like sqlite or postgres.  But if there's really strong reasons to, you can use object-oriented patterns when managing state or modeling entities.
- **Data Structures**: Immutable data structures are preferred for data transformations, but mutable state is acceptable when managing application state or building up complex objects.

# Neccesary Context

In order to complete this, you'll need several pieces of information:

- There's an overall plan in the plan.md file
- There's a specific step by step plan in the todos.md file that dictates how we will build this app together
- If there's any doubt, stop me so that we can proceed forward together
- You should always verify things are being done correctly by checking the documentation of air, which you have tools to inspect.  The best developers reference the documentation a lot.
- After doing something, you should verify that it works. You have access to playwright, and the app is running on port 8000.  Anytime one of the app python files are edited the app auto-reloads so you don't have to worry about refreshing or restarting.
- The air docs are great, you should always look for things in the docs directory to learn about air vs the source code when possible.