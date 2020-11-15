from testcsv import TestCsvs
import os, json

class CsvParser():
    def __init__(self, csv_file, seperator):
        """Initialize the CsvParser.

        Args:
            csv_file (String): path to a CSV file.
            sep (String): Seperator used in given CSV file.
        """
        self.csv_file = csv_file
        if not self.csv_file.endswith(".csv"):
            raise ValueError("wrong filetype")
        self.seperator = seperator
        self.headers = self.__getHeaders()
        self.data = self.__getData()
        self.dataDict = self.__convertDataToDict()
        self.json = self.__convertDataDictToJson()
        

    def __stripArray(self, inputList):
        """Strip the array of stringtags (' or ").

        Args:
            inputList (List): Array of strings with strings that still have stringtags.

        Returns:
            [List]: strings stripped of stringtags (' or ").
        """
        li = []
        for i in inputList:
            if i.startswith("\"") and i.endswith("\""):
                i = i.strip("\"")
            elif i.startswith("\'") and i.endswith("\'"):
                i = i.strip("\'")
            if "\n" in i:
                i = i.strip("\n")
            arr.append(i)
        return li

    def __getHeaders(self):
        """Gets all the headers from the given csv files.

        Returns:
            [List]: all the headers of the CSV file.
        """
        with open(self.csv_file, 'r') as c:
            headers = c.readline().split(self.seperator)
            stripped_headers = self.__stripArray(headers)
            return stripped_headers
    
    def __getData(self):
        """Gets all the data from the given csv file.

        Returns:
            [List]: Each row of the CSV file converted to a list.
        """
        data = []
        with open(self.csv_file, 'r') as c:
            lines = c.readlines()
            for line in lines:
                if line == lines[0]:
                    continue
                else:
                    stripped_data = self.__stripArray(line.split(self.seperator))
                    data.append(stripped_data)
        return data


    def __convertDataToDict(self):
        """Converts all entries to dictionaries with the headers as keys.

        Returns:
            [Dict]: dictionaries of all the CSV entries.
        """
        lineobjects = {}
        i = 0
        while i < len(self.data):
            for line in self.data:
                i2 = 0
                lineobject = {}
                while i2 < len(self.headers):
                    lineobject[self.headers[i2]] = line[i2]
                    i2 += 1
                lineobjects[i] = lineobject
                i += 1
        return lineobjects
    def __convertDataDictToJson(self):
        """Dump the data dictionary to json

        Returns:
            [List]: json format of self.dataDict
        """
        jsonData = json.dumps(self.dataDict)
        return jsonData


if __name__ == '__main__':
    testfolder = '2018-census-totals-by-topic-national-highlights-csv'
    myTestCsvs = TestCsvs(testfolder)

    
    # for csv in myTestCsvs.csvList:
    #     try:
    #         parsed = CsvParser(os.path.join(testfolder, csv), ",")
    #         print(f"\n{csv}")
    #         print(f"\n{parsed.dataDict}")
    #     except ValueError as e:
    #         print(f"Failed to parse {csv}, \n{e}")
    #     except:
    #         print(f"Failed to parse {csv}, error unknown")

    parsedCsv = CsvParser(myTestCsvs.getRandomCsv(), ",")
    print(parsedCsv.json)
    