# Code Quality Questions

Often, you need to define what code quality means to you (or the team).  Here are some things to consider about when defining that:

- **Abstraction**: How thick does a wrapper need to be for it to be worth the redirection?
- **Duplication**: Is the goal zero duplication (DRY), or is a little repetition acceptable for clarity (WET - Write Everything Twice)?  Or something else?
- **File Structure**: Do we favor many small, single-purpose files or fewer, larger files that group related logic?
- **Function Size**: Should functions be minimal (under 10 lines), or are longer, sequential functions acceptable if they represent a single, cohesive task?
- **Explicitness vs. Conciseness**: Do we prefer verbose, explicit code or more concise code that relies on convention and language features?
- **Performance vs. Readability**: Should the AI prioritize raw performance even if it makes the code harder to understand, or is readability paramount? 
- **Error Handling**: Should errors be handled with exceptions or by returning null/error codes? 
- **Comments**: Should comments explain the why (intent) or the how (complex implementation)?
- **Dependencies**: Is it better to write a native functionality or add a new third-party dependency to outsource that complexity?
- **Design Patterns**: Should the AI apply formal design patterns, or opt for the simplest possible solution? 
- **Data Structures**: Should the AI default to immutable data structures, or is mutable state acceptable?
- **Paradigm**: Do you tend to favor more functional patterns, or object oriented patterns?

# Isaac's Prompt/Answers

## Code Quality Guidelines

When generating or modifying code, please adhere to these principles:

### Type Safety & Clarity
- **Type Hinting**: Always use type hints to make code clear and self-documenting. Every function parameter and return value should have explicit type annotations.

### Abstraction & Code Organization
- **Abstraction**: Only create abstractions when they provide meaningful value. Evaluate each abstraction by:
    - How thick vs. thin it is (avoid thin wrappers that just call another function).
    - How many times the pattern is duplicated (don't abstract until there's clear duplication several times)
    - The cost of adding indirection to readability (complexity should be justified)
- **Duplication**: Some duplication is acceptable. If it's just a couple lines of code refactor on the third occurrence, not the second.  But if duplication is likely to lead to a bug that negatively effects functionality in a significant way the future, refactor more aggressively.
- **File Structure**: Maintain proper separation of concerns by file type. Python code belongs in `.py` files, CSS in `.css` files, JavaScript in `.js` files. Never embed large blocks of CSS or JavaScript as strings in Python or templates - import them instead.
- **Function Size**: Functions can be longer if they represent a single, cohesive task. Prioritize clarity over line limits.

### Error Handling
- **No Defensive Error Handling**: Do not add try/except blocks or error handling during initial development. Let the application fail with full stack traces so bugs can be identified and fixed at their source. Error handling should only be added surgically in specific cases where graceful degradation is truly needed.

### Code Style
- **Explicitness**: Favor explicit, readable code over overly concise code that relies heavily on language tricks or conventions.
- **Readability**: Prioritize readability over performance optimizations unless performance is explicitly a concern.
- **Comments**: Use comments to explain *why* (intent and business logic), not *how* (implementation details should be self-evident from clear code).

### Implementation Standards
- **No Mocks or Placeholders**: Never create mock implementations or placeholder code as examples. If you cannot implement something properly, stop and ask what information or resources are needed to do it correctly. All code should be realistic.
- **Dependencies**: Prefer adding well-maintained third-party libraries over writing complex functionality from scratch.  But never add a dependency without providing options and alternatives first for me to consider carefully.
- **Design Patterns**: Use the simplest solution that works. Only apply formal design patterns when they meaningfully simplify the code.  I do not care about design patterns, I care about simple solutions and readable code.
- **Paradigm**: Favor functional programming patterns where appropriate (pure functions, immutability for data transformations) wherever possible. In general, if state needs to be managed do so in a database like sqlite or postgres.  But if there's really strong reasons to, you can use object-oriented patterns when managing state or modeling entities.
- **Data Structures**: Immutable data structures are preferred for data transformations, but mutable state is acceptable when managing application state or building up complex objects.
