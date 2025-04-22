import os.path

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QPixmap, QColor
import re
import sys
from PyQt6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit, QMainWindow,
                             QProgressBar, QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout,
                             QStackedLayout, QGridLayout, QWidget, QListWidget, QListWidgetItem,
                             QTabWidget, QScrollArea, QToolTip, QTableWidget, QTableWidgetItem,
                             QComboBox
                             )
from StyleSheets import StyleSheet
from ViewModel import ViewModel


class MainWindow(QMainWindow):
    currentSelectedPage = 0
    repeatClean = False
    ss = StyleSheet()


    def __init__(self):
        super().__init__()
        self.cleaningThread = None
        self.setWindowTitle("IHCS")
        self.setFixedSize(800, 500)
        self.viewModel = ViewModel()

        self.viewModel.format_start.connect(self.format_start)
        self.viewModel.progress_changed.connect(self.update_progress)
        self.viewModel.cleaning_finished.connect(self.cleaning_finished)

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


        self.mainLayout.addLayout(self.tabLayout, 1)
        self.mainLayout.addLayout(self.pageLayout, 4)

        widget = QWidget()
        widget.setLayout(self.mainLayout)

        self.setCentralWidget(widget)

    def tabLayouts(self):

        #UI
        titleText = QLabel("IHCS")
        self.font = titleText.font()
        self.font.setPointSize(30)
        titleText.setFont(self.font)
        titleText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        introLabel = QLabel()
        introLabel.setPixmap(QPixmap('View/Images/intro.png'))

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
        settingsLabel.setPixmap(QPixmap('View/Images/settings.png'))

        self.paramPageButton = QPushButton("Parameter Setting")
        self.paramPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.paramPageButton.setFixedHeight(30)
        self.paramPageButton.clicked.connect(lambda: self.movetopage(3))

        cleaningLabel = QLabel()
        cleaningLabel.setPixmap(QPixmap('View/Images/cleaning.png'))

        self.cleaningPageButton = QPushButton("Hybrid Data Cleaning System")
        self.cleaningPageButton.setEnabled(False)
        self.cleaningPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.cleaningPageButton.setFixedHeight(30)
        self.cleaningPageButton.clicked.connect(lambda: self.movetopage(5))

        resultsLabel = QLabel()
        resultsLabel.setPixmap(QPixmap('View/Images/results.png'))

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

        # Adding all pages to pageLayout
        self.pageLayout.addWidget(self.aboutPageWidget)
        self.pageLayout.addWidget(self.helpPageWidget)
        self.pageLayout.addWidget(self.acknowledgementPageWidget)
        self.pageLayout.addWidget(self.paramPageWidget)
        self.pageLayout.addWidget(self.formatPageWidget)
        self.pageLayout.addWidget(self.cleaningPageWidget)
        self.pageLayout.addWidget(self.resultPageWidget)
        self.pageLayout.addWidget(self.evaluationPageWidget)

    def aboutLayout(self):

        welcomeText = QLabel("Welcome to IHCS!")
        welcomeText.setFont(self.font)
        welcomeText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        aboutText = QLabel(self.outputFile("View/Text/About.txt"))
        aboutText.setWordWrap(True)
        aboutText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # About Page Setup
        aboutLayout = QVBoxLayout(self.aboutPageWidget)
        aboutLayout.addWidget(welcomeText)
        aboutLayout.addWidget(aboutText)
        aboutLayout.addSpacing(150)

    def helpLayout(self):

        # Help UI Elements
        helpTitleWidget = QWidget()
        helpTitleLayout = QVBoxLayout()
        helpTitle = QLabel()
        helpTitle.setPixmap(QPixmap('View/Images/help page.png'))
        helpText = QLabel(self.outputFile("View/Text/Help.txt"))
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

    def acknowlegementLayout(self):

        acknowlegementTitleWidget = QWidget()
        acknowlegementTitleLayout = QVBoxLayout()
        acknowlegementTitle = QLabel()
        acknowlegementTitle.setPixmap(QPixmap('View/Images/acknowledgements page.png'))
        acknowledgementText = QLabel(self.outputFile("View/Text/Acknowledgements.txt"))
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

    def paramLayout(self):

        # Param UI Elements
        chooseWidget = QWidget()
        chooseLayout = QVBoxLayout()
        parameterSettingLabel = QLabel()
        parameterSettingLabel.setPixmap(QPixmap('View/Images/parameter page.png'))
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
        browseDatasetButton.clicked.connect(self.openFileDialog)
        rulesText = QLabel("MLN Rules:")
        self.rulesTextBox = QLineEdit()
        self.rulesTextBox.setStyleSheet("background-color: white")
        self.rulesTextBox.setMaximumWidth(370)
        rulesToolTip = QLabel()
        rulesToolTip.setToolTip(self.outputFile("View/Text/MLNRules.txt"))
        rulesToolTip.setPixmap(QPixmap("View/Images/tooltip.png"))
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
        rulesLayout.addWidget(rulesToolTip)
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
        formatButton.clicked.connect(self.viewModel.continueClean)

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

    def cleanLayout(self):

        # clean UI
        cleaningLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        buttonWidget = QWidget()
        cleaningLabel = QLabel()
        cleaningLabel.setPixmap(QPixmap('View/Images/cleaning page.png'))
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

    def resultLayout(self):

        #Result UI
        resultsLayout = QStackedLayout()
        tupleLayout = QVBoxLayout()
        attributeLayout = QVBoxLayout()

        #Tuple UI
        resultsLabel1 = QLabel()
        resultsLabel1.setPixmap(QPixmap('View/Images/result page.png'))
        congratsLabel = QLabel("Congratulations, cleaning finished!")
        #Dataset UI stuff
        chartButton = QPushButton()
        chartButton.setStyleSheet(self.ss.pageButtonStyle())
        duplicateCheck = QCheckBox("Keep Duplicates")
        downloadButton = QPushButton()
        downloadButton.setStyleSheet(self.ss.pageButtonStyle())


        #Chart UI
        resultsLabel2 = QLabel()
        resultsLabel2.setPixmap(QPixmap('View/Images/result page.png'))

        #Result Setup


    def evalLayout(self):
        print("hello")


    # Clean button will reset pages for next dataset stuff, and initiate the cleaning process
    def clean_button_clicked(self):

        # #Check if file and rules are set correctly
        # if not re.search(r'^(?:[a-zA-Z]:[\\/])?(?:[\w\s()-]+[\\/])*[\w\s()-]+\.(csv|xlsx|xls|json)$',
        #                  self.datasetTextBox.text()):
        #     self.errorDialog("You must input either a csv, xlsx, xls, or json file")
        #     return
        # if self.rulesTextBox.text() == "":
        #     self.errorDialog("Must put in MLN rules")
        #     return
        # elif not re.search(
        #         r'^([A-Za-z0-9]+\([A-Za-z0-9, .]+\))(?:(\^| \^|\^ | \^ )[A-Za-z0-9]+\([A-Za-z0-9, .]+\))*(=>| =>|=> | => )([A-Za-z0-9]+\([A-Za-z0-9, .]+\))(\^| \^|\^ | \^ )([0-9.]+)$',
        #         self.rulesTextBox.text().lower()):
        #     self.errorDialog("Only eligible rules are allowed")
        #     return

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

        self.movetopage(5)
        self.viewModel.startClean() 

    def format_start(self):

        # Add items to list to display
        for column, dtype in self.viewModel.formatList.items():
            item = QListWidgetItem(self.listWidget)
            itemWidget = QWidget()
            itemLayout = QHBoxLayout()
            itemLayout.setContentsMargins(0, 0, 0, 0)
            itemLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

            text = QLabel(str(column))
            text.setFixedWidth(100)
            comboBox = QComboBox()
            comboBox.addItems(["date/time", "email", 'country', 'phone number', "text", 'US street address', 'url', 'ISBN numbers'])
            comboBox.setCurrentText(dtype)
            comboBox.setFixedWidth(150)
            comboBox.setStyleSheet("background-color: white")


            yearWidget = QWidget()
            yearLayout = QHBoxLayout()
            yearLayout.setContentsMargins(0, 0, 0, 0)
            yearFormat = QCheckBox("Year format")
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

            yearWidget.setVisible(dtype == "date/time")

            def onTypeChanged(text, yearWidget=yearWidget):
                yearWidget.setVisible(text == "date/time")

            comboBox.currentTextChanged.connect(onTypeChanged)

            itemLayout.addWidget(text)
            itemLayout.addWidget(comboBox)
            itemLayout.addWidget(yearWidget)
            itemWidget.setLayout(itemLayout)

            self.listWidget.setItemWidget(item, itemWidget)
            self.formatItemsList.append((column, comboBox, yearFormat, min_year_input, max_year_input))
            self.movetopage(4)


    # Returns new formating changes if any, and continues cleaning process and sets up clean page
    def format_button_clicked(self):

        #Adds changed types to list if any
        for items in self.formatItemsList:
            if items[1].currentText() == "date/time" and items[2].isChecked():
                self.viewModel.changedTypes[items[0]] = {"data_type": "date_time_w_year_format", "min_year": items[3].text(), "max_year": items[4].text()}
            elif self.viewModel.formatList[items[0]] == items[1].currentText():
                continue
            else:
                self.viewModel.changedTypes[items[0]] = {"data_type": items[1].currentText()}
        
        self.movetopage(5)
        self.viewModel.continue_clean() 

    #Updates progress bar intermediately
    @pyqtSlot(int)
    def update_progress(self, value):
        self.progress_bar.setValue(value)

    #Display results from the cleaning process
    def cleaning_finished(self):
        self.evaluationPageButton.setEnabled(True)
        self.evaluationPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.resultPageButton.setEnabled(True)
        self.resultPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.finishButton.setEnabled(True)
        self.finishButton.setStyleSheet(self.ss.pageButtonStyle())

    #Moves over to the results page
    def finish_button_clicked(self):
        self.movetopage(6)

    #Switches to the attribute view in results
    def chart_button_clicked(self):
        print("moving to chart page")

    #Switches to the tuple view in results
    def tuple_button_clicked(self):
        print("moving to tuple page")

    #Downloads the dataset provided if the status of duplicate checkbox
    def download_button_clicked(self):
        print("download dataset")

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
        elif self.currentSelectedPage == 5:
            self.cleaningPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 6:
            self.resultPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 7:
            self.evaluationPageButton.setStyleSheet(self.ss.enabledButtonStyle())

        self.currentSelectedPage = page
        self.pageLayout.setCurrentIndex(page)

        if page == 0:
            self.aboutPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 1:
            self.helpPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 2:
            self.acknowledgementPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 3:
            self.paramPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 5:
            self.cleaningPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 6:
            self.resultPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 7:
            self.evaluationPageButton.setStyleSheet(self.ss.selectedButtonStyle())

    # Reads a file and returns the text
    def outputFile(self, file):
        f = open(file, "r")
        return f.read()

    # Opens filepath
    def openFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Datasheet")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            self.datasetTextBox.setText(file_dialog.selectedFiles()[0])

    # Provides a popup error given an error message
    def errorDialog(self, error):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Error")
        msgBox.setText(error)
        msgBox.exec()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
