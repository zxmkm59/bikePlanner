FROM python:3.8.6

COPY . ./app


WORKDIR /app

RUN pip install -r requirements.txt

CMD ["streamlit", "run", "main.py"]