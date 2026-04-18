# Tree-sitter — Links

## GitHub Repository
- **Repo:** https://github.com/tree-sitter/tree-sitter
- **Cloned to:** `github/tree-sitter/`
- **Organization:** https://github.com/tree-sitter
- **Releases:** https://github.com/tree-sitter/tree-sitter/releases (latest: v0.26.8)
- **Issues:** https://github.com/tree-sitter/tree-sitter/issues
- **Discussions:** https://github.com/tree-sitter/tree-sitter/discussions
- **Wiki (parser list):** https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers
- **Contributing:** https://github.com/tree-sitter/tree-sitter/blob/master/CONTRIBUTING.md

## Documentation
- **Docs home:** https://tree-sitter.github.io/tree-sitter/
- **Introduction:** https://tree-sitter.github.io/tree-sitter/index.html
- **Using Parsers:** https://tree-sitter.github.io/tree-sitter/using-parsers/index.html
- **Using Parsers — Getting Started:** https://tree-sitter.github.io/tree-sitter/using-parsers/1-getting-started.html
- **Creating Parsers:** https://tree-sitter.github.io/tree-sitter/creating-parsers/index.html
- **Creating Parsers — Getting Started:** https://tree-sitter.github.io/tree-sitter/creating-parsers/1-getting-started.html
- **Syntax Highlighting:** https://tree-sitter.github.io/tree-sitter/syntax-highlighting.html
- **Code Navigation:** https://tree-sitter.github.io/tree-sitter/code-navigation-systems.html
- **Playground:** https://tree-sitter.github.io/tree-sitter/playground.html
- **Printable book:** https://tree-sitter.github.io/tree-sitter/print.html

## C API
- **Header file:** https://github.com/tree-sitter/tree-sitter/blob/master/lib/include/tree_sitter/api.h

## What It Is
Tree-sitter is a parser generator tool and incremental parsing library written in C11.
It builds concrete syntax trees (CSTs) for source files and efficiently updates them
on every keystroke. Key properties:
- **General** — can parse any programming language
- **Fast** — keystroke-latency even in large files
- **Robust** — useful results even with syntax errors
- **Dependency-free** — pure C11 runtime embeddable in any application

## Language Bindings (Official)
| Language | Docs / Repo |
|----------|------------|
| Python | https://tree-sitter.github.io/py-tree-sitter · https://github.com/tree-sitter/py-tree-sitter |
| Rust | https://docs.rs/tree-sitter · (in main repo) |
| JavaScript (Node.js) | https://tree-sitter.github.io/node-tree-sitter · https://github.com/tree-sitter/node-tree-sitter |
| JavaScript (Wasm) | https://github.com/tree-sitter/tree-sitter/tree/master/lib/binding_web |
| Go | https://pkg.go.dev/github.com/tree-sitter/go-tree-sitter · https://github.com/tree-sitter/go-tree-sitter |
| Java (JDK 22+) | https://tree-sitter.github.io/java-tree-sitter · https://github.com/tree-sitter/java-tree-sitter |
| Kotlin | https://tree-sitter.github.io/kotlin-tree-sitter · https://github.com/tree-sitter/kotlin-tree-sitter |
| C# | https://github.com/tree-sitter/csharp-tree-sitter |
| Haskell | https://github.com/tree-sitter/haskell-tree-sitter |
| Swift | https://github.com/tree-sitter/swift-tree-sitter |
| Zig | https://tree-sitter.github.io/zig-tree-sitter · https://github.com/tree-sitter/zig-tree-sitter |

## Official Parsers (upstream org)
| Language | Repo |
|----------|------|
| Python | https://github.com/tree-sitter/tree-sitter-python |
| JavaScript | https://github.com/tree-sitter/tree-sitter-javascript |
| TypeScript | https://github.com/tree-sitter/tree-sitter-typescript |
| Rust | https://github.com/tree-sitter/tree-sitter-rust |
| C | https://github.com/tree-sitter/tree-sitter-c |
| C++ | https://github.com/tree-sitter/tree-sitter-cpp |
| C# | https://github.com/tree-sitter/tree-sitter-c-sharp |
| Go | https://github.com/tree-sitter/tree-sitter-go |
| Java | https://github.com/tree-sitter/tree-sitter-java |
| Ruby | https://github.com/tree-sitter/tree-sitter-ruby |
| JSON | https://github.com/tree-sitter/tree-sitter-json |
| HTML | https://github.com/tree-sitter/tree-sitter-html |
| CSS | https://github.com/tree-sitter/tree-sitter-css |
| Bash | https://github.com/tree-sitter/tree-sitter-bash |
| Scala | https://github.com/tree-sitter/tree-sitter-scala |
| OCaml | https://github.com/tree-sitter/tree-sitter-ocaml |
| PHP | https://github.com/tree-sitter/tree-sitter-php |
| Julia | https://github.com/tree-sitter/tree-sitter-julia |
| Haskell | https://github.com/tree-sitter/tree-sitter-haskell |
| Full list | https://github.com/tree-sitter/tree-sitter/wiki/List-of-parsers |

## Python Binding Quick Start
```bash
pip install tree-sitter
pip install tree-sitter-python   # grammar package
```
```python
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

PY_LANGUAGE = Language(tspython.language())
parser = Parser(PY_LANGUAGE)

tree = parser.parse(b"def foo(): pass")
print(tree.root_node.sexp())
```

## CLI (tree-sitter command)
```bash
# Install
cargo install tree-sitter-cli
npm install -g tree-sitter-cli

# Commands
tree-sitter generate        # generate parser from grammar.js
tree-sitter test            # run parser tests
tree-sitter parse <file>    # parse a file, print syntax tree
tree-sitter highlight <file> # syntax highlight a file
tree-sitter playground      # open interactive web playground
tree-sitter query <query> <file>  # run a query against a file
```
- **CLI Readme:** https://github.com/tree-sitter/tree-sitter/blob/master/crates/cli/README.md

## Community
- **Discord:** https://discord.gg/w7nTvsVJhm
- **Matrix:** https://matrix.to/#/#tree-sitter-chat:matrix.org
- **Open Collective:** https://opencollective.com/tree-sitter

## Talks
- **Strange Loop 2018:** https://www.thestrangeloop.com/2018/tree-sitter---a-new-parsing-system-for-programming-tools.html
- **FOSDEM 2018:** https://www.youtube.com/watch?v=0CGzC_iss-8
- **GitHub Universe 2017:** https://www.youtube.com/watch?v=a1rC79DHpmY
