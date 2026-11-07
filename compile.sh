#!/bin/bash

nazwa_pliku="fnaf-python"

rm -rf build/ __pycache__/ main.spec
rm -rf dist/

pyinstaller --name=$nazwa_pliku \
            --onefile \
            --noconsole \
            --add-data "rsc:rsc" \
            --clean \
            src/main.py

./dist/$nazwa_pliku
