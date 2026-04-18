# Mermaid — Links

## GitHub Repository
- **Repo:** https://github.com/mermaid-js/mermaid
- **Cloned to:** `github/mermaid/`
- **NPM:** https://www.npmjs.com/package/mermaid
- **CDN (latest):** https://cdn.jsdelivr.net/npm/mermaid@11

## Documentation
- **Docs home:** https://mermaid.js.org/
- **About Mermaid:** https://mermaid.ai/open-source/intro/
- **Getting Started:** https://mermaid.ai/open-source/intro/getting-started.html
- **Syntax Reference:** https://mermaid.ai/open-source/intro/syntax-reference.html
- **Live Editor:** https://mermaid.ai/live/edit
- **Configuration:** https://mermaid.ai/open-source/config/configuration.html
- **API Usage:** https://mermaid.ai/open-source/config/usage.html
- **Theming:** https://mermaid.ai/open-source/config/theming.html
- **Tutorials:** https://mermaid.ai/open-source/ecosystem/tutorials.html
- **Community Integrations:** https://mermaid.ai/open-source/ecosystem/integrations-community.html
- **Contributing:** https://mermaid.ai/open-source/community/contributing.html
- **Announcements / Blog:** https://mermaid.ai/open-source/news/announcements.html
- **Discord:** https://discord.gg/sKeNQX4Wtj

## What It Is
Mermaid is a JavaScript diagramming and charting library that renders
Markdown-inspired text definitions into SVG/PNG diagrams. Used natively in
GitHub, GitLab, Notion, Obsidian, Azure DevOps, and many more.

## Diagram Types
| Diagram | Syntax Doc |
|---------|-----------|
| Flowchart | https://mermaid.ai/open-source/syntax/flowchart.html |
| Sequence Diagram | https://mermaid.ai/open-source/syntax/sequenceDiagram.html |
| Class Diagram | https://mermaid.ai/open-source/syntax/classDiagram.html |
| State Diagram | https://mermaid.ai/open-source/syntax/stateDiagram.html |
| Entity Relationship | https://mermaid.ai/open-source/syntax/entityRelationshipDiagram.html |
| Gantt | https://mermaid.ai/open-source/syntax/gantt.html |
| Git Graph | https://mermaid.ai/open-source/syntax/gitgraph.html |
| Mindmap | https://mermaid.ai/open-source/syntax/mindmap.html |
| Timeline | https://mermaid.ai/open-source/syntax/timeline.html |
| Kanban | https://mermaid.ai/open-source/syntax/kanban.html |
| Architecture | https://mermaid.ai/open-source/syntax/architecture.html |
| XY Chart | https://mermaid.ai/open-source/syntax/xyChart.html |
| Quadrant Chart | https://mermaid.ai/open-source/syntax/quadrantChart.html |
| Sankey | https://mermaid.ai/open-source/syntax/sankey.html |
| User Journey | https://mermaid.ai/open-source/syntax/userJourney.html |
| Pie Chart | https://mermaid.ai/open-source/syntax/pie.html |
| Block Diagram | https://mermaid.ai/open-source/syntax/block.html |
| C4 Diagram | https://mermaid.ai/open-source/syntax/c4.html |

## Installation
```bash
npm install mermaid          # npm
yarn add mermaid             # yarn
pnpm add mermaid             # pnpm
```

## Quick Embed (HTML)
```html
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  mermaid.initialize({ startOnLoad: true });
</script>
<div class="mermaid">
  graph TD; A-->B; B-->C;
</div>
```

## Sibling Projects
- **Mermaid CLI:** https://github.com/mermaid-js/mermaid-cli
- **Mermaid Live Editor:** https://github.com/mermaid-js/mermaid-live-editor
- **Mermaid Chart (SaaS):** https://mermaid.ai/

## Submodules
- **[mermaid_mcp/](mermaid_mcp/LINKS.md)** — MCP server for AI-driven diagram generation
