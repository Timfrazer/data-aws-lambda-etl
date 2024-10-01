ARG BASE_IMAGE=public.ecr.aws/lambda/python:3.12.2024.09.13.17
FROM ${BASE_IMAGE}

# Copy & install requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}/requirements.txt

RUN cd ${LAMBDA_TASK_ROOT} && \
    pip install -r requirements.txt

# Copy function code
COPY main.py ${LAMBDA_TASK_ROOT}/main.py

WORKDIR ${LAMBDA_TASK_ROOT}
ENV PATH=${LAMBDA_TASK_ROOT}:${PATH}

CMD [ "app.lambda_handler" ]
