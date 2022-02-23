FROM python:3.9

WORKDIR /user_service

COPY requirements.txt /user_service/
RUN pip install --no-cache-dir -r /user_service/requirements.txt

COPY . /user_service/

EXPOSE 8000

#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]