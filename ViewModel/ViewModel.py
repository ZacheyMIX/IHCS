from PyQt6.QtCore import QObject, pyqtSignal, QThread
import time


class ViewModel(QObject):
    formatList = {"name": "object", "age": "int", "date": "date/time", "salary": "int"}
    newFormatList = []
    progress_changed = pyqtSignal(int)
    cleaning_finished = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

    def startFormat(self, file, rules):
        ruleList = rules.split(", ")

    def startClean(self):
        self.thread = QThread()
        self.worker = WorkerThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress_changed.emit)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.worker.finished.connect(self.cleaning_finished.emit)

        self.thread.start()


class WorkerThread(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

    def run(self):
        for i in range(101):
            time.sleep(0.05)  # Simulate cleaning
            self.progress.emit(i)
        self.finished.emit()
