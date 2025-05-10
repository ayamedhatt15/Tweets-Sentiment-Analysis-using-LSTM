FROM tensorflow/tensorflow:1.14.0-py3

WORKDIR /app

RUN apt-get update && \
    apt-get install -y python3-pip && \
    pip3 install --upgrade pip "setuptools<58.0.0"

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt && \
    python3 -m nltk.downloader stopwords

COPY ./app /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]