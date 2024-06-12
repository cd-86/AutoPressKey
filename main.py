import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QComboBox, QVBoxLayout, QCheckBox, QLabel, QGroupBox, \
    QHBoxLayout, \
    QDoubleSpinBox, QPushButton, QGridLayout, QWidget
import pyautogui

from LogView import LogView


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.timerID = -1
        self.keys = []
        self.preTime = 0

        self.setWindowTitle("AutoPressKey")
        self.resize(400, 300)
        self.setCentralWidget(QWidget())
        layout = QVBoxLayout(self.centralWidget())

        self.logView = LogView()

        logAction = self.menuBar().addAction("日志")

        # 视图
        self.resultLabel = QLabel()
        self.resultLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.nextSecondLabel = QLabel()
        viewGroupBox = QGroupBox("视图")
        groupBoxLayout = QGridLayout(viewGroupBox)
        groupBoxLayout.addWidget(QLabel("需要按下的按键："), 0, 0)
        groupBoxLayout.addWidget(self.resultLabel, 0, 1)
        groupBoxLayout.addWidget(QLabel("距离下一次触发的剩余时间 单位 秒："), 1, 0)
        groupBoxLayout.addWidget(self.nextSecondLabel, 1, 1)
        layout.addWidget(viewGroupBox)

        # 按键配置
        self.keyComboBox = QComboBox()
        self.keyComboBox.addItems(
            ["无", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
             "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
             "V", "W", "X", "Y", "Z",
             "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Space"])
        self.keyComboBox.setCurrentText("8")
        self.ctrlCheckBox = QCheckBox("Ctrl")
        self.ctrlCheckBox.setChecked(True)
        self.shiftCheckBox = QCheckBox("Shift")
        self.altCheckBox = QCheckBox("Alt")
        keyGroupBox = QGroupBox("按键设置")
        groupBoxLayout = QVBoxLayout(keyGroupBox)
        groupBoxLayout.addWidget(self.keyComboBox)
        groupBoxLayout.addWidget(self.ctrlCheckBox)
        groupBoxLayout.addWidget(self.shiftCheckBox)
        groupBoxLayout.addWidget(self.altCheckBox)
        layout.addWidget(keyGroupBox)

        # 时间配置
        timeLayout = QHBoxLayout()
        timeLayout.addWidget(QLabel("延时(多久执行一次，单位 秒)："))
        self.timeSpinBox = QDoubleSpinBox()
        self.timeSpinBox.setRange(0.5, 999999999)
        self.timeSpinBox.setValue(600)
        timeLayout.addWidget(self.timeSpinBox)
        layout.addLayout(timeLayout)
        # 开始停止按钮
        self.startStopButton = QPushButton("开始")
        layout.addWidget(self.startStopButton)

        # 信号槽
        logAction.triggered.connect(self.slotLogActionTrigered)

        self.keyComboBox.currentIndexChanged.connect(self.slotUpdateResult)
        self.ctrlCheckBox.checkStateChanged.connect(self.slotUpdateResult)
        self.shiftCheckBox.checkStateChanged.connect(self.slotUpdateResult)
        self.altCheckBox.checkStateChanged.connect(self.slotUpdateResult)

        self.timeSpinBox.valueChanged.connect(lambda x: self.logView.writeLog(f"[修改间隔按键] [{x}]"))

        self.startStopButton.clicked.connect(self.slotStartStopButtonClicked)

        self.slotUpdateResult()

    def timerEvent(self, event):
        t = self.timeSpinBox.value() - (time.time() - self.preTime)
        self.nextSecondLabel.setText(str(max(t, 0)))
        if t < 0:
            if len(self.keys) > 1:
                pyautogui.hotkey(*self.keys)
                self.logView.writeLog(f"[触发按键] [{'+'.join(self.keys)}]")
            elif len(self.keys) == 1:
                pyautogui.press(self.keys[0])
                self.logView.writeLog(f"[触发按键] [{self.keys[0]}]")
            self.preTime = time.time()

    def closeEvent(self, event):
        QApplication.closeAllWindows()

    def slotLogActionTrigered(self):
        if self.logView.isMinimized():
            self.logView.showNormal()
        self.logView.show()
        self.logView.activateWindow()

    def slotUpdateResult(self):
        self.keys = []
        if self.ctrlCheckBox.isChecked():
            self.keys.append("ctrl")
        if self.shiftCheckBox.isChecked():
            self.keys.append("shift")
        if self.altCheckBox.isChecked():
            self.keys.append("alt")
        if self.keyComboBox.currentText() != "无":
            self.keys.append(self.keyComboBox.currentText())
        self.resultLabel.setText("+".join(self.keys))
        self.logView.writeLog(f"[更新按键配置] [{'+'.join(self.keys)}]")

    def slotStartStopButtonClicked(self):
        if self.timerID != -1:
            self.startStopButton.setText("开始")
            self.killTimer(self.timerID)
            self.timerID = -1
            self.logView.writeLog(f"[停止任务]")
        else:
            self.startStopButton.setText("停止")
            self.preTime = time.time()
            self.timerID = self.startTimer(50)
            self.logView.writeLog(f"[启动任务]")


if __name__ == '__main__':
    app = QApplication()
    w = Window()
    w.show()
    app.exec()
