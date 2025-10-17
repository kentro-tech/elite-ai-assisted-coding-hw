# HW 1

This homework teaches you to give AI the right context.

Good AI assistance doesn't mean AI writes everything while you stop thinking. It means AI handles the tedious parts so you can focus on what matters.

Here's what that looks like: When you ask AI to add a button, it should click that button and check for errors—not wait for you to do it. When you need to understand an error, AI should reproduce it and show you the actual message instead of guessing. These things save time. They keep you from jumping between tasks. While AI gathers context, you work on something else.

Another example: I'm building a UI with Daisy-UI / Tailwind. I know the classes, but while prototyping I don't want to type `btn-primary` or `btn-secondary` every time. I let AI fill in those details,Then I edit. The same goes for refactoring: moving code from inside a function to above it, wrapping it properly, naming it correctly. AI can do this mechanical work.

Some tasks need careful thought. Others are straightforward but time-consuming. AI should handle the second kind and get close enough that you can quickly polish the result.

To make this work, AI needs tools. You have a mouse to click things in a browser. You can read documentation. Your AI should have the same capabilities. 

Video Introduction: https://youtu.be/KsZwxlUF3vs

> TIP: You can run the air app locally with `uv run fastapi dev`

## The Assignment

**THE TASK:** Accumulate requirements, tools, and other context and then give that to AI to help you build something.

This assignment can be scaled in difficulty based on your abilities and experience.  I recommend starting with #1, and progressing as far as you'd like to:

**Level 1**

Use the context I created in [The `demo/3. BetterContext` directory](https://github.com/kentro-tech/elite-ai-assisted-coding-hw/tree/main/HW1/demo/3.%20BetterContext), read it, and modify something about the app I created using the context and tools.  Create a new requirements document for the feature you are implementing so AI has proper context to help you. 

You don't have to do all of them, just pick one in an area that interests you.  Here's some ideas:

    - UI
        - Make it mobile friendly
        - Allow for re-ordering of the cards within sections.  Arrows or drag and drop
    - Data/Database:
        - Set up database migrations with alembic
        - Add users to make it a multi-user app
    - Features:
        - Add a create outline with AI feature
        - Add exporting and share features
    - Quality:
        - Add test suite
        - Refactor to improve code quality
        - Fix bugs (like styling bug shown in the demo in lecture #1)
    
**Level 2**

1. Read the context carefully to understand it and what is there.  Take notes on the *process* you think you would need to follow to recreate it.  Make notes on the kinds of things you want to include (Such as tech stack, acceptance criteria, tools, etc). 
2. Create a new directory based on the `incomplete` app and just using your notes try to recreate the context.  After you feel like it's good, re-review the context I created to see if there's anything you think you missed that should be included.  Iterate back and forth until you feel like you got everything.
3. Then start creating your app!  It's ok if it takes a few attempts, learn and improve the context each iteration as you see failures.

> ![NOTE]
> It's ok to pick a different framework, like NextJS, Django or FastHTML!  Pick what you like, understand, and can work efficiently in.

**Level 3**

Do this process for your own app or project!  Create an app, or add a new feature.
