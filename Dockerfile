FROM python:3.9-slim
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD [ "python", "main.py" ]