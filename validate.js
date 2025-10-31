const fs = require('fs');

// Load registry
const data = JSON.parse(fs.readFileSync('registry.json', 'utf8'));

console.log('=== MCP Registry Validation ===\n');
let valid = true;

// Check metadata
console.log('Checking metadata...');
const requiredMetadataFields = ['version', 'formatVersion', 'count'];
const metaMissing = requiredMetadataFields.filter(f => !data.metadata[f]);
if (metaMissing.length > 0) {
  console.error('✗ Missing metadata fields:', metaMissing.join(', '));
  valid = false;
} else {
  console.log('✓ Metadata has all required fields');
  console.log('  - version:', data.metadata.version);
  console.log('  - formatVersion:', data.metadata.formatVersion);
  console.log('  - count:', data.metadata.count);
}

// Check servers
console.log('\nChecking servers array...');
if (data.servers && Array.isArray(data.servers)) {
  console.log('✓ Servers array is valid');
  
  if (data.servers.length !== data.metadata.count) {
    console.error(`✗ Server count mismatch: metadata says ${data.metadata.count}, but found ${data.servers.length}`);
    valid = false;
  }
  
  data.servers.forEach((s, i) => {
    console.log(`\nServer ${i + 1}:`);
    const server = s.server;
    
    // Required fields
    const requiredServerFields = ['name', 'description', 'version', 'packages'];
    const missing = requiredServerFields.filter(f => !server[f]);
    if (missing.length > 0) {
      console.error(`  ✗ Missing: ${missing.join(', ')}`);
      valid = false;
    } else {
      console.log(`  ✓ Name: ${server.name}`);
      console.log(`  ✓ Version: ${server.version}`);
    }
    
    // Check packages
    if (server.packages && server.packages.length > 0) {
      const pkg = server.packages[0];
      console.log(`  ✓ Package: ${pkg.identifier} (${pkg.version})`);
      if (!pkg.transport) {
        console.error(`  ✗ Missing transport configuration`);
        valid = false;
      } else {
        console.log(`  ✓ Transport: ${pkg.transport.type}`);
      }
    }
    
    // Check remotes
    if (server.remotes && server.remotes.length > 0) {
      console.log(`  ✓ Remotes: ${server.remotes.length}`);
      server.remotes.forEach(r => console.log(`    - ${r.type}: ${r.url}`));
    } else {
      console.warn(`  ⚠ No remotes defined`);
    }
  });
} else {
  console.error('✗ Servers is not a valid array');
  valid = false;
}

console.log('\n=== Result ===');
if (valid) {
  console.log('✓ Registry is VALID and ready for use');
} else {
  console.log('✗ Registry has ERRORS');
  process.exit(1);
}
