class KVStoreLevel4:
    def __init__(self):
        self.store = {}
        self.transactions = [] # we are storing each transaction dictionary here
        self.backups = {}
    
    def set(self, key, val, ttl=None, current_time=None):
        if self.transactions and key not in self.transactions[-1]:
            # save current key, value pair to transaction only if it's not already in there (even if it's None, we need that for rollback)
            self.transactions[-1][key] = self.store.get(key)
        if ttl and current_time:
            self.store[key] = (val, ttl + current_time)
        else:
            self.store[key] = (val, None)
        
    def get(self, key, current_time=None):
        kv = self.store.get(key)
        if current_time and kv and kv[1]:
            if current_time < kv[1]:
                # if key has ttl AND current time is BEFORE ttl, then it's possible
                return kv[0]
            else:
                return None
        return kv[0] if kv else None
    
    def delete(self, key):
        if self.transactions and key not in self.transactions[-1]:
            # save current key, value pair to transaction only if it's not already in there
            # if already in there, that means we already performed a set or delete on this key within this transaction
            self.transactions[-1][key] = self.store.get(key)
        self.store.pop(key, None)
        
    def count(self, val):
        count = 0
        for v in self.store.values():
            if v[0] == val:
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
            # GET value <current_time>
            if len(parts) > 2:
                return self.get(parts[1], int(parts[2]))
            return self.get(parts[1])
        elif cmd == "SET":
            # SET key value <ttl> <current_time>
            if len(parts) > 3:
                return self.set(parts[1], parts[2], int(parts[3]), int(parts[4]))
            return self.set(parts[1], parts[2])
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