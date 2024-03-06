# LLM Factory

This repo maintains the source code for python pip package `llm-factory`.

## Setup dev environment

1. Create virtual environment: `conda create -n llm_factory_test_env -y python=3.8`
1. Activate environment: `conda activate llm_factory_test_env`
1. Install dependencies: `pip install -r dev_requirements.txt`

## Run unit tests

1. Activate environment: `conda activate llm_factory_test_env`
1. Run: `pytest src/tests/test_llm_factory.py -v --log-cli-level INFO`

## Release new package

1. Push your changes
1. In GitHub:
   1. Go to [New release](https://github.com/AIprojectflow/llm_factory/releases/new) page
   1. Create a new tag by incrementing patch version
   1. Enter the title for new release
   1. Click on "Generate release notes" to auto populate release notes
   1. Click on "Publish release" button
   1. Once the release is done, a GitHub Action will be triggered to release package to PyPI repository. Check [Actions](https://github.com/AIprojectflow/llm_factory/actions) here.
   1. Monitor the action to successful state.
   1. After the action is completed successfully, check the [PyPI repo](https://pypi.org/project/microlearn-llm-factory/) to make sure the new version is published.
