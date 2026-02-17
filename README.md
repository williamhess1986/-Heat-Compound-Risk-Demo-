# -Heat-Compound-Risk-DemoWhat This App Does
Given a CSV of hourly weather data, the app computes:

1. Effective Temperature (T_eff)
A humidity‑adjusted temperature proxy:

Code
T_eff = temp_c + 0.1 * rh
2. Cumulative Heat Load (CHL)
How much heat stress builds up during the day:

Code
baseline_day = 32
CHL_hour = max(T_eff - baseline_day, 0)
daily_CHL = sum(CHL_hour)
cumulative_CHL = running sum
3. Hot Night Excess (HNe)
How much heat remains at night (20:00–08:00):

Code
baseline_night = 25
HNe_hour = max(temp_c - baseline_night, 0)
daily_HNe = sum(HNe_hour)
cumulative_HNe = running sum
4. Compound Day–Night Strain
When hot days and hot nights stack:

Code
hot_day = daily_CHL > 20
hot_night = daily_HNe > 10
compound = hot_day and hot_night
Tracks streaks of:

consecutive hot days

consecutive hot nights

consecutive compound cycles

5. Risk States
Based on accumulated strain:

Code
Stable:
  CHL < 40 and HNe < 20 and compound_streak < 2

Straining:
  CHL >= 40 or HNe >= 20 or compound_streak >= 2

Failure:
  CHL >= 80 or HNe >= 40 or compound_streak >= 4
6. Nonlinear Escalation Gauge
A simple multiplier showing how fast risk ramps:

Code
risk_multiplier = 1 + (CHL/40) + (HNe/20) + (compound_streak * 0.5)
📊 Visualizations
The app generates five panels:

Timeline  
Daily max/min temp + T_eff overlay

CHL Curve  
Cumulative daytime heat load

HNe Bars  
Nighttime excess heat

Risk State Band  
Green → Amber → Red

Nonlinear Escalation Gauge  
Shows how strain compounds over time

Outputs are saved to /output as HTML and PNG.

📁 Project Structure
Code
/project
  /src
    data_loader.py
    metrics.py
    risk_states.py
    visualization.py
    main.py
  /data
    sample_chicago_1995.csv
    sample_europe_2003.csv
    sample_future_plus3c.csv
  /notebooks
    demo.ipynb
  README.md
  requirements.txt
  LICENSE
📥 Input CSV Format
Required columns:

Code
timestamp (ISO8601)
temp_c (float)
rh (float)
Optional:

Code
grid_strain (0–1)
vulnerability_factor (0–1)
Three sample datasets are included:

Chicago 1995

Europe 2003

Future scenario (+3°C warming)

▶️ How to Run
1. Install dependencies
Code
pip install -r requirements.txt
2. Run the demo
Code
python src/main.py
By default it loads sample_chicago_1995.csv.

3. Use your own data
Replace the CSV path:

Code
python src/main.py data/your_file.csv
Your file must follow the input schema above.

🧠 Why This Matters
Heat risk isn’t about the hottest hour of the day.
It’s about:

persistence

nighttime recovery

stacked strain

system margins

This demo shows how simple metrics can reveal the real danger — long before peak temperature does.

It’s not a forecasting tool.
It’s a public‑literacy tool.

A way to see heat the way the body and the grid experience it.

Risk State Interpretation (important note)

Risk states are evaluated per day, using that day’s heat strain and current streak conditions.

Cumulative metrics are tracked for visualization and context, but the risk classification reflects operational daily stress, not long-term rarity.

This model treats heat risk as an operational strain problem — defined by daily load, recovery failure, and persistence — rather than as a rare statistical anomaly.

📄 License
MIT License — free to use, modify, and build on.-
