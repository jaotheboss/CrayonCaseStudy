FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install -r /app/requirements_app.txt

CMD ["python", "-m", "streamlit", "run", "web_app.py"]