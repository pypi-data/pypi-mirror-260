## Build and Publish

```bash
rm -rf dist/*
python -m build
twine check dist/*
twine upload dist/*
```

## Setup

```bash
# update and pin requirements
uv pip compile pyproject.toml --all-extras -o requirements.txt

# install dependencies
uv pip sync requirements.txt

# install pre-commit hooks
pre-commit install
```

TODO: Figure out explicit dependency version constraining in setup based on requirements.txt