# Contributing to SuperTokens

Contributions are always welcome. Before contributing please read the [code of conduct](https://github.com/supertokens/supertokens-django-ref-jwt/blob/master/CODE_OF_CONDUCT.md) & search [the issue tracker](https://github.com/supertokens/supertokens-django-ref-jwt/issues); your issue may have already been discussed or fixed in master. To contribute, fork SuperTokens, commit your changes, & send a pull request.

# Questions
We are most accessible via team@supertokens.io, via the GitHub issues feature and our [Discord server](https://supertokens.io/discord). 

## Pull Requests
Before issuing a pull request, please make sure:
- Code is formatted properly - we have a pre-commit hook to enforce this
- All tests are passing. We will also be running tests when you issue a pull request.

Please only issue pull requests to the dev branch.


## Prerequisites

1) You will need Python(version >= 3.7) and Django(version >= 2.2) on your local system to run and test the repo.

2) Install additional development dependencies
    ```bash
    make dev-install
    ```

3) Set-up hooks
    ```bash
    make set-up-hooks
    ```

## Coding standards
In addition to the following guidelines, please follow the conventions already established in the code.

- **Naming**
    - Use snake case for all variable names: ```a_variable```
    - Use snake case for sql table names and column names: ```new_sql_table```
    - Use snake case name for new files: ```hello_world.py```
    - For classes, use pascal case: ```MyClass```
    - For constants, use all caps version of snake case: ```A_CONSTANT```

- **Comments**
    - Please refrain from commenting very obvious code. But for anything else, please do add comments.
    - For every function, please write what it returns, if it raises an exception (and what type), as well as what the params mean (if they are not obvious).

- **Exception handling**
    - All Exceptions must be extended from SuperTokensException.

All other issues like quote styles, spacing etc.. will be taken care of by the formatter.


## Pre committing checks

1) Run the make lint command
    ```bash
    make lint
    make check-lint
    ```

## Pre push

Run unit tests and make sure all tests are passing.
```bash
make test
```