# Assistive Device Needs Dashboard

Streamlit dashboard for reviewing assistive device requests across schools, districts, learner profiles, and catalog size requirements.

## 🚀 Live Dashboard

[![Open Dashboard](https://img.shields.io/badge/Streamlit-Dashboard-red?logo=streamlit&style=for-the-badge)](https://assistive-device-dashboard-r2syjajgp3broag4y2zea3.streamlit.app/)

## Current Setup

- App: `app.py`
- Data cleaning: `clean.py`
- Cleaned output: `data/cleaned_data.csv`
- Device catalog: `data/DEVICE_INFORMATION_CATALOG_FINAL.xlsx`
- Streamlit theme: `.streamlit/config.toml`

The dashboard loads response data from the published Google Sheet in `clean.py`, cleans and reshapes the three device-priority columns into request-level rows, and saves the cleaned dataset to `data/cleaned_data.csv`.

## Dashboard Sections

- `Demand overview`: district, device, priority, and category demand.
- `Learner profile`: disability, social category, gender, and measurement-based device demand.
- `Size chart`: catalog size-code demand by device.
- `Filtered data`: current filtered records and CSV download.

## Sizing Logic

The cleaned data does not classify devices into small, medium, and large.

Palm length and width are retained only for:

- `utensil holder`
- `palm pen holder`
- `toothbrush holder`

Those three devices are mapped to the catalog `ND` sizing chart using cleaned palm length and width.

All other devices are treated as fixed-measurement items. The size chart uses the catalog device code where a fixed or representative code is available.

## Filters

The sidebar uses collapsed slicers for:

- Districts
- Schools
- Device categories
- Devices
- Priorities
- Genders
- Ranked rows

Schools remain dependent on the selected districts.

## Refresh

The dashboard refreshes every hour. Cached data also uses a one-hour TTL.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Requirements

Key packages:

- `streamlit`
- `pandas`
- `plotly`
- `streamlit-autorefresh`
- `openpyxl`

`openpyxl` is required for reading the Excel device catalog.

