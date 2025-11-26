# GitHub Actions Setup for ACR Deployment

This guide explains how to configure GitHub Secrets for automatic deployment to Azure Container Registry.

## Required GitHub Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions → New repository secret

Add the following secret:

### ACR_PASSWORD (Required)
**Value:** `Adb68Hg0UzQ+bIjFyi=0jGIgwqk0AOja`

**Note:** The ACR login server (`hubnitroplatformacr.azurecr.io`) and username (`helm-nitro-token`) are already configured in the workflow.
**Value:** Your Azure resource group name (e.g., `rg-mcp-registry`)

### AZURE_RESOURCE_GROUP (Optional - for ACI deployment)
**Value:** Your Azure resource group name (e.g., `rg-mcp-registry`)

### Azure Service Principal (Optional - for ACI deployment)

If you want automatic deployment to Azure Container Instances, also add:

- **AZURE_CLIENT_ID**: Service principal client ID
- **AZURE_CLIENT_SECRET**: Service principal client secret  
- **AZURE_TENANT_ID**: Azure tenant ID

To create a service principal:
```bash
az ad sp create-for-rbac --name "github-mcp-registry" --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth
```

## Workflow Behavior

The workflow will automatically:

1. ✅ **Always:** Build and push Docker image to ACR when you push to `main` branch
2. ⚙️ **Optional:** Deploy to Azure Container Instances (if Azure secrets are configured)

## Manual Deployment

If you don't want automatic ACI deployment, the workflow will just build and push the image to ACR.

Then you or your IT team can manually deploy using:

```bash
az container create \
  --resource-group <your-rg> \
  --name mcp-registry \
  --image hubnitroplatformacr.azurecr.io/mcp-registry:latest \
  --registry-login-server hubnitroplatformacr.azurecr.io \
  --registry-username helm-nitro-token \
  --registry-password "Adb68Hg0UzQ+bIjFyi=0jGIgwqk0AOja" \
  --dns-name-label mcp-registry-akerbp \
  --ports 8000 \
  --cpu 1 \
  --memory 1
```

## Testing the Workflow

After setting up secrets:

1. Make a commit to the `main` branch
2. Go to Actions tab in GitHub
3. Watch the "Build and Deploy to ACR" workflow run
4. The Docker image will be pushed to your ACR

## Viewing Deployment URL

If ACI deployment is enabled, the workflow will output the container URL in the logs.

Example: `http://mcp-registry-akerbp.westeurope.azurecontainer.io:8000`

## Quick Setup Steps

1. ✅ **ACR configured:** `hubnitroplatformacr.azurecr.io`
2. Add `ACR_PASSWORD` secret: `Adb68Hg0UzQ+bIjFyi=0jGIgwqk0AOja`
3. Push a commit to trigger the workflow
4. Check the Actions tab to see the build progress

That's it! Your MCP registry will automatically build and deploy to ACR.
