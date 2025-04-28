from PyQt6.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
import time
from backend import data_formatting_pipeline, data_evaluation_pipeline
from backend.mln_files.pipeline import run_mln_pipeline



class ViewModel(QObject):
    cleaningTime = 0
    dirtyDataSet = "/somefilepath/data.csv"
    formatList = {"name": "text", "age": "text", "date": "date/time", "salary": "text", 'address': 'US street address', 'email': 'text'}
    formatPreview = {}
    changedTypes = {"date": {'datatype': 'date_w_year_format', 'minyear': '20', 'maxyear': '22'}, 'email': 'email'}
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
    cleanDatasetPath = ""
    groundTruthFile = ""
    cleanScores = {'dataset': 'cleandata.csv', 'runtime': cleaningTime, 'precision': '.9718', 'recall': '.9955', 'f1-score': '.9834'}
    dirtyScores = {'dataset': 'dirtydata.csv', 'runtime': cleaningTime, 'precision': '.8723', 'recall': '.9435', 'f1-score': '.8398'}
    history = []
    progress_changed = pyqtSignal(int)
    cleaning_finished = pyqtSignal()
    format_start = pyqtSignal()
    eval_finished = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.thread = None
        self.worker = None

    def startClean(self):
        self.thread = QThread()
        self.worker = WorkerThread(self.dirtyDataSet)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.runCleaning)
        self.worker.progress.connect(self.progress_changed.emit)
        self.worker.format_start.connect(self.format_start.emit)
        self.worker.format_ready.connect(self.handle_formatting_ready)
        self.worker.final_data_ready.connect(self.handle_final_data_ready)
        self.worker.cleaningFinished.connect(self.cleaning_finished.emit)

        self.worker.cleaningFinished.connect(self.thread.quit)
        self.worker.cleaningFinished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def handle_formatting_ready(self, types, preview):
        self.formatList = types
        self.formatPreview = preview

    def handle_final_data_ready(self, final_data):
        self.cleanDatasetDict = final_data
        
    def continue_clean(self):
        self.worker.update_types = self.changedTypes
        self.worker.continue_pipeline()

    def startEval(self):
        self.thread = QThread()
        self.worker = WorkerThread()
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.runEvaluation)
        self.worker.evaluationFinished.connect(self.eval_finished.emit)
        self.worker.evaluationFinished.connect(self.thread.quit)
        self.worker.evaluationFinished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()



#Multithread for the backend without freezing the UI
class WorkerThread(QObject):
    progress = pyqtSignal(int)
    format_start = pyqtSignal()
    format_ready = pyqtSignal(list, list)
    final_data_ready = pyqtSignal(list)
    cleaningFinished = pyqtSignal()
    
    scores_read = pyqtSignal(dict)
    evaluationFinished = pyqtSignal()

    def __init__(self, path):
        super().__init__()
        self.path = path
        self.update_types = None
        self.formatter = None

    

    def runCleaning(self):
        self.formatter = data_formatting_pipeline
        self.progress.emit(10)
        types, preview_data = self.formatter.main(self.path)
        self.progress.emit(30)
        self.format_ready.emit(types, preview_data)

        self._wait_for_continue()
        

    def _wait_for_continue(self):
        self.paused = True
        self.format_start.emit()
        while self.paused:
            time.sleep(.1)
        
        self.finish_cleaning()

    #Called by viewmodel when user updates formated types
    def continue_pipeline(self):
        self.paused = False

    def finish_cleaning(self):
        
        self.progress.emit(30)
        #Sends new updated types to Novella
        self.formatter.main_cont(self.update_types)
        self.progress.emit(30)

        #Starts Graces pipeline
        final_data = run_mln_pipeline.run()
        self.final_data_ready.emit(final_data)
        self.progress.emit(30)

        #Call when finished
        self.cleaningFinished.emit()

    def runEvaluation(self):
        self.evaluationFinished.emit()
