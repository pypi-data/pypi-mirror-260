# visiontext

<p align="center">
<a href="https://github.com/simon-ging/visiontext/actions/workflows/build-py38-cpu.yml">
  <img alt="build 3.8 status" title="build 3.8 status" src="https://img.shields.io/github/actions/workflow/status/simon-ging/visiontext/build-py38-cpu.yml?branch=main&label=build%203.8%20cpu" />
</a>
<a href="https://github.com/simon-ging/visiontext/actions/workflows/build-py310-cpu.yml">
  <img alt="build 3.10 status" title="build 3.10 status" src="https://img.shields.io/github/actions/workflow/status/simon-ging/visiontext/build-py310-cpu.yml?branch=main&label=build%203.10%20cpu" />
</a>
<a href="https://github.com/simon-ging/visiontext/actions/workflows/build-py312-cpu.yml">
  <img alt="build 3.12 status" title="build 3.12 status" src="https://img.shields.io/github/actions/workflow/status/simon-ging/visiontext/build-py312-cpu.yml?branch=main&label=build%203.12%20cpu" />
</a>
<img alt="coverage" title="coverage" src="https://raw.githubusercontent.com/simon-ging/visiontext/main/docs/coverage.svg" />
<a href="https://pypi.org/project/visiontext/">
  <img alt="version" title="version" src="https://img.shields.io/pypi/v/visiontext?color=success" />
</a>
</p>

Utilities for deep learning on multimodal data.

* jupyter notebooks / jupyter lab / ipython
* matplotlib
* pandas
* webdataset / tar
* pytorch

## Install

Requires `python>=3.8` `pytorch` `sqlite`

```bash
pip install visiontext
```

## Dev install

Clone repository and cd into, then:

~~~bash
pip install -e .
pip install pytest pytest-cov pylint

python -m pytest --cov

pylint visiontext
pylint tests
~~~

## Changelog

- 0.10.1: Test with python 3.12
- 0.8.1: Set minimum python version to 3.8 since PyTorch requires it
