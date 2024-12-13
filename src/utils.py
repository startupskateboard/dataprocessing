import logging
import re
from pathlib import Path

def setup_logging(log_file: Path):
    """Configure logging to both file and console."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def normalize_column_name(name: str) -> str:
    """Convert a column name to SQL-friendly format."""
    # Convert to string and lowercase
    name = str(name).lower()
    
    # Replace spaces and special characters with underscores
    name = re.sub(r'[^a-z0-9]+', '_', name)
    
    # Remove leading/trailing underscores
    name = name.strip('_')
    
    # Ensure the name doesn't start with a number
    if name[0].isdigit():
        name = f"col_{name}"
        
    return name 