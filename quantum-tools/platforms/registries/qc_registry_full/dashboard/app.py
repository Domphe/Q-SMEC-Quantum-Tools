
import streamlit as st
import pandas as pd
import json

st.title("🔬 Quantum Chemistry Methods")

data = [json.loads(line) for line in open("data/methods_enriched.jsonl")]
df = pd.DataFrame(data)

cat = st.sidebar.multiselect("Category", df["category"].unique(), default=df["category"].unique())
df = df[df["category"].isin(cat)]

st.dataframe(df[["name", "category", "complexity", "citation_count", "typical_use_cases"]])
st.bar_chart(df["category"].value_counts())
