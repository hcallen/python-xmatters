python ./setup.py sdist bdist_wheel
twine check ./dist/*
twine upload dist/*
rm -rf dist
rm -rf build
rm -rf python_xmatters.egg-info