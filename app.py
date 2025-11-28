"""
MCP Registry API Server
Implements the official MCP v0.1 Registry Specification
See: https://docs.github.com/en/copilot/how-tos/administer-copilot/manage-mcp-usage/configure-mcp-registry
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load server data - using official MCP Server JSON Schema format
# See: https://static.modelcontextprotocol.io/schemas/2025-09-29/server.schema.json
SERVERS_DATA = [
    {
        "name": "io.github/mcp-server",
        "description": "GitHub repository management MCP server",
        "version": "1.0.0",
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
        "name": "io.microsoft/docs-mcp-server",
        "description": "Microsoft documentation and learning resources MCP server",
        "version": "1.0.0",
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

# Create a map for easier lookups by server name
SERVERS_BY_NAME = {server["name"]: server for server in SERVERS_DATA}


def add_cors_headers(response):
    """Add required CORS headers to response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Authorization, Content-Type'
    return response


@app.route('/v0.1/servers', methods=['GET', 'OPTIONS'])
def v01_servers():
    """GET /v0.1/servers - Returns list of all MCP servers (v0.1 spec)"""
    if request.method == 'OPTIONS':
        return add_cors_headers(jsonify({})), 200
    
    # Return all servers
    response = jsonify({"servers": SERVERS_DATA})
    return add_cors_headers(response), 200


@app.route('/v0.1/servers/<server_name>/versions/latest', methods=['GET', 'OPTIONS'])
def v01_server_latest(server_name):
    """GET /v0.1/servers/{serverName}/versions/latest - Returns latest version of specific server"""
    if request.method == 'OPTIONS':
        return add_cors_headers(jsonify({})), 200
    
    # Find server by name
    if server_name not in SERVERS_BY_NAME:
        return add_cors_headers(jsonify({"error": "Server not found"})), 404
    
    server = SERVERS_BY_NAME[server_name]
    response = jsonify(server)
    return add_cors_headers(response), 200


@app.route('/v0.1/servers/<server_name>/versions/<version>', methods=['GET', 'OPTIONS'])
def v01_server_version(server_name, version):
    """GET /v0.1/servers/{serverName}/versions/{version} - Returns specific server version"""
    if request.method == 'OPTIONS':
        return add_cors_headers(jsonify({})), 200
    
    # Find server by name
    if server_name not in SERVERS_BY_NAME:
        return add_cors_headers(jsonify({"error": "Server not found"})), 404
    
    server = SERVERS_BY_NAME[server_name]
    
    # Check if requested version matches
    if server.get("version") != version:
        return add_cors_headers(jsonify({"error": "Version not found"})), 404
    
    response = jsonify(server)
    return add_cors_headers(response), 200


@app.route('/', methods=['GET', 'OPTIONS'])
def index():
    """Root endpoint - returns API info"""
    if request.method == 'OPTIONS':
        return add_cors_headers(jsonify({})), 200
    
    return jsonify({
        "name": "AkerBP MCP Registry",
        "version": "1.0.0",
        "endpoints": {
            "servers": "/v0.1/servers",
            "server-latest": "/v0.1/servers/{serverName}/versions/latest",
            "server-version": "/v0.1/servers/{serverName}/versions/{version}"
        },
        "documentation": "https://github.com/AkerBP/mcp-registry"
    }), 200


@app.route('/servers.json', methods=['GET'])
@app.route('/servers', methods=['GET'])
def servers_json():
    """Return servers in standard JSON format"""
    response = jsonify({"servers": SERVERS_DATA})
    return add_cors_headers(response), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    # Run on all interfaces, port 8000
    app.run(host='0.0.0.0', port=8000, debug=True)
