#!/bin/bash


git --version 2>&1 >/dev/null
GIT_IS_AVAILABLE=$?

if [ $GIT_IS_AVAILABLE -eq 0 ]; then

  git clone https://github.com/bastoscorp/pvAlert

  cd pvAlert

  python3 -m venv ../pvAlert

  source bin/activate

  pip install -r requirements.txt

  deactivate

else
  echo "Install Git first"
fi

