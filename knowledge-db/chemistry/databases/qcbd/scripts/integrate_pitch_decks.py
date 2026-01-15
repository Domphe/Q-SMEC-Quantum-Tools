"""
Comprehensive Pitch Deck Analysis & Database Integration
Analyzes all proprietary pitch decks and integrates new use cases, requirements, and market data
"""

import sqlite3, json, re
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "db" / "qc_qp_expert.db"

# ============================================================================
# EXTRACTED USE CASES FROM PITCH DECKS
# ============================================================================

PITCH_DECK_USE_CASES = [
    {
        'id': 'usecase.qsmec.mining_elf_sensor',
        'name': 'ELF Mineral Sensor (Cu/Au/Mo Porphyry)',
        'sector': 'Mining & Natural Resources',
        'partner': 'AIRTH.io / Erman Koc',
        'description': 'Extremely Low Frequency sensor tunable to characteristic frequencies of high-value minerals (Copper, Gold, Molybdenum) for porphyry deposit exploration',
        'market_size_billion': 8.5,
        'cagr_percent': 14,
        'trl_target': '7-9',
        'nre_cost_k': 770,
        'nre_timeline_weeks': 50,
        'performance_targets': {
            'nep_pw_sqhz': 0.001,  # Near elimination of 1/f flicker noise
            'snr_db': 30,
            'q_factor': 10000,
            'fom_pt_sqhz': 1.5,
            'frequency_hz_min': 0.01,
            'frequency_hz_max': 10,
            'sensitivity_pt_sqhz': 0.03,
            'response_time_ms': 65
        },
        'key_technologies': ['ELF_sensing', 'quantum_magnetometry', 'ground_penetrating', 'mineral_spectroscopy'],
        'competitive_advantages': ['Deeper penetration than GPR', 'Element-specific tuning', 'Lower false positives', 'Real-time processing'],
        'applications': ['Porphyry deposit mapping', 'Deep mineral exploration', 'Resource quantification', 'Geological surveying']
    },
    {
        'id': 'usecase.qsmec.sshel_power',
        'name': 'Solid-State High-Energy Laser + Power Storage',
        'sector': 'Defense & Aerospace',
        'partner': 'DeUVe Photonics / CM Laser',
        'description': 'SSHEL system with integrated quantum power storage for Golden Dome and DoD applications. Multi-wavelength capability with advanced thermal management',
        'market_size_billion': 18.3,
        'cagr_percent': 16,
        'trl_target': '6-8',
        'nre_cost_k': 770,
        'nre_timeline_weeks': 50,
        'performance_targets': {
            'power_kw': 100,
            'power_max_mw': 5,
            'beam_quality_m2': 1.1,
            'wavelength_micron_min': 0.4,
            'wavelength_micron_max': 14.0,
            'operating_range_km': 15,
            'bandwidth_nm': 100,
            'resolution_micron': 7.5,
            'pulse_mode': 'picosecond & continuous',
        },
        'key_technologies': ['SSHEL', 'quantum_energy_storage', 'thermal_management', 'beam_steering', 'multi_wavelength'],
        'wavelength_ranges': ['0.4-1.7 µm (visible-NIR)', '3-5 µm (MWIR)', '8-14 µm (LWIR)'],
        'applications': ['Directed energy weapons', 'Missile defense', 'Counter-UAS', 'Space debris removal', 'Communications'],
        'competitive_advantages': ['Order of magnitude higher power density', 'Multi-spectral operation', 'Integrated energy storage', 'Lower SWaP-C']
    },
    {
        'id': 'usecase.qsmec.sx_band_sensor',
        'name': 'S/X-Band Dual Sensor/Emitter',
        'sector': 'Defense & Aerospace',
        'partner': 'Delta Thermal / Sensor Group',
        'description': 'Combined S-band (2.3-2.5 GHz) and X-band (9.4-9.6 GHz) radar system for long-range surveillance and tracking',
        'market_size_billion': 12.0,
        'cagr_percent': 11,
        'trl_target': '6-8',
        'nre_cost_k': 770,
        'nre_timeline_weeks': 50,
        'performance_targets': {
            'power_kw': 60,
            'power_max_mw': 1,
            'eirp_dbmi': 50,
            'scan_ratio_sec': 15,
            'frequency_ghz_s_min': 2.3,
            'frequency_ghz_s_max': 2.5,
            'frequency_ghz_x_min': 9.4,
            'frequency_ghz_x_max': 9.6,
            'range_s_km': 500,
            'range_x_km': 70,
            'bandwidth_mhz': 625,
            'response_time_ps': 150,
            'resolution_s_m': 0.6,
            'resolution_x_m': 3,
            'dual_polarization': True
        },
        'key_technologies': ['S_band_radar', 'X_band_radar', 'dual_band', 'phased_array', 'AESA'],
        'applications': ['Air surveillance', 'Missile tracking', 'Weather monitoring', 'Maritime patrol', 'Ground moving target'],
        'competitive_advantages': ['Dual-band operation', 'Extended range', 'All-weather capability', 'Lower maintenance']
    },
    {
        'id': 'usecase.qsmec.thz_6g_cyber',
        'name': '6G THz Cyber-Resilient Communications',
        'sector': 'Telecommunications & Cybersecurity',
        'partner': 'FreeFall / BRN-HES',
        'description': 'Terahertz sensor/emitter for 6G communications with HES sensor fingerprinting and BRN cyber-resilience protocols. Anti-jamming and secure by design',
        'market_size_billion': 60.0,
        'cagr_percent': 12,
        'trl_target': '5-7',
        'nre_cost_k': 770,
        'nre_timeline_weeks': 50,
        'performance_targets': {
            'nep_pw_sqhz': 0.5,
            'snr_db': 120,
            'q_factor': 1500,
            'fom': 2500,
            'frequency_thz_min': 0.1,
            'frequency_thz_max': 10,
            'dynamic_range_db': 110,
            'response_time_ps': 150,
            'resolution_nm': 150,
        },
        'key_technologies': ['THz_sensing', '6G_communications', 'cyber_resilience', 'HES_fingerprinting', 'anti_jamming', 'post_quantum_crypto'],
        'applications': ['Ultra-high bandwidth comms', 'Secure tactical networks', 'Satellite links', 'Molecular detection', 'Non-destructive testing'],
        'competitive_advantages': ['Inherent cyber resilience', 'Anti-jamming', '100+ Gbps potential', 'Long-range THz', 'Post-quantum secure']
    },
    {
        'id': 'usecase.qsmec.rocket_fuel_thermal',
        'name': 'Solid-State Rocket Fuel + Thermal Management',
        'sector': 'Aerospace & Propulsion',
        'partner': 'Tiberius / Nobel Works / Quantum Motors',
        'description': 'Novel solid-state rocket propellant with liquid-like properties and advanced thermal management for rocket motors',
        'market_size_billion': 15.2,
        'cagr_percent': 9,
        'trl_target': '4-6',
        'nre_cost_k': 770,
        'nre_timeline_weeks': 50,
        'performance_targets': {
            'volumetric_heat_combustion_kj_sqcm': 250,
            'volumetric_energy_density_kj_ccm': 170,
            'gravimetric_heat_combustion_kj_g': 40,
            'thermal_conductivity_improvement': 10,
            'burn_rate_control': 'tunable'
        },
        'key_technologies': ['solid_state_propellant', 'thermal_management', 'combustion_control', 'high_energy_density'],
        'comparison_propellants': ['Methalox', 'Kerosene', 'Metallic hydrogen', 'APCP', 'CMDB', 'Zinc sulfur', 'Diborides'],
        'applications': ['Launch vehicles', 'Missiles', 'Space tugs', 'Tactical propulsion', 'Upper stages'],
        'competitive_advantages': ['Solid with liquid properties', 'Higher energy density', 'Safer handling', 'Tunable burn rate', 'Better thermal mgmt']
    },
    {
        'id': 'usecase.qsmec.prussian_blue_storage',
        'name': 'Prussian Blue Alternative Energy Storage',
        'sector': 'Energy Storage',
        'partner': 'Airtronics',
        'description': 'Quantum-optimized Prussian Blue analog (PBA) for next-gen battery cathode materials with enhanced performance',
        'market_size_billion': 25.0,
        'cagr_percent': 19,
        'trl_target': '5-7',
        'nre_cost_k': 770,
        'nre_timeline_weeks': 50,
        'performance_targets': {
            'matrix_diffusion_channel': 'optimized',
            'conductivity_improvement': 10,
            'strain_minimization': 'near_zero',
            'redox_voltage_improvement': 1.5,
            'interface_coating': 'quantum_optimized',
            'cycle_life_improvement': 5
        },
        'key_technologies': ['prussian_blue_analogs', 'quantum_cathodes', 'fast_charging', 'long_cycle_life'],
        'base_compound': 'Fe4(Fe(CN)6)3·H2O',
        'applications': ['Grid storage', 'EV batteries', 'Consumer electronics', 'Backup power', 'Microgrids'],
        'competitive_advantages': ['Lower cost than lithium', 'Abundant materials', 'Safer', 'Faster charging', 'Longer life']
    },
    {
        'id': 'usecase.qsmec.thz_sensor_general',
        'name': 'Terahertz Sensor/Emitter (General)',
        'sector': 'Multiple Sectors',
        'partner': 'Airtronics',
        'description': 'General-purpose THz sensor for imaging, communications, NDT, and molecular detection applications',
        'market_size_billion': 45.0,
        'cagr_percent': 18,
        'trl_target': '6-8',
        'nre_cost_k': 770,
        'nre_timeline_weeks': 50,
        'performance_targets': {
            'nep_pw_sqhz': 0.5,
            'snr_db': 120,
            'q_factor': 1500,
            'fom': 2500,
            'frequency_thz_min': 0.1,
            'frequency_thz_max': 10,
            'dynamic_range_db': 110,
            'response_time_ps': 150,
            'resolution_nm': 150,
        },
        'key_technologies': ['THz_sensing', 'THz_imaging', 'molecular_detection', 'NDT', 'spectroscopy'],
        'applications': ['6G communications', 'Security screening', 'Medical imaging', 'Quality control', 'Materials characterization', 'Pharmaceutical analysis'],
        'competitive_advantages': ['Sub-wavelength resolution', 'Non-ionizing', 'Material penetration', 'Chemical specificity', 'Real-time imaging']
    },
    {
        'id': 'usecase.qsmec.rcs_stealth',
        'name': 'RCS Multispectral Stealth Material',
        'sector': 'Defense & Aerospace',
        'partner': 'Airtronics',
        'description': 'Radar cross-section (RCS) reduction material with multispectral electromagnetic absorption across wide bandwidth',
        'market_size_billion': 9.8,
        'cagr_percent': 13,
        'trl_target': '6-8',
        'nre_cost_k': 770,
        'nre_timeline_weeks': 50,
        'performance_targets': {
            'complex_permittivity_imag': 0.1,
            'complex_permeability_imag': 0.1,
            'impedance_matching': 'wide_bandwidth',
            'dielectric_loss': 'high',
            'magnetic_loss': 'high',
            'weight_g_sqcm': 0.01,
            'layer_thickness_micron': 50,
            'bandwidth_decades': 3
        },
        'key_technologies': ['metamaterials', 'impedance_matching', 'wideband_absorption', 'lightweight_coatings'],
        'applications': ['Stealth aircraft', 'Naval vessels', 'Ground vehicles', 'Missiles', 'Drones', 'Antennas'],
        'competitive_advantages': ['Ultra-thin', 'Ultra-light', 'Wideband', 'Conformal', 'Durable', 'Low maintenance']
    }
]

