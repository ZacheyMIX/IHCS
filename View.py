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
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IHCS")
        self.setFixedSize(900, 600)

        titleText = QLabel("IHCS")
        font = titleText.font()
        font.setPointSize(30)
        titleText.setFont(font)
        titleText.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        #introImage = QLabel().setPixmap(QPixmap('folder.png'))
        introImage = QLabel("Stuff")
        introText = QLabel("INTRO")

        aboutButton = QPushButton("About")
        aboutButton.setStyleSheet(self.buttonStyle())
        aboutButton.clicked.connect(self.the_button_was_clicked)

        helpButton = QPushButton("Help")
        helpButton.setStyleSheet(self.buttonStyle())

        acknowlegementsButton = QPushButton("Acknowledgements")
        acknowlegementsButton.setStyleSheet(self.buttonStyle())

        settingImage = QLabel().setPixmap(QPixmap('setting.png'))
        settingText = QLabel("SETTING")

        paramSetButton = QPushButton("Parameter Setting")
        paramSetButton.setStyleSheet(self.buttonStyle())

        computerImage = QLabel().setPixmap(QPixmap('computer.png'))
        cleaningText = QLabel("CLEANING")

        cleaningButton = QPushButton("Hybrid Data Cleaning System")
        cleaningButton.setStyleSheet(self.buttonStyle())

        resultsText = QLabel("RESULTS")

        datasetInteractionButton = QPushButton("Dataset Interaction")
        datasetInteractionButton.setStyleSheet(self.buttonStyle())
        resultButton = QPushButton("Result Evaluation")
        resultButton.setStyleSheet(self.buttonStyle())

        mainLayout = QHBoxLayout()
        tabLayout = QVBoxLayout()
        introLayout = QHBoxLayout()
        settingLayout = QHBoxLayout()
        cleaningLayout = QHBoxLayout()
        resultsLayout = QHBoxLayout()
        pageLayout = QVBoxLayout()

        container = QWidget()
        container.setStyleSheet("background-color: white")
        pageLayout.addWidget(container)

        introLayout.addWidget(introImage)
        introLayout.addWidget(introText)

        settingLayout.addWidget(settingImage)
        settingLayout.addWidget(settingText)

        cleaningLayout.addWidget(computerImage)
        cleaningLayout.addWidget(cleaningText)

        resultsLayout.addWidget(computerImage)
        resultsLayout.addWidget(resultsText)

        #Layout settings for left side layouts for tabs
        tabLayout.setSpacing(2)
        tabLayout.setContentsMargins(0,0,0,0)
        tabLayout.addWidget(titleText)
        tabLayout.addLayout(introLayout)
        tabLayout.addWidget(aboutButton)
        tabLayout.addWidget(helpButton)
        tabLayout.addWidget(acknowlegementsButton)
        tabLayout.addLayout(settingLayout)
        tabLayout.addWidget(paramSetButton)
        tabLayout.addLayout(cleaningLayout)
        tabLayout.addWidget(cleaningButton)
        tabLayout.addLayout(resultsLayout)
        tabLayout.addWidget(datasetInteractionButton)
        tabLayout.addWidget(resultButton)

        mainLayout.addLayout(tabLayout, 1)
        mainLayout.addLayout(pageLayout, 4)




        generateRuleCheckBox = QCheckBox()

        generateRuleCheckBox.setCheckState(Qt.CheckState.Checked)

        generateRuleCheckBox.setText("This is a checkbox")

        keepDuplicatesCheckBox = QCheckBox()

        datasetTextBox = QLineEdit()

        rulesTextBox = QLineEdit()

        datasetCompareTextBox = QLineEdit()

        widget = QWidget()
        widget.setLayout(mainLayout)

        self.setCentralWidget(widget)

    def the_button_was_clicked(self):
        print("Clicked!")

    def buttonStyle(self):
        return """
            QPushButton {
                background-color: transparent;
                border: 2px solid transparent;
                color: black;
                font-size: 16px;
                padding: 2px;
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