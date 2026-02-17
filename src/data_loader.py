import pandas as pd

def load_data(csv_path):
    """
    Load CSV data with required schema.
    """
    df = pd.read_csv(csv_path)
    # Parse timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Ensure required columns
    required_cols = ['timestamp', 'temp_c', 'rh']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"CSV must include: {required_cols}")
    # Optional columns default to 0 if missing
    if 'grid_strain' not in df.columns:
        df['grid_strain'] = 0.0
    if 'vulnerability_factor' not in df.columns:
        df['vulnerability_factor'] = 0.0
    # Sort by timestamp
    df = df.sort_values('timestamp').reset_index(drop=True)
    return df
