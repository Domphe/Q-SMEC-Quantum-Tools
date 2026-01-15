
# QC Enhanced Platform V2

## Components
- 🧠 Graphormer model prototype in `gnn_models/`
- 🌐 FastAPI REST API server in `api/`
- 📊 Streamlit UI toggle in `visualizations/ui_toggle.py`
- 📓 Notebook auto-run script in `scripts/run_notebooks.sh`

## Launch API
```bash
uvicorn api.main:app --reload
```

## Auto-run Training Notebook
```bash
bash scripts/run_notebooks.sh
```

## Streamlit UI
```bash
streamlit run visualizations/ui_toggle.py
```
