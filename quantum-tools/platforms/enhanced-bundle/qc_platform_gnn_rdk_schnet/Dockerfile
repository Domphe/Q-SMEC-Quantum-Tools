FROM pytorch/pytorch:latest
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]