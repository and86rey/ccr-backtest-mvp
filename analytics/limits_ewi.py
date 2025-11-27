# analytics/limits_ewi.py
import pandas as pd

def apply_limits_and_ewi(profiles, trades_df):
    limits = {
        'Investment Grade': 1_200_000,
        'Hedge Funds':      800_000,
        'Private Equity':   600_000
    }
    results = []
    for ns, profile in profiles.items():
        row = trades_df[trades_df['netting_set_id'] == ns].iloc[0]
        peak_pfe = profile['PFE_total'].max()
        limit = limits.get(row['sector'].split()[-1] if ' ' in row['sector'] else row['sector'], 1_000_000)
        breach = peak_pfe > limit
        ewi_flags = []
        if row['rating'] in ['BBB', 'BB']:
            ewi_flags.append("Rating watch")
        if peak_pfe > 1.4 * limit:
            ewi_flags.append("Severe PFE spike")
        results.append({
            'Netting Set': ns,
            'Counterparty': row['counterparty'],
            'Sector': row['sector'],
            'Peak PFE (€)': f"€{peak_pfe:,.0f}",
            'Limit (€)': f"€{limit:,.0f}",
            'Status': 'BREACH' if breach else 'OK',
            'EWI': ' | '.join(ewi_flags) if ewi_flags else '-'
        })
    return pd.DataFrame(results)
