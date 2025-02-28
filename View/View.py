from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QPixmap, QPalette, QColor
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
    QGridLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IHCS")
        self.setFixedSize(800, 500)

        # Tab UI Elements
        titleText = QLabel("IHCS")
        font = titleText.font()
        font.setPointSize(30)
        titleText.setFont(font)
        titleText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        introLabel = QLabel()
        introLabel.setPixmap(QPixmap('Images/intro.png'))

        aboutButton = QPushButton("About")
        aboutButton.setStyleSheet(self.enabledButtonStyle())
        aboutButton.clicked.connect(self.about_button_clicked)

        helpButton = QPushButton("Help")
        helpButton.setStyleSheet(self.enabledButtonStyle())
        helpButton.clicked.connect(self.help_button_clicked)

        acknowledgementButton = QPushButton("Acknowledgements")
        acknowledgementButton.setStyleSheet(self.enabledButtonStyle())
        acknowledgementButton.clicked.connect(self.acknowledgement_button_clicked)

        settingsLabel = QLabel()
        settingsLabel.setPixmap(QPixmap('Images/settings.png'))

        paramSetButton = QPushButton("Parameter Setting")
        paramSetButton.setStyleSheet(self.enabledButtonStyle())

        cleaningLabel = QLabel()
        cleaningLabel.setPixmap(QPixmap('Images/cleaning.png'))

        cleaningButton = QPushButton("Hybrid Data Cleaning System")
        cleaningButton.setEnabled(False)
        cleaningButton.setStyleSheet(self.disabledButtonStyle())

        resultsLabel = QLabel()
        resultsLabel.setPixmap(QPixmap('Images/results.png'))

        datasetInteractionButton = QPushButton("Dataset Interaction")
        datasetInteractionButton.setEnabled(False)
        datasetInteractionButton.setStyleSheet(self.disabledButtonStyle())
        resultButton = QPushButton("Result Evaluation")
        resultButton.setEnabled(False)
        resultButton.setStyleSheet(self.disabledButtonStyle())

        # About UI Elements
        aboutText = QLabel("Here's what the project is about")
        aboutText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Help UI Elements
        helpText = QLabel("Here's how to use the project")
        helpText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Acknowledge UI Elements
        acknowledgementText = QLabel("Here's the people that helped bring this together")
        acknowledgementText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        # Param UI Elements

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
        aboutLayout.addWidget(aboutText)

        # Info Page Setup
        infoLayout = QGridLayout(helpWidget)
        infoLayout.addWidget(helpText)

        # Acknowledgement Page Setup
        acknowledgementLayout = QGridLayout(acknowledgementWidget)
        acknowledgementLayout.addWidget(acknowledgementText)

        # Adding all pages to pageLayout
        self.pageLayout.addWidget(aboutWidget)
        self.pageLayout.addWidget(helpWidget)
        self.pageLayout.addWidget(acknowledgementWidget)

        mainLayout.addLayout(tabLayout, 1)
        mainLayout.addLayout(self.pageLayout, 4)

        datasetTextBox = QLineEdit()
        rulesTextBox = QLineEdit()
        generateRuleCheckBox = QCheckBox()

        generateRuleCheckBox.setCheckState(Qt.CheckState.Checked)

        generateRuleCheckBox.setText("This is a checkbox")

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

    def enabledButtonStyle(self):
        return """
            QPushButton {
                background-color: transparent;
                color: black;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: rgba(100, 100, 255, 100);  /* Semi-transparent blue */
                border-radius: 10px;
            }
        """

    def disabledButtonStyle(self):
        return """
                    QPushButton {
                        background-color: transparent;
                        color: grey;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: rgba(100, 100, 255, 100);  /* Semi-transparent blue */
                        border-radius: 10px;
                    }
                """


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
