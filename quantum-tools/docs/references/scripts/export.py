#!/usr/bin/env python3
"""
Data export and pipeline execution script.
"""

import argparse
import logging
import sys
from pathlib import Path

from src.pipeline import DataPipeline, DataExporter
from src.introspector import DatabaseRegistry

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def export_table(args):
    """Export single table to file."""
    logger.info(f"Exporting table {args.table} from {args.database}")

    exporter = DataExporter(args.database)

    if args.format == "csv":
        exporter.export_to_csv(args.table, args.output)
    elif args.format == "json":
        exporter.export_to_json(args.table, args.output)

    logger.info(f"Exported to {args.output}")


def export_database(args):
    """Export all tables from database."""
    logger.info(f"Exporting database {args.database} to {args.output_dir}")

    pipeline = DataPipeline(args.database, args.output_dir)
    pipeline.export_all_tables(format=args.format)

    logger.info(f"Database exported to {args.output_dir}")


def export_directory(args):
    """Export all databases in directory."""
    logger.info(f"Exporting all databases in {args.directory}")

    registry = DatabaseRegistry(args.directory)

    for db_name, introspector in registry.databases.items():
        logger.info(f"Processing {db_name}...")
        db_path = str(introspector.db_path)

        output_dir = Path(args.output_dir) / db_name
        pipeline = DataPipeline(db_path, str(output_dir))
        pipeline.export_all_tables(format=args.format)

    logger.info(f"All databases exported to {args.output_dir}")


def create_summary(args):
    """Create summary report for database."""
    logger.info(f"Creating summary for {args.database}")

    pipeline = DataPipeline(args.database, ".")
    summary = pipeline.create_summary_report()

    import json

    output_file = args.output or f"{Path(args.database).stem}_summary.json"

    with open(output_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nSummary Report")
    print(f"{'=' * 60}")
    print(f"Database: {summary['database']}")
    print(f"Tables: {summary['table_count']}")
    for table in summary["tables"]:
        print(f"  {table['name']}: {table['row_count']:,} rows, {table['column_count']} columns")

    logger.info(f"Summary exported to {output_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Data export and pipeline tool")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Export single table
    table_parser = subparsers.add_parser("export-table", help="Export single table")
    table_parser.add_argument("database", help="Database path")
    table_parser.add_argument("table", help="Table name")
    table_parser.add_argument("-o", "--output", required=True, help="Output file path")
    table_parser.add_argument(
        "-f", "--format", choices=["csv", "json"], default="csv", help="Output format"
    )
    table_parser.set_defaults(func=export_table)

    # Export all tables from database
    db_parser = subparsers.add_parser(
        "export-database", help="Export all tables from database"
    )
    db_parser.add_argument("database", help="Database path")
    db_parser.add_argument("-o", "--output_dir", default="exports", help="Output directory")
    db_parser.add_argument(
        "-f", "--format", choices=["csv", "json"], default="csv", help="Output format"
    )
    db_parser.set_defaults(func=export_database)

    # Export all databases in directory
    dir_parser = subparsers.add_parser(
        "export-directory", help="Export all databases in directory"
    )
    dir_parser.add_argument("directory", help="Directory containing databases")
    dir_parser.add_argument("-o", "--output_dir", default="exports", help="Output directory")
    dir_parser.add_argument(
        "-f", "--format", choices=["csv", "json"], default="csv", help="Output format"
    )
    dir_parser.set_defaults(func=export_directory)

    # Create summary
    summary_parser = subparsers.add_parser("summary", help="Create database summary")
    summary_parser.add_argument("database", help="Database path")
    summary_parser.add_argument("-o", "--output", help="Output JSON file")
    summary_parser.set_defaults(func=create_summary)

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
