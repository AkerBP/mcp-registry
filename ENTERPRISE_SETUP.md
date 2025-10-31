# Enterprise MCP Registry Setup Guide

## Overview
This guide explains how to register and manage MCP (Model Context Protocol) servers in your enterprise environment.

## Current Setup
You have a local MCP registry configuration that can be used to manage MCP servers within your enterprise network.

## Registration Methods

### 1. Local Enterprise Registry (Current Setup)

#### Adding a New MCP Server
To add a new MCP server to your enterprise registry:

1. **Create server configuration** following MCP server.json format:
```json
{
  "name": "io.akerBP.enterprise/your-server-name",
  "description": "Description of your MCP server",
  "version": "1.0.0",
  "packages": [
    {
      "registryType": "npm",
      "identifier": "your-package-name",
      "version": "1.0.0",
      "transport": {
        "type": "stdio"
      }
    }
  ]
}
```

2. **Add to registry.json** in the servers array:
```json
{
  "servers": [
    {
      "serverId": "your-server-id",
      "name": "Your Server Name",
      "description": "Server description",
      "serverConfig": {
        // Your server.json content here
      },
      "status": "active",
      "publishedAt": "2025-10-31T00:00:00Z"
    }
  ]
}
```

### 2. Self-Hosted Enterprise Registry

For a more robust enterprise solution, you can deploy your own MCP registry server:

#### Requirements
- Kubernetes cluster or Docker environment
- PostgreSQL database
- GitHub OAuth application (for authentication)

#### Deployment Steps

1. **Clone the official registry**:
```bash
git clone https://github.com/modelcontextprotocol/registry.git
cd registry
```

2. **Configure environment**:
```bash
# Copy example environment file
cp .env.example .env

# Configure required variables
SERVER_ADDRESS=:8080
DATABASE_URL=postgres://user:pass@localhost:5432/mcp-registry
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

3. **Deploy using Docker**:
```bash
docker-compose up -d
```

4. **Deploy using Kubernetes**:
```bash
# Configure Pulumi for your environment
cd deploy
npm install
pulumi up
```

### 3. Official Registry Integration

To register with the official MCP registry:

#### Prerequisites
- GitHub repository containing your MCP server
- Valid server.json configuration
- GitHub authentication

#### Steps
1. **Install MCP publisher**:
```bash
go install github.com/modelcontextprotocol/registry/cmd/publisher@latest
```

2. **Authenticate with GitHub**:
```bash
publisher auth
```

3. **Publish your server**:
```bash
publisher publish path/to/your/server.json
```

## Enterprise Configuration Options

### Authentication
- **GitHub OAuth**: For developer authentication
- **Enterprise SSO**: Configure OIDC for enterprise identity providers
- **Anonymous Access**: For internal-only registries

### Package Registry Support
Your enterprise registry can support multiple package types:
- **NPM packages** (`registry.npmjs.org`)
- **PyPI packages** (`pypi.org`) 
- **NuGet packages** (`api.nuget.org`)
- **Docker/OCI images** (`docker.io`, `ghcr.io`)
- **MCPB packages** (custom binary format)

### Access Control
Configure server access based on:
- Repository ownership
- Organization membership
- Custom permission rules

## Server.json Configuration

### Basic Structure
```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/2025-10-17/server.schema.json",
  "name": "io.akerBP.enterprise/server-name",
  "title": "Human Readable Title",
  "description": "Detailed description of functionality",
  "version": "1.0.0",
  "repository": {
    "url": "https://github.com/AkerBP/your-repo",
    "source": "github",
    "id": "AkerBP/your-repo"
  },
  "packages": [
    // Package configurations
  ],
  "remotes": [
    // Remote service configurations
  ]
}
```

### Package Types

#### NPM Package
```json
{
  "registryType": "npm",
  "registryBaseUrl": "https://registry.npmjs.org",
  "identifier": "@akerBP/mcp-server",
  "version": "1.0.0",
  "runtimeHint": "npx",
  "transport": {
    "type": "stdio"
  }
}
```

#### Docker/OCI Image
```json
{
  "registryType": "oci", 
  "identifier": "ghcr.io/akerBP/mcp-server:1.0.0",
  "transport": {
    "type": "stdio"
  },
  "runtimeArguments": [
    {
      "type": "named",
      "name": "--mount",
      "value": "type=bind,src={source_path},dst={target_path}"
    }
  ]
}
```

## Validation Requirements

### Package Validation
Each package type requires specific validation:

- **NPM**: `mcpName` field in package.json must match server name
- **PyPI**: `mcp-name: server-name` format in package README
- **Docker**: `io.modelcontextprotocol.server.name` label in image
- **NuGet**: `mcp-name: server-name` format in package README

### Server Validation
- Unique server names within registry
- Valid semantic versioning
- Accessible package URLs
- Proper transport configuration

## API Usage

### List Servers
```bash
GET /v0/servers
```

### Get Server Details
```bash
GET /v0/servers/{serverId}
```

### Publish Server
```bash
POST /v0/publish
Authorization: Bearer <token>
Content-Type: application/json

{
  // server.json content
}
```

## Monitoring and Maintenance

### Health Checks
- Monitor registry API health: `GET /v0/health`
- Check database connectivity
- Validate package accessibility

### Updates
- Regularly update server versions
- Monitor for deprecated packages
- Review access permissions

## Best Practices

1. **Naming Convention**: Use reverse DNS notation (`io.akerBP.department.server-name`)
2. **Versioning**: Follow semantic versioning (major.minor.patch)
3. **Documentation**: Include comprehensive descriptions and usage examples
4. **Testing**: Validate servers before publishing
5. **Security**: Use enterprise authentication and access controls
6. **Monitoring**: Track server usage and health metrics

## Troubleshooting

### Common Issues
- **404 errors**: Check package availability and URLs
- **Authentication failures**: Verify GitHub OAuth configuration
- **Validation errors**: Ensure server.json follows schema requirements
- **Database errors**: Check PostgreSQL connectivity and configuration

### Support
- Internal IT support: admin@AkerBP.com
- MCP Documentation: https://modelcontextprotocol.io/
- Registry Issues: https://github.com/modelcontextprotocol/registry/issues