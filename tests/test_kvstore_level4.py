import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from kvstore import KVStore
from kvstore_level4 import KVStoreLevel4

# Test set
store = KVStore()
store.set('a', '1')

# Test get
assert store.get('a') == '1'
assert store.get('nonexistent') == None

# Test set
store.set('a', '2')
assert store.get('a') == '2'

# Test delete
store.delete('nonexistent')
store.delete('a')
assert store.get('a') == None

# Test count
store.set('a', '1')
store.set('b', '1')
assert store.count('1') == 2

store.set('c', '1')
store.set('d', '2')
assert store.count('1') == 3

store.set('a', '2')
assert store.count('1') == 2

# Test transactions
store = KVStore()
store.set('a', '1')
store.begin()
store.set('a', '4')
store.set('b', '1')
store.set('c', '3')
store.rollback()
assert store.get('a') == '1'
assert store.count('1') == 1
assert store.count('4') == 0
assert store.get('b') == None

store.begin()
store.set('b', '2')
store.commit()
store.rollback()
assert store.get('b') == '2'
assert store.count('2') == 1

# Test nested transactions
store = KVStore()
store.set('a', '1')

store.begin()
store.set('a', '2')

store.begin() # create nested begin
store.set('a', '3')

store.rollback() # roll back inner transaction
assert store.get('a') == '2' # should be '2' from outer transaction

store.rollback() # roll back outer transaction
assert store.get('a') == '1' # should be original '1'

# Test command parsing
store = KVStore()
store.execute("SET a 1") # None (or nothing)
print(store.execute("GET a")) # should print 1
assert store.get('a') == '1'
print(store.execute("COUNT 1")) # should print 1
store.execute("BEGIN")
store.execute("SET a 2")
store.execute("ROLLBACK")
store.execute("GET a") # should print 1
assert store.get('a') == '1'

### Extended test cases ###
# Multiple sets
store = KVStore()
store.set('a', '1')
store.begin()
store.set('a', '2')
store.set('a', '3') # modifying 'a' again
store.set('a', '4') # and again
store.rollback()
assert store.get('a') == '1'

# Delete and set same key, then rollback
store = KVStore()
store.set('a', '1')
store.begin()
store.delete('a')
store.set('a', '999') # set 'a' again
store.rollback()
assert store.get('a') == '1'

# Empty transactions, ensure no errors are thrown
store = KVStore()
store.begin()
store.rollback()

# More nested with complex ops
store = KVStore()
store.set('a', '1')
store.begin()
store.set('a', '2')
store.delete('a')
store.begin() # nested
store.set('a', '3')
store.rollback() # inner rollback, 'a' returns to None
assert store.get('a') == None
store.rollback() # outer rollback, 'a' returns to '1'
assert store.get('a') == '1'

# Backup and restore - basic
store = KVStore()
store.set('a', '1')
store.execute("BACKUP t1")
store.set('a', '2')
assert store.get('a') == '2'
store.execute("RESTORE t1")
assert store.get('a') == '1'

# Restore nonexistent timestamp - should do nothing
store = KVStore()
store.set('a', '1')
store.execute("RESTORE t99")
assert store.get('a') == '1'

# Restore twice from same backup - backup persists after restore
store = KVStore()
store.set('a', '1')
store.execute("BACKUP t1")
store.set('a', '2')
assert store.get('a') == '2'
store.execute("RESTORE t1")
assert store.get('a') == '1'
store.set('a', '2')
assert store.get('a') == '2'
store.execute("RESTORE t1")
assert store.get('a') == '1'

# Rollback with no active transaction - should do nothing
store = KVStore()
store.set('a', '1')
store.rollback()
assert store.get('a') == '1'

## Level 4 Cases
store = KVStoreLevel4()
store.execute('SET a hello 10 5') # expires at 15
assert store.execute('GET a 10') == 'hello' # not expired yet
assert store.execute('GET a 15') == None # expired
assert store.execute('GET a') == 'hello' # no timestamp, should return regardless

store.execute('SET b world') # no TTL, permanent
assert store.execute('GET b 999') == 'world' # should still return even with timestamp
