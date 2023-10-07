# A Dockerfile for the llama_store project

FROM python:3.11-bullseye

WORKDIR /llama_store/
 
COPY ./llama_store /llama_store/
COPY ./requirements.txt /requirements.txt
COPY ./scripts/recreate_database.sh /scripts/recreate_database.sh

RUN pip install -r /requirements.txt
RUN chmod +x /scripts/recreate_database.sh && /scripts/recreate_database.sh
 
EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
