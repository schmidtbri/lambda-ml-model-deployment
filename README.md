# AWS Lambda ML Model Deployment

![](https://github.com/schmidtbri/lambda-ml-model-deployment/workflows/Build/badge.svg)


Deploying an ML model in AWS Lambda.

This code is used in this [blog post](https://medium.com/@brianschmidt_78145/an-aws-lambda-ml-model-deployment-4ec83d6179d4).

## Requirements
This project requires the [serverless framework](https://serverless.com/framework/docs/getting-started/), which itself requires the [node.js framework](https://nodejs.org/en/download/package-manager/).

In order to create the lambda deployment package, the [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements) extension for serverless must be installed.

In order to compile the packages in the lambda deployment package [docker](https://docs.docker.com/v17.09/engine/installation/) needs to be installed.

## Installation 
The makefile included with this project contains targets that help to automate several tasks.

To download the source code execute this command:
```bash
git clone https://github.com/schmidtbri/lambda-ml-model-deployment
```
Then create a virtual environment and activate it:
```bash

# go into the project directory
cd lambda-ml-model-deployment

make venv

source venv/bin/activate
```

Install the dependencies:
```bash
make dependencies
```

## Running the unit tests
To run the unit test suite execute these commands:
```bash

# first install the test dependencies
make test-dependencies

# run the test suite
make test
```

