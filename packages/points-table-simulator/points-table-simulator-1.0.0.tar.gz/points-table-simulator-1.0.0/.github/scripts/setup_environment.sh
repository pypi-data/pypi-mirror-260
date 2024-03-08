#!/bin/bash

bash create_venv.sh
source venv/bin/activate
if [ "$1" == 'pylint_check' ]; then
    pip install pylint
elif [ "$1" == 'pyright_check' ]; then
    pip install pyright
elif [ "$1" == 'unittest_check' ]; then
    pip install pytest
else
    pip install isort
fi
