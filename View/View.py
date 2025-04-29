import os.path

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPixmap
import re
import sys
import os
from PyQt6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit, QMainWindow,
                             QProgressBar, QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout,
                             QStackedLayout, QGridLayout, QWidget, QListWidget, QListWidgetItem,
                             QScrollArea, QComboBox, QFrame
                             )
import shutil
from ViewModel import ViewModel
from View import StyleSheets
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json


class MainWindow(QMainWindow):
    currentSelectedPage = 0
    formatting = False
    ss = StyleSheets
    current_dir = os.path.dirname(__file__)
    mln_folder = os.path.join(current_dir, '..', 'backend', 'mln_files', 'mln')
    mln_folder = os.path.abspath(mln_folder)
    mln_folder = mln_folder + "/user_uploaded_rules.mln"


    def __init__(self):
        super().__init__()
        self.cleaningThread = None
        self.setWindowTitle("IHCS")
        self.setFixedSize(800, 500)
        self.viewModel = ViewModel.ViewModel()

        self.viewModel.format_start.connect(self.format_start)
        self.viewModel.progress_changed.connect(self.update_progress)
        self.viewModel.cleaning_finished.connect(self.cleaning_finished)
        self.viewModel.eval_finished.connect(self.evaluate_finished)

        # Main layouts displayed at all times
        self.mainLayout = QHBoxLayout()
        self.tabLayout = QGridLayout()
        self.pageLayout = QStackedLayout()

        #Layout setup
        self.tabLayouts()
        self.pageLayouts()
        self.aboutLayout()
        self.helpLayout()
        self.acknowlegementLayout()
        self.paramLayout()
        self.formatLayout()
        self.cleanLayout()
        self.resultLayout()
        self.evalLayout()
        self.chartLayout()

        self.mainLayout.addLayout(self.tabLayout, 1)
        self.mainLayout.addLayout(self.pageLayout, 4)

        widget = QWidget()
        widget.setLayout(self.mainLayout)

        self.setCentralWidget(widget)

    #Static tab UI
    def tabLayouts(self):

        #UI
        titleText = QLabel("IHCS")
        self.font = titleText.font()
        self.font.setPointSize(30)
        titleText.setFont(self.font)
        titleText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        introLabel = QLabel()
        introLabel.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'intro.png')))

        self.aboutPageButton = QPushButton("About")
        self.aboutPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        self.aboutPageButton.setFixedHeight(30)
        self.aboutPageButton.clicked.connect(lambda: self.movetopage(0))

        self.helpPageButton = QPushButton("Help")
        self.helpPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.helpPageButton.setFixedHeight(30)
        self.helpPageButton.clicked.connect(lambda: self.movetopage(1))

        self.acknowledgementPageButton = QPushButton("Acknowledgements")
        self.acknowledgementPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.acknowledgementPageButton.setFixedHeight(30)
        self.acknowledgementPageButton.clicked.connect(lambda: self.movetopage(2))

        settingsLabel = QLabel()
        settingsLabel.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'settings.png')))

        self.paramPageButton = QPushButton("Parameter Setting")
        self.paramPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.paramPageButton.setFixedHeight(30)
        self.paramPageButton.clicked.connect(lambda: self.movetopage(3))

        cleaningLabel = QLabel()
        cleaningLabel.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'cleaning.png')))

        self.cleaningPageButton = QPushButton("Hybrid Data Cleaning System")
        self.cleaningPageButton.setEnabled(False)
        self.cleaningPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.cleaningPageButton.setFixedHeight(30)
        self.cleaningPageButton.clicked.connect(lambda: self.movetopage(5))

        resultsLabel = QLabel()
        resultsLabel.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'results.png')))

        self.resultPageButton = QPushButton("Dataset Interaction")
        self.resultPageButton.setEnabled(False)
        self.resultPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.resultPageButton.setFixedHeight(30)
        self.resultPageButton.clicked.connect(lambda: self.movetopage(6))
        self.evaluationPageButton = QPushButton("Result Evaluation")
        self.evaluationPageButton.setEnabled(False)
        self.evaluationPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.evaluationPageButton.setFixedHeight(30)
        self.evaluationPageButton.clicked.connect(lambda: self.movetopage(7))

        # tab layout set up
        self.tabLayout.addWidget(titleText)
        self.tabLayout.addWidget(introLabel)
        self.tabLayout.addWidget(self.aboutPageButton)
        self.tabLayout.addWidget(self.helpPageButton)
        self.tabLayout.addWidget(self.acknowledgementPageButton)
        self.tabLayout.addWidget(settingsLabel)
        self.tabLayout.addWidget(self.paramPageButton)
        self.tabLayout.addWidget(cleaningLabel)
        self.tabLayout.addWidget(self.cleaningPageButton)
        self.tabLayout.addWidget(resultsLabel)
        self.tabLayout.addWidget(self.resultPageButton)
        self.tabLayout.addWidget(self.evaluationPageButton)

    #Static page UI
    def pageLayouts(self):

        self.aboutPageWidget = QWidget()
        self.aboutPageWidget.setStyleSheet("background-color: white")
        self.helpPageWidget = QWidget()
        self.helpPageWidget.setStyleSheet("background-color: white")
        self.acknowledgementPageWidget = QWidget()
        self.acknowledgementPageWidget.setStyleSheet("background-color: white")
        self.paramPageWidget = QWidget()
        self.paramPageWidget.setStyleSheet("background-color: white")
        self.formatPageWidget = QWidget()
        self.formatPageWidget.setStyleSheet("background-color: white")
        self.cleaningPageWidget = QWidget()
        self.cleaningPageWidget.setStyleSheet("background-color: white")
        self.resultPageWidget = QWidget()
        self.resultPageWidget.setStyleSheet("background-color: white")
        self.evaluationPageWidget = QWidget()
        self.evaluationPageWidget.setStyleSheet("background-color: white")
        self.chartPageWidget = QWidget()
        self.chartPageWidget.setStyleSheet("background-color: white")

        # Adding all pages to pageLayout
        self.pageLayout.addWidget(self.aboutPageWidget)
        self.pageLayout.addWidget(self.helpPageWidget)
        self.pageLayout.addWidget(self.acknowledgementPageWidget)
        self.pageLayout.addWidget(self.paramPageWidget)
        self.pageLayout.addWidget(self.formatPageWidget)
        self.pageLayout.addWidget(self.cleaningPageWidget)
        self.pageLayout.addWidget(self.resultPageWidget)
        self.pageLayout.addWidget(self.evaluationPageWidget)
        self.pageLayout.addWidget(self.chartPageWidget)

    #Static about page UI
    def aboutLayout(self):

        welcomeText = QLabel("Welcome to IHCS!")
        welcomeText.setFont(self.font)
        welcomeText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        textLayout = QVBoxLayout()
        textWidget = QWidget()
        textWidget.setLayout(textLayout)
        aboutScrollArea = QScrollArea()
        aboutScrollArea.setWidgetResizable(True)
        aboutText = QLabel(self.outputFile(os.path.join(self.current_dir, 'Text', 'About.txt')))
        aboutText.setWordWrap(True)
        aboutText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # About Page Setup
        aboutLayout = QVBoxLayout(self.aboutPageWidget)
        aboutLayout.addSpacing(75)
        aboutLayout.addWidget(welcomeText)
        aboutLayout.addSpacing(50)
        aboutLayout.addWidget(aboutScrollArea)
        aboutScrollArea.setWidget(textWidget)
        textLayout.addWidget(aboutText)
        aboutLayout.addSpacing(50)

    #Static help page UI
    def helpLayout(self):

        # Help UI Elements
        helpTitleWidget = QWidget()
        helpTitleLayout = QVBoxLayout()
        helpTitle = QLabel()
        helpTitle.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'help page.png')))
        helpText = QLabel(self.outputFile(os.path.join(self.current_dir, 'Text', 'Help.txt')))
        helpText.setWordWrap(True)
        helpText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Help Page Setup
        helpLayout = QVBoxLayout(self.helpPageWidget)
        helpTitleWidget.setLayout(helpTitleLayout)
        helpTitleLayout.addSpacing(20)
        helpTitleLayout.addWidget(helpTitle)
        helpTitleLayout.addSpacing(10)
        helpLayout.addWidget(helpTitleWidget)
        helpLayout.addWidget(helpText)

    #Static acknowlegment page UI
    def acknowlegementLayout(self):

        acknowlegementTitleWidget = QWidget()
        acknowlegementTitleLayout = QVBoxLayout()
        acknowlegementTitle = QLabel()
        
        acknowlegementTitle.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'acknowledgements page.png')))
        acknowledgementText = QLabel(self.outputFile(os.path.join(self.current_dir, 'Text', 'Acknowledgements.txt')))
        acknowledgementText.setWordWrap(True)
        acknowledgementText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Acknowledgement Page Setup
        acknowledgementLayout = QVBoxLayout(self.acknowledgementPageWidget)
        acknowlegementTitleWidget.setLayout(acknowlegementTitleLayout)
        acknowlegementTitleLayout.addWidget(acknowlegementTitle)
        acknowlegementTitleLayout.addSpacing(60)
        acknowledgementLayout.addWidget(acknowlegementTitleWidget)
        acknowledgementLayout.addWidget(acknowledgementText)
        acknowledgementLayout.addSpacing(150)

    #Static parameter setting page UI
    def paramLayout(self):

        # Param UI Elements
        chooseWidget = QWidget()
        chooseLayout = QVBoxLayout()
        parameterSettingLabel = QLabel()
        parameterSettingLabel.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'parameter page.png')))
        chooseText = QLabel("Choose the Files")
        chooseText.setStyleSheet("color: blue")
        chooseText.setFixedHeight(20)
        browseWidget = QWidget()
        browseWidget.setStyleSheet("background-color: rgba(220, 220, 220, 100)")
        browseLayout = QVBoxLayout(browseWidget)
        datasetWidget = QWidget()
        datasetWidget.setStyleSheet("background-color: transparent")
        datasetLayout = QHBoxLayout(datasetWidget)
        rulesWidget = QWidget()
        rulesWidget.setStyleSheet("background-color: transparent")
        rulesLayout = QHBoxLayout(rulesWidget)
        paramInfoText = QLabel("Select a dataset that you want to clean and input its corresponding data quality rules")
        paramInfoText.setStyleSheet("background-color: transparent")
        datasetText = QLabel("Dataset:")
        self.datasetTextBox = QLineEdit()
        self.datasetTextBox.setStyleSheet("background-color: white")
        self.datasetTextBox.setMaximumWidth(370)
        browseDatasetButton = QPushButton("Browse...")
        browseDatasetButton.setStyleSheet(self.ss.browseButtonStyle())
        browseDatasetButton.clicked.connect(lambda: self.openFileDialog("dirty_data"))
        rulesText = QLabel("MLN Rules:")
        self.rulesTextBox = QLineEdit()
        self.rulesTextBox.setStyleSheet("background-color: white")
        self.rulesTextBox.setMinimumWidth(370)
        self.rulesTextBox.setMaximumWidth(390)
        browseRulesButton = QPushButton("Browse...")
        browseRulesButton.setStyleSheet(self.ss.browseButtonStyle())
        browseRulesButton.clicked.connect(lambda: self.openFileDialog("rules"))
        browseRulesButton.setToolTip(self.outputFile(os.path.join(self.current_dir, 'Text', 'MLNRules.txt')))
        formatLayout = QHBoxLayout()
        formatWidget = QWidget()
        formatButton = QPushButton("Next")
        formatButton.setStyleSheet(self.ss.pageButtonStyle())
        formatButton.setFixedSize(100, 30)
        formatButton.clicked.connect(self.clean_button_clicked)

        # Param Page Setup
        paramLayout = QVBoxLayout(self.paramPageWidget)
        chooseWidget.setLayout(chooseLayout)
        browseWidget.setLayout(browseLayout)
        formatWidget.setLayout(formatLayout)
        chooseLayout.addWidget(parameterSettingLabel)
        chooseLayout.addWidget(chooseText)
        datasetLayout.addWidget(datasetText)
        datasetLayout.addWidget(self.datasetTextBox)
        datasetLayout.addWidget(browseDatasetButton)
        rulesLayout.addWidget(rulesText)
        rulesLayout.addWidget(self.rulesTextBox)
        rulesLayout.addSpacing(30)
        rulesLayout.addWidget(browseRulesButton)
        browseLayout.addWidget(paramInfoText)
        browseLayout.addWidget(datasetWidget)
        browseLayout.addWidget(rulesWidget)
        formatLayout.addSpacing(400)
        formatLayout.addWidget(formatButton)
        paramLayout.addWidget(chooseWidget)
        paramLayout.addWidget(browseWidget)
        paramLayout.addSpacing(20)
        paramLayout.addWidget(formatWidget)
        paramLayout.addSpacing(50)

    #Static format page UI
    def formatLayout(self):

        # Format page UI
        labelLayout = QVBoxLayout()
        labelWidget = QWidget()
        listLayout = QVBoxLayout()
        listLayoutWidget = QWidget()
        buttonLayout = QHBoxLayout()
        buttonWidget = QWidget()
        formatSettingLabel = QLabel()
        formatSettingLabel.setPixmap(QPixmap('View/Images/format page.png'))
        instructionLabel = QLabel('Look over the data types of each column and make any changes if needed')
        instructionLabel.setStyleSheet("color: blue")
        instructionLabel.setFixedHeight(40)
        self.listWidget = QListWidget()
        self.listWidget.setSpacing(1)
        self.listWidget.setStyleSheet("background-color: rgba(220, 220, 220, 100)")
        self.formatItemsList = []
        formatButton = QPushButton("Next")
        formatButton.setFixedSize(100, 30)
        formatButton.setStyleSheet(self.ss.pageButtonStyle())
        formatButton.clicked.connect(self.format_button_clicked)

        # Format page setup
        formatPageLayout = QVBoxLayout(self.formatPageWidget)
        labelWidget.setLayout(labelLayout)
        listLayoutWidget.setLayout(listLayout)
        buttonWidget.setLayout(buttonLayout)
        labelLayout.addWidget(formatSettingLabel)
        labelLayout.addWidget(instructionLabel)
        listLayout.addWidget(self.listWidget)
        buttonLayout.addSpacing(400)
        buttonLayout.addWidget(formatButton)
        formatPageLayout.addWidget(labelWidget)
        formatPageLayout.addWidget(listLayoutWidget)
        formatPageLayout.addSpacing(50)
        formatPageLayout.addWidget(buttonWidget)
        formatPageLayout.addSpacing(50)

    #Static cleaning page UI
    def cleanLayout(self):

        # clean UI
        cleaningLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        buttonWidget = QWidget()
        cleaningLabel = QLabel()
        cleaningLabel.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'cleaning page.png')))
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(self.ss.progressBarStyle())
        self.finishButton = QPushButton("Next")
        self.finishButton.setFixedSize(100, 30)
        self.finishButton.setStyleSheet(self.ss.disabledPageButtonStyle())
        self.finishButton.clicked.connect(self.finish_button_clicked)
        self.finishButton.setEnabled(False)

        # clean layout setup
        buttonWidget.setLayout(buttonLayout)
        cleaningLayout.addWidget(cleaningLabel)
        cleaningLayout.addWidget(self.progress_bar)
        buttonLayout.addSpacing(400)
        buttonLayout.addWidget(self.finishButton)
        cleaningLayout.addSpacing(200)
        cleaningLayout.addWidget(buttonWidget)
        self.cleaningPageWidget.setLayout(cleaningLayout)

    #Static result page UI
    def resultLayout(self):

        #Result UI
        resultsLayout = QVBoxLayout()
        downloadLayout = QHBoxLayout()


        resultsLabel = QLabel()
        resultsLabel.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'result page.png')))
        congratsLabel = QLabel("Congratulations, cleaning finished!")

        #Dataset UI stuff
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.datasetWidget = QWidget()
        self.datasetLayout = QVBoxLayout(self.datasetWidget)
        self.datasetHeader = QHBoxLayout()
        

        downloadWidget = QWidget()
        downloadButton = QPushButton("Download")
        downloadButton.setStyleSheet(self.ss.pageButtonStyle())
        downloadButton.setFixedSize(100, 30)
        downloadButton.clicked.connect(self.download_button_clicked)
        

        #Result Setup
        resultsLayout.addWidget(resultsLabel)
        resultsLayout.addWidget(congratsLabel)
        resultsLayout.addSpacing(5)
        self.scrollArea.setWidget(self.datasetWidget)
        resultsLayout.addWidget(self.scrollArea)
        downloadLayout.addSpacing(400)
        downloadLayout.addWidget(downloadButton)
        downloadWidget.setLayout(downloadLayout)
        resultsLayout.addWidget(downloadWidget)
        self.resultPageWidget.setLayout(resultsLayout)

    #Static evaluation page UI
    def evalLayout(self):

        #UI Stuff
        evalFullLayout = QVBoxLayout()        

        evalHeaderLayout = QHBoxLayout()
        evalHeaderWidget = QWidget()
        evalHeaderWidget.setLayout(evalHeaderLayout)
        evalLabel = QLabel()
        evalLabel.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'evaluation page.png')))
        self.chartButton = QPushButton("Chart")
        self.chartButton.setEnabled(False)
        self.chartButton.setStyleSheet(self.ss.disabledPageButtonStyle())
        self.chartButton.setFixedWidth(150)
        self.chartButton.clicked.connect(self.chart_button_clicked)

        compareLabel = QLabel("Compare")
        compareLabel.setStyleSheet("color: blue")
        
        evalMiniLayout = QVBoxLayout()
        evalMiniWidget = QWidget()
        evalMiniWidget.setStyleSheet("background-color: rgba(220, 220, 220, 100)")
        evalMiniWidget.setLayout(evalMiniLayout)
        groundTruthLabel = QLabel("If you have a ground truth file, please input the file into here. We utilize Presicion, Recall, and F1-score to evaluate the accuracy of the cleaning result")
        groundTruthLabel.setWordWrap(True)
        groundTruthLabel.setStyleSheet("background-color: transparent")

        fileLayout = QHBoxLayout()
        fileWidget = QWidget()
        fileWidget.setStyleSheet("background-color: transparent")
        fileWidget.setLayout(fileLayout)
        self.groundTruthTextBox = QLineEdit()
        self.groundTruthTextBox.setEnabled(False)
        self.groundTruthTextBox.setFixedWidth(300)
        self.groundTruthTextBox.setStyleSheet("background-color: white")
        browseButton = QPushButton("Browse...")
        browseButton.setStyleSheet(self.ss.browseButtonStyle())
        browseButton.setFixedWidth(100)
        browseButton.clicked.connect(lambda: self.openFileDialog("ground_truth"))
        evalButton = QPushButton("Evaluate")
        evalButton.setStyleSheet(self.ss.greyPageButtonStyle())
        evalButton.setFixedWidth(100)
        evalButton.clicked.connect(self.evaluate_button_clicked)

        currentCleaningLabel = QLabel("Current Cleaning Result:")
        currentCleaningLabel.setStyleSheet("background-color: transparent")

        resultVLayout = QVBoxLayout()
        resultVWidget = QWidget()
        resultVWidget.setLayout(resultVLayout)
        resultVWidget.setStyleSheet("background-color: transparent")
        
        resultHeaderLayout = QHBoxLayout()
        resultHeaderWidget = QWidget()
        resultHeaderWidget.setStyleSheet("background-color: white")
        resultHeaderWidget.setLayout(resultHeaderLayout)
        resultDatasetHead = QLabel(f"<b>Dataset<b>")
        resultRuntimeHead = QLabel(f"<b>Runtime<b>")
        resultPrecisionHead = QLabel(f"<b>Precision<b>")
        resultRecallHead = QLabel(f"<b>Recall<b>")
        resultF1Head = QLabel(f"<b>F1-Score<b>")

        self.resultLayout = QHBoxLayout()
        resultWidget = QWidget()
        resultWidget.setLayout(self.resultLayout)

        historyResultLayout = QHBoxLayout()
        historyResultWidget = QWidget()
        historyResultWidget.setStyleSheet("background-color: transparent")
        historyResultWidget.setLayout(historyResultLayout)
        historyResultLabel = QLabel("History Cleaning Results:")
        clearRecordButton = QPushButton("Clear Records")
        clearRecordButton.setFixedWidth(150)
        clearRecordButton.setStyleSheet(self.ss.greyPageButtonStyle())
        clearRecordButton.clicked.connect(self.clear_record_button_clicked)

        historyVLayout = QVBoxLayout()
        historyVWidget = QWidget()
        historyVWidget.setStyleSheet("background-color: transparent")
        historyVWidget.setLayout(historyVLayout)
        

        historyHeaderLayout = QHBoxLayout()
        historyHeaderWidget = QWidget()
        historyHeaderWidget.setStyleSheet("background-color: white")
        historyHeaderWidget.setLayout(historyHeaderLayout)
        historyDatasetHead = QLabel(f"<b>Dataset<b>")
        historyRuntimeHead = QLabel(f"<b>Runtime<b>")
        historyPrecisionHead = QLabel(f"<b>Precision<b>")
        historyRecallHead = QLabel(f"<b>Recall<b>")
        historyF1Head = QLabel(f"<b>F1-Score<b>")

        self.historyListWidget = QListWidget()
        self.historyListWidget.setMinimumHeight(125)


        #UI Setup
        evalFullLayout.addWidget(evalHeaderWidget)
        evalHeaderLayout.addWidget(evalLabel)
        evalHeaderLayout.addWidget(self.chartButton)
        evalFullLayout.addWidget(compareLabel)
        evalFullLayout.addWidget(evalMiniWidget)
        evalMiniLayout.addWidget(groundTruthLabel)
        evalMiniLayout.addWidget(fileWidget)
        fileLayout.addWidget(self.groundTruthTextBox)
        fileLayout.addWidget(browseButton)
        fileLayout.addWidget(evalButton)
        evalMiniLayout.addWidget(currentCleaningLabel)
        evalMiniLayout.addWidget(resultVWidget)
        resultVLayout.addWidget(resultHeaderWidget)
        resultHeaderLayout.addWidget(resultDatasetHead)
        resultHeaderLayout.addWidget(resultRuntimeHead)
        resultHeaderLayout.addWidget(resultPrecisionHead)
        resultHeaderLayout.addWidget(resultRecallHead)
        resultHeaderLayout.addWidget(resultF1Head)
        resultVLayout.addWidget(resultWidget)
        evalMiniLayout.addWidget(historyResultWidget)
        historyResultLayout.addWidget(historyResultLabel)
        historyResultLayout.addSpacing(100)
        historyResultLayout.addWidget(clearRecordButton)
        evalMiniLayout.addWidget(historyVWidget)
        historyVLayout.addWidget(historyHeaderWidget)
        historyHeaderLayout.addWidget(historyDatasetHead)
        historyHeaderLayout.addWidget(historyRuntimeHead)
        historyHeaderLayout.addWidget(historyPrecisionHead)
        historyHeaderLayout.addWidget(historyRecallHead)
        historyHeaderLayout.addWidget(historyF1Head)
        historyVLayout.addWidget(self.historyListWidget)

        self.evaluationPageWidget.setLayout(evalFullLayout)

    #Static chart page UI
    def chartLayout(self):
        
        #UI
        self.chartsLayout = QVBoxLayout()
        headerWidget = QWidget()
        headerLayout = QHBoxLayout()
        headerWidget.setLayout(headerLayout)
        
        headerLabel = QLabel()
        headerLabel.setPixmap(QPixmap(os.path.join(self.current_dir, 'Images', 'evaluation page.png')))
        evalButton = QPushButton("Evaluation Page")
        evalButton.setStyleSheet(self.ss.pageButtonStyle())
        evalButton.setMaximumWidth(150)
        evalButton.clicked.connect(self.eval_page_button_clicked)
        infoText = QLabel("These systems are evaluated based on the columns that are modified only. IHCS is being evaluated on 'Salary', 'DOB', 'JoinDate', 'Year of Service', 'Weight', 'Address', 'Email' columns (6 out of 9 columns). OpenRefine is being evaluated on 'Salary', 'DOB', 'JoinDate', 'Email' columns (4 out of 9 columns)")
        
        self.canvas = FigureCanvas(Figure(figsize=(7, 5)))
        
        
        
        #Setup
        self.chartsLayout.addWidget(headerWidget)
        headerLayout.addWidget(headerLabel)
        headerLayout.addWidget(evalButton)
        self.chartsLayout.addWidget(QLabel("Here you can view how scores compare to other cleaning systems"))
        self.chartsLayout.addWidget(self.canvas)
        self.chartsLayout.addWidget(infoText)
        
        self.chartPageWidget.setLayout(self.chartsLayout)
        
    # Clean button will reset pages for next dataset stuff, and initiate the cleaning process
    def clean_button_clicked(self):

        #Check if file and rules are set correctly
        if not re.search(r'^(?:[a-zA-Z]:[\\/])?(?:[\w\s()-]+[\\/])*[\w\s()-]+\.(csv|xlsx|xls|json)$',
                         self.datasetTextBox.text()) or not re.search(r'^\/(?:[\w\s()\[\]-]+\/)*[\w\s()\[\]-]+\.(csv|xlsx|xls|json)$', self.datasetTextBox.text()):
            self.errorDialog("You must input either a csv, xlsx, xls, or json file")
            return
        if not re.search(
                r'^(?:[a-zA-Z]:[\\/])?(?:[\w\s()-]+[\\/])*[\w\s()-]+\.mln$',
                self.rulesTextBox.text()) or not re.search(r'^\/(?:[\w\s()\[\]-]+\/)*[\w\s()\[\]-]+\.mln$', self.rulesTextBox.text()):
            self.errorDialog("Must put in mln rules")
            return
        
        self.viewModel.dirtyDataSet = self.datasetTextBox.text()
        try:
            shutil.copy(self.rulesTextBox.text(), self.mln_folder)
        except Exception as e:
            self.errorDialog(f"Error saving file: {e}")

        # Start cleaning sequence

        # Reset pages
        self.cleaningPageButton.setEnabled(False)
        self.cleaningPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.resultPageButton.setEnabled(False)
        self.resultPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.evaluationPageButton.setEnabled(False)
        self.evaluationPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.formatItemsList.clear()
        self.progress_bar.setValue(0)
        self.cleaningPageButton.setEnabled(True)
        self.finishButton.setEnabled(False)
        self.finishButton.setStyleSheet(self.ss.disabledPageButtonStyle())

        #reset data
        #self.viewModel.cleaningTime = 0
        self.viewModel.formatList.clear()
        self.viewModel.changedTypes.clear()
        self.viewModel.cleanDatasetDict.clear()
        #self.viewModel.cleanScores.clear()

        #Clear widgets on repeat iterations
        self.listWidget.clear()        
        while self.datasetLayout.count():
            child = self.datasetLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())
                
        self.movetopage(5)
        self.viewModel.startClean() 

    #Dyanmic portion of format UI
    def format_start(self):
        self.formatting = True
        self.originalTypes = {}
        
        # Add items to list to display
        for column in self.viewModel.formatList:
            colName = column['column_name']
            semantic = column['semantic_data_type']
            atomic = column['atomic_data_type']
            self.originalTypes[colName] = semantic
            item = QListWidgetItem(self.listWidget)
            itemWidget = QWidget()
            itemWidget.setStyleSheet("background-color: transparent")
            itemLayout = QHBoxLayout()
            itemLayout.setContentsMargins(0, 0, 0, 0)
            itemLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            colText = QLabel(colName)
            colText.setFixedWidth(100)
            comboBox = QComboBox()
            comboBox.addItems(["string", "date/time", "Email", 'country', 'phone number', "US currency", 'US address', 'URL', 'ISBN numbers'])
            comboBox.setCurrentText(semantic)
            comboBox.setFixedWidth(150)
            comboBox.setStyleSheet("background-color: white")
            typeText = QLabel(atomic)
            


            yearWidget = QWidget()
            yearLayout = QHBoxLayout()
            yearLayout.setContentsMargins(0, 0, 0, 0)
            yearFormat = QCheckBox("Year format")
            yearFormat.setToolTip(self.outputFile(os.path.join(self.current_dir, "Text", "Year_Info.txt")))
            min_year_input = QLineEdit()
            min_year_input.setPlaceholderText("Min Year")
            min_year_input.setStyleSheet("background-color: white")
            max_year_input = QLineEdit()
            max_year_input.setPlaceholderText("Max Year")
            max_year_input.setStyleSheet("background-color: white")
            

            yearLayout.addWidget(yearFormat)
            yearLayout.addWidget(min_year_input)
            yearLayout.addWidget(max_year_input)
            yearWidget.setLayout(yearLayout)

            yearWidget.setVisible(semantic == "date/time")

            def onTypeChanged(text, yearWidget=yearWidget):
                yearWidget.setVisible(text == "date/time")

            comboBox.currentTextChanged.connect(onTypeChanged)

            itemLayout.addWidget(colText)
            itemLayout.addWidget(comboBox)
            itemLayout.addWidget(typeText)
            itemLayout.addWidget(yearWidget)
            itemWidget.setLayout(itemLayout)

            self.listWidget.setItemWidget(item, itemWidget)
            self.formatItemsList.append((colName, comboBox, yearFormat, min_year_input, max_year_input))
        self.movetopage(4)

    # Returns new formating changes if any, and continues cleaning process and sets up clean page
    def format_button_clicked(self):
        self.formatting = False

        #Adds changed types to list if any
        for items in self.formatItemsList:
            if items[1].currentText() == "date/time" and items[2].isChecked():
                self.viewModel.changedTypes[items[0]] = {"data_type": "date_time_w_year_format", "min_year": items[3].text(), "max_year": items[4].text()}
            elif self.originalTypes[items[0]] == items[1].currentText():
                continue
            else:
                self.viewModel.changedTypes[items[0]] = {"data_type": items[1].currentText()}
        
        self.movetopage(5)
        self.viewModel.continue_clean()

    #Updates progress bar intermediately
    @pyqtSlot(int)
    def update_progress(self, value):
        newValue = self.progress_bar.value() + value
        self.progress_bar.setValue(newValue)

    #Sets up the final data for the rest of the pages
    def cleaning_finished(self):
        self.setup_json()
        self.resultSetup()
        
        self.finishButton.setEnabled(True)
        self.finishButton.setStyleSheet(self.ss.pageButtonStyle())

    #Sets up results and moves over to that page
    def finish_button_clicked(self):

        self.movetopage(6)

        #Enable rest of pages
        self.evaluationPageButton.setEnabled(True)
        self.evaluationPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.resultPageButton.setEnabled(True)
        self.resultPageButton.setStyleSheet(self.ss.enabledButtonStyle())

    #Switches to the attribute view in results
    def chart_button_clicked(self):
        self.pageLayout.setCurrentIndex(8)

    #Switches to the tuple view in results
    def eval_page_button_clicked(self):
        self.pageLayout.setCurrentIndex(7)

    #Starts the evaluation on the dataset
    def evaluate_button_clicked(self):
        #Check if file format is correct
        if not re.search(r'^(?:[a-zA-Z]:[\\/])?(?:[\w\s()-]+[\\/])*[\w\s()-]+\.(csv|xlsx|xls|json)$',
                         self.datasetTextBox.text()) or not re.search(r'^\/(?:[\w\s()\[\]-]+\/)*[\w\s()\[\]-]+\.(csv|xlsx|xls|json)$', self.datasetTextBox.text()):
            self.errorDialog("You must input either a csv, xlsx, xls, or json file")
            return
        #Run Novellas evaluation program
        self.viewModel.startEval()

    #Sets up results from evaluation onto UI
    def evaluate_finished(self):
        self.chartButton.setEnabled(True)
        self.chartButton.setStyleSheet(self.ss.pageButtonStyle())
        dataset = self.viewModel.cleanScores['dirty_dataset']
        ourResult = self.viewModel.cleanScores['ihcs']
        

        #Current Eval
        self.clear_layout(self.resultLayout)
        self.resultLayout.addWidget(QLabel(dataset))
        self.resultLayout.addWidget(QLabel(str(self.viewModel.cleaningTime)))
        self.resultLayout.addWidget(QLabel(ourResult["precision"]))
        self.resultLayout.addWidget(QLabel(ourResult["recall"]))
        self.resultLayout.addWidget(QLabel(ourResult["f1score"]))

        #History
        self.viewModel.history.append({'dataset': dataset, 'runtime': str(self.viewModel.cleaningTime), 'precision':  ourResult['precision'], 'recall': ourResult['recall'], 'f1-score': ourResult['f1score']})
        self.historyListWidget.clear()
        
        for row in self.viewModel.history:
            item = QListWidgetItem(self.historyListWidget)
            itemWidget = QWidget()
            itemLayout = QHBoxLayout()
            itemWidget.setStyleSheet("background-color: transparent")
            itemLayout.setContentsMargins(0, 0, 0, 0)

            itemLayout.addWidget(QLabel(row['dataset']))
            itemLayout.addWidget(QLabel(str(row["runtime"])))
            itemLayout.addWidget(QLabel(row["precision"]))
            itemLayout.addWidget(QLabel(row["recall"]))
            itemLayout.addWidget(QLabel(row["f1-score"]))
            itemWidget.setLayout(itemLayout)

            self.historyListWidget.setItemWidget(item, itemWidget)
        
        #Chart
        self.plot()   
    
    #Plots bar graph for evaluation
    def plot(self):
         metrics = ['Precision', 'Recall', 'F1 Score']
         x = range(len(metrics))
         scores = self.viewModel.cleanScores
         ihcsScores = [float(scores['ihcs']['precision']), float(scores['ihcs']['recall']), float(scores['ihcs']['f1score'])]
         otherScores = [float(scores['openrefine']['precision']),float(scores['openrefine']['recall']),float(scores['openrefine']['f1score'])]
         
         ax = self.canvas.figure.subplots()
         
         barWidth = .35
         
         ax.bar([i - .35/2 for i in x], ihcsScores, width=barWidth, label='IHCS', color='#007bff')
         ax.bar([i + barWidth/2 for i in x], otherScores, width=barWidth, label='Other', color='#00c853')
         
         ax.set_xticks(x)
         ax.set_xticklabels(metrics)
         ax.set_ylabel('Score')
         ax.set_title("IHCS vs Other Systems")
         ax.legend()
         ax.grid(axis='y', linestyle='--', alpha=0.7)
         ax.set_ylim(0,1)
         
         self.canvas.draw()
                
    #Downloads the clean dataset to the users choosing
    def download_button_clicked(self):

        # Let user choose where to save the file
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File As",
            "",  # Default directory or filename
            "CSV Files (*.csv);;XLSX Files (*.xlsx);;XLS Files (*.xls);;JSON Files (*.json);;All Files (*)"
        )

        #File copy to new path
        if file_path:
            try:
                shutil.copy(self.viewModel.cleanDatasetPath, file_path)
            except Exception as e:
                self.errorDialog(f"Error saving file: {e}")

    #Clears record and the UI associated
    def clear_record_button_clicked(self):
        self.historyListWidget.clear()
        self.viewModel.history = []

    # Changes tab button highlight and moves to page selected
    def movetopage(self, page):
        if self.currentSelectedPage == 0:
            self.aboutPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 1:
            self.helpPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 2:
            self.acknowledgementPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 3:
            self.paramPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 4 or self.currentSelectedPage == 5:
            self.cleaningPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 6:
            self.resultPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 7:
            self.evaluationPageButton.setStyleSheet(self.ss.enabledButtonStyle())

        self.currentSelectedPage = page
        if page == 4 or page == 5:
            if self.formatting:
                self.pageLayout.setCurrentIndex(4)
            else:
                self.pageLayout.setCurrentIndex(5)
        else:
            self.pageLayout.setCurrentIndex(page)

        if page == 0:
            self.aboutPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 1:
            self.helpPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 2:
            self.acknowledgementPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 3:
            self.paramPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 4 or page == 5:
            self.cleaningPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 6:
            self.resultPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 7:
            self.evaluationPageButton.setStyleSheet(self.ss.selectedButtonStyle())

    #Dynamic portion of result UI setup
    def resultSetup(self):

        changesColumn = QLabel("🔧")
        changesColumn.setFixedWidth(20)
        self.datasetHeader.addWidget(changesColumn, alignment=Qt.AlignmentFlag.AlignLeft)
        self.datasetHeader.addWidget(QLabel("|"))

        #Add header
        for key in self.viewModel.cleanDatasetDict[0].keys():
            if key != "Changes":
                label = QLabel(f"<b>{key}<b>")
                label.setFixedWidth(120)
                self.datasetHeader.addWidget(label, alignment=Qt.AlignmentFlag.AlignLeft)
                if key != list(self.viewModel.cleanDatasetDict[0].keys())[len(self.viewModel.cleanDatasetDict[0]) - 2]:
                    self.datasetHeader.addWidget(QLabel("|"))
        self.datasetLayout.addLayout(self.datasetHeader)
        self.datasetLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.add_seperator(self.datasetLayout)

        #Add Rows
        for row in self.viewModel.cleanDatasetDict:
            row_layout = QHBoxLayout()

            if row["Changes"]:
                icon_label = QLabel("🛈")
                icon_label.setToolTip(row["Changes"])
            else:
                icon_label = QLabel("")

            icon_label.setFixedWidth(20)
            row_layout.addWidget(icon_label)
            row_layout.addWidget(QLabel("|"))

            for key, value in row.items():
                if key != "Changes":
                    if value is None:
                        lbl = QLabel("N/A")
                    else:
                        lbl = QLabel(str(value))
                    lbl.setFixedWidth(120)
                    row_layout.addWidget(lbl)
                    if key != list(row.keys())[len(row) - 2]:
                        row_layout.addWidget(QLabel("|"))
            
            self.datasetLayout.addLayout(row_layout)
            self.add_seperator(self.datasetLayout)

    #Horizontal seperator for dataset visual
    def add_seperator(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

    #Layout cleaner for reseting
    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def setup_json(self):
        clean_path = os.path.join(self.current_dir, '..', 'backend', 'results', 'final_cleaned.json')
        clean_path = os.path.abspath(clean_path)
        
        with open(clean_path, 'r') as file:
            self.viewModel.cleanDatasetDict = json.load(file)
        
    # Reads a file and returns the text
    def outputFile(self, file):
        f = open(file, "r")
        return f.read()

    # Opens filepath
    def openFileDialog(self, type):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Datasheet")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            if type == "dirty_data":
                self.datasetTextBox.setText(file_dialog.selectedFiles()[0])
            elif type == "rules":
                self.rulesTextBox.setText(file_dialog.selectedFiles()[0])
            elif type == "ground_truth":
                self.groundTruthTextBox.setText(file_dialog.selectedFiles()[0])
                       
    # Provides a popup error given an error message
    def errorDialog(self, error):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Error")
        msgBox.setText(error)
        msgBox.exec()

def begin():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()