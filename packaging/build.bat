python ./setup.py sdist bdist_wheel
twine check ./dist/*
twine upload dist/* --verbose
rd /s /q "dist"
rd /s /q "build"
rd /s /q "python_xmatters.egg-info"