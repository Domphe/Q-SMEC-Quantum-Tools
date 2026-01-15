#!/usr/bin/env python3
"""
Comprehensive analysis module for QCBD benchmarks, methods, and use cases.
Provides statistical analysis, performance comparisons, and visualization support.
"""

import sqlite3
import json
from typing import Dict, List, Tuple, Any
from collections import defaultdict
import numpy as np

class QCBDAnalyzer:
    """Analyzer for quantum chemistry/physics database."""
    
    def __init__(self, db_path='db/qc_qp_expert.db'):
        self.db_path = db_path
        self.conn = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_path)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
    
    # ========================================================================
    # BENCHMARK ANALYSIS
    # ========================================================================
    
    def get_benchmark_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics on all benchmarks."""
        cursor = self.conn.cursor()
        
        stats = {
            'total_benchmarks': 0,
            'by_domain': {},
            'by_category': {},
            'total_entries': 0,
            'avg_entries_per_benchmark': 0,
            'benchmarks_by_property': {}
        }
        
        # Total count
        cursor.execute("SELECT COUNT(*) FROM datasets WHERE id LIKE 'benchmark.%'")
        stats['total_benchmarks'] = cursor.fetchone()[0]
        
        # By domain and category
        cursor.execute("""
            SELECT domain, json FROM datasets 
            WHERE id LIKE 'benchmark.%'
        """)
        
        total_entries = 0
        for domain, json_str in cursor.fetchall():
            data = json.loads(json_str)
            
            # Domain distribution
            stats['by_domain'][domain] = stats['by_domain'].get(domain, 0) + 1
            
            # Category distribution
            category = data.get('category', 'unknown')
            stats['by_category'][category] = stats['by_category'].get(category, 0) + 1
            
            # Property type
            prop = data.get('target_property', 'unknown')
            stats['benchmarks_by_property'][prop] = stats['benchmarks_by_property'].get(prop, 0) + 1
            
            # Entry count
            num_entries = data.get('num_entries', 0)
            total_entries += num_entries
        
        stats['total_entries'] = total_entries
        stats['avg_entries_per_benchmark'] = total_entries / stats['total_benchmarks'] if stats['total_benchmarks'] > 0 else 0
        
        return stats
    
    def find_benchmarks_for_property(self, property_type: str) -> List[Dict]:
        """Find all benchmarks that measure a specific property."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, domain, json FROM datasets 
            WHERE id LIKE 'benchmark.%'
        """)
        
        results = []
        for bench_id, domain, json_str in cursor.fetchall():
            data = json.loads(json_str)
            if property_type.lower() in data.get('target_property', '').lower():
                results.append({
                    'id': bench_id,
                    'name': data.get('name', 'N/A'),
                    'domain': domain,
                    'num_entries': data.get('num_entries', 0),
                    'accuracy_target': data.get('accuracy_target', {}),
                    'target_property': data.get('target_property', 'N/A')
                })
        
        return results
    
    def get_benchmark_coverage_gaps(self) -> Dict[str, List[str]]:
        """Identify gaps in benchmark coverage by analyzing property types."""
        cursor = self.conn.cursor()
        
        # Get all unique property types from benchmarks
        cursor.execute("""
            SELECT json FROM datasets WHERE id LIKE 'benchmark.%'
        """)
        
        covered_properties = set()
        for (json_str,) in cursor.fetchall():
            data = json.loads(json_str)
            prop = data.get('target_property', '')
            if prop:
                covered_properties.add(prop)
        
        # Get all equations (potential properties to benchmark)
        cursor.execute("SELECT id, json FROM equations")
        all_properties = set()
        for eq_id, json_str in cursor.fetchall():
            data = json.loads(json_str)
            # Extract property name from equation description
            all_properties.add(eq_id.split('.')[-1])
        
        # Identify gaps
        gaps = {
            'covered': sorted(covered_properties),
            'potential_gaps': sorted(all_properties - covered_properties),
            'coverage_rate': len(covered_properties) / len(all_properties) if all_properties else 0
        }
        
        return gaps
    
    # ========================================================================
    # METHOD ANALYSIS
    # ========================================================================
    
    def compare_methods(self, method_ids: List[str]) -> Dict[str, Any]:
        """Compare multiple methods across various attributes."""
        cursor = self.conn.cursor()
        
        comparison = {
            'methods': [],
            'comparison_matrix': {}
        }
        
        for method_id in method_ids:
            cursor.execute("SELECT json FROM methods WHERE id = ?", (method_id,))
            result = cursor.fetchone()
            if result:
                data = json.loads(result[0])
                comparison['methods'].append({
                    'id': method_id,
                    'name': data.get('name', 'N/A'),
                    'category': data.get('category', 'N/A'),
                    'complexity': data.get('complexity', 'N/A'),
                    'domain': data.get('domain', 'N/A')
                })
        
        return comparison
    
    def find_methods_for_problem(self, problem_type: str, system_size: int = None) -> List[Dict]:
        """Find suitable methods for a given problem type and system size."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, domain, json FROM methods")
        
        suitable_methods = []
        for method_id, domain, json_str in cursor.fetchall():
            data = json.loads(json_str)
            
            # Check if method applies to problem type
            use_cases = data.get('typical_use_cases', [])
            if any(problem_type.lower() in uc.lower() for uc in use_cases):
                method_info = {
                    'id': method_id,
                    'name': data.get('name', 'N/A'),
                    'domain': domain,
                    'category': data.get('category', 'N/A'),
                    'complexity': data.get('complexity', 'N/A'),
                    'strengths': data.get('strengths', []),
                    'limitations': data.get('limitations', [])
                }
                suitable_methods.append(method_info)
        
        return suitable_methods
    
    def get_method_hierarchy(self) -> Dict[str, List[str]]:
        """Build hierarchy of methods by accuracy/cost trade-off."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, json FROM methods")
        
        hierarchy = {
            'high_accuracy_high_cost': [],
            'medium_accuracy_medium_cost': [],
            'low_cost_screening': []
        }
        
        for method_id, json_str in cursor.fetchall():
            data = json.loads(json_str)
            complexity = data.get('complexity', '')
            category = data.get('category', '')
            
            # Classify based on complexity and category
            if 'post_hf' in category or 'CCSD' in method_id or 'CASSCF' in method_id:
                hierarchy['high_accuracy_high_cost'].append(method_id)
            elif 'dft' in category or 'B3LYP' in method_id or 'PBE' in method_id:
                hierarchy['medium_accuracy_medium_cost'].append(method_id)
            elif 'hf' in category or 'semi_empirical' in category:
                hierarchy['low_cost_screening'].append(method_id)
        
        return hierarchy
    
    # ========================================================================
    # USE CASE ANALYSIS
    # ========================================================================
    
    def get_use_case_market_analysis(self) -> Dict[str, Any]:
        """Comprehensive market analysis of all use cases."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, json FROM use_cases")
        
        analysis = {
            'total_tam': 0,
            'weighted_cagr': 0,
            'by_sector': defaultdict(lambda: {'count': 0, 'tam': 0, 'avg_cagr': 0}),
            'by_trl': defaultdict(int),
            'high_growth': [],  # CAGR >= 15%
            'mega_markets': [],  # TAM >= $50B
            'ready_for_deployment': []  # TRL >= 7
        }
        
        use_cases = []
        for uc_id, json_str in cursor.fetchall():
            data = json.loads(json_str)
            
            sector = data.get('sector', 'Unknown')
            tam = data.get('market_size_billion', 0) * 1e9  # Convert to dollars
            cagr = data.get('cagr_percent', 0)
            trl = data.get('trl_target', 'N/A')
            
            use_cases.append({
                'id': uc_id,
                'name': data.get('name', 'N/A'),
                'sector': sector,
                'tam': tam,
                'cagr': cagr,
                'trl': trl
            })
            
            # Accumulate statistics
            analysis['total_tam'] += tam
            analysis['by_sector'][sector]['count'] += 1
            analysis['by_sector'][sector]['tam'] += tam
            
            # TRL distribution
            analysis['by_trl'][trl] += 1
            
            # Identify special categories
            if cagr >= 15:
                analysis['high_growth'].append(uc_id)
            if tam >= 50e9:
                analysis['mega_markets'].append(uc_id)
            if '7' in str(trl) or '8' in str(trl) or '9' in str(trl):
                analysis['ready_for_deployment'].append(uc_id)
        
        # Calculate weighted CAGR
        if analysis['total_tam'] > 0:
            weighted_sum = sum(uc['tam'] * uc['cagr'] for uc in use_cases)
            analysis['weighted_cagr'] = weighted_sum / analysis['total_tam']
        
        # Calculate average CAGR per sector
        for sector_data in analysis['by_sector'].values():
            if sector_data['count'] > 0:
                sector_data['avg_cagr'] = sum(
                    uc['cagr'] for uc in use_cases if uc['sector'] == sector
                ) / sector_data['count']
        
        return analysis
    
    def get_technology_dependency_graph(self) -> Dict[str, List[str]]:
        """Build dependency graph showing which technologies are critical for multiple use cases."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, json FROM use_cases")
        
        tech_to_use_cases = defaultdict(list)
        
        for uc_id, json_str in cursor.fetchall():
            data = json.loads(json_str)
            technologies = data.get('key_technologies', [])
            
            for tech in technologies:
                tech_to_use_cases[tech].append(uc_id)
        
        # Sort by number of use cases
        sorted_deps = {
            tech: cases 
            for tech, cases in sorted(
                tech_to_use_cases.items(), 
                key=lambda x: len(x[1]), 
                reverse=True
            )
        }
        
        return sorted_deps
    
    def identify_strategic_priorities(self) -> Dict[str, List[str]]:
        """Identify strategic priorities based on market size, growth, and TRL."""
        analysis = self.get_use_case_market_analysis()
        
        priorities = {
            'immediate_deployment': analysis['ready_for_deployment'],  # TRL 7-9
            'high_value_targets': analysis['mega_markets'],  # TAM >= $50B
            'high_growth_markets': analysis['high_growth'],  # CAGR >= 15%
            'sweet_spot': []  # High value + high growth + near deployment
        }
        
        # Find sweet spot (intersection of high value, high growth, and near deployment)
        priorities['sweet_spot'] = list(
            set(priorities['immediate_deployment']) &
            set(priorities['high_value_targets']) &
            set(priorities['high_growth_markets'])
        )
        
        return priorities
    
    # ========================================================================
    # CROSS-CUTTING ANALYSIS
    # ========================================================================
    
    def generate_research_roadmap(self) -> Dict[str, Any]:
        """Generate a research roadmap based on database content and gaps."""
        roadmap = {
            'benchmark_gaps': self.get_benchmark_coverage_gaps(),
            'method_hierarchy': self.get_method_hierarchy(),
            'strategic_priorities': self.identify_strategic_priorities(),
            'technology_dependencies': self.get_technology_dependency_graph(),
            'recommendations': []
        }
        
        # Generate recommendations
        benchmark_gaps = roadmap['benchmark_gaps']
        if benchmark_gaps['coverage_rate'] < 0.75:
            roadmap['recommendations'].append(
                f"Benchmark coverage is only {benchmark_gaps['coverage_rate']:.1%}. "
                f"Consider adding benchmarks for: {', '.join(benchmark_gaps['potential_gaps'][:5])}"
            )
        
        tech_deps = roadmap['technology_dependencies']
        critical_techs = list(tech_deps.keys())[:5]
        roadmap['recommendations'].append(
            f"Critical technologies (used by most use cases): {', '.join(critical_techs)}"
        )
        
        return roadmap
    
    def print_summary_report(self):
        """Print comprehensive summary report."""
        print("=" * 80)
        print("QCBD COMPREHENSIVE ANALYSIS REPORT")
        print("=" * 80)
        
        # Benchmark statistics
        print("\n" + "=" * 80)
        print("BENCHMARK STATISTICS")
        print("=" * 80)
        bench_stats = self.get_benchmark_statistics()
        print(f"Total benchmarks: {bench_stats['total_benchmarks']}")
        print(f"Total entries across all benchmarks: {bench_stats['total_entries']:,}")
        print(f"Average entries per benchmark: {bench_stats['avg_entries_per_benchmark']:.1f}")
        
        print("\nBy domain:")
        for domain, count in sorted(bench_stats['by_domain'].items(), key=lambda x: x[1], reverse=True):
            domain_str = str(domain) if domain is not None else 'unknown'
            print(f"  {domain_str:30} : {count:3} benchmarks")
        
        print("\nBy category:")
        for category, count in sorted(bench_stats['by_category'].items(), key=lambda x: x[1], reverse=True):
            category_str = str(category) if category is not None else 'unknown'
            print(f"  {category_str:30} : {count:3} benchmarks")
        
        # Use case market analysis
        print("\n" + "=" * 80)
        print("USE CASE MARKET ANALYSIS")
        print("=" * 80)
        market = self.get_use_case_market_analysis()
        print(f"Total addressable market: ${market['total_tam']/1e9:.1f}B")
        print(f"Weighted average CAGR: {market['weighted_cagr']:.1f}%")
        print(f"High-growth opportunities (≥15% CAGR): {len(market['high_growth'])}")
        print(f"Mega markets (≥$50B TAM): {len(market['mega_markets'])}")
        print(f"Ready for deployment (TRL 7-9): {len(market['ready_for_deployment'])}")
        
        print("\nTop sectors by TAM:")
        for sector, data in sorted(market['by_sector'].items(), key=lambda x: x[1]['tam'], reverse=True)[:5]:
            print(f"  {sector:35} : ${data['tam']/1e9:6.1f}B ({data['count']} use cases, {data['avg_cagr']:.1f}% CAGR)")
        
        # Strategic priorities
        print("\n" + "=" * 80)
        print("STRATEGIC PRIORITIES")
        print("=" * 80)
        priorities = self.identify_strategic_priorities()
        print(f"Immediate deployment opportunities: {len(priorities['immediate_deployment'])}")
        print(f"High-value targets: {len(priorities['high_value_targets'])}")
        print(f"High-growth markets: {len(priorities['high_growth_markets'])}")
        print(f"Sweet spot (all three): {len(priorities['sweet_spot'])}")
        
        # Technology dependencies
        print("\n" + "=" * 80)
        print("CRITICAL TECHNOLOGY DEPENDENCIES")
        print("=" * 80)
        tech_deps = self.get_technology_dependency_graph()
        print("Top 10 most critical technologies:")
        for i, (tech, use_cases) in enumerate(list(tech_deps.items())[:10], 1):
            print(f"  {i:2}. {tech:40} → {len(use_cases):2} use cases")
        
        # Research roadmap
        print("\n" + "=" * 80)
        print("RESEARCH ROADMAP RECOMMENDATIONS")
        print("=" * 80)
        roadmap = self.generate_research_roadmap()
        for i, rec in enumerate(roadmap['recommendations'], 1):
            print(f"{i}. {rec}")


def main():
    """Run comprehensive analysis."""
    with QCBDAnalyzer() as analyzer:
        analyzer.print_summary_report()


if __name__ == '__main__':
    main()
