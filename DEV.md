## Development Helper Notes


#### Upload new release to **testpypi**

1. Increment release in `setup.py`
2. run `python setup.py sdist`
3. run `twine upload -r test dist/PACKAGENAME-VERSION.tar.gz`

#### Upload new release to **pypi**

1. Increment release in `setup.py` (if not already done when uploading the test release)
2. run `python setup.py sdist` (if like above not already done)
3. run `twine upload -r pypi dist/PACKAGENAME-VERSION.tar.gz`

#### Install package from **testpypi**

`pip install --extra-index-url https://testpypi.python.org/pypi insults`
