build:
	rm -rf dist/*
	python -m build

publish:
	test -d dist && \
	twine check dist/* && \
	twine upload dist/*

bumpver-patch:
	bumpver update --patch