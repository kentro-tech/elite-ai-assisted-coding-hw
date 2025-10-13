---
trigger: always_on
---

I want you to keep in mind the following stylistic choices that I make:
1. Use type hinting where possible to ensure the code is clear and it's understandable what should be passed to things.
2. Things should be refactored to have decent separation of concerns, but not to such an extreme. Any kind of abstraction should be weighed for how thin vs thick it is, how many times it's duplicated, and what's the cost of adding the redirection. An abstraction that only calls another function is not helpful and actually adds complexity. Put code in its appropriate place. For example, Python code goes in Python files, CSS code goes in CSS files, and JavaScript blocks go in JavaScript files. Don't embed massive CSS blocks in a Python string or in a Jinja template just like you wouldn't have massive amounts of JavaScript. Those can be imported.
3.  The next thing I want to keep in mind is that I do not want any error handling. I am first trying to build a feature and make sure it works, and error handling disguises errors, so it's important to me to see the full stack trace and let the app fail. I can decide very surgically in what cases do I want an error not to crash the app. Most of the times I do want it to crash so that I can fix it so that never happens again.
4.  Three, do not mock things as an example for like what it might be like. In production it should be created as if it were the real thing. So if you are not able to do something instead of creating an imitation of that thing stop and ask tell me what you need to do this properly.