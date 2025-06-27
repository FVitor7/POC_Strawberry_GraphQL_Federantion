FROM python:3.10-slim

# Install Node.js
RUN apt-get update && apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python requirements and install
COPY task_service/requirements.txt /app/task_service/requirements.txt
COPY user_service/requirements.txt /app/user_service/requirements.txt
RUN pip install --no-cache-dir -r task_service/requirements.txt && \
    pip install --no-cache-dir -r user_service/requirements.txt

# Copy Node dependencies and install
COPY gateway/package.json /app/gateway/package.json
COPY gateway/package-lock.json /app/gateway/package-lock.json
RUN cd gateway && npm install && cd ..

# Copy source
COPY . /app

EXPOSE 7000 8000 8800

CMD bash -c "uvicorn user_service.app:app --host 0.0.0.0 --port 8000 & \
              uvicorn task_service.app:app --host 0.0.0.0 --port 8800 & \
              npx ts-node gateway/server.ts"
