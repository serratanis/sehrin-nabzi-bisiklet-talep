# City Pulse

City Pulse predicts hourly bike-sharing demand in Washington D.C. from calendar and weather conditions. It combines Capital Bikeshare's complete 2025 trip history with Open-Meteo hourly weather data and includes a browser-based Streamlit dashboard.

## Result

Using a chronological 80/20 split, the linear regression model achieved an R² of 0.578, MAE of 234.3 trips and RMSE of 315.2 trips. A mean-only baseline produced an MAE of 476.8 on the same future test period.

## Reproducibility

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_experiment.py
python -m pytest -q
```

The processed CSV is included. To rebuild it from official sources:

```bash
python src/prepare_dataset.py --download
```

## Dashboard

On macOS, double-click `SEHRIN_NABZI_BASLAT.command` to open the dashboard and `SEHRIN_NABZI_DURDUR.command` to stop it.

## Data

- Capital Bikeshare System Data: https://capitalbikeshare.com/system-data
- Capital Bikeshare Data License: https://capitalbikeshare.com/data-license-agreement
- Open-Meteo Historical Weather API: https://open-meteo.com/en/docs/historical-weather-api

Raw trip archives are not redistributed. The repository includes only the hourly aggregate created for this analysis.
