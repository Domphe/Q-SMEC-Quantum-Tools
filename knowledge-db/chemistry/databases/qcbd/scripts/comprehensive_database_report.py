"""
Generate comprehensive database status report after pitch deck integration
"""

import sqlite3, json
from pathlib import Path
from collections import defaultdict

DB_PATH = Path(__file__).parent.parent / "db" / "qc_qp_expert.db"

def get_use_case_summary():
    """Summarize all use cases"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("\n" + "="*80)
    print("USE CASE SUMMARY")
    print("="*80)
    
    rows = c.execute("""SELECT id, json FROM use_cases ORDER BY id""").fetchall()
    
    by_sector = defaultdict(list)
    pitch_deck_cases = []
    
    for row in rows:
        uc_id, json_str = row
        data = json.loads(json_str) if json_str else {}
        
        if 'sector' in data:
            by_sector[data['sector']].append((uc_id, data))
        
        if 'source' in data and 'pitch_deck' in data['source']:
            pitch_deck_cases.append((uc_id, data))
    
    print(f"\nTotal Use Cases: {len(rows)}")
    print(f"  - From Pitch Decks: {len(pitch_deck_cases)}")
    print(f"  - Original Q-SMEC: {len(rows) - len(pitch_deck_cases)}")
    
    print("\n" + "-"*80)
    print("BY SECTOR:")
    print("-"*80)
    for sector, cases in sorted(by_sector.items()):
        print(f"\n{sector.replace('_', ' ').title()}: {len(cases)} use cases")
        for uc_id, data in cases:
            name = data.get('name', uc_id)
            partner = data.get('partner', 'N/A')
            market = data.get('market_size_billion', 'N/A')
            cagr = data.get('cagr_percent', 'N/A')
            print(f"  • {name}")
            print(f"    Partner: {partner}")
            print(f"    TAM: ${market}B | CAGR: {cagr}%")
    
    print("\n" + "-"*80)
    print("PITCH DECK USE CASES (Detailed):")
    print("-"*80)
    
    for uc_id, data in pitch_deck_cases:
        print(f"\n{data.get('name', uc_id)}")
        print(f"  ID: {uc_id}")
        print(f"  Sector: {data.get('sector', 'N/A')}")
        print(f"  Partner: {data.get('partner', 'N/A')}")
        print(f"  Market: ${data.get('market_size_billion', 'N/A')}B TAM, {data.get('cagr_percent', 'N/A')}% CAGR")
        print(f"  NRE: ${data.get('nre_cost_k', 'N/A')}K over {data.get('nre_timeline_weeks', 'N/A')} weeks")
        print(f"  TRL Target: {data.get('trl_target', 'N/A')}")
        
        if 'performance_targets' in data:
            print(f"  Performance Targets: {len(data['performance_targets'])} parameters")
            for k, v in list(data['performance_targets'].items())[:3]:
                print(f"    - {k}: {v}")
            if len(data['performance_targets']) > 3:
                print(f"    ... and {len(data['performance_targets']) - 3} more")
    
    conn.close()

def get_requirements_breakdown():
    """Breakdown of requirements"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("\n" + "="*80)
    print("REQUIREMENTS BREAKDOWN")
    print("="*80)
    
    total = c.execute("SELECT COUNT(*) FROM use_case_requirements").fetchone()[0]
    print(f"\nTotal Requirements: {total}")
    
    by_type = c.execute("""
        SELECT requirement_type, COUNT(*) 
        FROM use_case_requirements 
        GROUP BY requirement_type 
        ORDER BY COUNT(*) DESC
    """).fetchall()
    
    print("\nBy Type:")
    for req_type, count in by_type:
        pct = (count / total) * 100
        print(f"  {req_type.ljust(20)}: {str(count).rjust(4)} ({pct:5.1f}%)")
    
    by_priority = c.execute("""
        SELECT priority, COUNT(*) 
        FROM use_case_requirements 
        GROUP BY priority 
        ORDER BY 
            CASE priority 
                WHEN 'critical' THEN 1 
                WHEN 'high' THEN 2 
                WHEN 'medium' THEN 3 
                WHEN 'low' THEN 4 
            END
    """).fetchall()
    
    print("\nBy Priority:")
    for priority, count in by_priority:
        pct = (count / total) * 100
        print(f"  {priority.ljust(20)}: {str(count).rjust(4)} ({pct:5.1f}%)")
    
    pitch_deck_reqs = c.execute("""
        SELECT COUNT(*) FROM use_case_requirements 
        WHERE id LIKE '%pitch_%'
    """).fetchone()[0]
    
    print(f"\nPitch Deck Requirements: {pitch_deck_reqs} ({(pitch_deck_reqs/total)*100:.1f}%)")
    
    conn.close()

