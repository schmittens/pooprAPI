#!flask/bin/python
import pymysql

#from log import logger


class SQL:
    def __init__(self, query, fieldNames):
        self.host = r"159.203.20.247"
        self.user = r"pooprDBr"
        self.pw = r"lA5mOfez9MHF0IGQ"
        self.db = r"poopr_do"
        self.port = 3306

        self.query = query.encode("utf-8")
        self.fieldNames = fieldNames
        self.returnResult = []

    def connect(self):
        #logger.logInfo("Establishing DB connection", False)

        self.connection = pymysql.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db, autocommit=True)
        self.cursor = self.connection.cursor()
        self.conn = self.cursor

        #logger.logInfo("DB connection established", False)
        return True

    def runQuery(self):
        #logger.logInfo("Running query", False)

        self.conn.execute(self.query)
        self.result = self.conn.fetchall()

        #logger.logInfo("Query run", False)
        return True

    def cleanup(self):
        #logger.logInfo("Initiating cleanup", False)

        if self.cursor.rowcount == 0:
            self.returnResult = [{"error": "no result"}]
        elif len(self.result) == 0:
            self.returnResult = [{"success": "row updated or created"}]

        else:
            for item in self.result:
                self.returnResult.append(dict(zip(self.fieldNames, item)))

        #logger.logInfo(self.returnResult)

        #logger.logInfo("Closing connection to DB", False)
        self.connection.close()

        #logger.logInfo("Closing cursor", False)
        self.cursor.close()

        #logger.logInfo("Cleanup complete", False)
        return self.returnResult

    def cleanup2(self):
        self.connection.close()
        self.cursor.close()
        return self.result

    def run(self):
        #logger.logInfo("Starting DB Lookup", False)

        try:
            self.connect()
            try:
                self.runQuery()
                try:
                    return self.cleanup()
                except Exception as e:
                    raise e
            except Exception as e:
                raise e
        except ConnectionError as e:
            raise e
            return "Error"