# ============================================================================
# MARKET DATA FROM PITCH DECKS
# ============================================================================

MARKET_SEGMENTS = {
    'defense_intel_sensors': {
        'by_application': {
            'ISR': {'size_b': 7.3, 'cagr': 15},
            'GNC': {'size_b': 18.7, 'cagr': 7},
            'weapon_targeting': {'size_b': 9.0, 'cagr': 6},
            'electronic_warfare': {'size_b': 16.6, 'cagr': 7},
            'platform_control': {'size_b': 11.0, 'cagr': 5},
        },
        'by_sensor_type': {
            'EO_IR_hyperspectral': {'size_b': 13.8, 'cagr': 5},
            'MEMS': {'size_b': 16.3, 'cagr': 12},
            'LIDAR_RF_radar': {'size_b': 12.0, 'cagr': 5},
            'inertial_GNSS': {'size_b': 12.0, 'cagr': 5},
            'pressure': {'size_b': 2.9, 'cagr': 8.2},
            'acoustic_sonar': {'size_b': 1.8, 'cagr': 5},
            'chemical_biological': {'size_b': 2.1, 'cagr': 5},
            'fiber_optic': {'size_b': 1.2, 'cagr': 5},
        },
        'by_platform': {
            'space_airborne': {'size_b': 12.0, 'cagr': 5},
            'land': {'size_b': 13.1, 'cagr': 24},
            'naval': {'size_b': 4.5, 'cagr': 6.1},
        },
        'special_programs': {
            'golden_dome_shield': {'size_b': 360.0, 'cagr': 25, 'years': 10, 'sensor_comms_fraction': 0.33}
        }
    },
    'data_center_it_telecom': {
        'data_center_sensors': {
            'vibration': {'size_b': 1.2, 'cagr': 13},
            'thermal_ctm': {'size_b': 1.4, 'cagr': 8},
            'acoustic_das': {'size_b': 1.5, 'cagr': 8},
            'differential_pressure': {'size_b': 1.9, 'cagr': 8},
            'liquid_leak': {'size_b': 0.6, 'cagr': 13},
            'ir_motion': {'size_b': 2.0, 'cagr': 8},
            'rack_power_efficiency': {'size_b': 4.8, 'cagr': 8},
        },
        'telecom': {
            '5g_6g_sensors': {'size_b': 6.2, 'cagr': 11}
        }
    },
    'automotive': {
        'optical_fbg': {'size_b': 4.2, 'cagr': 8.6},
        'temperature_dic': {'size_b': 2.3, 'cagr': 6},
        'humidity': {'size_b': 7.3, 'cagr': 15},
        'ir_camera': {'size_b': 8.8, 'cagr': 15},
        'lidar': {'size_b': 1.2, 'cagr': 42},
        'ultrasonic': {'size_b': 6.0, 'cagr': 15},
        'co2': {'size_b': 0.03, 'cagr': 9.2},
        'gps_gnss_imu': {'size_b': 16.0, 'cagr': 8.3},
    },
    'energy_systems': {
        'advanced_metering': {'size_b': 21.4, 'cagr': 11.8},
        'fault_detection': {'size_b': 22.0, 'cagr': 8},
        'grid_asset_monitoring': {'size_b': 3.6, 'cagr': 19},
        'grid_load_monitoring': {'size_b': 5.8, 'cagr': 5.4},
        'distributed_energy_systems': {'size_b': 0.8, 'cagr': 13},
        'battery_storage': {'size_b': 25.0, 'cagr': 9},
        'small_nuclear_reactors': {'size_b': 10.0, 'cagr': 8},
        'solar_cell': {'size_b': 95.0, 'cagr': 17},
    }
}

