# PySide Skeleton

A [cookiecutter](https://cookiecutter.readthedocs.io/) template for PySide6 desktop applications. Generated projects use [uv](https://docs.astral.sh/uv/) for dependencies, [setuptools-scm](https://setuptools-scm.readthedocs.io/) for versioning, and [cx_Freeze](https://cx-freeze.readthedocs.io/) to build executables and MSI installers.

## Requirements

- Python 3.12+
- uv
- git
- cookiecutter

## Creating a Project

```
uvx cookiecutter gh:RuggedScience/PySide-Skeleton
```

You will be prompted for the following values:

| Variable       | Description                                              |
| -------------- | -------------------------------------------------------- |
| `app_name`     | Display name of the application.                         |
| `app_slug`     | Project folder and package name. Derived from `app_name`. |
| `module_name`  | Python package name. Defaults to `app_slug`.             |
| `organization` | Organization name used by Qt settings and the Start Menu folder. |
| `domain`       | Organization domain used by Qt settings.                 |
| `description`  | Short project description.                               |
| `author_name`  | Optional. Author name for `pyproject.toml`.              |
| `author_email` | Optional. Author email for `pyproject.toml`.             |

A unique MSI upgrade code is generated automatically. After generation, a git repository is initialized with an initial commit so setuptools-scm can determine the version.

## Using the Generated Project

Install dependencies:

```
uv sync
```

Run the application:

```
uv run main.py
```

Compile Qt Designer (`.ui`) and resource (`.qrc`) files:

```
uv run scripts/compile.py
```

By default this reads `.ui` files from `<module>/resources/ui`, `.qrc` files from `<module>/resources`, and writes output to `<module>/compiled`. Files are only recompiled when the source has changed; pass `-f` to force.

Build an executable:

```
uv run cxfreeze build_exe
```

Build an MSI installer:

```
uv run cxfreeze bdist_msi
```

The same commands are available as VS Code tasks in `.vscode/tasks.json`.

## Versioning

The version comes from git tags via setuptools-scm. Tag a release before building:

```
git tag v1.0.0
```

## Project Layout

```
<app_slug>/
├── main.py                 Entry point and logging setup
├── pyproject.toml          Project metadata and cx_Freeze configuration
├── scripts/compile.py      Compiles .ui and .qrc files
└── <module_name>/
    ├── __init__.py         App metadata and startup
    ├── resources/icons/    Application icons
    ├── utils/
    └── widgets/mainwindow.py
```

Logs are written to the platform's app data directory (`QStandardPaths.AppDataLocation`).
