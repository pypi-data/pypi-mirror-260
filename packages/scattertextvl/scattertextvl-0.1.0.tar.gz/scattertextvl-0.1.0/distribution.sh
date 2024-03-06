#!/usr/bin/env bash

#rm dist/*
#python setup.py sdist bdist_wheel
python -m pip install .
twine upload dist/*
#rm -rf build`
