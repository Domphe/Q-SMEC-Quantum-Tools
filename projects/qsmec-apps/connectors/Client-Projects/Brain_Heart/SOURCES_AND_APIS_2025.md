# SOURCES AND APIS (Verified 2025)

Curated primary sources and public/free APIs to support EEG/MEG and ECG/MCG development, validation, and integration. Prefer official, government, academic, or well‑maintained open projects. Check usage terms; PHI must never be uploaded to public endpoints.

## Brain (EEG/MEG) Datasets
- OMEGA (Open MEG Archive): https://doi.org/10.5281/zenodo.1491957 — Open MEG with MRI; raw + derivatives.
- OpenNeuro (EEG/MEG): https://openneuro.org/ — BIDS datasets; filter by modality.
- Cam-CAN MEG/EEG: https://camcan-archive.mrc-cbu.cam.ac.uk/ — Lifespan MEG/EEG cohort.
- HCP MEG: https://db.humanconnectome.org/ — Human Connectome Project; MEG sessions (registration required).
- MIPDB/EEGMMI (EEG): https://www.physionet.org/ — PhysioNet hosts multiple EEG corpora (sleep, seizure, etc.).

## Heart (ECG/MCG) Datasets
- PhysioNet: https://www.physionet.org/ — MIT‑BIH Arrhythmia, PTB/PTB‑XL, MIMIC waveform DBs.
- MCG (SQUID) datasets: OHSU/MCG (literature-linked; check institutional repos), PhysioNet collections tagged “magnetocardiography”.
- Telemetric and Holter ECG Database: https://www.physionet.org/content/thoraxecgdb/ — Long-term Holter.
- QT Database: https://www.physionet.org/content/qtdb/ — QT annotations.

## Standards & Formats
- BIDS (EEG/MEG/iEEG): https://bids.neuroimaging.io/ — Brain Imaging Data Structure.
- WFDB (PhysioNet): https://wfdb.readthedocs.io/ — WaveForm DataBase tools and formats.
- HL7 FHIR R4/R5: https://www.hl7.org/fhir/ — Interoperability resources (Observation, Device, Patient).
- IEEE/IEC/ISO (selection; via abstracts):
  - IEEE 11073 (medical device comms): https://standards.ieee.org/ 
  - IEC 60601 series (safety): https://www.iec.ch/ 
  - ISO 13485 (QMS): https://www.iso.org/standard/59752.html

## Public/Test APIs (No PHI)
- PhysioNet REST API: https://physionet.org/about/api/ — Programmatic dataset access.
- OpenFDA: https://open.fda.gov/apis/ — Device (510(k), recalls), Drug, Food endpoints.
- ClinicalTrials.gov API: https://clinicaltrials.gov/api/gui — Study metadata search.
- NIH RePORTER API: https://api.reporter.nih.gov/ — Grants/projects; portfolio mapping.
- HL7 FHIR Test Servers:
  - HAPI FHIR Public: https://hapi.fhir.org/ 
  - Inferno Test Tool: https://inferno.healthit.gov/ 
  - SMART Health IT Sandbox: https://sandbox.smarthealthit.org/ 
- NIST NVD (CVE) API: https://nvd.nist.gov/developers — Security advisories for dependencies/devices.

## Regulatory & Guidance
- FDA CDRH (Devices): https://www.fda.gov/medical-devices — Guidance, databases, recognized standards.
- FDA Recognized Consensus Standards search: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm
- FDA Digital Health: https://www.fda.gov/medical-devices/digital-health-center-excellence
- EU MDR/IVDR (EC): https://health.ec.europa.eu/medical-devices-sector_en
- IMDRF: https://www.imdrf.org/ — International harmonization docs.

## Developer Tooling
- WFDB Python: https://github.com/MIT-LCP/wfdb-python — Read/annotate PhysioNet signals.
- MNE-Python: https://mne.tools/ — EEG/MEG analysis toolkit with BIDS support.
- BIDS Validator: https://bids-standard.github.io/bids-validator/ — Validate dataset structure.

## Notes & Constraints
- De-identification: Ensure no PHI leaves secure environments; use synthetic or public demo data for tests.
- Licenses: Verify dataset/software licenses for commercial usage.
- API rate limits: Respect quotas; cache non-sensitive metadata locally.
- Clinical usage: Public/test servers are not for clinical data or decision-making.
