'''
    psycopg2-test.py
    Jeff Ondich, 1 Oct 2013
    Modified by Amy Csizmar Dalal, 1 February 2016

    This is a short example of how to access a PostgreSQL database in Python.
'''

import psycopg2
import getpass

class DataSource:
    # for simple search
    # input (string) is just user input

    # for advanced search
    # input (list) contains parameters (or None) for id, privilege, license, tradeName
    # streetAddress, city, zip.vendorType, totalSaleLowerBound, totalSaleUpperBound
    def __init__(self):
        self.searchType = None
        database = 'yuq'
        user = 'yuq'
        password = getpass.getpass()
        try:
            self.connection = psycopg2.connect(database = database, user = user, password = password)
        except Exception as e:
            print('Connection error: ', e)
            exit()

    def initSearch(self, searchType, input):
        if searchType == "simple":
            # changes input to uppercases to ensure query runs properly
            if not input.isdigit():
                input = input.upper()
            self.searchType = simpleSearch(input,self.connection)
        elif searchType == "advanced":
            # changes input to uppercases 
            for i in range(len(input)):
                tempInp = input[i]
                if not tempInp.isdigit():
                    input[i] = tempInp.upper() 
            self.searchType = advancedSearch(input,self.connection)
        self.searchType.search()


class simpleSearch:
    def __init__(self,inputStr, connection):
        self.searchTerm = inputStr
        self.connection = connection

    def search(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM marijuanaVendor WHERE ID = '%s' OR Priviledge = '%s' OR license = '%s' OR tradeName = '%s' OR streetAddress = '%s' OR city = '%s' OR zip = '%s' OR vendorType = '%s';" % (self.searchTerm, self.searchTerm, self.searchTerm, self.searchTerm, self.searchTerm, self.searchTerm, self.searchTerm, self.searchTerm)
            cursor.execute(query)
            searchResult = cursor.fetchall()
            for row in searchResult:
                print(row)
            return searchResult
        except Exception as e:
            print('Cursor error', e)


class advancedSearch:
    def __init__(self, inputList, connection):
        self.connection = connection
        self.inputList = inputList
        self.totalSaleL = inputList[8]
        self.totalSaleU = inputList[9]
        self.origList = ['id','priviledge','license','tradeName','streetAddress','city','zip','vendorType','totalSale']


    def search(self):
        # Query the database
        try:
            cursor = self.connection.cursor()
            if self.includeTotalSale():
                query = self.queryWithTotalSale()
            else:
                query = self.queryWithoutTotalSale()
            cursor.execute(query)
            searchResult = cursor.fetchall()
            for row in searchResult:
                print(row)
            return searchResult
        except Exception as e:
            print('Cursor error', e)
            connection.close()
            exit()
            
        
    def includeTotalSale(self):
        # if user specifies neither total sale lower nor upper bound, return false
        if self.totalSaleL == "" and self.totalSaleU == "":
            return False
        # otherwise, if user specifies upper bound only, set lower bound to 0.0
        elif self.totalSaleL == "":
            self.totalSaleL = 0.0
        # otherwise if user specifies lower bound only, set upper bound to a large number
        elif self.totalSaleU == "":
            self.totalSaleU = 999999999.9
        return True
            
    
    
    def queryWithoutTotalSale(self):
        indices = []
        for t in range (len(self.inputList)):
            if self.inputList[t] != "":
                indices.append(t)
        query = "SELECT * FROM marijuanaVendor WHERE "
        #Update string "query", complies with SQL format of searching for a satisfying data.
        for i in indices:
            if i != indices[-1]:
                query += self.origList[i] + " = '" + str(self.inputList[i]) + "' AND "
            else:
                query += self.origList[i] + " = '" + str(self.inputList[i]) + "';"
        return query
            


    def queryWithTotalSale(self):
        indices = []
        for t in range (len(self.inputList)-2):
            if self.inputList[t] != "":
                indices.append(t)
        query = "SELECT * FROM marijuanaVendor WHERE "
        #Update string "query", complies with SQL format of searching for a satisfying data.
        for i in indices:
            query += self.origList[i] + " = '" + str(self.inputList[i]) + "' AND "
        query += "totalSale BETWEEN " + str(self.totalSaleL) + " AND " + str(self.totalSaleU) + ";"
        return query

        
    
def main():
    testSearch = DataSource()
    searchType = inputStr = "go"
    print("type quit! if want to quit")
    while inputStr!= "quit!" and searchType != "quit!":
        searchType = input("search type (simple/advanced): ")
        if searchType == "simple":
            inputStr = input("search term (if simple) or list (if advanced): ")
        elif searchType == "advanced":
            inputStr = []
            inputStr.append(input("ID: "))
            inputStr.append(input("priviledge: "))
            inputStr.append(input("license: "))
            inputStr.append(input("trade name: "))
            inputStr.append(input("street address: "))
            inputStr.append(input("city: "))
            inputStr.append(input("zip code: "))
            inputStr.append(input("vendor type: "))
            inputStr.append(input("total sale lower bound: "))
            inputStr.append(input("total sale upper bound: "))
        testSearch.initSearch(str(searchType), inputStr)
        

if __name__ == "__main__":
    main()


