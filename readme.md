# RAG Service with FastAPI

This project is a standalone RAG (Retrieval-Augmented Generation) service. Its primary function is to act as a client that receives user queries, makes an API call to an external queryAPI for context, and then uses an OpenAI model to generate a natural language answer.

---

📂 Project Structure:

    main.py: The main entry point that launches the FastAPI application.

    api/: Defines the API endpoints for queries and health checks.

    core/: Contains the core logic for the RAG chain and communication with the external queryAPI.

    models/: Pydantic models for API request validation.

    Dockerfile: Instructions for building the application's Docker image.

    requirements.txt: A list of required Python packages.

---

🚀 Getting Started:

1. Prerequisites

    Python 3.9+

    Docker

    An OpenAI API Key

    The external queryAPI service (from the KM-KnowledgeManager project) must already be running.

2. Clone and cd
```Bash
git clone https://github.com/smartkms/SmartKMS_RAG.git
cd SmartKMS_RAG
```


3. Configuration (.env file)

Create a .env file in the root of this kms-rag-service directory. It requires two variables.

```env
OPENAI_API_KEY="sk-..."

# if you arent running with docker
QUERY_API_URL="http://127.0.0.1:8100/KM/search"

# with docker
QUERY_API_URL="http://host.docker.internal:8100/KM/search"
```

---

▶️ Running the Application:

You can run this service in two ways.

Method 1: Local

```Bash
# virtual environment
python3 -m venv .venv
source .venv/bin/activate 

# install dependencies
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

Method 2: Docker

```Bash
docker run -p 8001:8001 --env-file ./.env rag-service
```

---

⚙️ API: 

Your service will be available at `http://localhost:8001`. Interactive API documentation (Swagger UI) is at `http://localhost:8001/docs`.

Example curl command: 

Streaming: 

```Bash
curl -N -X POST "http://localhost:8001/api/v1/query/stream" \
-H "Content-Type: application/json" \
-d '{
  "query": "What are the main responsibilities of a project manager?",
  "user": "test-user-123"
}'
```

Non-streaming: 

```Bash
curl -X POST "http://localhost:8001/api/v1/query/non-stream" \
-H "Content-Type: application/json" \
-d '{
  "query": "What is the capital of Slovenia?",
  "user": "test-user-123",
  "type": "geography",
  "source": "world_facts.pdf"
}'
```
---

NOTE: Docker currently not working, am working on a fix
