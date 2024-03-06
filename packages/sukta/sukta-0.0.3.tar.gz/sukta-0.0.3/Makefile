build:
	rm -rf dist/*
	python -m build

publish:
	if [ -d dist ]; then
		twine check dist/*
		twine upload dist/*
	fi

bumpver-patch:
	bumpver update --patch