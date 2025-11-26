"""
MCP Registry API Server
A simple Flask server to serve MCP registry with proper API endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load server data
SERVERS_DATA = [
    {
        "name": "github",
        "displayName": "GitHub MCP Server",
        "description": "GitHub repository management MCP server",
        "version": "1.0.0",
        "categories": ["Tools"],
        "tags": ["github", "repository", "git"],
        "publisher": {
            "name": "GitHub",
            "url": "https://github.com"
        },
        "repository": {
            "type": "git",
            "url": "https://github.com/github/mcp-server"
        },
        "homepage": "https://github.com/github/mcp-server",
        "license": "MIT",
        "icon": "https://github.com/favicon.ico",
        "remote": {
            "type": "http",
            "url": "https://api.githubcopilot.com/mcp/"
        }
    },
    {
        "name": "microsoft.docs.mcp",
        "displayName": "Microsoft Docs MCP Server",
        "description": "Microsoft documentation and learning resources MCP server",
        "version": "1.0.0",
        "categories": ["Documentation"],
        "tags": ["microsoft", "docs", "documentation", "learning"],
        "publisher": {
            "name": "Microsoft",
            "url": "https://microsoft.com"
        },
        "repository": {
            "type": "git",
            "url": "https://github.com/microsoft/docs-mcp-server"
        },
        "homepage": "https://learn.microsoft.com",
        "license": "MIT",
        "icon": "https://microsoft.com/favicon.ico",
        "remote": {
            "type": "http",
            "url": "https://learn.microsoft.com/api/mcp"
        }
    }
]


@app.route('/v0.1/servers', methods=['GET', 'OPTIONS'])
def v01_servers():
    """Handle v0.1 servers endpoint"""
    if request.method == 'OPTIONS':
        return '', 200
    
    # Get query parameters
    limit = request.args.get('limit', default=50, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    # Apply pagination
    paginated_servers = SERVERS_DATA[offset:offset + limit]
    
    return jsonify({
        "data": paginated_servers,
        "total": len(SERVERS_DATA)
    })


@app.route('/v0/servers', methods=['GET', 'OPTIONS'])
def v0_servers():
    """Handle v0 servers endpoint (fallback)"""
    if request.method == 'OPTIONS':
        return '', 200
    
    # Get query parameters
    limit = request.args.get('limit', default=50, type=int)
    offset = request.args.get('offset', default=0, type=int)
    
    # Apply pagination
    paginated_servers = SERVERS_DATA[offset:offset + limit]
    
    return jsonify({
        "data": paginated_servers,
        "total": len(SERVERS_DATA)
    })


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
    return jsonify({"status": "healthy"})


if __name__ == '__main__':
    # Run on all interfaces, port 8000
    app.run(host='0.0.0.0', port=8000, debug=True)
