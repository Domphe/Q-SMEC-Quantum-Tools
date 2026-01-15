# Scrape Logs Summary

Output directory: `/mnt/g/My Drive/Databases/AI Tools/AI Tools w Quantum Database - Complete/QUANTUM AI MODEL TOOLS + QUANTUM AI SIMULATION TOOLS_ Analysis`

## Coverage

- Total tools: **64**
- Live pricing extracted: **11** (17.19%)
- Fallback used: **53**

## Error Categories

- http_404_not_found: **13**
- timeout: **7**
- http_403_forbidden: **5**
- dns_resolution: **2**
- ssl_error: **1**

## By Tool (Top offenders)

- **CASTEP** — 2 (http_404_not_found:2)
- **FHI-aims (commercial)** — 2 (http_404_not_found:1, timeout:1)
- **Q-Chem** — 2 (http_404_not_found:2)
- **Gaussian** — 1 (http_404_not_found:1)
- **Materials Studio** — 1 (http_404_not_found:1)
- **TeraChem** — 1 (ssl_error:1)
- **Spearmint (commercial support)** — 1 (dns_resolution:1)
- **PennyLane Enterprise** — 1 (http_404_not_found:1)
- **ANSYS (Mech/Fluent/AM)** — 1 (timeout:1)
- **COMSOL Multiphysics** — 1 (http_404_not_found:1)
- **LS-DYNA** — 1 (timeout:1)
- **MSC Nastran/Patran** — 1 (http_403_forbidden:1)
- **STAR-CCM+** — 1 (http_404_not_found:1)
- **Simcenter 3D** — 1 (http_404_not_found:1)
- **Altair HyperWorks** — 1 (http_404_not_found:1)

## Suggestions to Improve Confidence

- Keep both CSV and XLSX artifacts; they are stable even if scraping fails.
- For 404s: check vendor URL changes; prefer main product pages over deep pricing endpoints.
- For 403s: pages may block bots; try manual validation or contact sales.
- For timeouts/DNS: re-run with `--use-cache` to stabilize results; retry when network is stable.
- Consider adding alternative sources (docs, datasheets) that mention pricing tiers or "Contact Sales" explicitly.