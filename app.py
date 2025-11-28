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
        "shortDescription": "GitHub repository management",
        "description": "GitHub repository management MCP server providing access to repositories, issues, and pull requests",
        "version": "1.0.0",
        "publisher": {
            "publisherId": "github",
            "publisherName": "GitHub",
            "displayName": "GitHub",
            "domain": "github.com"
        },
        "versions": [
            {
                "version": "1.0.0",
                "lastUpdated": "2024-11-28T00:00:00Z"
            }
        ],
        "categories": ["Tools"],
        "tags": ["github", "repository", "git"],
        "statistics": [
            {"statisticName": "install", "value": 0}
        ],
        "releaseDate": "2024-11-28T00:00:00Z"
    },
    {
        "name": "microsoft-docs-mcp",
        "displayName": "Microsoft Docs MCP Server",
        "shortDescription": "Microsoft documentation",
        "description": "Microsoft documentation and learning resources MCP server providing access to technical documentation",
        "version": "1.0.0",
        "publisher": {
            "publisherId": "microsoft",
            "publisherName": "Microsoft",
            "displayName": "Microsoft Corporation",
            "domain": "microsoft.com"
        },
        "versions": [
            {
                "version": "1.0.0",
                "lastUpdated": "2024-11-28T00:00:00Z"
            }
        ],
        "categories": ["Documentation"],
        "tags": ["microsoft", "docs", "documentation", "learning"],
        "statistics": [
            {"statisticName": "install", "value": 0}
        ],
        "releaseDate": "2024-11-28T00:00:00Z"
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
    
    # Match VS Code Extension Gallery API format
    response = {
        "results": [
            {
                "extensions": paginated_servers,
                "pagingToken": None,
                "resultMetadata": [
                    {
                        "metadataType": "ResultCount",
                        "metadataItems": [
                            {"name": "TotalCount", "count": total}
                        ]
                    }
                ]
            }
        ]
    }
    
    return jsonify(response), 200, {
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
    
    # Match VS Code Extension Gallery API format
    response = {
        "results": [
            {
                "extensions": paginated_servers,
                "pagingToken": None,
                "resultMetadata": [
                    {
                        "metadataType": "ResultCount",
                        "metadataItems": [
                            {"name": "TotalCount", "count": total}
                        ]
                    }
                ]
            }
        ]
    }
    
    return jsonify(response), 200, {
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
