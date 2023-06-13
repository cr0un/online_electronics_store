FROM python:3.10-slim

WORKDIR /online_electronics_store/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 8000

CMD python3 ./manage.py runserver 0.0.0.0:8000

