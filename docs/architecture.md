# Architecture

The application separates collection, reasoning, and execution.

1. **Collectors** gather disk, system, network, and Docker state and return dictionaries.
2. **Orchestrator** combines those dictionaries into a timestamped snapshot.
3. **LLM client** serializes the snapshot and sends it to a local Ollama model for advisory analysis.
4. **Command runner** exposes only application-defined action IDs mapped to fixed argument arrays.

This separation keeps individual checks testable and prevents model-generated strings from becoming shell commands.
