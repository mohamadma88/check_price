FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

ENV PYTHONUNBUFFERED 1

CMD ["python","manage.py","runserver","3000"]