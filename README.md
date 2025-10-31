# AkerBP MCP Registry

Allowlist of MCP servers authorized for use within the AkerBP organization.

## 📋 Overview

This registry contains the **official whitelist of approved Model Context Protocol (MCP) servers** that AkerBP employees are authorized to use. Only servers listed in this registry are permitted for use with Claude Desktop, VS Code, and other MCP-compatible tools.

## ✅ Authorized MCP Servers

| Server | Purpose | Status |
|--------|---------|--------|
| `@modelcontextprotocol/server-github` | GitHub repository management and issue tracking | ✅ Active |
| `@modelcontextprotocol/server-filesystem` | File system access to AkerBP shared directories | ✅ Active |
| `markitdown-mcp-npx` | Document conversion to Markdown format | ✅ Active |

## 🚀 How to Use Whitelisted MCP Servers

### **Step 1: Verify the Server is Whitelisted**

Check if your desired MCP server is listed in the [Authorized MCP Servers](#-authorized-mcp-servers) table above.

- ✅ **Is it listed?** → Proceed to Step 2
- ❌ **Not listed?** → Request approval (see [Requesting New Servers](#-requesting-new-servers))

### **Step 2: Install Node.js (If Not Already Installed)**

MCP servers run on Node.js. Verify you have it installed:

```powershell
# Check Node.js version
node --version
npm --version
```

If not installed, download from [nodejs.org](https://nodejs.org)

### **Step 3: Configure Your MCP Client**

#### **Option A: Claude Desktop (Recommended)**

1. Open Claude Desktop configuration file:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. Add the whitelisted servers to the `mcpServers` section:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_TOKEN_HERE"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/akerbp/shared"]
    },
    "markitdown": {
      "command": "npx",
      "args": ["markitdown-mcp-npx"]
    }
  }
}
```

3. Restart Claude Desktop
4. The whitelisted servers are now available

#### **Option B: VS Code with Copilot**

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

Expected output: Command help text or initialization messages

### **Step 6: Start Using the Server**

Once configured, you can use the whitelisted servers in your MCP client:

**Example with Claude Desktop:**
> "Can you list the open issues in the AkerBP/github-management repository?"

Claude will automatically use the authorized `@modelcontextprotocol/server-github` to fetch the data.

## ❓ Troubleshooting

### **Server Not Found Error**

```
Error: npx: command not found
```

**Solution**: Install Node.js from [nodejs.org](https://nodejs.org)

### **Authentication Failed**

```
Error: Invalid GitHub token
```

**Solution**: 
1. Verify your GitHub Personal Access Token is correct
2. Check token has appropriate scopes
3. Ensure environment variable is set correctly

### **Permission Denied (Filesystem)**

```
Error: Access denied to /path/to/directory
```

**Solution**: 
1. Verify you have read/write permissions on the directory
2. Check path is under approved `/akerbp/shared` directories

### **Server Won't Start**

```
Error: Server initialization failed
```

**Solution**:
1. Check Node.js version compatibility
2. Try reinstalling: `npm install -g @modelcontextprotocol/server-github`
3. Contact IT Support (see below)

## 📝 Requesting New Servers

Want to use an MCP server not on the whitelist?

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
   - ✅ **Approved**: Added to registry, communicated to team
   - ❌ **Rejected**: Feedback provided with reasons

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

## 🔐 Security & Compliance

### **Whitelist Requirements**

All servers in this registry meet these criteria:

✅ **Open Source** - Code is publicly available and audited
✅ **Actively Maintained** - Regular security updates
✅ **Security Vetted** - No known vulnerabilities
✅ **Compliance Aligned** - Meets AkerBP data protection policies
✅ **Performance Verified** - Acceptable latency and resource usage

### **Unauthorized Server Usage**

Using MCP servers NOT on this whitelist is prohibited:

❌ Security risk - Not vetted by IT
❌ Compliance violation - May violate data protection policies
❌ Support unavailable - IT cannot assist with unauthorized servers

**Violations may result in disciplinary action.**

## 📞 Support

### **Need Help?**

- **Configuration Issues**: Create an issue in this repository
- **IT Support**: Contact `it-support@akerbp.com`
- **Security Concerns**: Email `security@akerbp.com`
- **Slack**: `#mcp-servers` channel

## 📚 Resources

- **MCP Documentation**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Official MCP Servers**: [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- **Claude Desktop Setup**: [claude.ai/docs](https://claude.ai/docs)
- **GitHub PAT Guide**: [github.com/settings/tokens](https://github.com/settings/tokens)

## 📋 Changelog

### Version 1.0.0 (2025-10-31)
- Initial registry setup
- Added GitHub, Filesystem, and Markitdown servers
- Documented usage and request process

---

**Last Updated**: 2025-10-31  
**Maintained By**: AkerBP IT Security Team  
**Questions?** Create an issue in this repository
