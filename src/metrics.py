import pandas as pd
import numpy as np

def compute_metrics(df):
    """
    Compute effective temperature, CHL, HNe, compound strain, and streaks.
    """
    # Effective temperature
    df['T_eff'] = df['temp_c'] + 0.1 * df['rh']
    
    # Cumulative Heat Load (CHL)
    baseline_day = 32
    df['CHL_hour'] = np.maximum(df['T_eff'] - baseline_day, 0)
    # Resample to daily
    df_daily = df.resample('D', on='timestamp').agg({
        'CHL_hour': 'sum',
        'temp_c': ['max', 'min'],
        'rh': 'mean',  # Average humidity for overlay
        'T_eff': 'mean'  # For overlay
    })
    df_daily.columns = ['daily_CHL', 'daily_max_temp', 'daily_min_temp', 'daily_rh', 'daily_T_eff']
    df_daily['cumulative_CHL'] = df_daily['daily_CHL'].cumsum()
    
    # Hot Night Excess (HNe)
    baseline_night = 25
    # Night window: 20:00–08:00 (filter hours)
    df['hour'] = df['timestamp'].dt.hour
    night_mask = (df['hour'] >= 20) | (df['hour'] < 8)
    df['HNe_hour'] = np.where(night_mask, np.maximum(df['temp_c'] - baseline_night, 0), 0)
    df['severe_HNe_hour'] = np.where(night_mask, np.maximum(df['temp_c'] - 28, 0), 0)
    # Daily sums
    df_daily_night = df.resample('D', on='timestamp').agg({
        'HNe_hour': 'sum',
        'severe_HNe_hour': 'sum'
    })
    df_daily_night.columns = ['daily_HNe', 'daily_severe_HNe']
    df_daily_night['cumulative_HNe'] = df_daily_night['daily_HNe'].cumsum()
    
    # Merge daily data
    df_daily = df_daily.join(df_daily_night)
    df_daily['date'] = df_daily.index  # For plotting
    
    # Compound Day-Night Strain
    df_daily['hot_day'] = df_daily['daily_CHL'] > 20
    df_daily['hot_night'] = df_daily['daily_HNe'] > 10
    df_daily['compound'] = df_daily['hot_day'] & df_daily['hot_night']
    
    # Streaks
    def compute_streak(series):
        streak = 0
        streaks = []
        for val in series:
            if val:
                streak += 1
            else:
                streak = 0
            streaks.append(streak)
        return streaks
    
    df_daily['consecutive_hot_days'] = compute_streak(df_daily['hot_day'])
    df_daily['consecutive_hot_nights'] = compute_streak(df_daily['hot_night'])
    df_daily['consecutive_compound_cycles'] = compute_streak(df_daily['compound'])
    
    return df_daily
