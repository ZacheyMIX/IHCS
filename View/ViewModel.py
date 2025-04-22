from PyQt6.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
import time


class ViewModel(QObject):
    dirtyDataSet = ""
    formatList = {"name": "text", "age": "text", "date": "date/time", "salary": "text", 'address': 'US street address'}
    changedTypes = {}
    progress_changed = pyqtSignal(int)
    cleaning_finished = pyqtSignal()
    format_start = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

    def startClean(self):
        self.thread = QThread()
        self.worker = WorkerThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress_changed.emit)
        self.worker.formatAwait.connect(self.format_start.emit)
        self.worker.cleaningFinished.connect(self.cleaning_finished.emit)

        self.worker.cleaningFinished.connect(self.thread.quit)
        self.worker.cleaningFinished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
    
    def continueClean(self):
        self.worker.continue_work()



#Multithread for the backend without freezing the UI
class WorkerThread(QObject):
    progress = pyqtSignal(int)
    formatAwait = pyqtSignal()
    cleaningFinished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._paused = False

    def run(self):
        for i in range(101):
            time.sleep(0.05)  # Simulate cleaning
            self.progress.emit(i)

            if i == 50:
                self._paused = True
                self.formatAwait.emit()

                while self._paused:
                    time.sleep(.1)

        self.cleaningFinished.emit()

    @pyqtSlot()
    def continue_work(self):
        self._paused = False
