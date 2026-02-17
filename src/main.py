import os
import pandas as pd
from data_loader import load_data
from metrics import compute_metrics
from risk_states import compute_risk_states
from visualization import generate_visualizations

def main(csv_path):
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Load
    df = load_data(csv_path)
    
    # Compute
    df_daily = compute_metrics(df)
    df_daily = compute_risk_states(df_daily)
    
    # Visualize
    generate_visualizations(df_daily, output_dir)
    
    # Save processed data
    df_daily.to_csv(os.path.join(output_dir, 'processed_daily.csv'), index=False)
    
    # Print summary table
    print("Daily Summary:")
    print(df_daily[['date', 'daily_CHL', 'cumulative_CHL', 'daily_HNe', 'cumulative_HNe', 
                    'consecutive_compound_cycles', 'risk_state', 'risk_multiplier']])

if __name__ == "__main__":
    # Example run with sample
    main('data/sample_chicago_1995.csv')  # Change to other samples or custom CSV
