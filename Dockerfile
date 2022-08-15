FROM python:3.8.6

COPY . ./app
COPY /frontend ./app
COPY /backend ./app

EXPOSE 8501

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "main.py"]