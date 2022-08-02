FROM python:3.10-slim
WORKDIR /sqlidecetor
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3", "main.py"]
CMD ["-h"]
