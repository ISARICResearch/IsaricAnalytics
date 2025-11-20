# How to contribute

We welcome all contributions to IsaricAnalytics, including:

- Reporting a bug
- Proposing new features
- Submitting new code

## Submit an Issue

To report bugs or propose new features, please
[submit an issue](https://github.com/IsaricResearch/IsaricAnalytics/issues)
on GitHub.

- Reporting a bug
- Proposing a new feature

Please be as detailed as possible, and include where possible:

- A short summary of the issue
- Steps to reproduce a bug
- What you expected would happen
- What actually happens
- Notes
    - Why you think this might be happening
    - Stuff you have tried that did not work

## Submit a Pull Request

You can contribute code to the project through pull requests. To submit a pull
request, you need to

- [Fork the rapids repository]
- Clone it to your local machine
- Implement your code and test it
- Push it to your GitHub repository
- [Create a pull request] in rapids repository

If you are contributing a new method within one of the modules, please include at least
one unit test. If you are contributing a new analysis pipeline, please include an
integration test. Please run the pre-commit hook before making your pull request.

[Fork the rapids repository]: https://github.com/IsaricResearch/IsaricAnalytics/fork

[Create a pull request]: https://github.com/IsaricResearch/IsaricAnalytics/pulls

If possible, try to create a pull request from a forked repository that is up-to-date
with the latest version of the rapids repository, and to include enough detail in the
pull request about the proposed new feature. You can create an issue in the rapids
repository first if you want to discuss the feature before submitting the pull request.

Please run the pre-commit hook before submitting the pull request. This will ensure
consistency with our coding style.

## Coding Style

We follow the [PEP8 style](https://peps.python.org/pep-0008/) for code. The line length
is set to 88 characters. We follow
the [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
for docstrings. We use [ruff](https://docs.astral.sh/ruff) as a linter.

Install [pre-commit](https://pre-commit.com) and setup pre-commit hooks
(`pre-commit install`) which will do linting checks before commit.

## Core development

### Branches

We aim to follow best practice for managing and releasing the code, including
`main`, `dev`, feature and hotfix branches. We will update this with more information
in due course.

### Pull Requests

All code changes happen through pull requests.

1. Create a new branch from `dev` (for feature) or `main` (for hotfix)
2. Make the changes
3. Write documentation for the changes
4. Write unit tests for the changes
5. Create a pull request to `dev` (for feature) or `main` branch (for hotfix)
6. Wait for the review and merge

### Code Review

We enforce code reviews as follows:

- `main` and `dev`: require one approvals from the core developers
