# Click Framework - Modern CLI in Python

> **Source**: [Click Documentation](https://click.palletsprojects.com/)
> **Day 8 - Backend Mastery: CLI Task Manager (Part 1)**

---

## What is Click?

**Click** is a Python package for creating beautiful command-line interfaces with minimal code. It uses decorators for clean, declarative syntax.

**Key Features:**
- Arbitrary nesting of commands
- Automatic help page generation
- Lazy loading of subcommands
- Built-in parameter validation

**Install:**
```bash
pip install click
```

---

## Basic Command

```python
import click

@click.command()
@click.option("--count", default=1, help="Number of greetings")
@click.argument("name")
def hello(count, name):
    """Greet NAME for COUNT times."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    hello()
```

**Usage:**
```bash
$ python hello.py World --count=3
Hello, World!
Hello, World!
Hello, World!
```

---

## Arguments vs Options

| Feature | Argument | Option |
|---------|----------|--------|
| Required | Yes (default) | No (default) |
| Naming | Positional | `--name` / `-n` |
| Use case | Primary input | Modifiers |

```python
@click.command()
@click.argument("filename")  # Required positional
@click.option("--output", "-o", default="out.txt")  # Optional flag
def process(filename, output):
    click.echo(f"Processing {filename} -> {output}")
```

---

## Common Option Types

```python
# String (default)
@click.option("--name", type=str)

# Integer
@click.option("--count", type=int, default=1)

# Float
@click.option("--rate", type=float)

# Boolean flag
@click.option("--verbose", "-v", is_flag=True)

# Choice from list
@click.option("--format", type=click.Choice(["json", "csv"]))

# File
@click.option("--config", type=click.File("r"))

# Path
@click.option("--output", type=click.Path(exists=False))
```

---

## Command Groups (Subcommands)

```python
import click

@click.group()
def cli():
    """Task Manager CLI."""
    pass

@cli.command()
@click.argument("title")
def add(title):
    """Add a new task."""
    click.echo(f"Added: {title}")

@cli.command()
@click.option("--all", is_flag=True)
def list(all):
    """List all tasks."""
    click.echo("Listing tasks...")

@cli.command()
@click.argument("task_id", type=int)
def complete(task_id):
    """Mark task as complete."""
    click.echo(f"Completed task #{task_id}")

if __name__ == "__main__":
    cli()
```

**Usage:**
```bash
$ python task.py add "Buy groceries"
Added: Buy groceries

$ python task.py list --all
Listing tasks...

$ python task.py complete 1
Completed task #1
```

---

## Prompting for Input

```python
@click.command()
@click.option("--name", prompt="Your name", help="Your name")
@click.password_option()  # Hidden password input
def login(name, password):
    click.echo(f"Logging in as {name}")
```

---

## Confirmation

```python
@click.command()
@click.confirmation_option(prompt="Are you sure?")
def delete_all():
    click.echo("Deleted everything!")
```

---

## Styled Output

```python
click.echo("Normal text")
click.secho("Success!", fg="green", bold=True)
click.secho("Warning!", fg="yellow")
click.secho("Error!", fg="red", bold=True)
```

---

## Click vs argparse

| Feature | argparse | Click |
|---------|----------|-------|
| Style | Imperative | Decorators |
| Learning curve | Moderate | Easy |
| Subcommands | Verbose | Clean |
| Third-party | No | Yes (`pip install`) |
| Help text | Auto | Auto + better |

**When to use argparse:** Standard library, no dependencies.
**When to use Click:** Cleaner code, complex CLIs.

---

## Key Takeaways

| Concept | Syntax |
|---------|--------|
| Command | `@click.command()` |
| Option | `@click.option("--name")` |
| Argument | `@click.argument("name")` |
| Boolean flag | `is_flag=True` |
| Group (subcommands) | `@click.group()` |
| Styled output | `click.secho()` |
