import logging
import pandas as pd
from pathlib import Path
import shutil

from schema_inferrer import SchemaInferrer
from utils import normalize_column_name

class ExcelProcessor:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.schema_inferrer = SchemaInferrer()
        
    def process(self, processed_dir: Path, output_dir: Path):
        """Process the Excel file and generate SQL-ready output."""
        # First, persist the file
        self._persist_file(processed_dir)
        
        # Read all sheets
        excel_file = pd.ExcelFile(self.file_path)
        
        for sheet_name in excel_file.sheet_names:
            try:
                self._process_sheet(excel_file, sheet_name, output_dir)
            except Exception as e:
                logging.error(f"Failed to process sheet {sheet_name}: {str(e)}")
                continue
                
    def _persist_file(self, processed_dir: Path):
        """Create a copy of the input file in the processed directory."""
        dest_path = processed_dir / self.file_path.name
        shutil.copy2(self.file_path, dest_path)
        logging.info(f"Persisted file to {dest_path}")
        
    def _process_sheet(self, excel_file: pd.ExcelFile, sheet_name: str, output_dir: Path):
        """Process a single sheet from the Excel file."""
        logging.info(f"Processing sheet: {sheet_name}")
        
        # Read the sheet with header inference
        df = self._read_sheet_with_header(excel_file, sheet_name)
        
        # Normalize column names
        df.columns = [normalize_column_name(col) for col in df.columns]
        
        # Infer and apply schema
        df = self.schema_inferrer.infer_and_apply_schema(df)
        
        # Save as CSV
        output_file = output_dir / f"{self.file_path.stem}_{sheet_name}.csv"
        df.to_csv(output_file, index=False)
        logging.info(f"Saved processed sheet to {output_file}")
        
    def _read_sheet_with_header(self, excel_file: pd.ExcelFile, sheet_name: str) -> pd.DataFrame:
        """Read sheet and handle multi-row headers."""
        # First, peek at the first few rows to detect the header structure
        df_peek = pd.read_excel(excel_file, sheet_name=sheet_name, nrows=5)
        
        # Try to detect if we have a multi-row header
        header_rows = self._detect_header_rows(df_peek)
        
        # Read the sheet with the correct header configuration
        if len(header_rows) > 1:
            df = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_rows)
            # Combine multi-level columns into single level
            df.columns = [
                '_'.join(str(level) for level in col if pd.notna(level))
                if isinstance(col, tuple) else str(col)
                for col in df.columns
            ]
        else:
            df = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_rows[0])
            
        return df
        
    def _detect_header_rows(self, df: pd.DataFrame) -> list:
        """Detect which rows comprise the header."""
        # Simple heuristic: Consider rows as headers if they contain string data
        # and not primarily numeric data
        header_rows = []
        for idx in range(min(5, len(df))):
            row = df.iloc[idx]
            if row.apply(lambda x: isinstance(x, str)).mean() > 0.5:
                header_rows.append(idx)
            else:
                break
                
        return header_rows if header_rows else [0] 