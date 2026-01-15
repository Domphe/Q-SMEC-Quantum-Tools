from arxiv_qc_harvester import fetcher, parser, utils, config
import time

def main():
    all_items = []
    for cat in config.CATEGORIES:
        start = 0
        while True:
            try:
                xml_text = fetcher.fetch_arxiv_xml(cat, start=start)
                entries = parser.parse_arxiv_entries(xml_text, cat)
                if not entries:
                    break
                all_items.extend(entries)
                start += len(entries)
                time.sleep(1)
            except Exception as e:
                print(f"[ERROR] {cat}: {e}")
                break
    utils.write_jsonl(config.DATA_RAW / f"preprints/arxiv_qcqp_{config.TODAY}.jsonl", all_items)

if __name__ == "__main__":
    main()
