.. _contributing:

Contributing
============

Contributors and contributions are welcome.

Contributions to this repository include all (`Git <https://git-scm.com/>`_) version-controlled changes made to one or more files (including documentation files) in the repository, specifically, in the default (``main``) branch of the repository, as well as `issues <https://github.com/ISARICResearch/IsaricAnalytics/issues>`_, which count as informal contributions that are external to version control.

Changes should be submitted in the form of a `pull request <https://docs.github.com/en/pull-requests/reference/pull-requests>`_ (PR), which is then reviewed and approved by a repository member with the appropriate level of permission, after which the pull request is merged into the repository and the changes incorporated.

.. _preliminaries:

Preliminaries
-------------

Before submitting pull requests contributors must first:

- Have a copy of the repository as a `clone <https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository>`_ or `fork <https://docs.github.com/en/pull-requests/how-tos/work-with-forks/fork-a-repo>`_.
- If working with a clone, check they have the right level of access to the repository, which is usually as an external collaborator with the ability to read from and write to the repository. Access is typically granted by repository maintainers, who are `listed <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/README.md#maintainers>`_ in the README.
- Install all the `development dependencies <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/pyproject.toml#L65>`_ of the project in the development environment using an appropriate tool such as `pip <https://pip.pypa.io/en/stable/installation/>`_ or `Astral uv <https://docs.astral.sh/uv/>`_ (recommended). The development dependencies are specified as groups of optional dependencies in the project TOML, each group listing the (third-party) dependencies specific to some aspect of project development, such as pre-commit hooks, testing, or documentation. Any optional dependency group can be installed by name, for example, test dependencies with :program:`pip` using:

.. code:: shell

   pip install -e . [test]

or, for example, documentation dependencies with :program:`uv`:

.. code:: shell

   uv sync --verbose --group docs

Note that in both examples above package-specific dependencies will also be installed, as development / optional dependency groups are not typically used in isolation but complement development. Also note that in the :program:`uv` example above the project will be installed as a package (:program:`isaricanalytics`) in the development environment - if this is not wanted then add the ``--no-install-project`` flag.

The basic PR-based contributions workflow is described below in very general terms, omitting specifics of any particular tools such as Git, command line shells, IDEs etc. Some familiarity with Git and GitHub is assumed and also useful. As this is independent of the contributions workflow the relevant and appropriate documentation or external learning resources can be consulted.

.. _pr-workflow:

Basic PR Workflow
-----------------

#. Create a new branch in your local repository for development - usually this will be created from the latest copy of the ``main`` branch of the `ISARICResearch/ISARICAnalytics <https://github.com/ISARICResearch/IsaricAnalytics>`_  repository or your fork (of that repository).
#. Push the branch upstream to the GitHub repository (called the **remote**, and usually named ``origin`` in Git), which will either be `ISARICResearch/ISARICAnalytics <https://github.com/ISARICResearch/IsaricAnalytics>`_ or your fork, then `create a PR <https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request>`_ from the upstream branch targeting the ``main`` branch of `ISARICResearch/ISARICAnalytics <https://github.com/ISARICResearch/IsaricAnalytics>`_, and **also mark the PR as a** `draft <https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/changing-the-stage-of-a-pull-request#converting-a-pull-request-to-a-draft>`_ to indicate that it is **under development** (or work in progress).
#. Make your changes in the PR. Once you're satisfied with the changes, **mark the PR as** `ready for review <https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/changing-the-stage-of-a-pull-request#marking-a-pull-request-as-ready-for-review>`_, and then `request a review <https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/requesting-a-pull-request-review>`_ from a repository member - one reviewer is sufficient and necessary, and all PRs require a minimum of one approval.
#. If the PR is approved, merge it yourself if you have the necessary permissions, or, alternatively, request a merge from either the reviewer(s) or another repository member who can merge it.
#. If there are questions or requested changes from the reviewer these must be addressed - this may require further changes to be staged and committed on the local branch in the usual way, before updating the upstream branch (which automatically updates the PR); it may also require PR discussions to be resolved. Request another review and approval if required, and merge the PR as described above.

.. note::

   A **draft PR cannot be merged**, which is why it is advisable to mark the PR as a draft while it is still in development. Draft status should be removed only when the PR is ready to be reviewed, as described above. The only possible exception to marking a PR as draft is if the changes are very simple and/or minimal, and are contained in 1-2 commits.

.. _pr-status-checks:

PR Status Checks
~~~~~~~~~~~~~~~~

Contributors should familiarise themselves with a number of automated `status checks <https://docs.github.com/en/pull-requests/reference/status-checks>`_ (running as GitHub Actions workflows) that are automatically triggered whenever a PR is updated. These are:

