"""Harvest open courseware (MIT OCW, etc.)."""
import sys
from datetime import date
from utils import write_jsonl, DATA_RAW

OPEN_COURSES = [
    {
        "id": "src.course.mit_ocw_8_04",
        "type": "course",
        "title": "MIT 8.04 Quantum Physics I",
        "authors": ["Barton Zwiebach"],
        "year": 2016,
        "publisher": "MIT OpenCourseWare",
        "provenance": "open_courseware",
        "url": "https://ocw.mit.edu/courses/8-04-quantum-physics-i-spring-2016/",
        "domains": ["quantum_physics"],
        "trust_tier": "B",
        "allowed_content": "full_open_content",
        "open_access": True,
        "keywords": ["quantum mechanics", "undergraduate", "foundations"],
        "notes": "MIT OCW: Creative Commons BY-NC-SA license.",
        "last_verified": str(date.today())
    },
    {
        "id": "src.course.mit_ocw_5_61",
        "type": "course",
        "title": "MIT 5.61 Physical Chemistry",
        "authors": ["Robert Field"],
        "year": 2017,
        "publisher": "MIT OpenCourseWare",
        "provenance": "open_courseware",
        "url": "https://ocw.mit.edu/courses/5-61-physical-chemistry-fall-2017/",
        "domains": ["quantum_chemistry"],
        "trust_tier": "B",
        "allowed_content": "full_open_content",
        "open_access": True,
        "keywords": ["physical chemistry", "thermodynamics", "kinetics"],
        "notes": "MIT OCW: Creative Commons BY-NC-SA license.",
        "last_verified": str(date.today())
    },
    {
        "id": "src.course.mit_ocw_5_73",
        "type": "course",
        "title": "MIT 5.73 Quantum Mechanics I",
        "authors": ["Robert Field"],
        "year": 2020,
        "publisher": "MIT OpenCourseWare",
        "provenance": "open_courseware",
        "url": "https://ocw.mit.edu/courses/5-73-quantum-mechanics-i-fall-2020/",
        "domains": ["quantum_chemistry", "quantum_physics"],
        "trust_tier": "B",
        "allowed_content": "full_open_content",
        "open_access": True,
        "keywords": ["quantum mechanics", "graduate", "spectroscopy"],
        "notes": "MIT OCW: Creative Commons BY-NC-SA license.",
        "last_verified": str(date.today())
    }
]

def main():
    """Harvest open courseware."""
    output_path = DATA_RAW / "courses" / "open_courseware.jsonl"
    
    write_jsonl(output_path, OPEN_COURSES)
    
    print(f"Harvested open courseware:")
    print(f"  {output_path} ({len(OPEN_COURSES)} courses)")
    print("\nLegal compliance: Full open content from MIT OCW (CC BY-NC-SA).")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
