# Copilot / Assistant Instructions

Purpose
- Provide clear, concise guidance for an AI assistant (Copilot/GitHub Copilot) when working on this repository.

When editing files
- Make minimal, focused changes that fix the issue at the root cause.
- Preserve the repository style and existing public APIs unless a change is requested.
- Use the project's virtual environment for commands and testing: `source .venv/bin/activate`.

Testing
- Run tests after changes: `python -m pytest -v`.
- If you modify tests or page objects, ensure all affected tests pass locally.

Coding style
- Follow existing naming and file layout conventions.
- Avoid adding unrelated refactors.

Commit / PR guidance
- Keep commits small and descriptive.
- Include tests for new behavior.

Files of interest
- `page_objects/` — page object classes (HomePage, LoginPage, RegisterPage, CheckoutPage).
- `tests/` — pytest test modules.
- `requirements.txt` — Python dependencies.

If uncertain
- Ask the repository owner for clarification before making large or invasive changes.

Shortcuts
- To run a single test: `python -m pytest tests/test_example.py::test_juice_shop_title -v`
- To run Playwright browsers: `playwright install`

Thank you — be precise and conservative with changes.