- `Pre-commit checks <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/.github/workflows/pre-commit.yml>`_ - mainly code linting.
- `Package builds <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/.github/workflows/build.yml>`_ - package artifact builds (source distribution, Python wheel) and a package import test from the wheel.
- `Unit tests with code coverage checks <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/.github/workflows/test.yml>`_ - running unit tests, and measuring and uploading a code coverage report (to `Codecov.io <Codecov.io>`_).
- `PR patch code coverage checks <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/codecov.yml>`_ - called `patch status <https://docs.codecov.com/docs/commit-status#patch-status>`_, this measures code coverage of the source lines modified in the PR, and is another status check involving `Codecov.io <Codecov.io>`_.
- `CodeQL <https://securitylab.github.com/codeql-wall-of-fame/>`_ code scanning and quality checks.
- PR-specific Read the Docs (RTD) `documentation builds <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/.readthedocs.yaml>`_ - see `this <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/CONTRIBUTING.md#documentation-prs>`_ for further information.

.. _pr-management:

Managing the PR
~~~~~~~~~~~~~~~

Any PR problems such as status check errors, `merge conflicts <https://docs.github.com/en/pull-requests/reference/merge-conflicts>`_, or other anomalies, should be investigated and resolved.

Status check errors can be investigated by inspecting the `GitHub Actions workflow logs <https://github.com/ISARICResearch/IsaricAnalytics/actions>`_ for the relevant workflow.

Merge conflicts can be `resolved locally on the command line <https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-using-the-command-line>`_, but this is best done **only if you're familiar with Git**, otherwise please ask a `maintainer <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/README.md#maintainers>`_. Merge conflicts can also be `resolved on GitHub <https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requestsresolving-a-merge-conflict-on-github>`_. Resolving a merge conflict will always create a new merge commit in the PR branch.

An example screenshot from a PR with all checks passing is given below.

|PR Checks|

Another point to note is that if the PR's target (or base) branch, usually ``main``, is updated (by other PRs or direct commits) while the PR is still in development or review (and is therefore unmerged), you should see a warning on the PR status checks box that it is `out of date and should be updated <https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/keeping-your-pull-request-in-sync-with-the-base-branch>`_. This may sometimes lead to merge conflicts, which must be resolved as described above, before proceeding with further PR changes.

.. _pr-rules:

PR Rules
~~~~~~~~

Contributors should note two basic rules that are in place and apply to all PRs. These are:

- A PR approval is dismissed if it is updated with new commits pushed after that approval - this is to ensure that all current changes are subject to review prior to any approval. For this reason contributors should, if possible, request a review once they're satisfied that all changes are complete. But if an approval is dismissed contributors should always request a new review, because only an approved PR can be merged (subject to the second rule).
- An approved PR cannot be merged until all PR discussions/conversations are `resolved <https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/commenting-on-a-pull-request#resolving-conversations>`_ - this is to ensure that any lingering questions or issues raised in a discussion have been addressed before merging the PR.

These rules can only be bypassed by an `ISARICResearch GitHub organisation <https://github.com/ISARICResearch>`_ owner or repository administrator. Please contact a `maintainer <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/README.md#maintainers>`_ for further information.

Documentation-related PRs
-------------------------

Contributors submitting PRs that include changes in the `documentation files <https://github.com/ISARICResearch/IsaricAnalytics/tree/main/docs>`_ - should familiarise themselves with the documentation tools (mainly, `Sphinx <https://www.sphinx-doc.org/en/master/index.html>`_), platforms (`Read the Docs <https://about.readthedocs.com>`_) and documentation-specific dependencies, used.

The basic PR workflow is the same as described above, but there are some important points to note:

- The development environment should contain, in addition to the `package-specific dependencies <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/pyproject.toml#L54>`_, all the documentation-specific dependencies, as listed in the `project TOML <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/pyproject.toml#L75>`_, in order to support local building and viewing of the complete documentation site. For dependency management it is recommended to use a modern, fast and accurate package / dependency manager such as `Astral UV <https://docs.astral.sh/uv/>`_. In particular, the UV `sync <https://docs.astral.sh/uv/concepts/projects/sync/>`_ command is very useful in keeping dependencies in the environment synchronised with the project dependencies.
- To build the complete documentation site locally run the Sphinx command below from the root of the repository, after which the site will be accessible from ``docs/_build/html/index.html``:

::

   make -C docs html

- Provided the PR branch has been activated for RTD PR builds - ask a `maintainer <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/README.md#maintainers>`_ if this is not the case - each PR commit triggers a complete RTD build of the documentation site that is available from:

::

   https://isaricanalytics--n.org.readthedocs.build/en/n/

where ``n`` should be **replaced** by the number of the PR as found in the PR URL. The build usually takes some time (1-2 minutes) before the site is updated.

Issues
------

As mentioned in the introduction to this page, `creating GitHub issues <https://github.com/ISARICResearch/IsaricAnalytics/issues>`_ also counts as contributing, but is external to version control.

Issues can be used to define and discuss features, bugs and other relevant improvements or changes. They can also be linked to PRs. For more information see the `GitHub documentation <https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/quickstart>`_.

