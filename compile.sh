#!/bin/bash

nazwa_pliku="fnaf-python"

rm -rf build/ dist/ __pycache__/ main.spec

# budowa biblioteki c
cd random_c

python3 setup.py build_ext --inplace
cp random_native*.so ../src/
rm random_native*.so
cd ..

pyinstaller --name=$nazwa_pliku \
            --onefile \
            --noconsole \
            --add-data "rsc:rsc" \
            --clean \
            src/main.py

./dist/$nazwa_pliku
