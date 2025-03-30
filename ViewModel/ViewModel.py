from PyQt6.QtCore import QThread, pyqtSignal


class ViewModel():
    formatList = {"name": "object", "age": "int", "date": "date/time", "salary": "int"}
    newFormatList = []
    progress = 0

    def __init__(self):
        super().__init__()

    def startFormat(self, file, rules):
        ruleList = rules.split(", ")

    def startClean(self):
        print("stuff")

    def beginProgress(self):
        for i in range(4):
            self.progress += 25


class WorkerThread(QThread):
    def __init__(self, viewModel):
        super().__init__()
        self.threadSignal = pyqtSignal(int)  # Signal to update UI
        self.viewModel = viewModel

    def run(self):
        while self.viewModel.progress < 100:
            self.viewModel.beginProgress()
        self.threadSignal.emit(-1)  # Signal completion
