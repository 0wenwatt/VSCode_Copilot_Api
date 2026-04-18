# Playwright — Model Context Protocol & Browser Automation

A modern browser automation framework with integrated MCP support for AI agents.

## Quick Links

- **GitHub:** https://github.com/microsoft/playwright-mcp
- **NPM:** https://www.npmjs.com/package/@playwright/mcp
- **Documentation:** https://playwright.dev/docs/getting-started-mcp
- **LINKS.md:** See [LINKS.md](LINKS.md) for comprehensive documentation links

## What's Here

- `github/` — Full Playwright MCP repository clone
- `LINKS.md` — Complete documentation index with resources

## Quick Start

Install Playwright MCP:
```bash
npx @playwright/mcp@latest
```

Or configure in VS Code for MCP:
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

## Key Features

✓ **LLM-optimized** — Uses accessibility trees, not screenshots  
✓ **Deterministic** — Structured data for consistent AI reasoning  
✓ **Fast** — No vision models or pixel-based input needed  
✓ **Multi-browser** — Chromium, Firefox, WebKit support  
✓ **MCP native** — Works with VS Code, Cursor, Claude Desktop, etc.  

## Use Cases

- **AI Agents** — Provide browser control to Claude, Copilot, or custom agents
- **Testing** — Full-featured test runner with auto-waiting and assertions
- **Scripting** — Reliable web automation with modern tooling
- **Exploration** — Self-healing tests with persistent browser context

## Capabilities

- Core automation (always available)
- Tab management
- Browser installation
- Configuration (opt-in)
- Network tools (opt-in)
- Storage/cookies (opt-in)
- DevTools (opt-in)
- Vision/coordinate-based (opt-in)
- PDF generation (opt-in)
- Test assertions (opt-in)

## Browser Support

| Browser | Platform | Status |
|---------|----------|--------|
| Chromium | Linux, macOS, Windows | ✓ |
| Firefox | Linux, macOS, Windows | ✓ |
| WebKit | Linux, macOS, Windows | ✓ |
| Chrome channels | All platforms | ✓ |

## Node.js Requirement

Node.js 18 or newer

## See Also

- **Model Context Protocol:** https://modelcontextprotocol.io/
- **Playwright Test:** https://playwright.dev/docs/intro
- **Playwright CLI:** https://playwright.dev/docs/getting-started-cli
- Related modules in `Modules/AI/agents/`
