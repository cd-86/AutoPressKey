import datetime

from PySide6.QtWidgets import QWidget, QPlainTextEdit, QVBoxLayout, QPushButton


class LogView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("执行日志")
        self.resize(600, 400)
        layout = QVBoxLayout(self)

        self.plainTextEdit = QPlainTextEdit()
        self.clearButton = QPushButton("清除日志")
        layout.addWidget(self.plainTextEdit)
        layout.addWidget(self.clearButton)

        self.clearButton.clicked.connect(self.plainTextEdit.clear)

    def writeLog(self, s: str):
        tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"[:-3])
        self.plainTextEdit.appendPlainText(f"[{tm}] {s}")
