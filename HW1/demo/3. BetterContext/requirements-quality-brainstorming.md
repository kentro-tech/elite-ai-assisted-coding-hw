Perfect — since you’re starting **Level 1: Quality**, the focus will be to
**(1)** add a test suite, **(2)** refactor for clarity and consistency, and **(3)** fix existing bugs.
Here’s a gradual path that fits the “AI-assisted coding” learning model while giving you hands-on full-stack understanding.

---

## 🧩 Step 1 — Establish Your Quality Baseline

### 🎯 Goal

Set up a testing environment that can run reliably, even before writing real tests.

### ✅ Actions

1. **Check the tech stack**
   Run the app, confirm it’s React + FastAPI (as per the HW demo).

   * If it’s a FastAPI backend → use `pytest`
   * If it’s a React frontend → use `vitest` or `jest` + `react-testing-library`

2. **Add testing dependencies**

   ```bash
   # Backend
   pip install pytest pytest-asyncio httpx

   # Frontend
   npm install --save-dev vitest @testing-library/react @testing-library/jest-dom
   ```

3. **Create test directories**

   ```
   backend/
     └── tests/
         └── test_healthcheck.py
   frontend/
     └── src/
         └── __tests__/
             └── App.test.jsx
   ```

4. **Sanity tests**

   * **Backend:** check API health endpoint

     ```python
     from httpx import AsyncClient
     from app.main import app

     import pytest

     @pytest.mark.asyncio
     async def test_healthcheck():
         async with AsyncClient(app=app, base_url="http://test") as ac:
             response = await ac.get("/health")
         assert response.status_code == 200
     ```
   * **Frontend:**

     ```jsx
     import { render, screen } from '@testing-library/react'
     import App from '../App'

     test('renders header', () => {
       render(<App />)
       expect(screen.getByText(/MICE/i)).toBeInTheDocument()
     })
     ```

5. **Verify test commands**

   ```bash
   pytest tests
   npm run test
   ```

---

## 🧠 Step 2 — Add Coverage Around Core Features

### 🎯 Goal

Cover “Create → Edit → Delete → Persist” of story cards.

### ✅ Actions

1. **Write backend tests for CRUD routes**

   * Test `POST /cards`, `GET /cards`, `PATCH /cards/{id}`, `DELETE /cards/{id}`
   * Check both HTTP response and database/localStorage persistence.

2. **Write frontend component tests**

   * Test that clicking “Add Card” updates DOM.
   * Mock localStorage so persistence is verified.

3. **Add a simple CI check**

   * Create `.github/workflows/test.yml`

     ```yaml
     name: Run Tests
     on: [push, pull_request]
     jobs:
       test:
         runs-on: ubuntu-latest
         steps:
           - uses: actions/checkout@v3
           - run: npm ci && npm test
     ```

---

## 🔧 Step 3 — Refactor for Code Quality

### 🎯 Goal

Improve readability, consistency, and maintainability without changing behavior.

### ✅ Focus Areas

| Area                 | Action                                                                   |
| -------------------- | ------------------------------------------------------------------------ |
| **Naming**           | Rename vague variables (`x`, `item`) to domain terms (`card`, `section`) |
| **Structure**        | Group related logic into `/components`, `/hooks`, `/utils`, `/api`       |
| **Duplication**      | Extract repeated UI fragments into reusable components (e.g. CardForm)   |
| **State Management** | Replace nested prop drilling with `useContext` or a simple store         |
| **Type Safety**      | Add PropTypes or TypeScript interfaces                                   |
| **Linting**          | Enable ESLint + Prettier; enforce via pre-commit hook                    |

### ✅ Verification

* Run existing tests — they should still pass.
* Use static analysis:

  ```bash
  npm run lint
  pytest --cov=app
  ```

---

## 🐛 Step 4 — Fix Known Bugs

Start with reproducible ones (like the styling bug shown in lecture #1).

### ✅ Workflow

1. Reproduce manually.
2. Capture the error/stack trace.
3. Write a **failing test** that replicates it.
4. Fix the bug.
5. Run the test suite — confirm green.

---

## 🧩 Step 5 — Reflect & Document

At the end of this phase, produce a `requirements-quality.md` that contains:

* **Goal:** Add quality layer to MICE Story Builder.
* **Tools:** pytest, vitest, Playwright (optional).
* **Acceptance Criteria:**

  * [ ] Automated test suite runs successfully
  * [ ] Codebase follows linting rules
  * [ ] All known bugs fixed and verified
  * [ ] CI runs automatically on push

This is the “context file” you’ll feed to AI next time you ask it to add new tests or refactor.

---

## 🔍 Next Step Suggestion (hands-on)

If you’d like, I can generate for you:

1. A **starter test suite** for both backend + frontend (so you can run it and see passing tests right away), or
2. A **`requirements-quality.md` context file** to give the AI before coding.

Which would you like me to create first — the **starter test suite** or the **context file**?
