import os
import re
import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

from PySide6.scripts.pyside_tool import rcc, uic

# Construct the path to the venv's Python interpreter.
if os.name == "nt":  # Windows
    venv_python = os.path.join(sys.prefix, "Scripts", "python.exe")
else:  # Linux / macOS
    venv_python = os.path.join(sys.prefix, "bin", "python")


def _run_command(
    output: Path, input: Path, force: bool = False, args: list[str] | None = None
):

    if input.suffix == ".ui":
        command = "uic"
    elif input.suffix == ".qrc":
        command = "rcc"
    else:
        raise ValueError(f"Unknown file type ({input.suffix})")

    input_mod_time = input.stat().st_mtime_ns
    if output.exists():
        output_mod_time = output.stat().st_mtime_ns
    else:
        output_mod_time = 0

    if not force and input_mod_time <= output_mod_time:
        print(f"Skipping {input}")
        return

    args = args or []
    script_file = str(Path(__file__).resolve())
    args = [venv_python, script_file, command, *args, "-o", str(output), str(input)]

    print(f"Compiling {input} to {output}")
    ret = subprocess.run(args, check=False, capture_output=True)
    if ret.returncode != 0:
        print(f"Failed to compile {input} using the following args: {args[2:]}")
        sys.exit(ret.returncode)


def find_project_root(start_path: Path) -> Path:
    """Walk upwards from the script's location to find pyproject.toml."""
    for parent in [start_path, *start_path.parents]:
        if (parent / "pyproject.toml").is_file():
            return parent
    return Path.cwd()  # Fallback to where the command was run


def get_app_name(project_root: Path, default: str = "app") -> str:
    """Extract the app name from pyproject.toml, replacing dashes with underscores."""
    toml_path = project_root / "pyproject.toml"
    if not toml_path.exists():
        return default

    try:
        # Python 3.11+ built-in TOML parser
        import tomllib

        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
            # Support standard PEP 621 or Poetry formats
            name = data.get("project", {}).get("name") or data.get("tool", {}).get(
                "poetry", {}
            ).get("name")
            if name:
                return name.replace("-", "_")
    except ImportError:
        # Fallback for Python < 3.11
        content = toml_path.read_text(encoding="utf-8")
        match = re.search(r'^name\s*=\s*["\']([^"\']+)["\']', content, re.MULTILINE)
        if match:
            return match.group(1).replace("-", "_")

    return default


def get_app_dir(project_root: Path, app_name: str) -> Path:
    """Find the actual application directory, verifying it is a Python package."""
    dirs_to_search = [
        project_root / app_name,  # e.g., ./my_app
        project_root / "src" / app_name,  # e.g., ./src/my_app (Standard src layout)
        project_root / "app",  # e.g., ./app (Generic fallback)
        project_root / "src" / "app",  # e.g., ./src/app
    ]

    for path in dirs_to_search:
        # Checking for __init__.py is the safest way to verify it's a valid package
        # without triggering side effects from an actual import.
        if path.is_dir() and (path / "__init__.py").is_file():
            return path

        # Python 3.3+ supports namespace packages (no __init__.py), but for
        # a Qt app, you almost always have one. If you use namespace packages,
        # you can remove the __init__ check and just use `path.is_dir()`.

    # Fallback assumption if no package is found
    return project_root / app_name


if __name__ == "__main__":
    script_path = Path(__file__).resolve()
    project_root = find_project_root(script_path)
    app_name = get_app_name(project_root)
    app_dir = get_app_dir(project_root, app_name)

    default_res_dir = app_dir / "resources"
    default_ui_dir = app_dir / "resources" / "ui"
    default_out_dir = app_dir / "compiled"

    main_parser = ArgumentParser(
        prog="compile", description="Compile QT designer and resource files"
    )
    main_parser.add_argument(
        "-r",
        "--resource-input-dir",
        type=Path,
        default=default_res_dir,
        help="Directory that contains all input resource files to be compiled.",
    )
    main_parser.add_argument(
        "-u",
        "--ui-input-dir",
        type=Path,
        default=default_ui_dir,
        help="Directory that contains all input UI files to be compiled.",
    )
    main_parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=default_out_dir,
        help="Direcotry to put all of the compiled files in.",
    )
    main_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force compilation even if output files already exist and are newer than input files.",
    )

    subparsers = main_parser.add_subparsers(dest="command", required=False)
    uic_parser = subparsers.add_parser(
        "uic", help="Compile a single QT designer file (.ui)"
    )
    uic_parser.add_argument("inputs", help="Input file (*.ui), otherwise, stdin")
    uic_parser.add_argument(
        "--from-imports", action="store_true", help="Generate imports relative to '.'"
    )
    uic_parser.add_argument(
        "--rc-prefix",
        action="store_true",
        help="Generate 'rc_file' instead of 'file_rc' import",
    )
    uic_parser.add_argument(
        "-o",
        "--output",
        metavar="file",
        help="Write output to <file> rather than stdout",
    )

    rcc_parser = subparsers.add_parser(
        "rcc", help="Compile a single QT resource file (.qrc)"
    )
    rcc_parser.add_argument("inputs", help="Input files (*.qrc)")
    rcc_parser.add_argument(
        "-o",
        "--output",
        metavar="file",
        help="Write output to <file> rather than stdout",
    )

    args = main_parser.parse_args()
    force = bool(args.force)

    if args.command is None:
        rc_input_dir = Path(args.resource_input_dir)
        ui_input_dir = Path(args.ui_input_dir)
        output_dir = Path(args.output_dir)

        os.makedirs(output_dir, exist_ok=True)
        init_file = output_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()

        if ui_input_dir.exists():
            for input_path in Path(ui_input_dir).glob("*.ui"):
                ui_args = ["--from-imports", "--rc-prefix"]
                output_path = output_dir / f"ui_{input_path.stem}.py"
                _run_command(output_path, input_path, force, ui_args)
        else:
            print(f"Warning: UI directory not found at {ui_input_dir}")

        if rc_input_dir.exists():
            for input_path in Path(rc_input_dir).glob("*.qrc"):
                output_path = output_dir / f"rc_{input_path.stem}.py"
                _run_command(output_path, input_path, force)
        else:
            print(f"Warning: Resource directory not found at {rc_input_dir}")
    elif args.command == "uic":
        del sys.argv[1]
        uic()
    elif args.command == "rcc":
        del sys.argv[1]
        rcc()
