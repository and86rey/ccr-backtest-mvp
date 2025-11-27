# analytics/backtest.py
import numpy as np
import pandas as pd
from core.exposure import CCRSimulator

def run_historical_backtest():
    hist = pd.read_csv('data/historical_fx.csv', parse_dates=['date'])
    hist.set_index('date', inplace=True)
    trade = {
        'notional': 1_000_000,
        'strike_or_rate': 1.13,
        'maturity_date': pd.Timestamp('2026-05-20')
    }
    breaches = []
    sim = CCRSimulator(n_paths=2000)

    for date in pd.date_range('2018-01-01', '2024-12-31', freq='QE'):
        spot = hist.loc[date:date + pd.Timedelta(90, 'D')]['EURUSD'].iloc[-1]
        t = (trade['maturity_date'] - date).days / 365.25
        if t < 0.25: continue
        profile = sim.simulate_fx_forward(trade['notional'], t, spot, trade['strike_or_rate'])
        pfe_95 = profile['PFE'].iloc[-1]
        realized_mtm = max(trade['notional'] * (spot - trade['strike_or_rate']), 0)
        breaches.append(realized_mtm > pfe_95)

    coverage = sum(breaches) / len(breaches) if breaches else 0
    return {
        'Period': '2018–2024',
        'Tests': len(breaches),
        'Breaches': sum(breaches),
        'Observed Coverage': f"{coverage:.1%}",
        'BIS Target': '3–7%',
        'Pass': 0.03 <= coverage <= 0.07
    }
