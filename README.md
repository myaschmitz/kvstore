# KVStore

A simple in-memory key-value store implemented in Python.

## Features

- Basic CRUD operations — set, get, delete, and count values
- Command parsing — accepts string commands for all operations
- Transaction support — begin, commit, and rollback changes with full nested transaction support
- Backup & restore — save and restore snapshots of the store
- TTL / expiration — store values with a time-to-live that expires at a given timestamp

## Usage

```python
store = KVStore()

store.set('a', '1')
store.get('a')        # '1'
store.count('1')      # 1
store.delete('a')

# Transactions
store.set('a', '1')
store.begin()
store.set('a', '2')
store.rollback()
store.get('a')        # '1'

# Command parsing
store.execute("SET a 1")
store.execute("GET a")        # '1'
store.execute("BEGIN")
store.execute("SET a 2")
store.execute("ROLLBACK")
store.execute("GET a")        # '1'
```

## Running Tests

```bash
python tests/test_kvstore.py
python tests/test_kvstore_level4.py
```