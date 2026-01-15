#!/usr/bin/env python3
"""Check Q-SMEC software tools registration in database."""

import sqlite3
import json

def main():
    conn = sqlite3.connect('db/qc_qp_expert.db')
    cursor = conn.cursor()
    
    print("=" * 80)
    print("Q-SMEC SOFTWARE TOOLS REGISTRATION CHECK")
    print("=" * 80)
    
    # Check for Q-SMEC tools
    cursor.execute("""
        SELECT id, domain, json
        FROM software_tools
        WHERE id LIKE 'tool.qsmec%'
        ORDER BY id
    """)
    
    qsmec_tools = cursor.fetchall()
    
    if qsmec_tools:
        print(f"\n✓ Found {len(qsmec_tools)} Q-SMEC tools:\n")
        for tool in qsmec_tools:
            data = json.loads(tool[2])
            name = data.get('name', 'N/A')
            license_info = data.get('license', 'N/A')
            url = data.get('official_url', 'N/A')
            print(f"  {name:30} | {tool[1]:20} | {license_info:15}")
            print(f"    → {url}")
    else:
        print("\n✗ No Q-SMEC tools found with 'tool.qsmec%' pattern")
        print("\nSearching for tools by name...")
        
        # Search by name
        tool_names = ['VASP', 'Wien2k', 'BoltzTraP', 'CST Studio', 'COMSOL', 
                      'openEMS', 'MEEP', 'Materials Project', 'AFLOW', 'Phonopy']
        
        cursor.execute("SELECT id, domain, json FROM software_tools")
        all_tools = cursor.fetchall()
        
        for target_name in tool_names:
            found = False
            for tool in all_tools:
                data = json.loads(tool[2])
                name = data.get('name', '')
                if target_name.lower() in name.lower():
                    print(f"  ✓ {target_name:20} found as: {name} (id: {tool[0]})")
                    found = True
                    break
            if not found:
                print(f"  ✗ {target_name:20} NOT FOUND")
    
    # Check all tools
    print("\n" + "=" * 80)
    print("ALL SOFTWARE TOOLS IN DATABASE:")
    print("=" * 80)
    cursor.execute("SELECT COUNT(*) FROM software_tools")
    total = cursor.fetchone()[0]
    print(f"\nTotal tools: {total}\n")
    
    cursor.execute("""
        SELECT domain, COUNT(*) as count
        FROM software_tools
        GROUP BY domain
        ORDER BY count DESC
    """)
    
    print("By domain:")
    for row in cursor.fetchall():
        print(f"  {row[0]:30} : {row[1]:3} tools")
    
    # List all tools
    print("\n" + "=" * 80)
    print("COMPLETE TOOL LIST:")
    print("=" * 80)
    cursor.execute("SELECT id, domain, json FROM software_tools ORDER BY domain, id")
    all_tools = cursor.fetchall()
    
    current_domain = None
    for tool in all_tools:
        if tool[1] != current_domain:
            current_domain = tool[1]
            print(f"\n{current_domain.upper()}:")
        data = json.loads(tool[2])
        name = data.get('name', 'N/A')
        print(f"  • {name:40} ({tool[0]})")
    
    conn.close()

if __name__ == '__main__':
    main()
