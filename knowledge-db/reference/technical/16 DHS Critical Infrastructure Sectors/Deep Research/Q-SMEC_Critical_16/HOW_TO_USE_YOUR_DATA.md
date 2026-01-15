# HOW TO USE YOUR Q-SMEC CRITICAL 16 DATA

**Created:** October 29, 2025  
**Your Data:** 2.26 MB across 16 DHS sectors, 1,175+ records, 11 government APIs

---

## 🎯 Quick Start Guide

### What You Have Now

```
data/raw/
├── chemical_sector.jsonl (141 KB - 100 EPA facility records)
├── commercial_facilities_sector.jsonl (9.4 KB - 50 BEA state records)
├── communications_sector.jsonl (38 KB - 100 FCC broadband records)
├── ... (13 more sector files)
└── Total: 16 JSONL files, all with real government API data
```

---

## 📊 Usage Options

### Option 1: Python Analysis (Recommended)

**Read and analyze any sector:**

```python
import json
import pandas as pd

# Load a sector
with open('data/raw/chemical_sector.jsonl', 'r') as f:
    data = json.load(f)

# Get the records
records = data['payload']
df = pd.DataFrame(records)

print(f"Sector: {data['sector']}")
print(f"Source: {data['source']}")
print(f"Records: {data['record_count']}")
print(df.head())
```

**Example output for Chemical sector:**
```
Sector: Chemical
Source: EPA_TRI_California
Records: 100
   facility_name         city  state  toxic_releases_lbs  year
0  Chevron USA Inc    Richmond    CA           1234.5    2023
1  Shell Oil         Martinez    CA            890.2    2023
...
```

### Option 2: Excel/CSV Export

**Convert JSONL to Excel:**

```python
import json
import pandas as pd

# Load sector data
with open('data/raw/healthcare_and_public_health_sector.jsonl', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data['payload'])

# Export to Excel
df.to_excel('healthcare_sector_data.xlsx', index=False)

# Or CSV
df.to_csv('healthcare_sector_data.csv', index=False)
```

### Option 3: Update Google Docs (Via Script)

**Using Google Docs API:**

```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Authenticate with Google
creds = Credentials.from_authorized_user_file('token.json', 
    ['https://www.googleapis.com/auth/documents'])
service = build('docs', 'v1', credentials=creds)

# Your Google Doc ID (from URL)
doc_id = 'YOUR_GOOGLE_DOC_ID'

# Read sector data
with open('data/raw/energy_sector.jsonl', 'r') as f:
    data = json.load(f)

# Create content
content = f"""
ENERGY SECTOR DATA (Updated {data['retrieved_at']})
Source: {data['source']}
Records: {data['record_count']}

Key Metrics:
{json.dumps(data['payload'][:5], indent=2)}
"""

# Insert into Google Doc
requests = [{
    'insertText': {
        'location': {'index': 1},
        'text': content
    }
}]

service.documents().batchUpdate(
    documentId=doc_id, 
    body={'requests': requests}
).execute()
```

### Option 4: Update Excel Workbook

**Populate your SMEC_Critical_Infrastructure v1.xlsx:**

```python
import json
import pandas as pd
from openpyxl import load_workbook

# Load your existing workbook
wb = load_workbook('SMEC_Critical_Infrastructure v1.xlsx')

# For each sector, add/update a sheet
sectors = [
    'chemical', 'commercial_facilities', 'communications',
    'critical_manufacturing', 'dams', 'defense_industrial_base',
    # ... all 16
]

for sector in sectors:
    # Load sector data
    with open(f'data/raw/{sector}_sector.jsonl', 'r') as f:
        data = json.load(f)
    
    # Convert to DataFrame
    df = pd.DataFrame(data['payload'])
    
    # Add metadata sheet
    metadata_df = pd.DataFrame([{
        'Sector': data['sector'],
        'Source': data['source'],
        'Retrieved': data['retrieved_at'],
        'Records': data['record_count'],
        'API Stability': data['api_stability']
    }])
    
    # Create or update sheet
    sheet_name = data['sector'][:31]  # Excel limit
    
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    
    # Write data
    ws = wb.create_sheet(sheet_name)
    for r_idx, row in enumerate(metadata_df.values, 1):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    # Add data rows
    for r_idx, row in enumerate(df.values, len(metadata_df)+2):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

wb.save('SMEC_Critical_Infrastructure_Updated.xlsx')
```

