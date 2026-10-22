import importlib.resources as pkg_resources
from pathlib import Path

from PySide6.QtGui import QIcon, QPixmap


def get_asset_path(subfolder: str, filename: str) -> Path:
    """
    Returns the absolute Path to an asset within the package.
    """

    package_path = pkg_resources.files("{{ cookiecutter.module_name }}.resources")
    file_path = package_path.joinpath(f"{subfolder}/{filename}")

    # The Fail-Fast Check
    if not file_path.is_file():
        raise FileNotFoundError(
            f"Asset not found! The UI requested '{filename}' "
            f"but it does not exist at: {file_path}"
        )

    return Path(str(file_path))


def get_pixmap(filename: str, folder="images") -> QPixmap:
    """Returns a QPixmap for use in standard UI labels or Graphics Scenes."""
    path = get_asset_path(folder, filename)
    return QPixmap(str(path))


def get_icon(filename: str, folder="icons") -> QIcon:
    """Returns a QIcon for use in buttons, window titles, or system trays."""
    path = get_asset_path(folder, filename)
    return QIcon(str(path))
