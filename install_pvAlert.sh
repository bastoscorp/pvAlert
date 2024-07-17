#!/bin/bash

script_dir=`pwd`

python3 -m venv ../pvAlert

source bin/activate

pip install -r requirements.txt

deactivate