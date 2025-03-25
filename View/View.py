import os.path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import re
import sys
from PyQt6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit, QMainWindow,
                             QProgressBar, QFileDialog, QMessageBox, QPushButton, QVBoxLayout, QHBoxLayout,
                             QStackedLayout, QGridLayout, QWidget, QListWidget, QListWidgetItem
                             )
from Spacers import Spacer
from StyleSheets import StyleSheet
from ViewModel.ViewModel import ViewModel


class MainWindow(QMainWindow):
    currentSelectedPage = 0
    ss = StyleSheet()
    viewModel = ViewModel()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IHCS")
        self.setFixedSize(800, 500)
        spacers = Spacer()

        # Tab UI Elements
        titleText = QLabel("IHCS")
        font = titleText.font()
        font.setPointSize(30)
        titleText.setFont(font)
        titleText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        introLabel = QLabel()
        introLabel.setPixmap(QPixmap('Images/intro.png'))

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
        settingsLabel.setPixmap(QPixmap('Images/settings.png'))

        self.paramPageButton = QPushButton("Parameter Setting")
        self.paramPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.paramPageButton.setFixedHeight(30)
        self.paramPageButton.clicked.connect(lambda: self.movetopage(3))

        self.formatPageButton = QPushButton("Format Setting")
        self.formatPageButton.setEnabled(False)
        self.formatPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.formatPageButton.setFixedHeight(30)
        self.formatPageButton.clicked.connect(lambda: self.movetopage(4))

        cleaningLabel = QLabel()
        cleaningLabel.setPixmap(QPixmap('Images/cleaning.png'))

        self.cleaningPageButton = QPushButton("Hybrid Data Cleaning System")
        self.cleaningPageButton.setEnabled(False)
        self.cleaningPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.cleaningPageButton.setFixedHeight(30)
        self.cleaningPageButton.clicked.connect(lambda: self.movetopage(5))

        resultsLabel = QLabel()
        resultsLabel.setPixmap(QPixmap('Images/results.png'))

        self.datasetPageButton = QPushButton("Dataset Interaction")
        self.datasetPageButton.setEnabled(False)
        self.datasetPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.datasetPageButton.setFixedHeight(30)
        self.datasetPageButton.clicked.connect(lambda: self.movetopage(6))
        self.resultPageButton = QPushButton("Result Evaluation")
        self.resultPageButton.setEnabled(False)
        self.resultPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.resultPageButton.setFixedHeight(30)
        self.resultPageButton.clicked.connect(lambda: self.movetopage(7))

        # About UI Elements
        welcomeText = QLabel("Welcome to IHCS!")
        welcomeText.setFont(font)
        welcomeText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        aboutText = QLabel(self.outputFile("Text/About.txt"))
        aboutText.setWordWrap(True)
        aboutText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Help UI Elements
        helpText = QLabel(self.outputFile("Text/Help.txt"))
        helpText.setWordWrap(True)
        helpText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Acknowledge UI Elements
        acknowledgementText = QLabel(self.outputFile("Text/Acknowledgements.txt"))
        acknowledgementText.setWordWrap(True)
        acknowledgementText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Param UI Elements
        chooseWidget = QWidget()
        chooseLayout = QVBoxLayout()
        parameterSettingLabel = QLabel()
        parameterSettingLabel.setPixmap(QPixmap('Images/parameter setting.png'))
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
        rulesText = QLabel("Rules:")
        self.rulesTextBox = QLineEdit()
        self.rulesTextBox.setStyleSheet("background-color: white")
        self.rulesTextBox.setMaximumWidth(370)
        browseRulesButton = QPushButton("Browse...")
        browseRulesButton.setStyleSheet(self.ss.browseButtonStyle())
        self.generateRuleCheckBox = QCheckBox()
        self.generateRuleCheckBox.setText("Generate rules automatically")
        self.generateRuleCheckBox.setStyleSheet("background-color: transparent")
        self.generateRuleCheckBox.clicked.connect(self.rules_checkbox_clicked)
        formatLayout = QHBoxLayout()
        formatLayout.setSpacing(0)
        formatWidget = QWidget()
        formatButton = QPushButton("Clean")
        formatButton.setStyleSheet(self.ss.pageButtonStyle())
        formatButton.setFixedSize(100, 30)
        formatButton.clicked.connect(self.format_button_clicked)

        # Cleaning UI Elements

        # Interaction UI Elements

        # Results UI Elements

        # Main layouts displayed at all times
        mainLayout = QHBoxLayout()
        tabLayout = QGridLayout()
        self.pageLayout = QStackedLayout()

        # tab layout set up
        tabLayout.addWidget(titleText)
        tabLayout.addWidget(introLabel)
        tabLayout.addWidget(self.aboutPageButton)
        tabLayout.addWidget(self.helpPageButton)
        tabLayout.addWidget(self.acknowledgementPageButton)
        tabLayout.addWidget(settingsLabel)
        tabLayout.addWidget(self.paramPageButton)
        tabLayout.addWidget(self.formatPageButton)
        tabLayout.addWidget(cleaningLabel)
        tabLayout.addWidget(self.cleaningPageButton)
        tabLayout.addWidget(resultsLabel)
        tabLayout.addWidget(self.datasetPageButton)
        tabLayout.addWidget(self.resultPageButton)

        # Page based layouts setup
        aboutPageWidget = QWidget()
        aboutPageWidget.setStyleSheet("background-color: white")
        helpPageWidget = QWidget()
        helpPageWidget.setStyleSheet("background-color: white")
        acknowledgementPageWidget = QWidget()
        acknowledgementPageWidget.setStyleSheet("background-color: white")
        paramPageWidget = QWidget()
        paramPageWidget.setStyleSheet("background-color: white")
        self.formatPageWidget = QWidget()
        self.formatPageWidget.setStyleSheet("background-color: white")
        self.cleaningPageWidget = QWidget()
        self.cleaningPageWidget.setStyleSheet("background-color: white")
        self.datasetPageWidget = QWidget()
        self.datasetPageWidget.setStyleSheet("background-color: white")
        self.resultsPageWidget = QWidget()
        self.resultsPageWidget.setStyleSheet("background-color: white")

        # About Page Setup
        aboutLayout = QGridLayout(aboutPageWidget)
        aboutLayout.addWidget(welcomeText)
        aboutLayout.addWidget(aboutText)
        aboutLayout.addWidget(spacers.s1)

        # Info Page Setup
        infoLayout = QGridLayout(helpPageWidget)
        infoLayout.addWidget(helpText)

        # Acknowledgement Page Setup
        acknowledgementLayout = QGridLayout(acknowledgementPageWidget)
        acknowledgementLayout.addWidget(acknowledgementText)

        # Param Page Setup
        paramLayout = QVBoxLayout(paramPageWidget)
        chooseWidget.setLayout(chooseLayout)
        browseWidget.setLayout(browseLayout)
        formatWidget.setLayout(formatLayout)
        chooseLayout.addWidget(parameterSettingLabel)
        chooseLayout.addWidget(chooseText)
        datasetLayout.addWidget(datasetText)
        datasetLayout.addWidget(self.datasetTextBox)
        datasetLayout.addWidget(browseDatasetButton)
        datasetLayout.setSpacing(1)
        rulesLayout.addWidget(rulesText)
        rulesLayout.addWidget(self.rulesTextBox)
        rulesLayout.addWidget(spacers.s6)
        rulesLayout.setSpacing(1)
        browseLayout.addWidget(paramInfoText)
        browseLayout.addWidget(datasetWidget)
        browseLayout.addWidget(rulesWidget)
        browseLayout.addWidget(self.generateRuleCheckBox)
        formatLayout.addWidget(spacers.s4)
        formatLayout.addWidget(spacers.s5)
        formatLayout.addWidget(formatButton)
        paramLayout.addWidget(chooseWidget)
        paramLayout.addWidget(browseWidget)
        paramLayout.addWidget(spacers.s2)
        paramLayout.addWidget(formatWidget)
        paramLayout.addWidget(spacers.s3)

        # Adding all pages to pageLayout
        self.pageLayout.addWidget(aboutPageWidget)
        self.pageLayout.addWidget(helpPageWidget)
        self.pageLayout.addWidget(acknowledgementPageWidget)
        self.pageLayout.addWidget(paramPageWidget)
        self.pageLayout.addWidget(self.formatPageWidget)
        self.pageLayout.addWidget(self.cleaningPageWidget)
        self.pageLayout.addWidget(self.datasetPageWidget)
        self.pageLayout.addWidget(self.resultsPageWidget)

        mainLayout.addLayout(tabLayout, 1)
        mainLayout.addLayout(self.pageLayout, 4)

        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)

    # Clean button will reset pages for next dataset stuff, and initiate the cleaning process
    def format_button_clicked(self):

        # Check if file and rules are set correctly
        # if not re.search(r'^(?:[a-zA-Z]:[\\/])?(?:[\w\s()-]+[\\/])*[\w\s()-]+\.(csv|xlsx|xls|json)$',
        #                  self.datasetTextBox.text()):
        #     self.errorDialog("You must input either a csv, xlsx, xls, or json file")
        #     return
        # if self.rulesTextBox.text() == "":
        #     self.errorDialog("Must put in data quality rules")
        #     return
        # elif not re.search(
        #         r'^(accuracy|completeness|conformity|consistency|timeliness|uniqueness)(?:, (accuracy|completeness|conformity|consistency|timeliness|uniqueness))*$',
        #         self.rulesTextBox.text().lower()):
        #     self.errorDialog("Only eligible rules are allowed")
        #     return

        # Start cleaning sequence
        self.viewModel.startFormat(self.datasetTextBox.text(), self.rulesTextBox.text().lower())

        # Reset pages
        self.cleaningPageButton.setEnabled(False)
        self.cleaningPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.datasetPageButton.setEnabled(False)
        self.datasetPageButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.resultPageButton.setEnabled(False)
        self.resultPageButton.setStyleSheet(self.ss.disabledButtonStyle())

        self.formatPageButton.setEnabled(True)

        # Format page UI
        listWidget = QListWidget()
        listWidget.setFixedHeight(100)
        self.textBoxes = []
        elements = [1, 2, 3, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        for element in elements:
            item = QListWidgetItem(listWidget)
            textBox = QLineEdit(str(element))
            listWidget.setItemWidget(item, textBox)
            self.textBoxes.append(textBox)

        selectButton = QPushButton("Get Selected", self)
        selectButton.clicked.connect(self.get_items)

        # Format page setup
        formatPageLayout = QVBoxLayout(self.formatPageWidget)

        formatPageLayout.addWidget(listWidget)
        formatPageLayout.addWidget(selectButton)

        self.movetopage(4)

    def get_items(self):
        selected_items = [cb.text() for cb in self.textBoxes]
        print(f'Selected items: {selected_items}')

    # Generates rules in rule textbox on param page
    def rules_checkbox_clicked(self):
        if self.generateRuleCheckBox.isChecked():
            self.rulesTextBox.setText("Accuracy, Completeness, Conformity, Consistency, Timeliness, Uniqueness")

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
        elif self.currentSelectedPage == 4:
            self.formatPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 5:
            self.cleaningPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 6:
            self.datasetPageButton.setStyleSheet(self.ss.enabledButtonStyle())
        else:
            self.resultPageButton.setStyleSheet(self.ss.enabledButtonStyle())

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
        elif page == 4:
            self.formatPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 5:
            self.cleaningPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        elif page == 6:
            self.resultPageButton.setStyleSheet(self.ss.selectedButtonStyle())
        else:
            self.datasetPageButton.setStyleSheet(self.ss.selectedButtonStyle())

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
