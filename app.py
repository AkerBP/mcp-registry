"""
MCP Registry API Server
A simple Flask server to serve MCP registry with proper API endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load server data - using official MCP Server JSON Schema format
# See: https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json
SERVERS_DATA = [
    {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json",
        "name": "io.github/mcp-server",
        "description": "GitHub repository management MCP server providing access to repositories, issues, and pull requests",
        "version": "1.0.0",
        "websiteUrl": "https://github.com/modelcontextprotocol/servers",
        "repository": {
            "url": "https://github.com/modelcontextprotocol/servers",
            "source": "github",
            "id": "github-repo-id-123"
        },
        "packages": [
            {
                "registryType": "npm",
                "registryBaseUrl": "https://registry.npmjs.org",
                "identifier": "@modelcontextprotocol/server-github",
                "version": "1.0.0",
                "transport": {
                    "type": "stdio"
                }
            }
        ]
    },
    {
        "$schema": "https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json",
        "name": "io.microsoft/docs-mcp-server",
        "description": "Microsoft documentation and learning resources MCP server providing access to technical documentation",
        "version": "1.0.0",
        "websiteUrl": "https://learn.microsoft.com",
        "repository": {
            "url": "https://github.com/microsoft/docs-mcp",
            "source": "github",
            "id": "microsoft-docs-repo-id-456"
        },
        "packages": [
            {
                "registryType": "npm",
                "registryBaseUrl": "https://registry.npmjs.org",
                "identifier": "@microsoft/mcp-server-docs",
                "version": "1.0.0",
                "transport": {
                    "type": "stdio"
                }
            }
        ]
    }
]


@app.route('/v0.1/servers', methods=['GET', 'OPTIONS'])
@app.route('/v0.1/servers/', methods=['GET', 'OPTIONS'])
def v01_servers():
    """Handle v0.1 servers endpoint"""
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response, 200
    
    # Get query parameters
    limit = request.args.get('limit', default=50, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    # Apply pagination
    total = len(SERVERS_DATA)
    paginated_servers = SERVERS_DATA[offset:offset + limit]
    
    # Return array of servers matching MCP Server JSON Schema
    return jsonify(paginated_servers), 200, {
        'Content-Type': 'application/json; charset=utf-8'
    }


@app.route('/v0/servers', methods=['GET', 'OPTIONS'])
@app.route('/v0/servers/', methods=['GET', 'OPTIONS'])
def v0_servers():
    """Handle v0 servers endpoint (fallback)"""
    if request.method == 'OPTIONS':
        response = jsonify({})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response, 200
    
    # Get query parameters
    limit = request.args.get('limit', default=50, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    # Apply pagination
    total = len(SERVERS_DATA)
    paginated_servers = SERVERS_DATA[offset:offset + limit]
    
    # Return array of servers matching MCP Server JSON Schema
    return jsonify(paginated_servers), 200, {
        'Content-Type': 'application/json; charset=utf-8'
    }


@app.route('/', methods=['GET'])
def index():
    """Root endpoint with API information"""
    return jsonify({
        "name": "AkerBP MCP Registry",
        "version": "1.0.0",
        "endpoints": {
            "v0.1": "/v0.1/servers",
            "v0": "/v0/servers"
        },
        "documentation": "https://github.com/AkerBP/mcp-registry"
    })


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    # Run on all interfaces, port 8000
    app.run(host='0.0.0.0', port=8000, debug=True)
