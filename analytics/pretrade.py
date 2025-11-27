# analytics/pretrade.py
from core.exposure import CCRSimulator
import pandas as pd

def what_if_new_trade(current_profiles, new_trade_row, trades_df):
    sim = CCRSimulator(n_paths=2000)
    temp_df = pd.concat([trades_df, pd.DataFrame([new_trade_row])], ignore_index=True)
    temp_df['maturity_date'] = pd.to_datetime(temp_df['maturity_date'])
    new_profiles = sim.run_netting_set(temp_df)
    
    ns = new_trade_row['netting_set_id']
    incremental = new_profiles[ns]['PFE_total'].max() - current_profiles[ns]['PFE_total'].max()
    return {
        'New Trade': f"{new_trade_row['product']} {new_trade_row['notional']:,} {new_trade_row['counterparty']}",
        'Incremental Peak PFE': f"€{incremental:,.0f}",
        'New Total Peak PFE': f"€{new_profiles[ns]['PFE_total'].max():,.0f}"
    }