# ============================================================================
# TECHNOLOGY SPECIFICATIONS
# ============================================================================

QSMEC_CORE_TECH = {
    'id': 'tech.qsmec.core',
    'name': 'Q-SMEC Core Technology',
    'description': 'Quantum Superconducting Magnetic Energy Containment - Dirac Plasmon Polariton Metamaterials',
    'key_features': [
        'Maximized quantum bonds (bondons) - 100 trillion mechanical bond equivalent per cm²',
        'Optimized plasmon quantum tunneling',
        '22 meta-elements: 10 disclosed (Mg, Ga, Sb, Te, Se, Al, Nb, N, Ti) + 12 confidential',
        'Hilbert space density matrices (DFT) + correlated wave functions (CWF)',
        '3D printing / thin-film vapor deposition compatible',
        'Lowest SWaP-C (Size/Weight/Power/Cost)',
        'Inherently anti-tamper (ITAR exportability)',
        'Inherently post-quantum crypto cyber resilient',
        'AI/ML DOE optimized'
    ],
    'disclosed_elements': ['Mg', 'Ga', 'Sb', 'Te', 'Se', 'Al', 'Nb', 'N', 'Ti'],
    'confidential_elements': 12,
    'performance_improvements': {
        'sensor_sensitivity': '10-100x',
        'energy_storage': '10-100x',
        'swp_reduction': '10x',
        'cost_reduction': '5-10x'
    },
    'manufacturing': ['Stratasys_3D_printing', 'thin_film_vapor_deposition', 'atomic_layer_deposition'],
    'nre_structure': {
        'task1': {'weeks': 8, 'hours': 1000, 'cost_k': 100, 'deliverable': 'Quantum model optimization', 'trl': 2},
        'task2': {'weeks': 6, 'hours': 1100, 'cost_k': 110, 'deliverable': 'DOE optimized configurations', 'trl': 2},
        'task3': {'weeks': 12, 'hours': 1900, 'cost_k': 190, 'deliverable': 'Prototype manufacture', 'trl': 4},
        'task4': {'weeks': 10, 'hours': 1100, 'cost_k': 110, 'deliverable': 'Lab integration simulated', 'trl': 6},
        'task5': {'weeks': 8, 'hours': 1300, 'cost_k': 130, 'deliverable': 'LRIP manufacturing demo', 'trl': 7},
        'task6': {'weeks': 8, 'hours': 1300, 'cost_k': 130, 'deliverable': 'Operational demo + V&V', 'trl': 8},
    },
    'ip_strategy': 'Joint IP with partners, exclusive field-of-use licensing',
    'citations': ['Q-SMEC White Paper V8', 'NIKET Proprietary Models']
}

