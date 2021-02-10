import os, random, sys
from pathlib import Path

class TestCsvs():

    def __init__(self, folder):
        self.folder = Path(folder)
        self.csvList = []
        self.importFilesToCsvList()


    def importFilesToCsvList(self):
        try:
            # os.walk() retrieves the 3-tuple root, dirs, files of the given path.
            for root, dirs, files in os.walk(self.folder):
                # append all files in the test csv folder to the csv list.
                for f in files:
                    if f.endswith('.csv'):
                        self.csvList.append(f)
                    else:
                        continue
            return
        except:
            return 'An error has occurred retreiving test csv files.'

    def getRandomCsv(self):
        randomcsv = self.csvList[random.randint(-1, len(self.csvList)-1)]
        return os.path.join(self.folder, randomcsv)
