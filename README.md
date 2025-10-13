# Elite AI Assisted Coding Homework

We're building a SaaS app to help writers outline short stories using Orson Scott Card's "MICE Quotient" structure.

## Why Short Stories

We thought about making the assignments based on something like a SaaS todo app.  We felt we wanted to replicate what it might be like to code an actual product. This fills that need because:

1. Real products have some complexity that they are solving that isn't solved 10,000 times before
2. I know it's a real product, because it's part of a real product i'm building!  (You're totally free to do anything with this, even release your own product!)
3. Like a real product, you might have to learn a bit about how it's supposed to work while you create it.

## Homework Structure

Each assignment directory has its own `ASSIGNMENT_OVERVIEW.md` file and `ASSIGNMENT_CONCISE.md`.  That file will include:

1. Information about the homework
2. Variety of options for scaling difficulty up and down

You have lifetime access.  My recommmendation is start with the simplest ones and focus on doing them phenomenally well.  Then slowly build up in complexity.  If that takes you 2 weeks or 2 months or 6 months that's fine!

## Why Air?

Air is a FastAPI-based web framework by Daniel and Audrey Roy Greenfeld.

Why I'm using it:

1. Built on FastAPI—proven foundation
2. New — minimal training data. You'll work with context, not memorization.
3. I like it. Use what works for you.  If Air doesn't work for you, do all the assignments in your framework of choice.

## Why Something New?

Real work involves internal libraries, private repos, and code that's not in training data. 

Learning with tools that don't have significant representation in the training data builds those skills.

## 📊 Tech Debt Analysis

A comprehensive analysis of code quality and tech debt has been completed based on the guidelines in `.github/copilot-instructions.md`.

**Start here:** [TECH_DEBT_INDEX.md](./TECH_DEBT_INDEX.md) - Documentation index and overview

**Quick links:**
- [Summary & Priority Matrix](./TECH_DEBT_SUMMARY.md) - Fast reference
- [Detailed Analysis](./TECH_DEBT_ANALYSIS.md) - Complete evaluation with pros/cons
- [Implementation Checklist](./TECH_DEBT_CHECKLIST.md) - Step-by-step guide
- [Visual Guide](./TECH_DEBT_VISUAL_GUIDE.md) - Diagrams and examples

**Key findings:**
- ✅ Demo 3 is the gold standard - follow its patterns
- ⚠️ Missing type hints in 2 files (quick fix: 30 min)
- ⚠️ Inline CSS/JS in Python files (fix: 4-6 hours)
- ✅ Error handling and abstraction quality are excellent

