from PyQt6.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
import time


class ViewModel(QObject):
    cleaningTime = 0
    dirtyDataSet = "/somefilepath/data.csv"
    formatList = {"name": "text", "age": "text", "date": "date/time", "salary": "text", 'address': 'US street address', 'email': 'text'}
    changedTypes = {"date": {'datatype': 'date w year format', 'minyear': '20', 'maxyear': '22'}, 'email': 'email'}
    cleanDatasetDict = [{
            "TID": "001",
            "HospitalName": "General Hospital",
            "Address": "123 Main St",
            "City": "Metropolis",
            "State": "NY",
            "Zipcode": "10001",
            "Phonenumber": "555-1234",
            "Patient": "John Smith",
            "Reason": "Cough",
            "changes": "Address corrected"
        },
        {
            "TID": "002",
            "HospitalName": "City Clinic",
            "Address": "456 Elm St",
            "City": "Gotham",
            "State": "NJ",
            "Zipcode": "07001",
            "Phonenumber": "555-5678",
            "Patient": "Joker",
            "Reason": "Broken Everything",
            "changes": None
        }]
    groundTruthFile = ""
    cleanScores = {'dataset': 'cleandata.csv', 'runtime': cleaningTime, 'precision': '.9718', 'Recall': '.9955', 'F1-score': '.9834'}
    dirtyScores = {'dataset': 'dirtydata.csv', 'runtime': cleaningTime, 'precision': '.8723', 'Recall': '.9435', 'F1-score': '.8398'}
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
