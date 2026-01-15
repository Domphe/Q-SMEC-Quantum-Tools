# API Keys Guide - Q-SMEC Critical 16

**Last Updated:** October 29, 2025

---

## 🔑 Overview

This document provides comprehensive guidance on obtaining and using API keys for the Q-SMEC Critical 16 research package. All government APIs are **FREE** but require registration for higher rate limits and better access.

---

## 📋 Required vs. Optional Keys

### ✅ Highly Recommended (Free)

These APIs provide the most valuable data for DHS Critical Infrastructure research:

| API | Get Key From | Primary Sectors | Rate Limit |
|-----|--------------|-----------------|------------|
| **Census Bureau** | https://api.census.gov/data/key_signup.html | All 16 sectors | 500/day (no key) → 5000/day (with key) |
| **EIA (Energy)** | https://www.eia.gov/opendata/register.php | Energy, Critical Manufacturing | 1000/hour |
| **BEA (Economics)** | https://apps.bea.gov/API/signup/index.cfm | All sectors (economic data) | No published limit |
| **BLS (Labor)** | https://www.bls.gov/developers/ | All sectors (employment) | 25/day (no key) → 500/day (with key) |

### 🔵 Optional but Useful

| API | Get Key From | Use Case | Notes |
|-----|--------------|----------|-------|
| **NOAA Climate** | https://www.ncdc.noaa.gov/cdo-web/token | Dams, Water, Agriculture | Free registration |
| **Data.gov** | https://api.data.gov/signup/ | General federal data | Most endpoints work without key |
| **OSF** | https://osf.io/settings/tokens/ | Academic research | Free account required |
| **Zenodo** | https://zenodo.org/account/settings/applications/tokens/new/ | Research datasets, publications | 50GB file support! |

### 🟢 No Key Required (But Recommended Setup)

| API | Setup | Use Case | Notes |
|-----|-------|----------|-------|
| **OpenAlex** | Add email to requests | Scholarly research, publications | 100k/day free! Polite pool = better performance |

### ⚪ Not Needed for Core Functionality

- EPA API (limited availability, contact required)
- NVD/NIST (public endpoints, no key needed)

---

## 🚀 Quick Start - Get Your Keys

### 1️⃣ U.S. Census Bureau (5 minutes)

**Best for:** Population, economic, demographic data across all sectors

```
1. Go to: https://api.census.gov/data/key_signup.html
2. Fill out form with:
   - Organization: NIKET North America LLC
   - Email: your-email@niketllc.com
3. Receive key instantly via email
4. Add to .env: CENSUS_API_KEY=your_key_here
```

**Test:** `https://api.census.gov/data/2019/cbp?get=EMP&for=state:*&key=YOUR_KEY`

---

### 2️⃣ Energy Information Administration (5 minutes)

**Best for:** Energy production, consumption, prices (critical for Energy sector)

```
1. Go to: https://www.eia.gov/opendata/register.php
2. Complete registration form
3. Receive key via email (instant)
4. Add to .env: EIA_API_KEY=your_key_here
```

**Test:** `https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key=YOUR_KEY`

---

### 3️⃣ Bureau of Economic Analysis (10 minutes)

**Best for:** GDP, economic indicators, industry statistics

```
1. Go to: https://apps.bea.gov/API/signup/index.cfm
2. Request API key (instant approval)
3. Add to .env: BEA_API_KEY=your_key_here
```

**Test:** `https://apps.bea.gov/api/data/?UserID=YOUR_KEY&method=GetDataSetList`

---

### 4️⃣ Bureau of Labor Statistics (5 minutes)

**Best for:** Employment, wages, labor statistics

```
1. Go to: https://www.bls.gov/developers/home.htm
2. Register for account
3. Request API key (instant)
4. Add to .env: BLS_API_KEY=your_key_here
```

**Test:** POST to `https://api.bls.gov/publicAPI/v2/timeseries/data/`

---

### 5️⃣ NOAA Climate Data (5 minutes)

**Best for:** Climate patterns, weather data (Dams, Water, Agriculture)

```
1. Go to: https://www.ncdc.noaa.gov/cdo-web/token
2. Enter email address
3. Receive token via email
4. Add to .env: NOAA_TOKEN=your_token_here
```

