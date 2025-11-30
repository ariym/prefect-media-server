# MediaProcessor

Python project of Prefect Flows for composing video processing pipelines.

## Getting Started

### Installation

```bash
python -m venv .venv # create a python virtual env named ".venv"

source .venv/bin/activate # activate

pip install -r requirements.txt
```

### Usage

```bash
source .venv/bin/activate # activate

poe listen
```

### Development

```bash
source .venv/bin/activate

poe start
```

#### Save all current venv pip depenency versions to a requirements.txt file

```bash
pip freeze > requirements.txt
```