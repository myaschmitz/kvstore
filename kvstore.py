class KVStore:
    def __init__(self):
        self.store = {}
        self.transactions = [] # we are storing each transaction dictionary here
        self.backups = {}
    
    def set(self, key, val):
        if self.transactions and key not in self.transactions[-1]:
            # save current key, value pair to transaction only if it's not already in there (even if it's None, we need that for rollback)
            self.transactions[-1][key] = self.store.get(key)
        self.store[key] = val
        
    def get(self, key):
        return self.store.get(key)
    
    def delete(self, key):
        if self.transactions and key not in self.transactions[-1]:
            # save current key, value pair to transaction only if it's not already in there
            # if already in there, that means we already performed a set or delete on this key within this transaction
            self.transactions[-1][key] = self.store.get(key)
        self.store.pop(key, None)
        
    def count(self, val):
        count = 0
        for v in self.store.values():
            if v == val:
                count += 1
        return count
    
    def begin(self):
        self.transactions.append({})
        
    def rollback(self):
        if self.transactions:
            snapshot = self.transactions.pop()
            
            for k, v in snapshot.items():
                if v == None:
                    self.store.pop(k, None)
                else:
                    self.store[k] = v

    def commit(self):
        self.transactions = []
        
    def backup(self, timestamp):
        self.backups[timestamp] = self.store.copy()
        
    def restore(self, timestamp):
        if self.backups:
            restore_backup = self.backups.get(timestamp, None)
            if restore_backup is not None:
                self.store = restore_backup.copy()
        
    def execute(self, command):
        parts = command.split()
        cmd = parts[0]
        
        if cmd == "GET":
            return self.get(parts[1])
        elif cmd == "SET":
            self.set(parts[1], parts[2])
        elif cmd == "DELETE":
            self.delete(parts[1])
        elif cmd == "COUNT":
            return self.count(parts[1])
        elif cmd == "BEGIN":
            self.begin()
        elif cmd == "ROLLBACK":
            self.rollback()
        elif cmd == "COMMIT":
            self.commit()
        elif cmd == "BACKUP":
            self.backup(parts[1])
        elif cmd == "RESTORE":
            self.restore(parts[1])
        else:
            print("Command not recognized.")