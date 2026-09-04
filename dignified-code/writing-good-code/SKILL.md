---
name: writing-good-code
description: Use when making a software implementation, no matter the language, or when asked for a refactor.
---

This are common patterns or anti-patterns that should be followed on ANY language.

## Discipline in helper functions

Single-use helper functions that obscure control flow and force readers to jump around are not correct. The add indirection without hiding real complexity.

bad:

```c
static bool check_buffer_valid(struct buf *b)
{
    if (!b || !b->data || b->len == 0)
        return false;
    return true;
}

int process(struct buf *b)
{
    if (!check_buffer_valid(b))
        return -EINVAL;

    /* ... actual work ... */
}
```

correct:

```c
int process(struct buf *b)
{
    if (!b || !b->data || b->len == 0)
        return -EINVAL;

    /* ... actual work ... */
}
```

bad:

```c
def should_skip(row):
    return row is None or row.get("deleted")

for row in rows:
    if should_skip(row):
        continue
    process(row)
```

## CRITICAL: Avoid functions depending on its parent context

A function that's only correct because of caller-set-up state, not its own parameters, hides its real contract, breaking silently when call order or context changes.

bad:

```js
let currentUser = null;

function login(u) {
  currentUser = u;
  renderGreeting(); // works only because currentUser was just set above
}

function renderGreeting() {
  document.getElementById("greeting").textContent = `Hi, ${currentUser.name}`;
}
```

### Pair variable's declaration with its use

Minimize variable lifetime/scope.

## C

**Bad**

```c
void process(int *data, int n) {
    int sum = 0;
    // ... 40 lines of unrelated setup ...
    for (int i = 0; i < n; i++) {
        sum += data[i];
    }
}
```

**Good**

```c
void process(int *data, int n) {
    // ... 40 lines of unrelated setup ...
    int sum = 0;
    for (int i = 0; i < n; i++) {
        sum += data[i];
    }
    printf("%d\n", sum);
}
```

## Java

**Bad**

```java
Connection conn = null;
// lots of other logic
conn = dataSource.getConnection();
ResultSet rs = conn.executeQuery(sql);
```

**Good**

```java
try (Connection conn = dataSource.getConnection();
     ResultSet rs = conn.executeQuery(sql)) {
    while (rs.next()) {
        process(rs);
    }
}
```

## Python

**Bad**

```python
def build_report(rows):
    total = 0
    formatted = []
    for row in rows:
        total += row.value
        formatted.append(str(row))
    # ... 30 lines later ...
    print(total)
```

**Good**

```python
def build_report(rows):
    formatted = [str(row) for row in rows]
    # ... other logic ...
    total = sum(row.value for row in rows)
    print(total)
```

## Go

**Bad**

```go
var err error
doStepOne()
doStepTwo()
result, err := doStepThree()
if err != nil {
    return err
}
```

**Good**

```go
if _, err := doStepOne(); err != nil {
    return err
}
if _, err := doStepTwo(); err != nil {
    return err
}
```

## Rust

**Bad**

```rust
let mut buffer = String::new();
// lots of unrelated code
read_into(&mut buffer);
println!("{}", buffer);
do_unrelated_work();
```

**Good**

```rust
// lots of unrelated code
{
    let mut buffer = String::new();
    read_into(&mut buffer);
    println!("{}", buffer);
}
do_unrelated_work();
```
