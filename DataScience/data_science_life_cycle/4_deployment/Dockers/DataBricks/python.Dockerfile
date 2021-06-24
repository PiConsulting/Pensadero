FROM databricksruntime/python:latest

COPY python-requirements.txt ./
RUN /databricks/conda/envs/dcs-minimal/bin/pip install -r python-requirements.txt
