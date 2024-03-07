# Wrensh

Wrensh is a library that allows you to process data in Python using UNIX / POSIX shell idioms.

Currently it only supports interactive or batch processing of text in-memory. The goal is to
provide a range of modes that allow you to do almost anything that is quick and intuitive to shell
users, but in Python environments.

## Using Wrensh

Install it:

```bash
pip install wrensh
```

Import it:

```python
from wrensh import text
```

And go:

```python
text.cat("input.csv").grep(",active,").sort().uniq().append("output.csv")
```

## Starting Pipelines

Each of the following options returns a new pipeline.

From in-memory data:

```python
data = """key,value
key1,value1
key2,value2
"""

sh = text.echo(data.split("\n"))
# OR
sh = text.echo("A string to test a regex command")
```

From a file:

```python
sh = text.cat("data.csv")
```

## Processing Pipelines

You can use many POSIX commands on your pipelines:

```python
sh.grep("a Python regular expression") # Filters out records that match the reg

sh.head()  # Passes at most the first 10 records
sh.head(2) # Passes at most the first 2 records
sh.tail()  # Passes at most the last 10 records
sh.head(2) # Passes at most the last 2 records

sh.sort() # Sorts the records
sh.uniq() # Deduplicates the records
```

And you can use higher-order functions:

```python
sh.map(lambda x: x.upper()) # The lambda is called once for each record, and can return None to
                            # ignore it, or it can return a record, or a list of records
```

## Ending Pipelines

Each of the following functions can be used at the end of your pipeline.

Create a file and write the pipeline's contents:

```python
sh.redirect("output.csv") # Create or truncate the file
sh.append("output.csv") # Create or append to the file
```

You can also get the output as a string:

```python
str(pipe)
```

Or access the raw list of strings used interally:

```python
sh.pipe
```

## Future Work

Ideas for future work include:

- negative numbers to tail and head
- additional POSIX tools (awk, cut, expand, unexpand, tr, sed, curl
- additional higher order functions (filter, apply)
- maybe support for binary formats: zipping, conversions
- streaming
- multiprocessing

Please submit an issue (or pull request) if you have feedback or input.
