# AkerBP MCP Registry

Allowlist of MCP servers authorized for use within the AkerBP organization.

##  Overview

This registry contains the **official whitelist of approved Model Context Protocol (MCP) servers** that AkerBP employees are authorized to use. Only servers listed in this registry are permitted for use with Claude Desktop, VS Code, and other MCP-compatible tools.

## Authorized MCP Servers

| Server | Purpose | Status |
|--------|---------|--------|
| `@modelcontextprotocol/server-github` | GitHub repository management and issue tracking |  Active |
| `@modelcontextprotocol/server-filesystem` | File system access to AkerBP shared directories |  Active |
| `markitdown-mcp-npx` | Document conversion to Markdown format |  Active |

##  How to Use Whitelisted MCP Servers

### **Step 1: Verify the Server is Whitelisted**

Check if your desired MCP server is listed in the [Authorized MCP Servers](#-authorized-mcp-servers) table above.

- **Is it listed?** → Proceed to Step 2
-  **Not listed?** → Request approval (see [Requesting New Servers](#-requesting-new-servers))

### **Step 2: Install Node.js (If Not Already Installed)**

MCP servers run on Node.js. Verify you have it installed:

```powershell
# Check Node.js version
node --version
npm --version
```

If not installed, download from [nodejs.org](https://nodejs.org)

### **Step 3: Configure Your MCP Client**



2. Add the whitelisted servers to the `mcpServers` section:

#### ** VS Code with Copilot**

1. Install the GitHub Copilot extension
2. Add MCP configuration to your workspace settings (`.vscode/settings.json`):

```json
{
  "github.copilot.advanced": {
    "mcp_servers": [
      "@modelcontextprotocol/server-github",
      "@modelcontextprotocol/server-filesystem",
      "markitdown-mcp-npx"
    ]
  }
}
```

3. Reload VS Code

### **Step 4: Authenticate (If Required)**

Some servers require authentication:

#### **GitHub Server**
```powershell
# Create a GitHub Personal Access Token
# https://github.com/settings/tokens

# Set environment variable
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "ghp_your_token_here"
```

#### **Filesystem Server**
```powershell
# No authentication needed
# Access is based on your system file permissions
```

### **Step 5: Test the MCP Server**

Verify the server is working:

```powershell
# Test GitHub server
npx @modelcontextprotocol/server-github --help

# Test Filesystem server
npx @modelcontextprotocol/server-filesystem /akerbp/shared

# Test Markitdown server
npx markitdown-mcp-npx --help
```

Expected output: GitHub MCP Server running on stdio

### **Step 6: Start Using the Server**

Once configured, you can use the whitelisted servers in your MCP client:


### **Submission Process**

1. **Create a request** in the AkerBP GitHub organization:
   - Repository: `AkerBP/mcp-registry`
   - Issue title: `[REQUEST] Add {server-name} to whitelist`
   - Include server GitHub/npm link and business justification

2. **IT Security review** (3-5 business days):
   - Evaluate security implications
   - Check compliance requirements
   - Verify maintenance status

3. **Approval or Rejection**:
   -  **Approved**: Added to registry, communicated to team
   -  **Rejected**: Feedback provided with reasons

4. **Implementation**:
   - Server added to `registry.json`
   - Documentation updated
   - Version controlled in GitHub

### **Request Template**

```markdown
**Server Name**: @organization/server-name
**npm/GitHub Link**: https://github.com/.../
**Version**: 1.0.0

**Business Justification**: 
Brief explanation of why this server is needed

**Security Considerations**:
- Does it require external API access?
- Does it handle sensitive data?
- Any compliance concerns?

**Expected Usage**:
How will this server be used within AkerBP?
```

**Last Updated**: 2025-10-31  

