import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def generate_visualizations(df_daily, output_dir):
    """
    Generate all 5 panels and save to output_dir.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Panel 1: Timeline (daily max/min temp, humidity or T_eff overlay)
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig1.add_trace(go.Scatter(x=df_daily['date'], y=df_daily['daily_max_temp'], name='Max Temp', mode='lines+markers'))
    fig1.add_trace(go.Scatter(x=df_daily['date'], y=df_daily['daily_min_temp'], name='Min Temp', mode='lines+markers'))
    fig1.add_trace(go.Scatter(x=df_daily['date'], y=df_daily['daily_T_eff'], name='Avg T_eff', mode='lines', line=dict(dash='dot')), secondary_y=True)
    fig1.update_layout(title='Timeline: Daily Temps & T_eff')
    fig1.write_html(os.path.join(output_dir, 'panel1_timeline.html'))
    
    # Panel 2: CHL curve (cumulative CHL line)
    fig2 = px.line(df_daily, x='date', y='cumulative_CHL', title='Cumulative Heat Load (CHL)')
    fig2.write_html(os.path.join(output_dir, 'panel2_chl.html'))
    
    # Panel 3: HNe bars (nightly HNe)
    fig3 = px.bar(df_daily, x='date', y='daily_HNe', title='Daily Hot Night Excess (HNe)')
    fig3.write_html(os.path.join(output_dir, 'panel3_hne.html'))
    
    # Panel 4: Risk state band
    color_map = {'Stable': 'green', 'Straining': 'orange', 'Failure': 'red'}
    fig4 = px.area(df_daily, x='date', y=[1]*len(df_daily), color='risk_state', color_discrete_map=color_map,
                   title='Risk State Bands')
    fig4.update_traces(line=dict(width=0), showlegend=True)
    fig4.update_layout(yaxis={'visible': False})
    fig4.write_html(os.path.join(output_dir, 'panel4_risk_states.html'))
    
    # Panel 5: Nonlinear escalation gauge
    df_daily['risk_multiplier'] = 1 + (df_daily['cumulative_CHL']/40) + (df_daily['cumulative_HNe']/20) + (df_daily['consecutive_compound_cycles'] * 0.5)
    fig5 = px.line(df_daily, x='date', y='risk_multiplier', title='Nonlinear Risk Multiplier')
    fig5.write_html(os.path.join(output_dir, 'panel5_escalation.html'))
    
    # Matplotlib fallback for static images
    plt.figure(figsize=(12, 8))
    plt.subplot(511)
    plt.plot(df_daily['date'], df_daily['daily_max_temp'], label='Max Temp')
    plt.plot(df_daily['date'], df_daily['daily_min_temp'], label='Min Temp')
    plt.plot(df_daily['date'], df_daily['daily_T_eff'], '--', label='T_eff')
    plt.title('Timeline')
    plt.legend()
    
    plt.subplot(512)
    plt.plot(df_daily['date'], df_daily['cumulative_CHL'])
    plt.title('CHL')
    
    plt.subplot(513)
    plt.bar(df_daily['date'], df_daily['daily_HNe'])
    plt.title('HNe')
    
    plt.subplot(514)
    colors = df_daily['risk_state'].map({'Stable': 'green', 'Straining': 'orange', 'Failure': 'red'})
    plt.bar(df_daily['date'], [1]*len(df_daily), color=colors)
    plt.title('Risk States')
    plt.yticks([])
    
    plt.subplot(515)
    plt.plot(df_daily['date'], df_daily['risk_multiplier'])
    plt.title('Risk Multiplier')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'all_panels_static.png'))
