import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "qc_qp_expert.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

use_cases = c.execute("SELECT id, json FROM use_cases").fetchall()
print(f"Found {len(use_cases)} use cases")

requirements = []
req_id_counter = 0

for uc_id, uc_json in use_cases:
    data = json.loads(uc_json)
    
    if 'market_size_billion' in data:
        req_id_counter += 1
        requirements.append((f"req.{uc_id}.market_{req_id_counter:04d}", uc_id, "market", "Market Size (TAM)", f"${data['market_size_billion']}B", None, None, "USD", "high", None, "target", None, f"TAM for {data.get('name', 'use case')}", json.dumps({"value": data['market_size_billion'], "unit": "billion USD"})))
    
    if 'cagr_percent' in data:
        req_id_counter += 1
        requirements.append((f"req.{uc_id}.growth_{req_id_counter:04d}", uc_id, "market", "Growth Rate (CAGR)", f"{data['cagr_percent']}%", None, None, "percent", "high", None, "target", None, "CAGR", json.dumps({"value": data['cagr_percent'], "unit": "percent"})))
    
    if 'trl_target' in data:
        req_id_counter += 1
        requirements.append((f"req.{uc_id}.trl_{req_id_counter:04d}", uc_id, "technical", "Technology Readiness Level", f"TRL {data['trl_target']}", None, None, "TRL_scale", "critical", None, "target", data['trl_target'], "Required TRL", json.dumps({"value": data['trl_target'], "scale": "1-9"})))
    
    if 'performance_targets' in data:
        targets = data['performance_targets']
        for target_name, target_value in targets.items():
            req_id_counter += 1
            priority = "high"
            if "optional" in target_name.lower():
                priority = "low"
            elif "critical" in target_name.lower() or "accuracy" in target_name.lower():
                priority = "critical"
            requirements.append((f"req.{uc_id}.perf_{req_id_counter:04d}", uc_id, "performance", target_name.replace('_', ' ').title(), str(target_value), None, None, "various", priority, None, "target", None, f"Performance: {target_name}", json.dumps({"target": target_value})))
    
    if 'key_technologies' in data:
        for tech in data['key_technologies']:
            req_id_counter += 1
            requirements.append((f"req.{uc_id}.tech_{req_id_counter:04d}", uc_id, "technology", f"{tech.replace('_', ' ').title()} Technology", "REQUIRED", None, None, None, "high", None, "required", None, f"Requires {tech}", json.dumps({"technology": tech, "status": "required"})))

print(f"Inserting {len(requirements)} requirements...")
c.executemany("""INSERT OR REPLACE INTO use_case_requirements (id, use_case_id, requirement_type, requirement_name, target_value, min_value, max_value, unit, priority, validation_method, current_status, trl_milestone, notes, json) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", requirements)
conn.commit()

count = c.execute("SELECT COUNT(*) FROM use_case_requirements").fetchone()[0]
print(f"Total: {count} records")
conn.close()
