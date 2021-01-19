import pandas as pd


class User:
    def __init__(self, ident):
        self.id = f"'{str(ident)}'"
        self.userdb = None
        self.day = None
        self.winnings = None

    def get_record(self):
        self.userdb = pd.read_csv('users.csv')
        if self.id not in self.userdb['id'].values.tolist():
            self.day = 0
            self.winnings = 0
            self.save(new=True)
        else:
            record = list(self.userdb[self.userdb['id'] == self.id].values)[0]
            self.day = record[1]
            self.winnings = record[2]

    def update_record(self, cash=0):
        self.day = self.day + 1
        self.winnings = self.winnings + cash
        self.save()

    def save(self, new=False):
        if new:
            self.userdb.loc[len(self.userdb)] = [self.id, 0, 0]
        else:
            self.userdb[self.userdb['id'] == self.id] = [[self.id, self.day, self.winnings]]
        self.userdb.to_csv('users.csv', index=False)

    @property
    def print_record(self):
        return [self.id, self.day, self.winnings]
