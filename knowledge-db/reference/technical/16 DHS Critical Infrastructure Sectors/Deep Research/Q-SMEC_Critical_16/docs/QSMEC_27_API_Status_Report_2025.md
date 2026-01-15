
# QSMEC 27-API Status Report — 2025

Use these official endpoints. Some need free keys.

## Sector → Endpoints (excerpt)

### Energy
- EIA Electricity Generation — https://api.eia.gov/v2/electricity/operating-generator-capacity/data/ (api_key)
- EIA Energy Consumption — https://api.eia.gov/v2/energy-consumption/data/ (api_key)

### Healthcare and Public Health
- HHS Hospital Capacity — https://protect-public.hhs.gov/api/v1/hospitals/capacity (no key)
- OpenFDA Adverse Events — https://api.fda.gov/drug/event.json (optional key)

### Communications
- FCC Broadband Deployment — https://opendata.fcc.gov/resource/ykms-bh5e.json (optional X-App-Token)

### Food and Agriculture
- USDA NASS Quick Stats — https://quickstats.nass.usda.gov/api/api_GET/ (key)

### Information Technology
- CISA KEV — https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json (no key)

## Pitfalls
- EPA and SDWIS can 500/504 → use retries.
- FEMA base page moved; use dataset pages like `/openfema-data-page/disaster-declarations-summaries-v2`.
- CDC WONDER often needs interactive query; treat as manual or cookie-based.
