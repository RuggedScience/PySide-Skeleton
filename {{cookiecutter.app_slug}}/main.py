import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from PySide6.QtCore import QStandardPaths

from {{ cookiecutter.module_name }} import APP_NAME, run

if hasattr(sys, "frozen"):
    exe = sys.executable
else:
    exe = sys.argv[0]

dir = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation)
os.makedirs(dir, exist_ok=True)
log_file = os.path.join(dir, f"{APP_NAME}.log")

handler = RotatingFileHandler(log_file, maxBytes=100_000_000, backupCount=2)
logging.basicConfig(level=logging.WARNING, handlers=[handler])

run()
