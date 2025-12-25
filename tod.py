# Built-in Modules
import json, random

# -----------------------------------------------------------------------
# TRUTH AND DARE STATEMENTS:
# Used to fetch and randomly choose dares,
# Statements are fetched from statements.json.
# -----------------------------------------------------------------------

class TodStatements:
    # Fecthes Statements
    def __init__(self):
        with open("statements.json", "r") as file:
            data = json.load(file)
        
        self.TRUTHS = data["TRUTHS"]
        self.DARES = data["DARES"]
    
    # Grabbing a dare
    def get_dare(self):
        if len(self.DARES) == 0:
            self.refetch_statements("DARE")
        return self.DARES.pop(random.randrange(len(self.DARES)))
    
    # Grabbing a truth
    def get_truth(self):
        if len(self.TRUTHS) == 0:
            self.refetch_statements("TRUTH")
        return self.TRUTHS.pop(random.randrange(len(self.TRUTHS)))
    
    # Refetching Statements in case they exhaust
    def refetch_statements(self, type):
        with open("statements.json", "r") as file:
            data = json.load(file)
        
        if type == "DARE":
            self.DARES = data["DARES"]
        elif type == "TRUTH":
            self.TRUTHS = data["TRUTHS"]

    def debug(self):
        print(self.TRUTHS, self.DARES)