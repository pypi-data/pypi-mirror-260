# The RelationalAI Python Library

This repo contains PyRel, the Python library for RelationalAI.

## Links
- [Getting Started](https://github.com/RelationalAI/relationalai-python/blob/main/docs/getting_started.md)
- [Video Demo](https://relationalai.slack.com/archives/C0652R3806T/p1699899660005289)
- [AT&T Demo (using Jupyter and graph vis!)](https://relationalai.slack.com/archives/C0652R3806T/p1702493565063899)

## Install

> :bulb: Want to try PyRel right away? Check out [`examples/`](./examples) for a ready-made project with a variety of usage samples.

### For Users

Before installing `relationalai-python`, make sure you have Python 3.10 or Python 3.11 and `pip` installed on your system. You can check this by running `python --version` at the command line. Other package management solutions should work but are not actively tested.

Begin by creating a folder for your PyRel project and navigating to it in your terminal. Then create a virtual environment and install the `relationalai` package:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
pip install relationalai
```

Create a config file for Azure or SPCS using the included CLI:

```bash
rai init
```

You can also inspect the status of your config file with `rai config:explain`.

Use it to build graph queries and rules in your project:

```python
import relationalai as rai

graph = rai.Graph("MyFirstGraph")
Movie = graph.Type("Movie")

# Add some movies to the graph
with graph.rule():
    Movie.add(title="The Mummy")
    Movie.add(title="The Mummy Returns")
    Movie.add(title="George of the Jungle")

# Retrieve data from the graph to use in python
with graph.query() as select:
    movie = Movie()
    results = select(movie, movie.title)

# Results are a dataframe, use any library or function you like to work with them.
print(results)
```

Documentation is available in the [`docs/`](./docs) directory.
For more examples, see [`examples/`](./examples).

### For Contributors

> :warning: Ensure you're in a virtual env to isolate dependencies and avoid hard to diagnose conflicts.

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

Install relationalai-python in editable mode with the dev dependencies included.

```bash
pip install -e .[dev]
```

### Building a Release

Follow the instructions above to install and activate a virtualenv.

```bash
python -m build
```

The resulting wheel and tarball will be in the `dist` directory.

## Config Notes

If you have the environment variable `RAI_PROFILE` set, that profile will be used instead of `default`.

## Examples

See [`examples/`](./examples).

## Testing

See [`src/gentest/`](./src/gentest).