**Test:** `https://www.ncdc.noaa.gov/cdo-web/api/v2/datasets?token=YOUR_TOKEN`

---

### 6️⃣ Zenodo Research Repository (10 minutes)

**Best for:** Academic datasets, research publications, validated scientific outputs

```
1. Register account: https://zenodo.org/signup
2. Go to: https://zenodo.org/account/settings/applications/tokens/new/
3. Select scopes:
   - deposit:write (upload/edit depositions)
   - deposit:actions (publish/edit/discard)
4. Create token (instant)
5. Add to .env: ZENODO_API_TOKEN=your_token_here
```

**Key Features:**
- **Rate Limits:** 
  - Guest users: 60/min, 2000/hour
  - Authenticated: 100/min, 5000/hour
- **File Size:** Up to 50GB per file, 50GB total per record!
- **DOI Assignment:** Automatic DOI minting for published records
- **Versioning:** Full version control for datasets
- **Sandbox:** https://sandbox.zenodo.org/ for testing

**Test:**
```bash
# List your depositions
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://zenodo.org/api/deposit/depositions

# Search published records
curl "https://zenodo.org/api/records/?q=critical+infrastructure"
```

**Use Cases for Q-SMEC:**
- Download validated research datasets on infrastructure sectors
- Search for academic publications on quantum sensors
- Access government-funded research outputs
- Harvest metadata via OAI-PMH (120 req/min!)

---

### 7️⃣ OpenAlex Scholarly Database (2 minutes)

**Best for:** Academic publications, citations, author networks, research trends

**NO API KEY REQUIRED!** OpenAlex is completely free and open.

```
# Option 1: Add email to URL for "polite pool" (better performance)
https://api.openalex.org/works?mailto=s.dely@niketllc.com

# Option 2: Add to User-Agent header
# No setup file needed - just use in your HTTP requests
```

**Setup in .env:**
```bash
# Just add your email for polite pool access (optional but recommended)
OPENALEX_EMAIL=s.dely@niketllc.com
```

**Key Features:**
- **No Authentication:** Completely free, no signup required
- **Rate Limits:**
  - Common pool: 100,000/day, 10/second
  - Polite pool: Same limits but better response times
  - Premium (free for academics): Higher limits + special filters
- **Coverage:** 250M+ works, 2x coverage of Scopus/Web of Science
- **Data License:** CC0 (fully open)
- **Monthly Snapshots:** Complete database downloads available

**Test:**
```bash
# Search for critical infrastructure research
curl "https://api.openalex.org/works?search=critical+infrastructure&mailto=YOUR_EMAIL"

# Get works by topic
curl "https://api.openalex.org/works?filter=topics.id:T12345&mailto=YOUR_EMAIL"
```

**Use Cases for Q-SMEC:**
- Search 250M+ scholarly works on infrastructure topics
- Find citations and related research automatically
- Build author/institution collaboration networks
- Track emerging research trends across 16 sectors
- Download complete database snapshot for offline analysis

**Premium (Optional):**
- Free for academic researchers!
- Contact: support@openalex.org
- Benefits: Higher rate limits, `from_updated_date` filter for incremental updates

---

## 🔧 Configuration

### Setup .env File

```bash
# In Q-SMEC_Critical_16 directory
cp .env.example .env

# Edit .env with your favorite editor
code .env
# or
notepad .env
```

### Example .env (with keys)

```bash
# Government APIs
CENSUS_API_KEY=abc123def456ghi789
EIA_API_KEY=xyz789abc123def456
BEA_API_KEY=12345-67890-ABCDE
BLS_API_KEY=your_bls_key_here
NOAA_TOKEN=AbCdEfGhIjKlMnOp

# Optional
OPENALEX_EMAIL=research@niketllc.com
DATA_GOV_API_KEY=
ZENODO_API_TOKEN=your_zenodo_token_here
```

---

## 🧪 Testing Your Keys

Run the included test script:

```bash
cd Q-SMEC_Critical_16
python scripts/test_api_keys.py
```

Expected output:
```
✓ Census API: WORKING (rate limit: 5000/day)
✓ EIA API: WORKING (rate limit: 1000/hour)
✓ BEA API: WORKING
✓ BLS API: WORKING (rate limit: 500/day)
⚠ NOAA API: Not configured (optional)
⚠ Zenodo API: Not configured (optional)
```