---

## 🔄 Automated Daily Updates

**Create a script to refresh all sectors:**

```python
# scripts/daily_update.py
import subprocess
from datetime import datetime

print(f"Starting daily update: {datetime.now()}")

# Re-fetch all sectors
subprocess.run([
    'python', 'scripts/refetch_all_sectors_enhanced.py'
])

# Verify coverage
subprocess.run([
    'python', 'scripts/verify_no_samples.py'
])

# Export to Excel
subprocess.run([
    'python', 'scripts/export_to_excel.py'
])

print("Update complete!")
```

**Schedule with Windows Task Scheduler:**
```powershell
# Run daily at 6 AM
$action = New-ScheduledTaskAction -Execute 'python' -Argument 'scripts/daily_update.py'
$trigger = New-ScheduledTaskTrigger -Daily -At 6am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "QSMEC_Daily_Update"
```

---

## 📈 Analysis Examples

### Example 1: Compare Sectors by Record Count

```python
import json
from pathlib import Path
import matplotlib.pyplot as plt

sectors = {}
for file in Path('data/raw').glob('*_sector.jsonl'):
    with open(file, 'r') as f:
        data = json.load(f)
        sectors[data['sector']] = data['record_count']

# Plot
plt.figure(figsize=(12, 6))
plt.barh(list(sectors.keys()), list(sectors.values()))
plt.xlabel('Number of Records')
plt.title('Q-SMEC Data Coverage by Sector')
plt.tight_layout()
plt.savefig('sector_coverage.png')
```

### Example 2: Geographic Analysis

```python
# Find all state-level data
import json
import pandas as pd

all_states = []
for file in Path('data/raw').glob('*_sector.jsonl'):
    with open(file, 'r') as f:
        data = json.load(f)
        if data['geo_level'] == 'state':
            for record in data['payload']:
                if 'state' in record:
                    all_states.append({
                        'sector': data['sector'],
                        'state': record.get('state'),
                        'value': record.get('gdp_millions', 0)
                    })

df = pd.DataFrame(all_states)
state_summary = df.groupby('state')['value'].sum().sort_values(ascending=False)
print(state_summary.head(10))
```

### Example 3: Time Series Trends

```python
# Extract year-over-year trends
import json
import pandas as pd

with open('data/raw/energy_sector.jsonl', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data['payload'])
if 'year' in df.columns:
    yearly = df.groupby('year').sum()
    yearly.plot(kind='line', figsize=(10, 6))
    plt.title(f"{data['sector']} Trends Over Time")
    plt.savefig('energy_trends.png')
```

---

## 🛠️ Integration Tools

### Tool 1: Google Sheets Integration

```python
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials.json', scope)
client = gspread.authorize(creds)

# Open spreadsheet
sheet = client.open('QSMEC Critical Infrastructure').sheet1

# Load sector data
with open('data/raw/chemical_sector.jsonl', 'r') as f:
    data = json.load(f)

# Write to Google Sheets
df = pd.DataFrame(data['payload'])
sheet.update([df.columns.values.tolist()] + df.values.tolist())
```

### Tool 2: Power BI Integration

**Create a Python script for Power BI:**

```python
# For Power BI "Get Data > Python Script"
import json
import pandas as pd
from pathlib import Path

# Load all sectors
all_data = []
for file in Path('data/raw').glob('*_sector.jsonl'):
    with open(file, 'r') as f:
        data = json.load(f)
        for record in data['payload']:
            record['sector'] = data['sector']
            record['source'] = data['source']
            record['retrieved_at'] = data['retrieved_at']
            all_data.append(record)

# This DataFrame will be available in Power BI
df = pd.DataFrame(all_data)
```

