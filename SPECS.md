# In-Memory Key-Value Store

Your task is to implement a simple in-memory key-value store. Plan your design according to the level specifications below.

To move to the next level, you need to pass all the tests at the current level.

---

## Level 1 — Basic Operations

Implement a key-value store that supports the following operations:

- `SET key value` — store `value` under `key`. Overwrites if key already exists.
- `GET key` — return the value for `key`, or `None` if it doesn't exist.
- `DELETE key` — remove `key` from the store. No-op if key doesn't exist.
- `COUNT value` — return the number of keys whose value equals `value`.

**Examples:**
```
SET a 1
GET a       → 1
GET b       → None
SET a 2
GET a       → 2
DELETE a
GET a       → None
SET a 1
SET b 1
COUNT 1     → 2
COUNT 2     → 0
```

---

## Level 2 — Command Parsing

Implement a `solution(queries)` function that:
- Accepts a list of command strings
- Parses and dispatches each command to the appropriate operation
- Returns a list of results for commands that produce output (`GET`, `COUNT`)
- Commands that don't produce output (`SET`, `DELETE`) are not included in the results

**Examples:**
```
solution(["SET a 1", "GET a", "COUNT 1", "DELETE a", "GET a"])
→ ["1", 1, None]
```

---

## Level 3 — Transactions

Add transaction support to the key-value store.

- `BEGIN` — start a new transaction.
- `COMMIT` — make all changes since the last `BEGIN` permanent. Closes all open transactions.
- `ROLLBACK` — undo all changes since the last `BEGIN`. Only undoes the most recent transaction level.

**Rules:**
- Transactions can be nested — a `BEGIN` inside an active transaction creates a new transaction level.
- `ROLLBACK` undoes only the most recent transaction level.
- `COMMIT` closes all open transaction levels at once.
- `ROLLBACK` with no active transaction is a no-op.
- `COMMIT` with no active transaction is a no-op.
- Changes made during a transaction take effect immediately — they are only undone if `ROLLBACK` is called.

**Examples:**
```
SET a 1
BEGIN
SET a 2
GET a           → 2
ROLLBACK
GET a           → 1

SET a 1
BEGIN
SET a 2
BEGIN
SET a 3
ROLLBACK
GET a           → 2
ROLLBACK
GET a           → 1

SET a 1
BEGIN
SET a 2
COMMIT
ROLLBACK        → no-op
GET a           → 2
```

---

## Level 4A — Backup & Restore

Add the ability to save and restore snapshots of the store.

- `BACKUP timestamp` — save the current state of the store, keyed by `timestamp`.
- `RESTORE timestamp` — restore the store to the state saved at `timestamp`. If no backup exists for `timestamp`, do nothing.

**Rules:**
- Backups persist after being restored — you can restore to the same backup multiple times.
- Restoring and then modifying the store does not affect the saved backup.
- `timestamp` is a string identifier (e.g. `"t1"`, `"t2"`).

**Examples:**
```
SET a 1
BACKUP t1
SET a 2
GET a           → 2
RESTORE t1
GET a           → 1
SET a 3
RESTORE t1
GET a           → 1

RESTORE t99     → no-op
```

---

## Level 4B — TTL / Expiration

Add support for values with a time-to-live (TTL).

- `SET key value` — store the value permanently (no expiry).
- `SET key value ttl current_time` — store the value with expiry at `current_time + ttl`.
- `GET key` — return the value regardless of expiry.
- `GET key current_time` — return the value only if it has not expired at `current_time`. Return `None` if expired or not found.

**Rules:**
- Time is always passed as a parameter — never use the system clock.
- A value expires when `current_time >= expiry_time`.
- A value with no TTL never expires.
- `ttl` and `current_time` are integers.

**Examples:**
```
SET a hello 10 5    # expires at 15
GET a 10            → hello
GET a 15            → None
GET a               → hello

SET b world
GET b 999           → world
GET b               → world
```
