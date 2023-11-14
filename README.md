# rss-reader [![Build Status][build-badge]][action-link] [![Coverage Status][codecov-badge]][codecov-link] [![Maintainability][codeclimate-badge]][codeclimate-link] [![Code Quality][codacy-badge]][codacy-link]

rss-reader provides an API to serve users with RSS feeds.

## Installation

To install, follow these steps:

1.  Create a Python virtual environment using your preferred choice ([pyenv][]
    is recommended)
2.  With the recently created virtual environment activated, install the package
    with the following command:

    ```shell
    make setup
    ```

> _Note: rss-reader requires Python 3.10 or newer._

## Database

rss-reader uses PostgreSQL to store its date. Provide the database connection
URL via the `RSS_READER_DATABASE_URL` environment variable. For instance:

```
export RSS_READER_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/rss_reader"
```

Then proceed to create the tables:

```shell
make create-tables
```

## Running locally

Once the package is installed, run the API with the following:

```shell
make run
```

Or with debug level logging:

```shell
LOG_LEVEL=DEBUG make run
```

The API should be available at http://localhost:8000

## Accessing the API

The API documentation is available at http://localhost:8000/docs and provides
details on how to interact with the API.

## Running tests

1. Run tests with:
    ```shell
    make test
    ```
2. And check code coverage with:
    ```shell
    make coverage
    open htmlcov/index.html
    ```

## Extra

1. To see all available make targets:
    ```shell
    make list
    ```

[pyenv]: https://github.com/pyenv/pyenv

## License

Code in this repository is distributed under the terms of the BSD 3-Clause
License (BSD-3-Clause).

See [LICENSE][] for details.

[build-badge]: https://github.com/scorphus/rss-reader/workflows/Python/badge.svg
[action-link]: https://github.com/scorphus/rss-reader/actions?query=workflow%3APython
[codecov-badge]: https://codecov.io/gh/scorphus/rss-reader/graph/badge.svg?token=MD0pKnNybT
[codecov-link]: https://codecov.io/gh/scorphus/rss-reader
[codeclimate-badge]: https://api.codeclimate.com/v1/badges/cde7b675db4cca078ee1/maintainability
[codeclimate-link]: https://codeclimate.com/github/scorphus/rss-reader/maintainability
[codacy-badge]: https://app.codacy.com/project/badge/Grade/c683c6cc5fa14aecb600c4e37a1285f9
[codacy-link]: https://app.codacy.com/gh/scorphus/rss-reader/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade
[LICENSE]: LICENSE
