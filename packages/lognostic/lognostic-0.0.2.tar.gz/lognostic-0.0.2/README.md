# lognostic

[![PyPI](https://img.shields.io/pypi/v/lognostic?style=flat-square)](https://pypi.python.org/pypi/lognostic/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lognostic?style=flat-square)](https://pypi.python.org/pypi/lognostic/)
[![PyPI - License](https://img.shields.io/pypi/l/lognostic?style=flat-square)](https://pypi.python.org/pypi/lognostic/)


---

**Documentation**: [https://Mamdasn.github.io/lognostic](https://Mamdasn.github.io/lognostic)

**Source Code**: [https://github.com/Mamdasn/lognostic](https://github.com/Mamdasn/lognostic)

**PyPI**: [https://pypi.org/project/lognostic/](https://pypi.org/project/lognostic/)

---

lognostic is a lightweight, efficient Python package designed to seamlessly integrate into existing Python applications to provide comprehensive logging statistics. ThiThis package caters to development teams seeking to optimize logging performance, diagnose issues, and understand logging loads without introducing significant overhead or complexity into their applications.

## Installation

```sh
pip install lognostic
```

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.9+
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Custom logging Handler

The `lognostic` module can be integrated into logging subsystems by employing a custom logging handler:

```python
import logging
from lognostic import Lognostic


class LogHandler(logging.Handler):
    def __init__(self, lognostic: Lognostic):
        super().__init__()
        self._lognostic = lognostic

    def emit(self, log_record: logging.LogRecord):
        self._lognostic.record(log_record)
```


### Testing

```sh
pytest tests
```
### Docker Usage

Build the image of the Dockerfile using
```sh
docker build -t lognostic .
```
Run the image with
```sh
docker run --name lognostic_instance lognostic
```

The docker builds the envioronment followed by running the pre-commits and unit tests.
### Documentation

The documentation is automatically generated from the content of the [docs directory](./docs) and from the docstrings of the public signatures of the source code.

### Releasing

Trigger the [Draft release workflow](https://github.com/Mamdasn/lognostic/actions/workflows/draft_release.yml) (press _Run workflow_). This will update the changelog & version and create a GitHub release which is in _Draft_ state.

Find the draft release from the [GitHub releases](https://github.com/Mamdasn/lognostic/releases) and publish it. When a release is published, it'll trigger [release](https://github.com/Mamdasn/lognostic/blob/master/.github/workflows/release.yml) workflow which creates PyPI release and deploys updated documentation.

### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

## Future features and improvements
+ Data persistency: Store statistics on the disk persistency for future historical logging analysis.
+ Logging Dashboard: A web dashboard to visualize logging statistics in real-time, allowing teams to monitor logging load dynamically.
+ Throw warning/error messages if certain logging thresholds are met, such as an unusually high logging rate, to quickly identify potential issues.
---

This project was generated using the [python-package-cookiecutter](https://github.com/Mamdasn/python-package-cookiecutter) template.
