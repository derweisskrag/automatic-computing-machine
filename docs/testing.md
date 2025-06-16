# How to Test?

## Objective

We want to test our code differently:

- test assets and all data associated with it will be stored in "./src/tests/testdata"
- integration tests: they test actual dataset, rather small unit tests. As such, we modify the "./bin/run_tests.ps1" to include only unittests or only integration tests
- I added the `requirements-dev.txt` to install necessary tools for testing
- Quick benchmark: `%time print("hi")` -> an example of quick benching single function. You can see them in action inside "./playground/test_dsa.ipynb". 

## Future?

I grab redis-py functions to utilize for my own benefit:

- timer as a dictionary: 


```python
@timer
def print_hello():
    print("hello")
```

- timer as a context manager:

```python
with Timer() as timer:
    print("hello")
```

There are more to it and I have to spend more days to fully utilize all their fancy tools. 

Of them, I liked:

```python
# Source: https://github.com/redis/redis-py/blob/master/tasks.py

@task
def devenv(c, endpoints="all"):
    """Brings up the test environment, by wrapping docker compose."""
    clean(c)
    cmd = f"docker compose --profile {endpoints} up -d --build"
    run(cmd)


@task
def build_docs(c):
    """Generates the sphinx documentation."""
    run("pip install -r docs/requirements.txt")
    run("make -C docs html")
```