# analytics/stress.py
import numpy as np
from core.exposure import CCRSimulator

def stress_exposure(profile, shock_factor=1.5, vol_multiplier=2.0):
    """Apply parallel shock + volatility spike (e.g. March 2020 style)"""
    stressed = profile.copy()
    stressed['EE_total'] *= shock_factor
    stressed['PFE_total'] *= shock_factor * vol_multiplier**0.5
    return stressed

def wrong_way_risk_uplift(profile, sector):
    """Private Equity / Hedge Funds get extra uplift"""
    uplift = {'Private Equity': 1.8, 'Hedge Funds': 1.5}.get(sector, 1.0)
    stressed = profile.copy()
    stressed['PFE_total'] *= uplift
    return stressed
