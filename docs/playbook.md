# CCR Framework Playbook – MVP Edition

## 1. Measurement Methodology
- **Models**: Geometric Brownian Motion (FX), simple netting logic (full MTM offset)
- **Parameters**: 2,500 paths, 95% PFE, monthly time steps
- **Risk Factors**: EURUSD volatility = 12% (calibrated to 2018–2025 history)
- **Future Extensions**: Vasicek/Hull-White rates, equity diffusion, CSA modelling

## 2. Limits & Risk Appetite (example)
| Counterparty Type   | Single-Name PFE Limit | Rationale                     |
|---------------------|-----------------------|-------------------------------|
| Investment Grade    | €1.2m                 | Board-approved appetite       |
| Hedge Funds         | €0.8m                 | Higher volatility & leverage  |
| Private Equity      | €0.6m                 | Illiquidity + wrong-way risk  |

## 3. Early Warning Indicators (EWIs)
- Rating downgrade (A → BBB)
- PFE increase >40% MoM
- Notional > €10m without daily margining

## 4. Backtesting Framework (to be added in Sprint 3)
- Rolling 5-year historical window
- Quantile coverage test (target 3–7% exceedances)
- RMSE of realised vs forecasted exposure
- Trigger: model review if coverage outside band

## 5. Governance & Operating Model
**Monthly CCR Forum Agenda**
1. Top 10 exposures + limit breaches
2. EWI watchlist & escalation actions
3. Backtesting results & model performance
4. New trades / what-if scenarios
5. Model change log & validation status

**Roles & Responsibilities**
- 1LoD: Trade capture, daily exposure monitoring
- 2LoD (CCR Head): Methodology, limits, backtesting, challenge
- Model Validation: Annual independent review

**Regulatory Alignment**
- ECB SSR Guide on CCR Governance (2023)
- BIS BCBS 279 – Counterparty Credit Risk
- SA-CCR / IMM principles (simplified)

This MVP is deliberately lightweight yet fully aligned with sound practices — perfect as a foundation for a global platform.
