```bash
rm -rf dist/*
python -m build
twine check dist/*
twine upload dist/*
```