def create_pitch_deck_use_cases():
    """Add all pitch deck use cases to database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    added = 0
    updated = 0
    
    for uc in PITCH_DECK_USE_CASES:
        existing = c.execute("SELECT id FROM use_cases WHERE id = ?", (uc['id'],)).fetchone()
        
        json_data = uc.copy()
        json_data['source'] = 'pitch_deck_analysis_2024'
        json_data['date_added'] = datetime.now().isoformat()
        
        if existing:
            # Update existing
            c.execute("UPDATE use_cases SET json = ? WHERE id = ?", (json.dumps(json_data), uc['id']))
            updated += 1
        else:
            # Insert new
            c.execute("INSERT INTO use_cases (id, domain, json) VALUES (?, ?, ?)", 
                     (uc['id'], 'quantum_physics', json.dumps(json_data)))
            added += 1
    
    conn.commit()
    conn.close()
    return added, updated

def create_pitch_deck_requirements():
    """Extract and add requirements from pitch deck use cases"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    records = []
    req_counter = 0
    
    for uc in PITCH_DECK_USE_CASES:
        uc_id = uc['id']
        
        # Market requirements
        if 'market_size_billion' in uc:
            req_counter += 1
            req_id = f"req.{uc_id}.pitch_market_{req_counter:04d}"
            json_data = {'value': uc['market_size_billion'], 'unit': 'billion USD', 'partner': uc.get('partner', 'N/A')}
            records.append((req_id, uc_id, "market", "TAM", f"${uc['market_size_billion']}B", None, None, "USD", 
                          "high", "Market analysis", "target", None, f"Total addressable market for {uc['name']}", json.dumps(json_data)))
        
        if 'cagr_percent' in uc:
            req_counter += 1
            req_id = f"req.{uc_id}.pitch_growth_{req_counter:04d}"
            json_data = {'value': uc['cagr_percent'], 'unit': 'percent', 'partner': uc.get('partner', 'N/A')}
            records.append((req_id, uc_id, "market", "CAGR", f"{uc['cagr_percent']}%", None, None, "percent", 
                          "high", "Market analysis", "target", None, "Compound annual growth rate", json.dumps(json_data)))
        
        # Technical requirements
        if 'nre_cost_k' in uc:
            req_counter += 1
            req_id = f"req.{uc_id}.pitch_nre_cost_{req_counter:04d}"
            json_data = {'value': uc['nre_cost_k'], 'unit': 'k USD', 'tasks': 6}
            records.append((req_id, uc_id, "technical", "NRE Cost", f"${uc['nre_cost_k']}K", uc['nre_cost_k'], uc['nre_cost_k'], "k_USD", 
                          "critical", "Budget", "target", None, "Non-recurring engineering cost (6 tasks)", json.dumps(json_data)))
        
        if 'nre_timeline_weeks' in uc:
            req_counter += 1
            req_id = f"req.{uc_id}.pitch_nre_timeline_{req_counter:04d}"
            json_data = {'value': uc['nre_timeline_weeks'], 'unit': 'weeks', 'tasks': 6}
            records.append((req_id, uc_id, "technical", "NRE Timeline", f"{uc['nre_timeline_weeks']} weeks", uc['nre_timeline_weeks'], 
                          uc['nre_timeline_weeks'], "weeks", "critical", "Schedule", "target", None, "Total NRE schedule", json.dumps(json_data)))
        
        if 'trl_target' in uc:
            req_counter += 1
            req_id = f"req.{uc_id}.pitch_trl_{req_counter:04d}"
            trl_val = re.search(r'(\d+)', uc['trl_target'])
            trl_num = int(trl_val.group(1)) if trl_val else 7
            json_data = {'value': uc['trl_target'], 'scale': '1-9'}
            records.append((req_id, uc_id, "technical", "TRL Target", f"TRL {uc['trl_target']}", None, None, "TRL", 
                          "critical", "Readiness", "target", trl_num, "Technology readiness level target", json.dumps(json_data)))
        
        # Performance requirements
        if 'performance_targets' in uc:
            for perf_name, perf_value in uc['performance_targets'].items():
                req_counter += 1
                req_id = f"req.{uc_id}.pitch_perf_{req_counter:04d}"
                
                priority = "high"
                if any(x in perf_name.lower() for x in ['critical', 'snr', 'nep', 'power']):
                    priority = "critical"
                
                json_data = {'parameter': perf_name, 'value': perf_value, 'use_case': uc['name']}
                records.append((req_id, uc_id, "performance", perf_name.replace('_', ' ').title(), str(perf_value), 
                              None, None, "mixed", priority, "Performance", "target", None, f"{perf_name} specification", json.dumps(json_data)))
        
        # Technology requirements
        if 'key_technologies' in uc:
            for tech in uc['key_technologies']:
                req_counter += 1
                req_id = f"req.{uc_id}.pitch_tech_{req_counter:04d}"
                json_data = {'technology': tech, 'status': 'required', 'use_case': uc['name']}
                records.append((req_id, uc_id, "technology", f"{tech.replace('_', ' ').title()} Technology", "REQUIRED", 
                              None, None, None, "high", "Technology", "required", None, f"Requires {tech} technology", json.dumps(json_data)))
    
    print(f"Creating {len(records)} pitch deck requirements...")
    c.executemany("""INSERT OR REPLACE INTO use_case_requirements 
                     (id, use_case_id, requirement_type, requirement_name, target_value, min_value, max_value, unit, 
                      priority, validation_method, current_status, trl_milestone, notes, json) 
                     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", records)
    conn.commit()
    conn.close()
    return len(records)

def create_qsmec_core_technology():
    """Add Q-SMEC core technology specification"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Add as method
    method_id = QSMEC_CORE_TECH['id']
    existing = c.execute("SELECT id FROM methods WHERE id = ?", (method_id,)).fetchone()
    
    if not existing:
        json_data = QSMEC_CORE_TECH.copy()
        json_data.pop('id')
        c.execute("INSERT INTO methods (id, domain, json) VALUES (?, ?, ?)", 
                 (method_id, "quantum_physics", json.dumps(json_data)))
        print("Added Q-SMEC core technology method")
    
    conn.commit()
    conn.close()

def create_market_data_records():
    """Add comprehensive market segment data"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    records = []
    
    for sector, subsectors in MARKET_SEGMENTS.items():
        for subsector_name, applications in subsectors.items():
            if not isinstance(applications, dict):
                continue
            for app_name, data in applications.items():
                if not isinstance(data, dict) or 'size_b' not in data:
                    continue
                rec_id = f"market.{sector}.{subsector_name}.{app_name}"
                title = f"{sector.replace('_', ' ').title()} - {subsector_name.replace('_', ' ').title()} - {app_name.replace('_', ' ').title()}"
                json_data = {
                    'sector': sector,
                    'subsector': subsector_name,
                    'application': app_name,
                    'size_billion': data['size_b'],
                    'cagr_percent': data['cagr'],
                    'source': 'NIKET pitch deck market analysis 2024',
                    'date': '2024-10-21'
                }
                
                # Store in sources table as market data
                c.execute("""INSERT OR REPLACE INTO sources (id, title, abstract, json) VALUES (?, ?, ?, ?)""",
                         (rec_id, title, f"Market data: ${data['size_b']}B TAM, {data['cagr']}% CAGR", json.dumps(json_data)))
                records.append(rec_id)
    
    conn.commit()
    conn.close()
    return len(records)

def main():
    print("\n" + "="*80)
    print("PITCH DECK COMPREHENSIVE ANALYSIS & DATABASE INTEGRATION")
    print("="*80)
    
    print("\nAnalyzing 8 proprietary Q-SMEC use case presentations...")
    print("  1. Mining ELF Sensor (AIRTH.io)")
    print("  2. SSHEL + Power Storage (DeUVe/CM Laser)")
    print("  3. S/X-Band Dual Sensor (Delta Thermal)")
    print("  4. 6G THz Cyber-Resilient Comms (FreeFall/BRN-HES)")
    print("  5. Rocket Fuel + Thermal Mgmt (Tiberius/Quantum Motors)")
    print("  6. Prussian Blue Energy Storage (Airtronics)")
    print("  7. General THz Sensor (Airtronics)")
    print("  8. RCS Stealth Material (Airtronics)")
    
    total = 0
    
    print("\n" + "-"*80)
    added, updated = create_pitch_deck_use_cases()
    print(f"✓ Use cases: {added} added, {updated} updated")
    total += added
    
    n_reqs = create_pitch_deck_requirements()
    print(f"✓ Requirements extracted: {n_reqs}")
    total += n_reqs
    
    create_qsmec_core_technology()
    print(f"✓ Q-SMEC core technology specification added")
    total += 1
    
    n_market = create_market_data_records()
    print(f"✓ Market segment data records: {n_market}")
    total += n_market
    
    print("\n" + "="*80)
    print(f"TOTAL RECORDS ADDED/UPDATED: {total}")
    print("="*80)
    
    # Summary statistics
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("\n" + "="*80)
    print("DATABASE SUMMARY AFTER PITCH DECK INTEGRATION")
    print("="*80)
    
    uc_total = c.execute("SELECT COUNT(*) FROM use_cases").fetchone()[0]
    print(f"Total use cases: {uc_total}")
    
    reqs_total = c.execute("SELECT COUNT(*) FROM use_case_requirements").fetchone()[0]
    print(f"Total requirements: {reqs_total}")
    
    methods_total = c.execute("SELECT COUNT(*) FROM methods").fetchone()[0]
    print(f"Total methods: {methods_total}")
    
    sources_total = c.execute("SELECT COUNT(*) FROM sources WHERE id LIKE 'market.%'").fetchone()[0]
    print(f"Market data sources: {sources_total}")
    
    print("="*80 + "\n")
    
    conn.close()

if __name__ == "__main__":
    main()
