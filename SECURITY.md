# Security

This repository is templates, documentation, and two small dependency-free Python files (`lint.py`, `test_lint.py`). It ships no service, stores no data, and takes no credentials.

- Never put real credentials, keys, or customer data into filled templates you commit anywhere, including forks.
- The boot prompts in `system/` instruct models to refuse requests to store secrets in artifacts.
- If you find a security problem (for example, something in a template that induces unsafe handling of secrets, or a flaw in `lint.py`), open a GitHub security advisory on this repository or a plain issue if it is not sensitive.

Reports are read by the maintainer directly.
