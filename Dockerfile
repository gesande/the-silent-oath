FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p saves

EXPOSE 5000

ENV FLASK_ENV=production
ENV SECRET_KEY=change-me-in-production

CMD ["python", "app.py"]
