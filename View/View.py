from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
    QGridLayout,
    QWidget,
)
from Spacers import Spacer
from StyleSheets import StyleSheet


class MainWindow(QMainWindow):

    currentSelectedPage = 0

    def __init__(self):
        super().__init__()
        self.setWindowTitle("IHCS")
        self.setFixedSize(800, 500)
        spacers = Spacer()
        self.ss = StyleSheet()

        # Tab UI Elements
        titleText = QLabel("IHCS")
        font = titleText.font()
        font.setPointSize(30)
        titleText.setFont(font)
        titleText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        introLabel = QLabel()
        introLabel.setPixmap(QPixmap('Images/intro.png'))

        self.aboutButton = QPushButton("About")
        self.aboutButton.setStyleSheet(self.ss.enabledButtonSelectedStyle())
        self.aboutButton.setFixedHeight(30)
        self.aboutButton.clicked.connect(self.about_button_clicked)

        self.helpButton = QPushButton("Help")
        self.helpButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.helpButton.setFixedHeight(30)
        self.helpButton.clicked.connect(self.help_button_clicked)

        self.acknowledgementButton = QPushButton("Acknowledgements")
        self.acknowledgementButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.acknowledgementButton.setFixedHeight(30)
        self.acknowledgementButton.clicked.connect(self.acknowledgement_button_clicked)

        settingsLabel = QLabel()
        settingsLabel.setPixmap(QPixmap('Images/settings.png'))

        self.paramSetButton = QPushButton("Parameter Setting")
        self.paramSetButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.paramSetButton.setFixedHeight(30)
        self.paramSetButton.clicked.connect(self.param_button_clicked)

        cleaningLabel = QLabel()
        cleaningLabel.setPixmap(QPixmap('Images/cleaning.png'))

        self.cleaningButton = QPushButton("Hybrid Data Cleaning System")
        self.cleaningButton.setEnabled(False)
        self.cleaningButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.cleaningButton.setFixedHeight(30)
        self.cleaningButton.clicked.connect(self.clean_page_button_clicked)

        resultsLabel = QLabel()
        resultsLabel.setPixmap(QPixmap('Images/results.png'))

        self.datasetInteractionButton = QPushButton("Dataset Interaction")
        self.datasetInteractionButton.setEnabled(False)
        self.datasetInteractionButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.datasetInteractionButton.setFixedHeight(30)
        self.datasetInteractionButton.clicked.connect(self.dataset_interaction_page_button_clicked)
        self.resultButton = QPushButton("Result Evaluation")
        self.resultButton.setEnabled(False)
        self.resultButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.resultButton.setFixedHeight(30)
        self.resultButton.clicked.connect(self.dataset_result_page_button_clicked)

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
        browseDatasetButton.clicked.connect(self.button_was_clicked)
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
        cleanLayout = QHBoxLayout()
        cleanLayout.setSpacing(0)
        cleanWidget = QWidget()
        cleanButton = QPushButton("Clean")
        cleanButton.setStyleSheet(self.ss.pageButtonStyle())
        cleanButton.setFixedSize(100, 30)
        cleanButton.clicked.connect(self.clean_button_clicked)




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
        tabLayout.addWidget(self.aboutButton)
        tabLayout.addWidget(self.helpButton)
        tabLayout.addWidget(self.acknowledgementButton)
        tabLayout.addWidget(settingsLabel)
        tabLayout.addWidget(self.paramSetButton)
        tabLayout.addWidget(cleaningLabel)
        tabLayout.addWidget(self.cleaningButton)
        tabLayout.addWidget(resultsLabel)
        tabLayout.addWidget(self.datasetInteractionButton)
        tabLayout.addWidget(self.resultButton)

        # Page based layouts setup
        aboutWidget = QWidget()
        aboutWidget.setStyleSheet("background-color: white")
        helpWidget = QWidget()
        helpWidget.setStyleSheet("background-color: white")
        acknowledgementWidget = QWidget()
        acknowledgementWidget.setStyleSheet("background-color: white")
        paramWidget = QWidget()
        paramWidget.setStyleSheet("background-color: white")
        cleaningWidget = QWidget()
        cleaningWidget.setStyleSheet("background-color: white")
        interactWidget = QWidget()
        interactWidget.setStyleSheet("background-color: white")
        resultsWidget = QWidget()
        resultsWidget.setStyleSheet("background-color: white")

        # About Page Setup
        aboutLayout = QGridLayout(aboutWidget)
        aboutLayout.addWidget(welcomeText)
        aboutLayout.addWidget(aboutText)
        aboutLayout.addWidget(spacers.s1)

        # Info Page Setup
        infoLayout = QGridLayout(helpWidget)
        infoLayout.addWidget(helpText)

        # Acknowledgement Page Setup
        acknowledgementLayout = QGridLayout(acknowledgementWidget)
        acknowledgementLayout.addWidget(acknowledgementText)

        # Param Page Setup
        paramLayout = QVBoxLayout(paramWidget)
        chooseWidget.setLayout(chooseLayout)
        browseWidget.setLayout(browseLayout)
        cleanWidget.setLayout(cleanLayout)
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
        cleanLayout.addWidget(spacers.s4)
        cleanLayout.addWidget(spacers.s5)
        cleanLayout.addWidget(cleanButton)
        paramLayout.addWidget(chooseWidget)
        paramLayout.addWidget(browseWidget)
        paramLayout.addWidget(spacers.s2)
        paramLayout.addWidget(cleanWidget)
        paramLayout.addWidget(spacers.s3)


        # Adding all pages to pageLayout
        self.pageLayout.addWidget(aboutWidget)
        self.pageLayout.addWidget(helpWidget)
        self.pageLayout.addWidget(acknowledgementWidget)
        self.pageLayout.addWidget(paramWidget)
        self.pageLayout.addWidget(cleaningWidget)

        mainLayout.addLayout(tabLayout, 1)
        mainLayout.addLayout(self.pageLayout, 4)



        keepDuplicatesCheckBox = QCheckBox()

        datasetCompareTextBox = QLineEdit()

        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)

    def about_button_clicked(self):
        self.resetSelectedButton()
        self.currentSelectedPage = 0
        self.aboutButton.setStyleSheet(self.ss.enabledButtonSelectedStyle())
        self.pageLayout.setCurrentIndex(0)

    def help_button_clicked(self):
        self.resetSelectedButton()
        self.currentSelectedPage = 1
        self.helpButton.setStyleSheet(self.ss.enabledButtonSelectedStyle())
        self.pageLayout.setCurrentIndex(1)

    def acknowledgement_button_clicked(self):
        self.resetSelectedButton()
        self.currentSelectedPage = 2
        self.acknowledgementButton.setStyleSheet(self.ss.enabledButtonSelectedStyle())
        self.pageLayout.setCurrentIndex(2)

    def param_button_clicked(self):
        self.resetSelectedButton()
        self.currentSelectedPage = 3
        self.paramSetButton.setStyleSheet(self.ss.enabledButtonSelectedStyle())
        self.pageLayout.setCurrentIndex(3)

    def clean_page_button_clicked(self):
        self.resetSelectedButton()
        self.currentSelectedPage = 4
        self.cleaningButton.setStyleSheet(self.ss.enabledButtonSelectedStyle())
        self.pageLayout.setCurrentIndex(4)

    def dataset_interaction_page_button_clicked(self):
        self.resetSelectedButton()
        self.currentSelectedPage = 5
        self.datasetInteractionButton.setStyleSheet(self.ss.enabledButtonSelectedStyle())
        self.pageLayout.setCurrentIndex(5)

    def dataset_result_page_button_clicked(self):
        self.resetSelectedButton()
        self.currentSelectedPage = 6
        self.resultButton.setStyleSheet(self.ss.enabledButtonSelectedStyle())
        self.pageLayout.setCurrentIndex(6)

    def rules_checkbox_clicked(self):
        if self.generateRuleCheckBox.isChecked():
            self.rulesTextBox.setEnabled(False)
            self.rulesTextBox.setText("buncha rules")
        else:
            self.rulesTextBox.setEnabled(True)
            self.rulesTextBox.setText("")

    #Clean button will reset pages for next dataset stuff
    def clean_button_clicked(self):
        self.datasetInteractionButton.setEnabled(False)
        self.datasetInteractionButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.resultButton.setEnabled(False)
        self.resultButton.setStyleSheet(self.ss.disabledButtonStyle())
        self.cleaningButton.setEnabled(True)
        self.cleaningButton.setStyleSheet(self.ss.enabledButtonStyle())
        self.resetSelectedButton()
        self.currentSelectedPage = 4
        self.cleaningButton.setStyleSheet(self.ss.enabledButtonSelectedStyle())
        self.pageLayout.setCurrentIndex(4)

    def resetSelectedButton(self):
        if self.currentSelectedPage == 0:
            self.aboutButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 1:
            self.helpButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 2:
            self.acknowledgementButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 3:
            self.paramSetButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 4:
            self.cleaningButton.setStyleSheet(self.ss.enabledButtonStyle())
        elif self.currentSelectedPage == 5:
            self.datasetInteractionButton.setStyleSheet(self.ss.enabledButtonStyle())
        else:
            self.resultButton.setStyleSheet(self.ss.enabledButtonStyle())


    def button_was_clicked(self):
        print("button was clicked")



    def outputFile(self, file):
        f = open(file, "r")
        return f.read()

    def openFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select Datasheet")
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setViewMode(QFileDialog.ViewMode.List)

        if file_dialog.exec():
            selected_directory = file_dialog.selectedFiles()[0]
            #To be continued


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
