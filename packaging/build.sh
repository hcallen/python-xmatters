python ./setup.py sdist bdist_wheel
twine check ./dist/*
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
rm -rf dist
rm -rf build
rm -rf python_xmatters.egg-info