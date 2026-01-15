import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def show_metrics(metrics_file: str):
    df = pd.read_json(metrics_file)
    st.line_chart(df[['epoch', 'mae', 'r2']].set_index('epoch'))