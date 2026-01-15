import streamlit as st
import pandas as pd
import json
from pathlib import Path

from arxiv_qc_harvester.semantic import rank_by_semantic_similarity
from arxiv_qc_harvester.topics import tag_topics
from arxiv_qc_harvester.doi_enrich import enrich_with_crossref

st.set_page_config(page_title="Quantum Research Dashboard", layout="wide")
st.title("🧪 Quantum & Chemistry Research Assistant")

files = list(Path("data/raw/preprints").glob("*.jsonl"))
if not files:
    st.error("No preprint files found.")
    st.stop()

latest_file = sorted(files)[-1]
st.markdown(f"Loaded dataset: `{latest_file.name}`")

with open(latest_file) as f:
    entries = [json.loads(line) for line in f]

# Topic tagging
entries = tag_topics(entries, n_topics=6, n_top_words=6)

# Enrich with DOI metadata
entries = enrich_with_crossref(entries)

df = pd.DataFrame(entries)
df['published'] = pd.to_datetime(df['published'], errors='coerce')

# Sidebar: Semantic Search
st.sidebar.header("🔍 Semantic Search")
query = st.sidebar.text_input("Enter a semantic search query:")
top_k = st.sidebar.slider("Number of results", min_value=5, max_value=30, value=10)

if query:
    st.subheader(f"🔍 Top {top_k} semantic matches for: _{query}_")
    results = rank_by_semantic_similarity(entries, query, top_k=top_k)
    df = pd.DataFrame(results)

# Topic filter
all_topics = sorted({topic for entry in entries for tlist in entry.get("topics", []) for topic in tlist})
selected_topics = st.multiselect("🏷️ Filter by topics", all_topics)
if selected_topics:
    df = df[df["topics"].apply(lambda t: any(st in tlist for tlist in t for st in selected_topics))]

df = df.sort_values("published", ascending=False)

# Display
st.subheader("📄 Preprint Results")
for _, row in df.iterrows():
    st.markdown(f"### [{row['title']}]({row['url']})")
    st.write(f"**Authors:** {', '.join(row['authors'])}")
    st.write(f"**Published:** {row['published'].date() if pd.notnull(row['published']) else 'N/A'}")
    st.write(f"**Abstract:** {row['abstract']}")
    if row.get("topics"):
        st.markdown("**Topics:** " + ", ".join([" / ".join(t) for t in row["topics"]]))
    if row.get("publisher_full"):
        st.write(f"**Publisher:** {row['publisher_full']}")
    if row.get("journal"):
        st.write(f"**Journal:** {row['journal']}")
    if row.get("doi_url"):
        st.markdown(f"**DOI Link:** [{row['doi']}]({row['doi_url']})")
    st.markdown("---")

# EXPORTER SECTION
st.sidebar.subheader("📤 Export Session Results")
session_name = st.sidebar.text_input("Session name for exports", value="session")
export_format = st.sidebar.selectbox("Choose format", ["CSV", "Markdown", "BibTeX"])
if st.sidebar.button("Export"):
    from arxiv_qc_harvester.exporter import to_csv, to_markdown, to_bibtex, create_export_zip
    if export_format == "CSV":
        f = to_csv(df.to_dict("records"), session_name)
    elif export_format == "Markdown":
        f = to_markdown(df.to_dict("records"), session_name)
    else:
        f = to_bibtex(df.to_dict("records"), session_name)
    zip_path = create_export_zip([f], session_name)
    with open(zip_path, "rb") as zf:
        st.sidebar.download_button("⬇️ Download Export ZIP", zf, file_name=zip_path.name)

# ---- Crossref Enrichment ----
crossref_path = Path("data/raw/journals/crossref_qcqp.jsonl")
if crossref_path.exists():
    st.sidebar.markdown("✅ Crossref records loaded")
    with open(crossref_path, "r", encoding="utf-8") as f:
        crossref_entries = [json.loads(line) for line in f]
        st.sidebar.write(f"{len(crossref_entries)} records loaded from Crossref")

    # Optional: allow user to toggle view
    if st.sidebar.checkbox("Show Crossref records"):
        st.subheader("🔗 Crossref Enriched Records")
        crossref_df = pd.DataFrame(crossref_entries)
        for _, row in crossref_df.iterrows():
            st.markdown(f"### {row.get('title', [''])[0]}")
            st.write(f"**DOI**: [{row.get('DOI', 'N/A')}](https://doi.org/{row.get('DOI', '')})")
            st.write(f"**Type**: {row.get('type', '')}")
            st.write(f"**Publisher**: {row.get('publisher', '')}")
            st.write(f"**Published:** {row.get('issued', {}).get('date-parts', [['N/A']])[0][0]}")
            st.markdown("---")
else:
    st.sidebar.warning("No Crossref records found")

from arxiv_qc_harvester.openalex import fetch_openalex_citations

# DOI-based linking
doi_map = {entry['doi']: entry for entry in entries if entry.get('doi')}
crossref_df['matched_arxiv_doi'] = crossref_df['DOI'].apply(lambda d: doi_map.get(d) if isinstance(d, str) else None)

# Enrich with citations (cached)
if "citations" not in crossref_df.columns:
    crossref_df['citations'] = crossref_df['DOI'].apply(fetch_openalex_citations)

# Visualize type distribution
st.subheader("📊 Crossref Record Type Distribution")
import altair as alt
if not crossref_df.empty:
    type_chart = alt.Chart(crossref_df).mark_bar().encode(
        x=alt.X('type:N', sort='-y', title='Type'),
        y=alt.Y('count()', title='Count'),
        color='type:N'
    ).properties(height=300)
    st.altair_chart(type_chart, use_container_width=True)
