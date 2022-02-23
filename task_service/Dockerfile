FROM python:3.9

WORKDIR /task_service

COPY requirements.txt /task_service/
RUN pip install --no-cache-dir -r /task_service/requirements.txt

COPY . /task_service/

EXPOSE 8800

#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8800"]