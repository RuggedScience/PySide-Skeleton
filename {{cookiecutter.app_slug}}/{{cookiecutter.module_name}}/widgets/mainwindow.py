from PySide6.QtCore import QSettings
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMainWindow

from ..utils.assets import get_icon


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        window_title = f"{QApplication.applicationDisplayName()} - {QApplication.applicationVersion()}"
        self.setWindowTitle(window_title)

        window_icon = get_icon("icon.png")
        self.setWindowIcon(window_icon)

        self._load_settings()

    def _load_settings(self) -> None:
        settings = QSettings()
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("state"))

    def _save_settings(self) -> None:
        settings = QSettings()
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("state", self.saveState())

    def closeEvent(self, event: QCloseEvent) -> None:
        self._save_settings()
        return super().closeEvent(event)
