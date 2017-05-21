## Development Helper Notes


#### Upload new release to **testpypi**

1. Increment release in `setup.py`
2. run `python setup.py sdist`
3. run `twine upload -r test dist/PACKAGENAME-VERSION.tar.gz`


#### Install package from **testpypi**

`pip install --extra-index-url https://testpypi.python.org/pypi insults`
