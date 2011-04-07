#!/bin/bash -x

# install requirements if requirements.txt is newer than the virtualenv (assuming virtualenv has something in)
if [ ! -d "/home/jenkins/virtualenvs/${JOB_NAME}" ] || [ "${WORKSPACE}/requirements.txt" -nt "/home/jenkins/virtualenvs/${JOB_NAME}" ]; then
  mkdir -p /home/jenkins/virtualenvs
  mkdir -p /home/jenkins/pip-cache
  rm -rf "/home/jenkins/virtualenvs/${JOB_NAME}"
  virtualenv "/home/jenkins/virtualenvs/${JOB_NAME}"
  pip install --download-cache=/home/jenkins/pip-cache -E "/home/jenkins/virtualenvs/${JOB_NAME}" -r "${WORKSPACE}/requirements.txt"
fi

source "/home/jenkins/virtualenvs/${JOB_NAME}/bin/activate"

PYTHONPATH=py nosetests -w test