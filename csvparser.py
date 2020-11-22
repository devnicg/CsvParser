from testcsv import TestCsvs
import os, json, sqlite3, sys

os.chdir(sys.path[0])

class CsvParser():
    def __init__(self, csv_file, seperator):
        """Initialize the CsvParser.

        Args:
            csv_file (String): path to a CSV file.
            sep (String): Seperator used in given CSV file.
        """
        self.csv_file = csv_file
        if not self.csv_file.endswith('.csv'):
            raise ValueError("wrong filetype")
        self.seperator = seperator
        self.headers = self.__getHeaders()
        self.data = self.__getData()
        self.dataDict = self.__convertDataToDict()
        self.json = self.__convertDataDictToJson()
        self.database_name = self.csv_file.replace('.csv', '.db')
        self.table_name = self.csv_file.rstrip('.csv')
        self.tablekeys = self.__generateSqlTableQuery()


    def __stripArray(self, inputList):
        """Strip the array of stringtags (' or ").

        Args:
            inputList (List): Array of strings with strings that still have stringtags.

        Returns:
            [List]: strings stripped of stringtags (' or ").
        """
        li = []
        for i in inputList:
            if "\n" in i:
                i = i.strip("\n")
            if i.startswith("\"") and i.endswith("\""):
                i = i.strip("\"")
            elif i.startswith("\'") and i.endswith("\'"):
                i = i.rstrip("\'").lstrip("\'")
            li.append(i)
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
        # indent=4 and sort_keys=True returns a nicely formated json
        jsonData = json.dumps(self.dataDict, indent=4, sort_keys=True)
        return jsonData

    def __generateSqlTableQuery(self):
        tablecolumns = "("
        for header in self.headers:
            if not header == self.headers[-1]:
                tablecolumns += f"{header}, "
            else:
                tablecolumns += f"{header})"
        return str(tablecolumns)


    def createDatabase(self):
        try:
            con = sqlite3.connect(self.database_name)
            cur = con.cursor()
            q = f"CREATE TABLE IF NOT EXISTS csvfile {self.tablekeys}"
            cur.execute(q)
            con.commit()
        except sqlite3.Error as e:
            return "Could not create database", e
        finally:
            if con:
                con.close()


    #dr = csv.DictReader(file, delimiter=";")
    #to_db = [(i['ObjectNummer'], i['Type'], i['Indienst'], i['Voornaam'], i['Naam'], i['Status'], i['Firma'], i['Afdeling'], i['Serienr'], i['FactuurDatum']) for i in dr]

    #def insertDataIntoDatabase(self):
    #    try:
    #        con = sqlite3.connect(self.database_name)
    #        cur = sqlite3.cursor()
    #        for d in

    def convertJsonToDatabase(self):
        try:
            database_name = self.database_name.rstrip(".db") + "_json.db"
            con = sqlite3.connect(database_name)
            cur = con.cursor()
            q = "CREATE TABLE IF NOT EXISTS csvtojson (id INTEGER PRIMARY KEY AUTOINCREMENT, jsondata json)"
            cur.execute(q)
            con.commit()
            qin = [(x, self.dataDict[x]) for x in self.dataDict]
            cur.executemany("INSERT INTO csvtojson values (?,?)", qin)
            con.commit()
        except sqlite3.Error as e:
            return f"Failed to create json database:\n {e}"
        else:
            if con:
                con.close()
                return "Succesfully created json database, inserted json into database and closed database connection."

if __name__ == "__main__":
    testfolder = '2018-census-totals-by-topic-national-highlights-csv'
    myTestCsvs = TestCsvs(testfolder)

    testparse = CsvParser(myTestCsvs.getRandomCsv(), ",")

    print(testparse.convertJsonToDatabase())