---

## 📊 Rate Limits & Best Practices

### Government API Rate Limits

| API | Without Key | With Key | Recommended Usage |
|-----|-------------|----------|-------------------|
| Census | 500/day | 5,000/day | Cache results, batch requests |
| EIA | N/A | 1,000/hour | Spread requests over time |
| BEA | Limited | No limit | Be polite, cache data |
| BLS | 25/day | 500/day | Use v2 API, batch series |
| NOAA | N/A | 1,000/day | Download bulk datasets when possible |
| Zenodo | 60/min (2000/hr) | 100/min (5000/hr) | Use for research datasets, OAI-PMH harvesting |
| OpenAlex | 100k/day, 10/sec | Same (polite pool) | No key needed! Just add email to URL |

### Best Practices

1. **Cache Everything**
   - Save API responses to `data/raw/`
   - Don't re-fetch unchanged data

2. **Respect Rate Limits**
   - Use `tenacity` library for retries (included in requirements.txt)
   - Add delays between requests (1-2 seconds)

3. **Batch Requests**
   - BLS allows up to 50 series per request
   - Census allows multiple variables in one call

4. **Use Bulk Downloads**
   - Many agencies offer bulk data downloads
   - Faster and more respectful than API calls

---

## 🔒 Security

### DO NOT:
- ❌ Commit `.env` to Git
- ❌ Share keys in public repositories
- ❌ Email keys in plain text
- ❌ Hard-code keys in scripts

### DO:
- ✅ Keep `.env` in `.gitignore`
- ✅ Use environment variables
- ✅ Rotate keys periodically
- ✅ Use separate keys for dev/prod

### Existing Keys Location

**Available at:** `I:\My Drive\Website\DataAnalysisWebsite\API Keys\`

Current keys available:
- IBM Cloud API Key (IBM Cloud API Key.json)
- Atlassian/Jira API (id.atlassian_API Token.txt)
- Google Cloud service accounts (majestic-choir-*.json)
- AWS credentials (AWS Cloud Front Keys/, AWS X.509 Certificate/)
- Azure credentials (Azure - Deployment-Workspace-/)

**Note:** Government data API keys are NOT currently in this folder. You'll need to obtain them using the instructions above.

---

## 🆘 Troubleshooting

### "Invalid API Key" Error

**Solution:**
1. Verify key is copied correctly (no spaces)
2. Check if key is activated (some require email confirmation)
3. Ensure key is for correct environment (dev vs. prod)

### "Rate Limit Exceeded" Error

**Solution:**
1. Wait for rate limit reset (usually hourly or daily)
2. Implement caching to reduce requests
3. Use bulk download options when available

### "403 Forbidden" Error

**Solution:**
1. Check if API requires additional registration
2. Verify your IP isn't blocked
3. Ensure proper request headers (User-Agent, etc.)

---

## 📚 Additional Resources

### Official Documentation

- **Census API:** https://www.census.gov/data/developers/guidance/api-user-guide.html
- **EIA API:** https://www.eia.gov/opendata/documentation.php
- **BEA API:** https://apps.bea.gov/api/_pdf/bea_web_service_api_user_guide.pdf
- **BLS API:** https://www.bls.gov/developers/api_signature_v2.htm
- **NOAA API:** https://www.ncdc.noaa.gov/cdo-web/webservices/v2
- **Zenodo API:** https://developers.zenodo.org/
- **Zenodo OAI-PMH:** https://developers.zenodo.org/#oai-pmh
- **OpenAlex API:** https://docs.openalex.org/
- **OpenAlex Snapshot:** https://docs.openalex.org/download-all-data/openalex-snapshot

### Community Resources

- **Stack Overflow:** Search "census api", "eia api", etc.
- **GitHub Examples:** Many repos demonstrate API usage
- **Data.gov:** Portal to all federal datasets

---

## 📞 Support

**Questions about:**
- **API Keys:** Contact respective agency (links above)
- **Q-SMEC Package:** See main README.md
- **Technical Issues:** Check scripts/ directory for examples

---

**Last Updated:** October 29, 2025  
**Package Version:** Q-SMEC_Critical_16 v1.0
