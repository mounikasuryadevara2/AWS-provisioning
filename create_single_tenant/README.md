# Create Single Tenant

This Python package creates a new client account based on environment variables.

## Installation

Create and activate a Python 3 virtual environment.

```bash
python3 -m venv /path/to/new/virtual/environment
source /path/to/new/virtual/environment/bin/activate
```

Then install dependencies in your active virtualenv.

```bash
pip install -r requirements.txt
```

## Usage

You can call create_single_tenant from its parent directory with the virtual
environment active:

```bash
python create_single_tenant
```

## Testing

```bash
python -m pytest
```
