#!/usr/bin/env python3
"""
Command-line tool for database introspection and schema documentation.
"""

import argparse
import logging
import sys
from pathlib import Path

from src.introspector import DatabaseRegistry, DatabaseIntrospector
from src.schema_generator import RegistryDocumentationGenerator
from src.validator import DatabaseValidator

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def introspect_single(args):
    """Introspect a single database."""
    logger.info(f"Introspecting database: {args.database}")

    introspector = DatabaseIntrospector(args.database)
    metadata = introspector.introspect()

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"Database: {metadata.path}")
    print(f"Generated: {metadata.generated_at}")
    print(f"Total Tables: {len(metadata.tables)}")
    print(f"{'=' * 60}\n")

    for table in metadata.tables:
        print(f"Table: {table.name}")
        print(f"  Rows: {table.row_count:,}")
        print(f"  Columns: {len(table.columns)}")
        for col in table.columns:
            pk_marker = "[PK]" if col.primary_key else ""
            nullable = "NULL" if col.not_null else ""
            print(f"    - {col.name}: {col.type} {pk_marker} {nullable}")
        print()

    # Export if requested
    if args.output:
        introspector.export_metadata_json(args.output)
        logger.info(f"Metadata exported to {args.output}")


def introspect_directory(args):
    """Introspect all databases in directory."""
    logger.info(f"Introspecting databases in: {args.directory}")

    registry = DatabaseRegistry(args.directory)

    print(f"\n{'=' * 60}")
    print(f"Database Registry")
    print(f"Directory: {args.directory}")
    print(f"Total Databases: {len(registry.databases)}")
    print(f"{'=' * 60}\n")

    for db_name, introspector in registry.databases.items():
        print(f"Database: {db_name}")
        print(f"  Path: {introspector.db_path}")
        tables = introspector.get_table_names()
        print(f"  Tables: {len(tables)}")
        print()

    # Export all metadata if requested
    if args.output:
        registry.export_all_metadata(args.output)
        logger.info(f"All metadata exported to {args.output}")


def generate_documentation(args):
    """Generate schema documentation."""
    logger.info(f"Generating documentation for: {args.directory}")

    registry = DatabaseRegistry(args.directory)
    all_metadata = registry.get_all_metadata()

    generator = RegistryDocumentationGenerator(all_metadata)
    generator.export_all_documentation(args.output)

    logger.info(f"Documentation generated in {args.output}")


def validate_database(args):
    """Validate database integrity."""
    logger.info(f"Validating database: {args.database}")

    validator = DatabaseValidator(args.database)
    issues = validator.validate_all()

    report = validator.get_report()

    print(f"\n{'=' * 60}")
    print(f"Validation Report")
    print(f"Database: {args.database}")
    print(f"{'=' * 60}")
    print(f"Total Issues: {report['total_issues']}")
    print(f"  Critical: {report['severity_counts']['critical']}")
    print(f"  Errors: {report['severity_counts']['error']}")
    print(f"  Warnings: {report['severity_counts']['warning']}")
    print(f"  Info: {report['severity_counts']['info']}")
    print(f"{'=' * 60}\n")

    if issues:
        print("Issues Found:\n")
        for issue in issues:
            print(f"[{issue.severity.value.upper()}] {issue.issue_type}")
            print(f"  Table: {issue.table}")
            if issue.column:
                print(f"  Column: {issue.column}")
            print(f"  Message: {issue.message}")
            if issue.details:
                for key, value in issue.details.items():
                    print(f"  {key}: {value}")
            print()

    # Export report if requested
    if args.output:
        import json

        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        logger.info(f"Validation report exported to {args.output}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Database introspection and validation tool"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Introspect single database
    introspect_parser = subparsers.add_parser(
        "introspect", help="Introspect a single database"
    )
    introspect_parser.add_argument("database", help="Path to database file")
    introspect_parser.add_argument("-o", "--output", help="Output JSON file path")
    introspect_parser.set_defaults(func=introspect_single)

    # Introspect directory
    introspect_dir_parser = subparsers.add_parser(
        "introspect-dir", help="Introspect all databases in directory"
    )
    introspect_dir_parser.add_argument(
        "directory", help="Directory containing databases"
    )
    introspect_dir_parser.add_argument("-o", "--output", help="Output metadata directory")
    introspect_dir_parser.set_defaults(func=introspect_directory)

    # Generate documentation
    docs_parser = subparsers.add_parser(
        "generate-docs", help="Generate schema documentation"
    )
    docs_parser.add_argument("directory", help="Directory containing databases")
    docs_parser.add_argument("-o", "--output", default="schema_docs", help="Output directory")
    docs_parser.set_defaults(func=generate_documentation)

    # Validate database
    validate_parser = subparsers.add_parser("validate", help="Validate database")
    validate_parser.add_argument("database", help="Path to database file")
    validate_parser.add_argument("-o", "--output", help="Output report JSON file")
    validate_parser.set_defaults(func=validate_database)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        args.func(args)
        return 0
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
