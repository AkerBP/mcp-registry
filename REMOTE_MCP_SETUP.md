# Remote MCP Server Setup Guide

## Overview
This guide shows how to use MCP servers without installing them locally on your computer.

## Option 1: Remote MCP Services

### Configuration for Claude Desktop
Instead of local installation, use remote endpoints:

```json
{
  "mcpServers": {
    "markitdown-remote": {
      "command": "mcp-proxy",
      "args": ["--url", "https://markitdown-mcp.example.com/sse"]
    },
    "filesystem-remote": {
      "command": "mcp-proxy", 
      "args": ["--url", "https://filesystem-mcp.example.com/http"]
    }
  }
}
```

## Option 2: Enterprise MCP Gateway

Deploy MCP servers on a shared enterprise server:

### Server Setup (IT Department)
```bash
# On enterprise server (e.g., mcp.akerBP.com)
docker run -d --name markitdown-mcp -p 3001:3001 \
  markitdown-mcp:latest --http --host 0.0.0.0 --port 3001

docker run -d --name filesystem-mcp -p 3002:3002 \
  filesystem-mcp:latest --http --host 0.0.0.0 --port 3002
```

### Client Configuration
```json
{
  "mcpServers": {
    "markitdown": {
      "command": "curl",
      "args": ["-X", "POST", "https://mcp.akerBP.com:3001/mcp"]
    },
    "filesystem": {
      "command": "curl", 
      "args": ["-X", "POST", "https://mcp.akerBP.com:3002/mcp"]
    }
  }
}
```

## Option 3: MCP Proxy Tools

Use proxy tools that connect to remote MCP servers:

### Install MCP Proxy (One-time setup)
```bash
npm install -g mcp-proxy
```

### Configuration
```json
{
  "mcpServers": {
    "remote-markitdown": {
      "command": "mcp-proxy",
      "args": [
        "--transport", "sse",
        "--url", "https://remote-mcp-service.com/markitdown/sse",
        "--auth-header", "Bearer YOUR_API_KEY"
      ]
    }
  }
}
```

## Option 4: Browser-Based MCP Services

Use web-based MCP services that don't require local installation:

### Service Examples:
- **MarkItDown Online**: Convert documents via web interface
- **MCP as a Service (MCPaaS)**: Enterprise-hosted MCP endpoints
- **Anthropic's MCP Hub**: Official remote MCP services

### Integration:
```json
{
  "mcpServers": {
    "web-markitdown": {
      "command": "mcp-web-proxy",
      "args": [
        "--service", "markitdown-online",
        "--api-key", "YOUR_API_KEY"
      ]
    }
  }
}
```

## Benefits of Remote MCP Servers

✅ **No Local Installation**: Nothing runs on your computer
✅ **Enterprise Management**: IT controls server versions and updates  
✅ **Shared Resources**: Multiple users share the same server instances
✅ **Scalability**: Servers can handle multiple concurrent users
✅ **Security**: Centralized security and access control
✅ **Maintenance**: IT handles updates, backups, and monitoring

## Security Considerations

- Use HTTPS endpoints only
- Implement proper authentication (API keys, JWT tokens)
- Network access controls (VPN, firewall rules)
- Audit logging for MCP server access
- Data encryption for sensitive document processing

## Enterprise Deployment

For AkerBP, consider:

1. **Kubernetes deployment** of MCP servers
2. **Load balancer** for high availability
3. **API Gateway** for authentication and rate limiting
4. **Monitoring** and logging infrastructure
5. **Backup and disaster recovery** for MCP services

This approach gives you all MCP functionality without local installations!