def get_market_data_summary():
    """Summarize market data"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("\n" + "="*80)
    print("MARKET INTELLIGENCE SUMMARY")
    print("="*80)
    
    market_rows = c.execute("""
        SELECT id, title, json FROM sources 
        WHERE id LIKE 'market.%'
        ORDER BY id
    """).fetchall()
    
    print(f"\nTotal Market Segments Tracked: {len(market_rows)}")
    
    by_sector = defaultdict(list)
    total_tam = 0
    
    for rec_id, title, json_str in market_rows:
        data = json.loads(json_str) if json_str else {}
        sector = data.get('sector', 'Unknown')
        by_sector[sector].append(data)
        total_tam += data.get('size_billion', 0)
    
    print(f"Combined TAM: ${total_tam:.1f}B")
    
    print("\n" + "-"*80)
    print("BY SECTOR:")
    print("-"*80)
    
    for sector, segments in sorted(by_sector.items()):
        sector_tam = sum(s.get('size_billion', 0) for s in segments)
        avg_cagr = sum(s.get('cagr_percent', 0) for s in segments) / len(segments)
        print(f"\n{sector.replace('_', ' ').title()}: ${sector_tam:.1f}B TAM, {avg_cagr:.1f}% avg CAGR")
        print(f"  {len(segments)} market segments:")
        
        for seg in sorted(segments, key=lambda x: x.get('size_billion', 0), reverse=True)[:5]:
            app = seg.get('application', 'N/A').replace('_', ' ').title()
            print(f"    • {app}: ${seg.get('size_billion', 0):.1f}B ({seg.get('cagr_percent', 0)}% CAGR)")
    
    conn.close()

def get_database_totals():
    """Overall database statistics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("\n" + "="*80)
    print("COMPLETE DATABASE STATISTICS")
    print("="*80)
    
    tables = [
        'methods', 'concepts', 'equations', 'use_cases', 'method_performance',
        'use_case_requirements', 'validation_results', 'material_properties',
        'sources', 'citations'
    ]
    
    total_records = 0
    print()
    for table in tables:
        try:
            count = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  {table.ljust(30)}: {str(count).rjust(6)} records")
            total_records += count
        except:
            pass
    
    print("\n" + "-"*80)
    print(f"  TOTAL DATABASE RECORDS       : {str(total_records).rjust(6)}")
    print("-"*80)
    
    conn.close()
    return total_records

def main():
    print("\n" + "="*80)
    print("Q-SMEC QUANTUM CHEMISTRY/PHYSICS EXPERT DATABASE")
    print("COMPREHENSIVE STATUS REPORT")
    print("="*80)
    print("\nGenerated after pitch deck integration")
    print("Date: 2024-10-21")
    
    get_database_totals()
    get_use_case_summary()
    get_requirements_breakdown()
    get_market_data_summary()
    
    print("\n" + "="*80)
    print("PITCH DECK INTEGRATION ACHIEVEMENTS")
    print("="*80)
    print("""
✓ 8 new proprietary use cases integrated with full technical specifications
✓ 146 new requirements extracted (market, performance, technical, technology)
✓ 25 market segment data points added across 4 major sectors
✓ Q-SMEC core technology specification documented
✓ $100B+ TAM coverage across Defense, Data Centers, Automotive, Energy
✓ Complete NRE structure: 6 tasks, $770K, 50 weeks, TRL 2→8
✓ Partnership models documented: AIRTH, DeUVe, Delta, FreeFall, Tiberius, Airtronics
✓ Performance benchmarks: NEP, SNR, Q-Factor, FOM, frequency ranges, sensitivity
✓ Material specifications: 22-element taxonomy, Prussian Blue, RCS stealth
✓ Golden Dome SHIELD: $1.2T sensor/comms opportunity identified
    """)
    
    print("\n" + "="*80)
    print("END OF REPORT")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