Issues have settings such as assignees, colour-coded tags/labels, type, priority and effort, project etc. and can be linked to PRs. These appear on the right hand side of the issue page, and it is recommended to apply as many of the relevant settings, especially the setting to link an issue to a relevant PR where possible. Refer to the screenshot below of an actual current issue in this repository.

|Issues|

Code Hygiene
------------

Code hygiene is an informal notion of good code quality and of ways of achieving this through standardised development practices, standards and tools. It is useful to keep some basic principles in mind:

- Code should be **readable** in the sense of being (relatively) easy to follow and understand by others.

- Code formatting and styling, including naming conventions, should be **consistent**, as this not only contributes to readability but makes it easier to identify inconsistencies.

- Code should be **concise** in the sense of being simple enough to achieve the task at hand, and not too verbose or overcomplicated.

- Code should be **tested** where possible - if this isn't possible then a follow-up task should be created to add tests.

Contributors are recommended to consider using the following practices:

- Ensure that **pre-commit hooks** are integrated into your development environment so that they are triggered by local commits in the repository. This requires the Python `pre-commit dependency <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/pyproject.toml#L66>`_ to be installed. The hooks specific to this repository, which include `Ruff <https://astral.sh/ruff>`_ code **linting**, are defined `here <https://github.com/ISARICResearch/IsaricAnalytics/blob/main/.pre-commit-config.yaml>`_, and can also be triggered manually by running:

.. code:: shell

   pre-commit run --all-files

- Use **docstrings** and **type hints** for all public functions and public class methods in public modules, excluding private (non-public) functions and methods in public modules, and private modules entirely. The recommended docstring style is the `Numpy style <https://numpydoc.readthedocs.io/en/latest/format.html>`__, which uses `reStructuredText <http://docutils.sourceforge.net/rst.html>`__ syntax and is rendered (in HTML) with `Sphinx <https://www.sphinx-doc.org/>`__. Function and method docstrings should contain, at minimum, the following details: a top-level **concise description**, **parameters** (arguments) if present, **return values** if present, **exceptions** if present, in that order. `Example snippets <https://numpydoc.readthedocs.io/en/latest/format.html#examples>`__ that can be used for `doctests <https://docs.python.org/3/library/doctest.html>`__ are optional, but should be added if examples are available and easy to reproduce. Any warnings or notes can also be added using the appropriate `reStructuredText directives <https://docutils.sourceforge.io/docs/ref/rst/directives.html>`__. Docstrings should be kept up-to-date with changes in the source code. Refer to the `package libraries <https://github.com/ISARICResearch/IsaricAnalytics/tree/main/isaricanalytics>`__ in this repository, where all public functions and class methods have Numpy docstrings.

- Where code is lengthy, complex or not self-explanatory, organise the code into logically related **blocks** and prefix each block with a concise explanatory **comment**. This can really help in making the code readable and comprehensible.

- In public modules, **list all public members** lexicographically in the special `__all__ <https://docs.python.org/3/reference/simple_stmts.html#module.__all__>`_ member. The list should be kept up-to-date with changes in module members. This is already done in all the existing package libraries, so if you're modifying any of their members ensure that the ``__all__`` list is updated appropriately.

- **Order module members** in some meaningful way, for example, lexicographically. In an unordered module with many members, say, upwards of 20, it is harder to locate members. If you're adding or modifying members in an existing module ensure that the existing member order is respected. Module member ordering is not currently being applied in the package libraries, but this could easily be done.

- If you're working on a **reusable** function, class method or, generally, some callable, use an **appropriate level of generality**, i.e. a level that is not too general or too specific to the task. There is **no absolute level of generality**, and finding the right level requires a subjective judgment about what is appropriate to the level or scope of reusability. It may be useful to refer to the `SOLID principles <https://en.wikipedia.org/wiki/SOLID>`_ for general guidance, particularly, the `single responsibility principle <https://en.wikipedia.org/wiki/Single-responsibility_principle>`_ as applied to functions and methods, which says that each function or method should do one and only one thing. This recommendation does not apply to code that is task- or problem-specific where reuse isn't possible.

- **Locate new code appropriately**. So, new functions, class methods, or callables (such as classes) should be added to an existing module or library if the new functionality is logically related to that module. Otherwise, a new module, or even a new subpackage, may be more appropriate.

- Where possible, **minimise changes to dependencies**, especially, package-specific (third-party) dependencies, and instead look to re-use the existing set of dependencies and/or the standard libraries. A good rule to follow is to only add a dependency if it is necessary for the implementation of whatever changes are being developed. Every additional dependency introduces its own dependencies, each of which introduces its own dependencies (called transitive dependencies), and this not only increases the complexity of maintaining the enlarged set of dependencies (in reality, a dependency tree) but may introduce new pathways for vulnerabilities and dependency-related errors to enter the project.

.. |PR Checks| image:: ../_static/github-pr-checks.png
.. |Issues| image:: ../_static/github-issues.png
