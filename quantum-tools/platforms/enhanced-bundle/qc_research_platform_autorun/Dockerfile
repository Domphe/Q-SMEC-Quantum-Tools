FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -U scikit-learn joblib requests jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]