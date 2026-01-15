"""
Synchronize all Q-SMEC databases with pitch deck integration data
Updates: strategic_partners.db, quantum_ai_tools.db, qc_graph.db, embeddings.db
"""

import sqlite3, json, shutil
from pathlib import Path
from datetime import datetime

# Database paths
MAIN_DB = Path("g:/My Drive/Databases/QCBD/db/qc_qp_expert.db")
STRATEGIC_DB = Path("g:/My Drive/Databases/strategic_partners.db")
TOOLS_DB = Path("g:/My Drive/Databases/Quantumn AI DB _ Tools/quantum_ai_tools.db")
GRAPH_DB = Path("g:/My Drive/Databases/QCBD/qc_graph.db")
EMBEDDINGS_DB = Path("g:/My Drive/Databases/QCBD/expert/embeddings.db")

# Backup all databases first
def backup_database(db_path):
    """Create timestamped backup"""
    if db_path.exists():
        backup_path = db_path.with_suffix(f'.db.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(db_path, backup_path)
        print(f"  ✓ Backed up: {db_path.name} -> {backup_path.name}")
        return backup_path
    return None

def sync_strategic_partners():
    """Update strategic_partners.db with pitch deck partner data"""
    print("\n" + "="*80)
    print("SYNCING: strategic_partners.db")
    print("="*80)
    
    backup_database(STRATEGIC_DB)
    
    conn_main = sqlite3.connect(MAIN_DB)
    conn_strat = sqlite3.connect(STRATEGIC_DB)
    c_main = conn_main.cursor()
    c_strat = conn_strat.cursor()
    
    # Create partners table if not exists
    c_strat.execute("""
        CREATE TABLE IF NOT EXISTS partners (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            sector TEXT,
            partnership_type TEXT,
            use_cases TEXT,
            tam_billion REAL,
            cagr_percent REAL,
            nre_cost_k REAL,
            trl_target TEXT,
            status TEXT,
            contact_info TEXT,
            notes TEXT,
            json TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)
    
    # Extract partner data from pitch deck use cases
    partners = [
        {
            'id': 'partner.airth',
            'name': 'AIRTH.io / Erman Koc',
            'sector': 'Mining & Natural Resources',
            'partnership_type': 'Joint Development',
            'use_cases': 'ELF Mineral Sensor (Cu/Au/Mo Porphyry)',
            'tam_billion': 8.5,
            'cagr_percent': 14,
            'nre_cost_k': 770,
            'trl_target': '7-9',
            'status': 'Active',
            'notes': 'Porphyry deposit exploration partnership'
        },
        {
            'id': 'partner.deuve_cmlaser',
            'name': 'DeUVe Photonics / CM Laser',
            'sector': 'Defense & Aerospace',
            'partnership_type': 'Joint IP',
            'use_cases': 'SSHEL + Power Storage',
            'tam_billion': 18.3,
            'cagr_percent': 16,
            'nre_cost_k': 770,
            'trl_target': '6-8',
            'status': 'Active',
            'notes': 'Solid-State High-Energy Laser development'
        },
        {
            'id': 'partner.delta_sensor',
            'name': 'Delta Thermal / Sensor Group',
            'sector': 'Defense & Aerospace',
            'partnership_type': 'Field-of-Use License',
            'use_cases': 'S/X-Band Dual Sensor/Emitter',
            'tam_billion': 12.0,
            'cagr_percent': 11,
            'nre_cost_k': 770,
            'trl_target': '6-8',
            'status': 'Active',
            'notes': 'Combined S-band and X-band radar system'
        },
        {
            'id': 'partner.freefall_brn',
            'name': 'FreeFall / BRN-HES',
            'sector': 'Telecommunications & Cybersecurity',
            'partnership_type': 'Technology Integration',
            'use_cases': '6G THz Cyber-Resilient Communications',
            'tam_billion': 60.0,
            'cagr_percent': 12,
            'nre_cost_k': 770,
            'trl_target': '5-7',
            'status': 'Active',
            'notes': 'THz with HES fingerprinting and BRN cyber protocols'
        },
        {
            'id': 'partner.tiberius_qm',
            'name': 'Tiberius / Nobel Works / Quantum Motors',
            'sector': 'Aerospace & Propulsion',
            'partnership_type': 'Co-Development',
            'use_cases': 'Rocket Fuel + Thermal Management',
            'tam_billion': 15.2,
            'cagr_percent': 9,
            'nre_cost_k': 770,
            'trl_target': '4-6',
            'status': 'Active',
            'notes': 'Solid-state rocket propellant development'
        },
        {
            'id': 'partner.airtronics',
            'name': 'Airtronics',
            'sector': 'Multiple Sectors',
            'partnership_type': 'Multi-Use Case Partnership',
            'use_cases': 'Prussian Blue Storage, THz Sensor, RCS Stealth',
            'tam_billion': 79.8,  # 25 + 45 + 9.8
            'cagr_percent': 16.7,  # Average
            'nre_cost_k': 2310,  # 3 use cases × 770
            'trl_target': '5-8',
            'status': 'Active',
            'notes': 'Three use case partnership: energy storage, THz, stealth'
        },
        {
            'id': 'partner.tier1_defense',
            'name': 'Defense Tier 1 Partner',
            'sector': 'Defense & Aerospace',
            'partnership_type': 'Strategic Partnership',
            'use_cases': 'Multiple Defense Applications',
            'tam_billion': 514.3,  # Total defense market
            'cagr_percent': 8.8,
            'nre_cost_k': None,
            'trl_target': 'Variable',
            'status': 'Prospective',
            'notes': 'Fortune 5000 strategic partner (confidential)'
        },
        {
            'id': 'partner.tier1_semiconductor',
            'name': 'AI Semiconductor Tier 1 Partner',
            'sector': 'Data Centers & IT',
            'partnership_type': 'Strategic Partnership',
            'use_cases': 'Data Center Sensors, AI Infrastructure',
            'tam_billion': 19.6,
            'cagr_percent': 9.6,
            'nre_cost_k': None,
            'trl_target': 'Variable',
            'status': 'Prospective',
            'notes': 'Fortune 5000 strategic partner (confidential)'
        },
        {
            'id': 'partner.tier1_automotive',
            'name': 'Automotive Tier 1 Partner',
            'sector': 'Automotive',
            'partnership_type': 'Strategic Partnership',
            'use_cases': 'LIDAR, IR Camera, Humidity, GPS/GNSS/IMU',
            'tam_billion': 47.6,  # Sum of automotive segments
            'cagr_percent': 17.4,
            'nre_cost_k': None,
            'trl_target': 'Variable',
            'status': 'Prospective',
            'notes': 'Fortune 5000 strategic partner (confidential)'
        },
        {
            'id': 'partner.tier1_energy',
            'name': 'Energy Tier 1 Partner',
            'sector': 'Energy Systems',
            'partnership_type': 'Strategic Partnership',
            'use_cases': 'Battery Storage, Smart Grid, Solar, Nuclear',
            'tam_billion': 282.6,  # Sum of energy segments
            'cagr_percent': 11.4,
            'nre_cost_k': None,
            'trl_target': 'Variable',
            'status': 'Prospective',
            'notes': 'Fortune 5000 strategic partner (confidential)'
        }
    ]
    
    inserted = 0
    updated = 0
    
    for partner in partners:
        existing = c_strat.execute("SELECT id FROM partners WHERE id = ?", (partner['id'],)).fetchone()
        
        json_data = partner.copy()
        json_data['source'] = 'pitch_deck_integration_2024'
        json_data['sync_date'] = datetime.now().isoformat()
        
        timestamp = datetime.now().isoformat()
        
        if existing:
            c_strat.execute("""
                UPDATE partners SET 
                    name=?, sector=?, partnership_type=?, use_cases=?, tam_billion=?, 
                    cagr_percent=?, nre_cost_k=?, trl_target=?, status=?, notes=?, 
                    json=?, updated_at=?
                WHERE id=?
            """, (partner['name'], partner['sector'], partner['partnership_type'], 
                  partner['use_cases'], partner['tam_billion'], partner['cagr_percent'],
                  partner['nre_cost_k'], partner['trl_target'], partner['status'], 
                  partner['notes'], json.dumps(json_data), timestamp, partner['id']))
            updated += 1
        else:
            c_strat.execute("""
                INSERT INTO partners 
                (id, name, sector, partnership_type, use_cases, tam_billion, cagr_percent, 
                 nre_cost_k, trl_target, status, notes, json, created_at, updated_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (partner['id'], partner['name'], partner['sector'], partner['partnership_type'],
                  partner['use_cases'], partner['tam_billion'], partner['cagr_percent'],
                  partner['nre_cost_k'], partner['trl_target'], partner['status'], 
                  partner['notes'], json.dumps(json_data), timestamp, timestamp))
            inserted += 1
    
    conn_strat.commit()
    conn_main.close()
    conn_strat.close()
    
    print(f"  ✓ Partners added: {inserted}")
    print(f"  ✓ Partners updated: {updated}")
    print(f"  ✓ Total partners: {inserted + updated}")

def sync_quantum_ai_tools():
    """Update quantum_ai_tools.db with use case and performance data"""
    print("\n" + "="*80)
    print("SYNCING: quantum_ai_tools.db")
    print("="*80)
    
    backup_database(TOOLS_DB)
    
    conn_main = sqlite3.connect(MAIN_DB)
    conn_tools = sqlite3.connect(TOOLS_DB)
    c_main = conn_main.cursor()
    c_tools = conn_tools.cursor()
    
    # Create use_cases table if not exists
    c_tools.execute("""
        CREATE TABLE IF NOT EXISTS use_cases (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            sector TEXT,
            description TEXT,
            tam_billion REAL,
            cagr_percent REAL,
            trl_target TEXT,
            performance_params TEXT,
            json TEXT,
            updated_at TEXT
        )
    """)
    
    # Create benchmarks table if not exists
    c_tools.execute("""
        CREATE TABLE IF NOT EXISTS benchmarks (
            id TEXT PRIMARY KEY,
            method TEXT,
            use_case_id TEXT,
            metric_name TEXT,
            metric_value REAL,
            metric_unit TEXT,
            reference TEXT,
            json TEXT,
            updated_at TEXT
        )
    """)
    
    # Copy use cases from main DB
    use_cases = c_main.execute("""
        SELECT id, json FROM use_cases WHERE id LIKE 'usecase.qsmec.%'
    """).fetchall()
    
    uc_count = 0
    for uc_id, json_str in use_cases:
        data = json.loads(json_str) if json_str else {}
        
        perf_params = json.dumps(data.get('performance_targets', {})) if 'performance_targets' in data else None
        
        c_tools.execute("""
            INSERT OR REPLACE INTO use_cases 
            (id, name, sector, description, tam_billion, cagr_percent, trl_target, performance_params, json, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (uc_id, data.get('name'), data.get('sector'), data.get('description'),
              data.get('market_size_billion'), data.get('cagr_percent'), data.get('trl_target'),
              perf_params, json_str, datetime.now().isoformat()))
        uc_count += 1
    
    # Copy performance benchmarks
    benchmarks = c_main.execute("""
        SELECT id, json FROM method_performance LIMIT 100
    """).fetchall()
    
    bench_count = 0
    for bench_id, json_str in benchmarks:
        data = json.loads(json_str) if json_str else {}
        
        c_tools.execute("""
            INSERT OR REPLACE INTO benchmarks
            (id, method, use_case_id, metric_name, metric_value, metric_unit, reference, json, updated_at)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (bench_id, data.get('method'), data.get('use_case'), data.get('property'),
              data.get('mae'), 'hartree', data.get('reference'), json_str, datetime.now().isoformat()))
        bench_count += 1
    
    conn_tools.commit()
    conn_main.close()
    conn_tools.close()
    
    print(f"  ✓ Use cases synced: {uc_count}")
    print(f"  ✓ Benchmarks synced: {bench_count}")

def sync_knowledge_graph():
    """Update qc_graph.db with relationships and entities"""
    print("\n" + "="*80)
    print("SYNCING: qc_graph.db")
    print("="*80)
    
    backup_database(GRAPH_DB)
    
    conn_main = sqlite3.connect(MAIN_DB)
    conn_graph = sqlite3.connect(GRAPH_DB)
    c_main = conn_main.cursor()
    c_graph = conn_graph.cursor()
    
    # Check if nodes table has the right schema
    existing_cols = [col[1] for col in c_graph.execute("PRAGMA table_info(nodes)").fetchall()]
    
    # Use existing schema: id, label, name, properties
    # edges table already exists with correct schema
    
    # Add use case nodes
    use_cases = c_main.execute("SELECT id, json FROM use_cases WHERE id LIKE 'usecase.qsmec.%'").fetchall()
    
    nodes_added = 0
    edges_added = 0
    timestamp = datetime.now().isoformat()
    
    for uc_id, json_str in use_cases:
        data = json.loads(json_str) if json_str else {}
        
        # Add use case node (using existing schema: id, label, name, properties)
        c_graph.execute("""
            INSERT OR REPLACE INTO nodes (id, label, name, properties)
            VALUES (?,?,?,?)
        """, (uc_id, data.get('name'), f"[USE_CASE] {data.get('name')}", json_str))
        nodes_added += 1
        
        # Add partner node and relationship
        if 'partner' in data:
            partner_id = f"partner.{uc_id.split('.')[-1]}"
            partner_props = json.dumps({'type': 'partner', 'name': data['partner'], 'use_case': uc_id})
            
            c_graph.execute("""
                INSERT OR REPLACE INTO nodes (id, label, name, properties)
                VALUES (?,?,?,?)
            """, (partner_id, data['partner'], f"[PARTNER] {data['partner']}", partner_props))
            nodes_added += 1
            
            # Add edge: use_case -> partner
            edge_id = f"edge.{uc_id}.partner"
            c_graph.execute("""
                INSERT OR REPLACE INTO edges (id, source_id, target_id, relationship, properties, created_at)
                VALUES (?,?,?,?,?,?)
            """, (edge_id, uc_id, partner_id, 'HAS_PARTNER', '{}', timestamp))
            edges_added += 1
        
        # Add sector node and relationship
        if 'sector' in data:
            sector_id = f"sector.{data['sector'].lower().replace(' ', '_').replace('&', 'and')}"
            sector_props = json.dumps({'type': 'sector', 'name': data['sector']})
            
            c_graph.execute("""
                INSERT OR REPLACE INTO nodes (id, label, name, properties)
                VALUES (?,?,?,?)
            """, (sector_id, data['sector'], f"[SECTOR] {data['sector']}", sector_props))
            nodes_added += 1
            
            # Add edge: use_case -> sector
            edge_id = f"edge.{uc_id}.sector"
            c_graph.execute("""
                INSERT OR REPLACE INTO edges (id, source_id, target_id, relationship, properties, created_at)
                VALUES (?,?,?,?,?,?)
            """, (edge_id, uc_id, sector_id, 'IN_SECTOR', '{}', timestamp))
            edges_added += 1
    
    conn_graph.commit()
    conn_main.close()
    conn_graph.close()
    
    print(f"  ✓ Nodes added: {nodes_added}")
    print(f"  ✓ Edges added: {edges_added}")

def sync_embeddings():
    """Update embeddings.db with use case text embeddings"""
    print("\n" + "="*80)
    print("SYNCING: embeddings.db")
    print("="*80)
    
    backup_database(EMBEDDINGS_DB)
    
    conn_main = sqlite3.connect(MAIN_DB)
    conn_embed = sqlite3.connect(EMBEDDINGS_DB)
    c_main = conn_main.cursor()
    c_embed = conn_embed.cursor()
    
    # Create documents table for embedding
    c_embed.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            doc_type TEXT,
            title TEXT,
            content TEXT,
            metadata TEXT,
            embedding BLOB,
            updated_at TEXT
        )
    """)
    
    # Extract use case text for embedding
    use_cases = c_main.execute("""
        SELECT id, json FROM use_cases WHERE id LIKE 'usecase.qsmec.%'
    """).fetchall()
    
    docs_added = 0
    timestamp = datetime.now().isoformat()
    
    for uc_id, json_str in use_cases:
        data = json.loads(json_str) if json_str else {}
        
        # Create text content for embedding
        content_parts = [
            data.get('name', ''),
            data.get('description', ''),
            f"Sector: {data.get('sector', '')}",
            f"Partner: {data.get('partner', '')}",
            f"Market: ${data.get('market_size_billion', 'N/A')}B TAM, {data.get('cagr_percent', 'N/A')}% CAGR"
        ]
        
        if 'performance_targets' in data:
            content_parts.append("Performance: " + ", ".join([f"{k}={v}" for k, v in list(data['performance_targets'].items())[:3]]))
        
        content = " | ".join([p for p in content_parts if p])
        
        metadata = json.dumps({
            'use_case_id': uc_id,
            'sector': data.get('sector'),
            'partner': data.get('partner'),
            'tam_billion': data.get('market_size_billion'),
            'source': 'pitch_deck_integration'
        })
        
        c_embed.execute("""
            INSERT OR REPLACE INTO documents (id, doc_type, title, content, metadata, updated_at)
            VALUES (?,?,?,?,?,?)
        """, (uc_id, 'use_case', data.get('name'), content, metadata, timestamp))
        docs_added += 1
    
    conn_embed.commit()
    conn_main.close()
    conn_embed.close()
    
    print(f"  ✓ Documents added for embedding: {docs_added}")
    print(f"  ℹ Note: Embeddings need to be generated separately using embedding model")

def generate_summary():
    """Generate final summary"""
    print("\n" + "="*80)
    print("DATABASE SYNCHRONIZATION COMPLETE")
    print("="*80)
    
    # Check all databases
    databases = [
        ("Main Expert DB", MAIN_DB),
        ("Strategic Partners DB", STRATEGIC_DB),
        ("Quantum AI Tools DB", TOOLS_DB),
        ("Knowledge Graph DB", GRAPH_DB),
        ("Embeddings DB", EMBEDDINGS_DB)
    ]
    
    print("\nDatabase Status:")
    for name, db_path in databases:
        if db_path.exists():
            size_mb = db_path.stat().st_size / (1024 * 1024)
            print(f"  ✓ {name.ljust(25)}: {size_mb:>8.2f} MB - {db_path.name}")
        else:
            print(f"  ✗ {name.ljust(25)}: NOT FOUND")
    
    print("\n" + "="*80)
    print("NEXT STEPS:")
    print("="*80)
    print("""
1. Generate embeddings for new use case documents in embeddings.db
2. Verify strategic_partners.db for partnership tracking
3. Update quantum_ai_tools.db with ML/AI model outputs
4. Export knowledge graph visualization from qc_graph.db
5. Run Phase 2 enrichment for remaining scientific gaps

All databases backed up with timestamp: {timestamp}
    """.format(timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")))

def main():
    print("\n" + "="*80)
    print("Q-SMEC DATABASE SYNCHRONIZATION")
    print("Pitch Deck Integration -> All Supporting Databases")
    print("="*80)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        sync_strategic_partners()
        sync_quantum_ai_tools()
        sync_knowledge_graph()
        sync_embeddings()
        generate_summary()
        
        print("\n✅ All databases synchronized successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during synchronization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
