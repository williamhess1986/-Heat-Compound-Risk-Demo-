def compute_risk_states(df_daily):
    """
    Compute daily risk states based on exact thresholds.
    """
    conditions = [
        # Failure
        (df_daily['cumulative_CHL'] >= 80) | 
        (df_daily['cumulative_HNe'] >= 40) | 
        (df_daily['consecutive_compound_cycles'] >= 4),
        # Straining
        (df_daily['cumulative_CHL'] >= 40) | 
        (df_daily['cumulative_HNe'] >= 20) | 
        (df_daily['consecutive_compound_cycles'] >= 2),
        # Stable (default)
        True
    ]
    states = ['Failure', 'Straining', 'Stable']
    df_daily['risk_state'] = np.select(conditions, states)
    return df_daily
