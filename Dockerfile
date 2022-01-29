FROM python:3.8-slim
RUN mkdir -p /app
COPY . /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]