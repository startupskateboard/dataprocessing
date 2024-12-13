#!/usr/bin/env python3
import logging
import os
from datetime import datetime
from pathlib import Path

from excel_processor import ExcelProcessor
from utils import setup_logging

class Pipeline:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.input_dir = self.base_dir / "data" / "input"
        self.processed_dir = self.base_dir / "data" / "processed"
        self.output_dir = self.base_dir / "data" / "output"
        self.setup_directories()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        setup_logging(self.base_dir / "logs" / f"pipeline_{timestamp}.log")
        
    def setup_directories(self):
        """Create necessary directories if they don't exist."""
        for dir_path in [self.input_dir, self.processed_dir, self.output_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def run(self):
        """Execute the pipeline on all Excel files in the input directory."""
        logging.info("Starting pipeline execution")
        
        excel_files = list(self.input_dir.glob("*.xlsx"))
        if not excel_files:
            logging.warning("No Excel files found in input directory")
            return
            
        for excel_file in excel_files:
            try:
                logging.info(f"Processing file: {excel_file.name}")
                processor = ExcelProcessor(excel_file)
                processor.process(self.processed_dir, self.output_dir)
            except Exception as e:
                logging.error(f"Failed to process {excel_file.name}: {str(e)}")
                continue
                
        logging.info("Pipeline execution completed")

if __name__ == "__main__":
    pipeline = Pipeline()
    pipeline.run() 