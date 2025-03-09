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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IHCS")
        self.setFixedSize(800, 500)
        spacers = Spacer()
        ss = StyleSheet()

        # Tab UI Elements
        titleText = QLabel("IHCS")
        font = titleText.font()
        font.setPointSize(30)
        titleText.setFont(font)
        titleText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        introLabel = QLabel()
        introLabel.setPixmap(QPixmap('Images/intro.png'))

        aboutButton = QPushButton("About")
        aboutButton.setStyleSheet(ss.enabledButtonStyle())
        aboutButton.clicked.connect(self.about_button_clicked)

        helpButton = QPushButton("Help")
        helpButton.setStyleSheet(ss.enabledButtonStyle())
        helpButton.clicked.connect(self.help_button_clicked)

        acknowledgementButton = QPushButton("Acknowledgements")
        acknowledgementButton.setStyleSheet(ss.enabledButtonStyle())
        acknowledgementButton.clicked.connect(self.acknowledgement_button_clicked)

        settingsLabel = QLabel()
        settingsLabel.setPixmap(QPixmap('Images/settings.png'))

        paramSetButton = QPushButton("Parameter Setting")
        paramSetButton.setStyleSheet(ss.enabledButtonStyle())
        paramSetButton.clicked.connect(self.param_button_clicked)

        cleaningLabel = QLabel()
        cleaningLabel.setPixmap(QPixmap('Images/cleaning.png'))

        cleaningButton = QPushButton("Hybrid Data Cleaning System")
        cleaningButton.setEnabled(False)
        cleaningButton.setStyleSheet(ss.disabledButtonStyle())

        resultsLabel = QLabel()
        resultsLabel.setPixmap(QPixmap('Images/results.png'))

        datasetInteractionButton = QPushButton("Dataset Interaction")
        datasetInteractionButton.setEnabled(False)
        datasetInteractionButton.setStyleSheet(ss.disabledButtonStyle())
        resultButton = QPushButton("Result Evaluation")
        resultButton.setEnabled(False)
        resultButton.setStyleSheet(ss.disabledButtonStyle())

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
        datasetTextBox = QLineEdit()
        datasetTextBox.setStyleSheet("background-color: white")
        datasetTextBox.setMaximumWidth(370)
        browseDatasetButton = QPushButton("Browse...")
        browseDatasetButton.setStyleSheet(ss.browseButtonStyle())
        browseDatasetButton.clicked.connect(self.button_was_clicked)
        rulesText = QLabel("Rules:")
        rulesTextBox = QLineEdit()
        rulesTextBox.setStyleSheet("background-color: white")
        rulesTextBox.setMaximumWidth(370)
        browseRulesButton = QPushButton("Browse...")
        browseRulesButton.setStyleSheet(ss.browseButtonStyle())
        generateRuleCheckBox = QCheckBox()
        generateRuleCheckBox.setCheckState(Qt.CheckState.Checked)
        generateRuleCheckBox.setText("Generate rules automatically")
        generateRuleCheckBox.setStyleSheet("background-color: transparent")
        cleanLayout = QHBoxLayout()
        cleanLayout.setSpacing(0)
        cleanWidget = QWidget()
        cleanButton = QPushButton("Clean")
        cleanButton.setStyleSheet(ss.pageButtonStyle())
        cleanButton.setFixedSize(100, 30)




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
        tabLayout.addWidget(aboutButton)
        tabLayout.addWidget(helpButton)
        tabLayout.addWidget(acknowledgementButton)
        tabLayout.addWidget(settingsLabel)
        tabLayout.addWidget(paramSetButton)
        tabLayout.addWidget(cleaningLabel)
        tabLayout.addWidget(cleaningButton)
        tabLayout.addWidget(resultsLabel)
        tabLayout.addWidget(datasetInteractionButton)
        tabLayout.addWidget(resultButton)

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
        datasetLayout.addWidget(datasetTextBox)
        datasetLayout.addWidget(browseDatasetButton)
        datasetLayout.setSpacing(1)
        rulesLayout.addWidget(rulesText)
        rulesLayout.addWidget(rulesTextBox)
        rulesLayout.addWidget(browseRulesButton)
        rulesLayout.setSpacing(1)
        browseLayout.addWidget(paramInfoText)
        browseLayout.addWidget(datasetWidget)
        browseLayout.addWidget(rulesWidget)
        browseLayout.addWidget(generateRuleCheckBox)
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

        mainLayout.addLayout(tabLayout, 1)
        mainLayout.addLayout(self.pageLayout, 4)



        keepDuplicatesCheckBox = QCheckBox()

        datasetCompareTextBox = QLineEdit()

        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)

    def about_button_clicked(self):
        self.pageLayout.setCurrentIndex(0)

    def help_button_clicked(self):
        self.pageLayout.setCurrentIndex(1)

    def acknowledgement_button_clicked(self):
        self.pageLayout.setCurrentIndex(2)

    def param_button_clicked(self):
        self.pageLayout.setCurrentIndex(3)

    def button_was_clicked(self):
        print("button was clicked")



    def outputFile(self, file):
        f = open(file, "r")
        return f.read()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