### Tool 3: Tableau Prep

**Export as Hyper file:**

```python
from tableauhyperapi import HyperProcess, Connection, TableDefinition, \
    SqlType, Inserter, CreateMode, TableName

# Start Hyper
with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU) as hyper:
    with Connection(hyper.endpoint, 'qsmec_data.hyper', CreateMode.CREATE_AND_REPLACE) as connection:
        
        # Define table
        table = TableDefinition(
            table_name=TableName('Extract', 'Sectors'),
            columns=[
                TableDefinition.Column('sector', SqlType.text()),
                TableDefinition.Column('source', SqlType.text()),
                TableDefinition.Column('record_count', SqlType.int()),
                # ... more columns
            ]
        )
        
        connection.catalog.create_table(table)
        
        # Insert data from all sectors
        # ... (data insertion code)
```

---

## 📋 Common Tasks

### Task 1: Generate Sector Summary Report

```python
import json
from pathlib import Path
from datetime import datetime

report = f"""
# Q-SMEC SECTOR SUMMARY REPORT
Generated: {datetime.now()}

"""

for file in sorted(Path('data/raw').glob('*_sector.jsonl')):
    with open(file, 'r') as f:
        data = json.load(f)
    
    report += f"""
## {data['sector']}
- **Source:** {data['source']}
- **Records:** {data['record_count']}
- **Retrieved:** {data['retrieved_at']}
- **Stability:** {data['api_stability']}
- **File Size:** {file.stat().st_size:,} bytes

"""

with open('SECTOR_SUMMARY_REPORT.md', 'w') as f:
    f.write(report)
```

### Task 2: Export Specific Fields to CSV

```python
import json
import csv

# Extract just the key metrics you need
with open('data/raw/financial_services_sector.jsonl', 'r') as f:
    data = json.load(f)

# Write to CSV
with open('financial_metrics.csv', 'w', newline='') as f:
    if data['payload']:
        writer = csv.DictWriter(f, fieldnames=data['payload'][0].keys())
        writer.writeheader()
        writer.writerows(data['payload'])
```

### Task 3: Create Pivot Table Data

```python
import json
import pandas as pd

# Load multiple sectors
sectors_data = []
for sector_name in ['energy', 'transportation', 'water']:
    with open(f'data/raw/{sector_name}_sector.jsonl', 'r') as f:
        data = json.load(f)
        df = pd.DataFrame(data['payload'])
        df['sector'] = data['sector']
        sectors_data.append(df)

# Combine
combined = pd.concat(sectors_data, ignore_index=True)

# Create pivot
if 'state' in combined.columns and 'year' in combined.columns:
    pivot = pd.pivot_table(combined, 
                          values='value', 
                          index='state', 
                          columns='sector', 
                          aggfunc='sum')
    
    pivot.to_excel('sector_pivot.xlsx')
```

---

## 🎓 Next Steps

1. **Choose your tool:**
   - Python + Pandas (most flexible)
   - Excel (familiar interface)
   - Google Sheets (collaboration)
   - Power BI/Tableau (visualization)

2. **Start simple:**
   - Load one sector
   - Explore the data
   - Create a basic chart

3. **Automate:**
   - Set up daily updates
   - Create standard reports
   - Build dashboards

4. **Scale up:**
   - Combine sectors
   - Add calculations
   - Share with stakeholders

---

## 🆘 Need Help?

**Common issues:**

1. **Can't read JSONL?**
   ```python
   # JSONL is just JSON, one object per file
   import json
   with open('file.jsonl', 'r') as f:
       data = json.load(f)  # Single object, not array
   ```

2. **Want CSV instead?**
   ```bash
   python scripts/export_to_csv.py
   ```

3. **Need specific fields only?**
   ```python
   records = data['payload']
   subset = [{k: r[k] for k in ['field1', 'field2']} for r in records]
   ```

---

**Your data is production-ready and waiting to be used!** 🚀
