# [Redacted]

[Redacted]
## Features

[Redacted]

## Installation

1. Create a virtual environment:
```bash
python3 -m venv venv --without-pip
source venv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your Excel files in the `data/input` directory

2. Run the pipeline:
```bash
python3 src/pipeline.py
```

The pipeline will:
- Process all Excel files found in the input directory
- Store processed files in `data/processed`
- Generate output in `data/output`
- Create logs in the `logs` directory
```

```