# Excel Data Pipeline - System Design Document

## Overview

This pipeline is designed to convert Excel files with varying structures into SQL-ready data. The implementation focuses on handling real-world Excel files.

## Core Components and Implementation

The system is divided into four Python modules, each handling a specific aspect of the pipeline:

### Pipeline (pipeline.py)
The main entry point that:
- Creates and manages the directory structure (input, processed, output)
- Sets up logging with timestamps for traceability
- Iterates through Excel files and coordinates their processing
- Implements basic error handling to ensure one file's failure doesn't stop the entire pipeline

### Excel Processor (excel_processor.py)
Handles the core Excel processing logic:
- Persists input files to a processed directory for safety
- Processes each sheet in the Excel file independently
- Implements multi-row header detection using a simple heuristic
- Transforms headers into SQL-compatible column names
- Outputs processed data as CSV files

### Schema Inferrer (schema_inferrer.py)
Focuses on data type detection and normalization:
- Attempts numeric conversion first (integers, then floats)
- Handles date parsing with multiple format attempts
- Falls back to string type when other conversions fail
- Maintains consistent types within columns
- Uses pandas' built-in type inference capabilities

### Utilities (utils.py)
Provides shared functionality:
- Configures logging to both file and console
- Normalizes column names to be SQL-compatible
- Handles special character replacement in column names

## Data Flow

The pipeline follows a simple, linear flow:
1. Excel files are detected in the input directory
2. Files are copied to a processed directory
3. Each sheet is processed independently
4. Normalized data is saved as CSV files in the output directory

## Error Handling

- Sheet-level isolation (errors in one sheet don't affect others)
- Logging of errors with timestamps
- Continuation of processing despite individual failures

## Current Limitations

The current implementation has several constraints:
- Processes files sequentially, not in parallel
- Holds entire sheets in memory
- No automated testing implementation
- Basic data type inference

## Usage

The system is designed for straightforward usage:
1. Place Excel files in the input directory
2. Run pipeline.py
3. Retrieve processed CSV files from the output directory
4. Check logs for any processing issues
