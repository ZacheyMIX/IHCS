import time

class ViewModel():

    formatList = {"name": "object", "age": "int", "date": "date/time", "salary": "int"}
    newFormatList = []
    progress = 0

    def __init__(self):
        super().__init__()

    def startFormat(self, file, rules):
        ruleList = rules.split(", ")

    def startClean(self):
        print("stuff")

    def beginProgress(self):
        self.progress += 25