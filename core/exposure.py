# core/exposure.py
import numpy as np
import pandas as pd
from datetime import datetime

class CCRSimulator:
    def __init__(self, n_paths=2500, seed=42):
        np.random.seed(seed)
        self.n_paths = n_paths

    def simulate_fx_forward(self, notional, maturity_years, spot, strike, vol=0.12, r_d=0.03, r_f=0.00):
        steps = max(int(maturity_years * 24), 1)
        dt = maturity_years / steps
        drift = (r_d - r_f - 0.5 * vol**2) * dt
        diffusion = vol * np.sqrt(dt) * np.random.randn(self.n_paths, steps)
        log_path = np.cumsum(np.hstack([np.zeros((self.n_paths, 1)), drift + diffusion]), axis=1)
        st = spot * np.exp(log_path)
        mtm = notional * (st - strike)
        ee = np.maximum(mtm, 0).mean(axis=0)
        pfe = np.percentile(np.maximum(mtm, 0), 95, axis=0)
        times = np.linspace(0, maturity_years, steps + 1)
        return pd.DataFrame({'time': times, 'EE': ee, 'PFE': pfe})

    def run_netting_set(self, trades_df, as_of_date=pd.Timestamp('2025-11-25')):
        results = {}
        for ns, group in trades_df.groupby('netting_set_id'):
            total = pd.DataFrame()
            for _, trade in group.iterrows():
                if trade['product'] != 'FX Forward':
                    continue
                t = max((pd.to_datetime(trade['maturity_date']) - as_of_date).days / 365.25, 0.01)
                spot = 1.088  # current EURUSD
                sim = self.simulate_fx_forward(trade['notional'], t, spot, trade['strike_or_rate'])
                total = pd.concat([total, sim.add_suffix(f"_{trade.name}")], axis=1)
            if not total.empty:
                total['EE_total'] = total.filter(like='EE').sum(axis=1)
                total['PFE_total'] = total.filter(like='PFE').sum(axis=1)
                results[ns] = total[['time', 'EE_total', 'PFE_total']].copy()
        return results
