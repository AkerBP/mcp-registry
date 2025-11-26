# MCP Registry - Docker Deployment Guide

## Azure Container Registry (ACR) Deployment

This guide explains how to build and deploy the MCP Registry to Azure Container Registry.

## Prerequisites

- Docker installed on your machine
- Access to Azure Container Registry
- ACR credentials (provided by IT team)

## Quick Start

### 1. Build the Docker Image

```powershell
# Navigate to the project directory
cd c:\Users\fdumont\Desktop\mcp-registry

# Build the Docker image
docker build -t mcp-registry:latest .
```

### 2. Test Locally (Optional)

```powershell
# Run the container locally
docker run -p 8000:8000 mcp-registry:latest

# Test the API
Invoke-RestMethod -Uri "http://localhost:8000/v0.1/servers?limit=50"
```

Or use Docker Compose:

```powershell
# Start the service
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### 3. Push to Azure Container Registry

**Note:** Replace `<your-acr-name>` with your actual ACR name (e.g., `akerbpacr.azurecr.io`)

```powershell
# Login to ACR
docker login <your-acr-name>.azurecr.io -u helm-nitro-token

# When prompted, paste the password: Adb68Hg0UzQ+bIjFyi=0jGIgwqk0AOja

# Tag the image for ACR
docker tag mcp-registry:latest <your-acr-name>.azurecr.io/mcp-registry:latest

# Push to ACR
docker push <your-acr-name>.azurecr.io/mcp-registry:latest
```

### 4. Deploy to Azure Container Instances (ACI)

```powershell
# Create container instance
az container create `
  --resource-group <your-resource-group> `
  --name mcp-registry `
  --image <your-acr-name>.azurecr.io/mcp-registry:latest `
  --registry-login-server <your-acr-name>.azurecr.io `
  --registry-username helm-nitro-token `
  --registry-password "Adb68Hg0UzQ+bIjFyi=0jGIgwqk0AOja" `
  --dns-name-label mcp-registry-akerbp `
  --ports 8000 `
  --cpu 1 `
  --memory 1

# Get the FQDN
az container show `
  --resource-group <your-resource-group> `
  --name mcp-registry `
  --query ipAddress.fqdn `
  --output tsv
```

Your API will be available at: `http://mcp-registry-akerbp.<region>.azurecontainer.io:8000`

### 5. Deploy to Azure App Service (Web App for Containers)

```powershell
# Create App Service Plan (if not exists)
az appservice plan create `
  --name mcp-registry-plan `
  --resource-group <your-resource-group> `
  --sku B1 `
  --is-linux

# Create Web App
az webapp create `
  --resource-group <your-resource-group> `
  --plan mcp-registry-plan `
  --name mcp-registry-akerbp `
  --deployment-container-image-name <your-acr-name>.azurecr.io/mcp-registry:latest

# Configure ACR credentials
az webapp config container set `
  --name mcp-registry-akerbp `
  --resource-group <your-resource-group> `
  --docker-custom-image-name <your-acr-name>.azurecr.io/mcp-registry:latest `
  --docker-registry-server-url https://<your-acr-name>.azurecr.io `
  --docker-registry-server-user helm-nitro-token `
  --docker-registry-server-password "Adb68Hg0UzQ+bIjFyi=0jGIgwqk0AOja"

# Set port
az webapp config appsettings set `
  --resource-group <your-resource-group> `
  --name mcp-registry-akerbp `
  --settings WEBSITES_PORT=8000
```

Your API will be available at: `https://mcp-registry-akerbp.azurewebsites.net`

## Environment Variables

The container uses the following environment variables:

- `FLASK_APP=app.py` - Flask application entry point
- `PYTHONUNBUFFERED=1` - Ensure logs are not buffered

## Health Check

Test the deployed API:

```powershell
# Health check
Invoke-RestMethod -Uri "http://<your-url>/health"

# List servers
Invoke-RestMethod -Uri "http://<your-url>/v0.1/servers?limit=50"
```

## Updating the Registry

To add or modify servers:

1. Edit `app.py` and update the `SERVERS_DATA` array
2. Rebuild the Docker image
3. Push to ACR
4. Restart the container/web app

## Troubleshooting

### Check container logs (ACI)
```powershell
az container logs --resource-group <your-resource-group> --name mcp-registry
```

### Check web app logs (App Service)
```powershell
az webapp log tail --resource-group <your-resource-group> --name mcp-registry-akerbp
```

### Test locally
```powershell
docker run -p 8000:8000 mcp-registry:latest
```

## Security Notes

- **IMPORTANT:** The ACR credentials in this document should be rotated regularly
- Consider using Azure Managed Identity for production deployments
- Enable HTTPS for production deployments
- Use Azure Key Vault for storing credentials

## VS Code Configuration

Once deployed, configure VS Code to use your registry:

```json
{
  "mcp.registry.url": "https://mcp-registry-akerbp.azurewebsites.net"
}
```

Or if using ACI:

```json
{
  "mcp.registry.url": "http://mcp-registry-akerbp.<region>.azurecontainer.io:8000"
}
```
