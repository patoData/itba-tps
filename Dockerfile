FROM python:3.9

WORKDIR /to_sql

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY csv_to_sql.py .

CMD ["python", "csv_to_sql.py"]
