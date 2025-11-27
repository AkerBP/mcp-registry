# MCP Registry

A custom Model Context Protocol (MCP) server registry for AkerBP that provides a centralized API to discover and access MCP servers.

## What is This?

This repository contains a Flask-based API server (`app.py`) that implements a registry service for MCP (Model Context Protocol) servers. It allows applications like VS Code with GitHub Copilot to discover and connect to available MCP servers within the AkerBP organization.

## How app.py Works

The `app.py` file is a lightweight Flask web server that:

### 1. **Serves MCP Server Metadata**
   - Maintains a list of available MCP servers with their details (name, description, endpoints, etc.)
   - Currently includes:
     - **GitHub MCP Server** - For GitHub repository management
     - **Microsoft Docs MCP Server** - For Microsoft documentation access

### 2. **Provides REST API Endpoints**
   - **`/v0.1/servers`** - Returns the list of MCP servers (v0.1 protocol)
   - **`/v0/servers`** - Returns the list of MCP servers (v0 protocol, fallback)
   - **`/health`** - Health check endpoint for monitoring
   - **`/`** - API information and available endpoints

### 3. **Supports Query Parameters**
   - `limit` - Maximum number of servers to return (default: 50)
   - `offset` - Pagination offset (default: 0)
   - Example: `/v0.1/servers?limit=10&offset=0`

### 4. **Enables CORS**
   - Allows cross-origin requests so VS Code and other tools can access the API

### 5. **Returns JSON Responses**
   - All responses are in JSON format with proper content-type headers
   - Example response:
     ```json
     {
       "data": [
         {
           "name": "github",
           "displayName": "GitHub MCP Server",
           "description": "GitHub repository management MCP server",
           "version": "1.0.0",
           "remote": {
             "type": "http",
             "url": "https://api.githubcopilot.com/mcp/"
           }
         }
       ],
       "total": 2
     }
     ```

## Architecture

```
┌─────────────────┐
│   VS Code +     │
│ GitHub Copilot  │
└────────┬────────┘
         │
         │ HTTP Request: /v0.1/servers?limit=50
         │
         ▼
┌─────────────────┐
│   app.py        │
│  (Flask API)    │
├─────────────────┤
│ • CORS enabled  │
│ • Routes:       │
│   /v0.1/servers │
│   /v0/servers   │
│   /health       │
└────────┬────────┘
         │
         │ JSON Response
         │
         ▼
┌─────────────────┐
│ SERVERS_DATA    │
│ (In-memory list)│
├─────────────────┤
│ • GitHub Server │
│ • MS Docs Server│
└─────────────────┘
```

## Running Locally

### Prerequisites
- Python 3.11+
- pip

### Steps
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Server starts on http://localhost:8000
```

### Test the API
```bash
# Health check
curl http://localhost:8000/health

# Get servers
curl http://localhost:8000/v0.1/servers?limit=50

# API info
curl http://localhost:8000/
```

## Deployment

The registry can be deployed to:

1. **Azure Kubernetes Service (AKS)** - Recommended for production
   - See `AKS_DEPLOYMENT.md` for instructions
   - Uses manifests in `kubernetes/` folder

2. **Azure Container Instances** - Simple deployment
   - See `DEPLOYMENT.md` for instructions

3. **Docker** - Local testing
   - Use `docker-compose up` to run locally

## Adding New MCP Servers

To add a new MCP server to the registry:

1. **Edit `app.py`**
2. **Add a new entry to the `SERVERS_DATA` list**:
   ```python
   {
       "name": "your-server-id",
       "displayName": "Your Server Name",
       "description": "Description of your MCP server",
       "version": "1.0.0",
       "categories": ["Tools"],
       "tags": ["tag1", "tag2"],
       "publisher": {
           "name": "Publisher Name",
           "url": "https://publisher.com"
       },
       "repository": {
           "type": "git",
           "url": "https://github.com/org/repo"
       },
       "homepage": "https://server-homepage.com",
       "license": "MIT",
       "icon": "https://icon-url.com/icon.ico",
       "remote": {
           "type": "http",
           "url": "https://your-mcp-server-url.com/mcp/"
       }
   }
   ```
3. **Commit and push changes**
4. **GitHub Actions will automatically rebuild and deploy**

## Using the Registry in VS Code

Configure the MCP registry URL in VS Code settings:

```json
{
  "github.copilot.advanced": {
    "mcp.registry.url": "http://<your-deployment-url>"
  }
}
```

Replace `<your-deployment-url>` with your deployed registry URL.

## CI/CD Pipeline

GitHub Actions automatically:
1. ✅ Builds Docker image on push to `main`
2. ✅ Pushes to Azure Container Registry (ACR)
3. ✅ Deploys to AKS (if configured)

See `GITHUB_ACTIONS_SETUP.md` for configuration details.

## API Documentation

### GET /v0.1/servers

Returns list of available MCP servers.

**Query Parameters:**
- `limit` (optional, default: 50) - Maximum servers to return
- `offset` (optional, default: 0) - Pagination offset

**Response:**
```json
{
  "data": [
    {
      "name": "string",
      "displayName": "string",
      "description": "string",
      "version": "string",
      "categories": ["string"],
      "tags": ["string"],
      "publisher": { "name": "string", "url": "string" },
      "remote": { "type": "string", "url": "string" }
    }
  ],
  "total": 2
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Technology Stack

- **Python 3.11** - Runtime
- **Flask 3.0** - Web framework
- **Flask-CORS 4.0** - CORS support
- **Gunicorn 21.2** - Production WSGI server
- **Docker** - Containerization
- **Kubernetes** - Orchestration
- **Azure** - Cloud platform

## Repository Structure

```
mcp-registry/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container definition
├── kubernetes/                 # Kubernetes manifests
├── .github/workflows/          # CI/CD pipeline
├── DEPLOYMENT.md              # Deployment guide
├── AKS_DEPLOYMENT.md          # AKS deployment guide
└── README.md                  # This file
```

## Support

- **Repository:** https://github.com/AkerBP/mcp-registry
- **Contact:** AkerBP DevOps team

## License

Internal use only - AkerBP

