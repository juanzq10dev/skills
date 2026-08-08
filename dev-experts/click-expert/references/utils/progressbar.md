---
title: `click.progressbar`
triggers:
  - "showing progress while a command processes many items"
  - "advancing a progress bar from an irregular or external loop"
  - "a progress bar shows no ETA"
  - "suppressing the progress bar in non-interactive runs"
---

# Progress bars

Docs: https://click.palletsprojects.com/en/stable/utils/

```python
with click.progressbar(users, label="Modifying user accounts") as bar:
    for user in bar:
        modify_the_user(user)
```

The ETA needs a length. Supply one when the iterable has no `len()`:

```python
with click.progressbar(users, length=number_of_users) as bar:
    for user in bar:
        modify_the_user(user)
```

For an external loop, give `length` and **no** iterable, then call `bar.update(n)`:

```python
with click.progressbar(length=total_size, label="Unzipping archive") as bar:
    for archive in zip_file:
        archive.extract()
        bar.update(archive.size)
```

The bar updates **after** each iteration, so the work is what is timed.

Useful keywords: `label`, `length`, `hidden` (8.2+, suppress rendering entirely),
`show_eta`, `show_percent`, `show_pos`, `item_show_func`, `fill_char`, `empty_char`,
`bar_template`, `width`, `file`, `color`, `update_min_steps`.

Click's own docs point at [tqdm](https://tqdm.github.io/) when the requirements exceed
this.

## Common Anti-Patterns

- `click.progressbar(generator)` without `length=` and then wondering where the ETA went →
  no length, no estimate.
- Building the whole list just to get a length → pass `length=` and keep streaming.
- Printing inside the loop with `print` → it corrupts the bar; use `bar.label` /
  `item_show_func`, or `click.echo` after the block.
- Leaving the bar on in CI → `hidden=True` when `not sys.stdout.isatty()`.
