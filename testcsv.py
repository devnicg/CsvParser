import os, random
from pathlib import *

class TestCsvs():

    def __init__(self, folder):
        self.folder = Path(folder)
        self.csvList = []
        self.importFilesToCsvList()

    
    def importFilesToCsvList(self):
        try:
            # os.walk() retrieves root, dirs, files of the given path.
            for root, dirs, files in os.walk(self.folder):
                # append all files in the test csv folder to the csv list.
                for filename in files:
                    self.csvList.append(filename)
            return
        except:
            return 'An error has occurred retreiving test csv files.'

    def getRandomCsv(self):
        randomcsv = self.csvList[random.randint(-1, len(self.csvList))]
        # return the absolute path of a csv.
        return os.path.abspath(randomcsv)