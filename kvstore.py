class KVStore:
    def __init__(self):
        self.store = {}
        self.transactions = [] # we are storing each transaction dictionary here
    
    def set(self, key, val):
        if self.transactions and key not in self.transactions[-1]:
            # only need to save it if we haven't already (even if it's None, we need that for rollback)
            self.transactions[-1][key] = self.store.get(key)
        self.store[key] = val
        
    def get(self, key):
        return self.store.get(key)
    
    def delete(self, key):
        if self.transactions and key not in self.transactions[-1]:
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
        else:
            print("Command not recognized.")