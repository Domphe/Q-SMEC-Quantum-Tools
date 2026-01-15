
import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Quantum Chemistry Method Explorer", layout="wide")

st.title("🔬 Quantum Chemistry Methods Registry")
data = [json.loads(line) for line in open("data/methods_linked.jsonl")]
df = pd.DataFrame(data)

category = st.sidebar.multiselect("Category", df["category"].unique(), default=df["category"].unique())
filtered = df[df["category"].isin(category)]

st.dataframe(filtered[["name", "category", "complexity", "accuracy_level", "typical_use_cases"]])
st.bar_chart(filtered["category"].value_counts())
