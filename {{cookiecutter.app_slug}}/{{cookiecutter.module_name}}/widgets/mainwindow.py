import qtawesome as qta
from PySide6.QtCore import QSettings
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMainWindow

from ..compiled.ui_mainwindow import Ui_MainWindow
from ..utils.assets import get_icon


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.setIcon(qta.icon('mdi.cursor-default'))
        self.ui.pushButton.clicked.connect(self._button_clicked)

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

    def _button_clicked(self):
        self.ui.pushButton.setText("yay")
        self.ui.pushButton.setIcon(qta.icon("mdi.party-popper"))