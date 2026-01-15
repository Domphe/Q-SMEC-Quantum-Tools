#!/usr/bin/env python3
"""Deep analysis of all Q-SMEC use cases - extract technical requirements, metrics, and insights."""

import sqlite3
import json
from collections import defaultdict

def main():
    conn = sqlite3.connect('db/qc_qp_expert.db')
    cursor = conn.cursor()
    
    print("=" * 100)
    print("COMPREHENSIVE Q-SMEC USE CASE ANALYSIS")
    print("=" * 100)
    
    # Get all use cases
    cursor.execute("SELECT id, domain, json FROM use_cases ORDER BY id")
    use_cases = cursor.fetchall()
    
    print(f"\nTotal Use Cases: {len(use_cases)}\n")
    
    # Analysis structures
    sector_analysis = defaultdict(list)
    trl_distribution = defaultdict(int)
    market_segments = []
    performance_requirements = defaultdict(list)
    technology_dependencies = defaultdict(set)
    customer_segments = defaultdict(list)
    
    # Analyze each use case
    for uc in use_cases:
        data = json.loads(uc[2])
        
        sector = data.get('sector', 'Unknown')
        title = data.get('title', 'N/A')
        trl = data.get('trl', 'N/A')
        tam = data.get('tam_2030', 0)
        cagr = data.get('cagr', 0)
        
        # Market analysis
        market_segments.append({
            'id': uc[0],
            'title': title,
            'sector': sector,
            'tam': tam,
            'cagr': cagr,
            'trl': trl
        })
        
        sector_analysis[sector].append({
            'title': title,
            'tam': tam,
            'cagr': cagr,
            'trl': trl
        })
        
        trl_distribution[trl] += 1
        
        # Performance requirements
        perf = data.get('performance_requirements', {})
        for key, value in perf.items():
            performance_requirements[key].append({
                'use_case': title,
                'value': value
            })
        
        # Technology dependencies
        tech_deps = data.get('technology_dependencies', [])
        for dep in tech_deps:
            technology_dependencies[dep].add(title)
        
        # Customer segments
        customers = data.get('customer_segments', [])
        for customer in customers:
            customer_segments[customer].append(title)
    
    # Print Sector Analysis
    print("=" * 100)
    print("SECTOR ANALYSIS")
    print("=" * 100)
    
    sorted_sectors = sorted(sector_analysis.items(), 
                          key=lambda x: sum(uc['tam'] for uc in x[1]), 
                          reverse=True)
    
    for sector, cases in sorted_sectors:
        total_tam = sum(uc['tam'] for uc in cases)
        avg_cagr = sum(uc['cagr'] for uc in cases) / len(cases) if cases else 0
        print(f"\n{sector}")
        print(f"  Use Cases: {len(cases)}")
        print(f"  Total TAM 2030: ${total_tam/1e9:.1f}B")
        print(f"  Avg CAGR: {avg_cagr:.1f}%")
        
        # Show top use cases by TAM
        top_cases = sorted(cases, key=lambda x: x['tam'], reverse=True)[:3]
        print(f"  Top Opportunities:")
        for uc in top_cases:
            print(f"    • {uc['title']:50} ${uc['tam']/1e9:5.1f}B, {uc['cagr']:4.1f}% CAGR, TRL {uc['trl']}")
    
    # TRL Distribution
    print("\n" + "=" * 100)
    print("TECHNOLOGY READINESS LEVEL (TRL) DISTRIBUTION")
    print("=" * 100)
    
    for trl in sorted(trl_distribution.keys()):
        count = trl_distribution[trl]
        bar = "█" * (count * 2)
        print(f"  TRL {trl}: {bar} ({count} use cases)")
    
    # Market Opportunity Analysis
    print("\n" + "=" * 100)
    print("MARKET OPPORTUNITY TIERS")
    print("=" * 100)
    
    mega_markets = [m for m in market_segments if m['tam'] >= 50e9]
    large_markets = [m for m in market_segments if 20e9 <= m['tam'] < 50e9]
    medium_markets = [m for m in market_segments if 10e9 <= m['tam'] < 20e9]
    small_markets = [m for m in market_segments if m['tam'] < 10e9]
    
    print(f"\nMega Markets (≥$50B TAM): {len(mega_markets)}")
    for m in sorted(mega_markets, key=lambda x: x['tam'], reverse=True):
        print(f"  • {m['title']:50} ${m['tam']/1e9:5.1f}B @ {m['cagr']:4.1f}% CAGR")
    
    print(f"\nLarge Markets ($20-50B TAM): {len(large_markets)}")
    for m in sorted(large_markets, key=lambda x: x['tam'], reverse=True):
        print(f"  • {m['title']:50} ${m['tam']/1e9:5.1f}B @ {m['cagr']:4.1f}% CAGR")
    
    print(f"\nMedium Markets ($10-20B TAM): {len(medium_markets)}")
    for m in sorted(medium_markets, key=lambda x: x['tam'], reverse=True):
        print(f"  • {m['title']:50} ${m['tam']/1e9:5.1f}B @ {m['cagr']:4.1f}% CAGR")
    
    print(f"\nSmall Markets (<$10B TAM): {len(small_markets)}")
    for m in sorted(small_markets, key=lambda x: x['tam'], reverse=True)[:5]:
        print(f"  • {m['title']:50} ${m['tam']/1e9:5.1f}B @ {m['cagr']:4.1f}% CAGR")
    
    # High-Growth Analysis
    print("\n" + "=" * 100)
    print("HIGH-GROWTH OPPORTUNITIES (CAGR ≥ 15%)")
    print("=" * 100)
    
    high_growth = sorted([m for m in market_segments if m['cagr'] >= 15], 
                        key=lambda x: x['cagr'], reverse=True)
    
    for m in high_growth:
        print(f"  • {m['title']:50} {m['cagr']:4.1f}% CAGR, ${m['tam']/1e9:5.1f}B TAM, TRL {m['trl']}")
    
    # Performance Requirements Analysis
    print("\n" + "=" * 100)
    print("PERFORMANCE REQUIREMENTS SUMMARY")
    print("=" * 100)
    
    for req_type, requirements in sorted(performance_requirements.items()):
        print(f"\n{req_type.upper().replace('_', ' ')}:")
        unique_values = set(str(r['value']) for r in requirements)
        print(f"  Use cases requiring: {len(requirements)}")
        print(f"  Range of requirements:")
        for r in requirements[:5]:
            print(f"    • {r['use_case']:40} → {r['value']}")
    
    # Technology Dependencies
    print("\n" + "=" * 100)
    print("CRITICAL TECHNOLOGY DEPENDENCIES")
    print("=" * 100)
    
    sorted_deps = sorted(technology_dependencies.items(), 
                        key=lambda x: len(x[1]), reverse=True)
    
    print(f"\nTop 10 Most Critical Technologies:")
    for tech, use_cases in sorted_deps[:10]:
        print(f"\n  {tech}:")
        print(f"    Required by {len(use_cases)} use cases")
        for uc in sorted(use_cases)[:3]:
            print(f"      • {uc}")
    
    # Customer Segment Analysis
    print("\n" + "=" * 100)
    print("CUSTOMER SEGMENT PENETRATION")
    print("=" * 100)
    
    sorted_customers = sorted(customer_segments.items(), 
                             key=lambda x: len(x[1]), reverse=True)
    
    for customer, cases in sorted_customers[:15]:
        print(f"\n  {customer}:")
        print(f"    Addressable by {len(cases)} use cases")
        for case in cases[:3]:
            print(f"      • {case}")
    
    # Strategic Recommendations
    print("\n" + "=" * 100)
    print("STRATEGIC RECOMMENDATIONS")
    print("=" * 100)
    
    total_tam = sum(m['tam'] for m in market_segments)
    weighted_cagr = sum(m['tam'] * m['cagr'] for m in market_segments) / total_tam if total_tam > 0 else 0
    
    print(f"\n1. MARKET POSITIONING:")
    print(f"   • Total Addressable Market: ${total_tam/1e9:.1f}B")
    print(f"   • Weighted Average CAGR: {weighted_cagr:.1f}%")
    print(f"   • Number of sectors covered: {len(sector_analysis)}")
    
    print(f"\n2. PRIORITIZATION:")
    print(f"   • Focus on {len(mega_markets)} mega markets (${sum(m['tam'] for m in mega_markets)/1e9:.1f}B)")
    print(f"   • Target {len(high_growth)} high-growth segments (≥15% CAGR)")
    
    print(f"\n3. TECHNOLOGY ROADMAP:")
    print(f"   • {trl_distribution.get(9, 0)} use cases at TRL 9 (ready for deployment)")
    print(f"   • {trl_distribution.get(7, 0) + trl_distribution.get(8, 0)} use cases at TRL 7-8 (near-term)")
    print(f"   • {sum(v for k, v in trl_distribution.items() if k <= 6)} use cases at TRL ≤6 (R&D phase)")
    
    print(f"\n4. GO-TO-MARKET:")
    priority_sectors = sorted_sectors[:3]
    print(f"   • Lead with: {', '.join([s[0] for s in priority_sectors])}")
    print(f"   • Combined TAM: ${sum(sum(uc['tam'] for uc in s[1]) for s in priority_sectors)/1e9:.1f}B")
    
    conn.close()

if __name__ == '__main__':
    main()
