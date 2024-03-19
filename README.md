# user_service_playground
Build a Demo Service With gRPC

# Prepare
1. [Python](https://www.python.org/downloads/)
2. [Docker](https://docs.docker.com/engine/install/)
3. [Docker Compose](https://docs.docker.com/compose/install/)
4. Install Packages
   ```
   pip install -r requirements.txt
   ```

# Build & Deploy
1. `docker build -t user-service:latest .`
2. `docker compose up -d`

# Test
1. cd clients
2. CREATE: `python create_user.py`
3. GET: `python get_user.py`

# Reference
* [gRPC Python](https://grpc.github.io/grpc/python/)
* [Quick Start](https://grpc.io/docs/languages/python/quickstart/)
* [GitHub](https://github.com/grpc/grpc)

# TBD
* Secure Channel & Credentials
* AsyncIO