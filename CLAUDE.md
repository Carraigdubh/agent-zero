# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Agent Zero is a personal, organic agentic framework built in Python that uses the computer as a tool to accomplish tasks. It features a modular architecture with Docker containerization, multi-agent cooperation, and persistent memory capabilities.

## Key Development Commands

### Running the Application
- **Web UI**: `python run_ui.py` - Starts the Flask server with web interface at port 50001
- **CLI (Deprecated)**: `python run_cli.py` - Legacy CLI interface (discontinued, use run_ui.py instead)
- **Docker**: `docker pull agent0ai/agent-zero && docker run -p 50001:80 agent0ai/agent-zero`

### Setup and Dependencies
- **Install dependencies**: `pip install -r requirements.txt`
- **Environment setup**: Copy `example.env` to `.env` and configure API keys
- **Initialize**: `python initialize.py` - Sets up initial configurations

### Testing and Development
- No specific test commands are defined in this codebase
- Check the Docker containers in `/docker/` for runtime environment setup
- Use `/logs/` directory for session logs and debugging

## Architecture Overview

### Core Components
1. **Agent System** (`agent.py`):
   - `AgentContext` - Main context manager for agent instances
   - Multi-agent hierarchy with superior/subordinate relationships
   - Persistent memory and knowledge management

2. **Tools** (`python/tools/`):
   - `code_execution_tool.py` - Executes code in isolated environment
   - `browser_agent.py` - Web browsing capabilities
   - `memory_*.py` - Memory management (save, load, delete, forget)
   - `search_engine.py` - Web search functionality
   - `document_query.py` - Document analysis and querying

3. **Web Interface** (`webui/`):
   - Flask-based web UI with real-time streaming
   - Components-based frontend architecture
   - Settings management, file browser, chat history

4. **API Layer** (`python/api/`):
   - RESTful endpoints for all major operations
   - Authentication and CSRF protection
   - MCP (Model Context Protocol) server integration

### Key Directories
- `/prompts/` - System prompts that define agent behavior (highly customizable)
- `/memory/` - Persistent agent memory storage
- `/knowledge/` - Knowledge base for document storage and retrieval
- `/instruments/` - Custom tools and scripts
- `/python/helpers/` - Utility modules for core functionality
- `/python/extensions/` - Extensibility framework for custom behaviors

## Development Patterns

### Agent Behavior Customization
- Primary system prompt: `prompts/default/agent.system.main.md`
- Tool-specific prompts in `prompts/default/agent.system.tool.*.md`
- Framework messages in `prompts/default/fw.*.md`

### Tool Development
- Tools inherit from base classes in `python/helpers/tool.py`
- Each tool has corresponding prompt files for LLM instructions
- Tools are automatically loaded from `python/tools/` directory

### Extension System
- Extensions hook into message loop stages in `python/extensions/`
- Organized by lifecycle events (start, prompts_before, prompts_after, end)
- Enables custom behaviors without modifying core code

### MCP Integration
- Supports both MCP client and server functionality
- MCP servers defined in settings for external tool integration
- Streamable HTTP MCP server support

## Important Configuration Files

- `.env` - Environment variables (API keys, settings)
- `models.py` - LLM model configurations
- `jsconfig.json` - JavaScript/TypeScript configuration for frontend
- `requirements.txt` - Python dependencies

## Security Considerations

- Runs in Docker container for isolation
- Basic authentication and CSRF protection
- API key requirements for external access
- Loopback address restrictions for sensitive endpoints

## Development Notes

- Framework is designed to be completely transparent and customizable
- No hard-coded limitations - everything can be modified via prompts
- Agent behavior is defined by prompts, not code constraints
- Real-time streaming interface allows intervention during agent execution
- Multi-agent cooperation enables complex task delegation and management

## Identity/Branding Changes

When changing agent identity (e.g., from "Agent Zero" to "Father Ted"):

1. **Update all prompt files** in `/prompts/default/` containing identity references
2. **Update UI elements** in headings and extensions (search for "A0" and "Agent Zero")
3. **Clear conversation history** in `/tmp/chats/` - old conversations contain previous identity responses that get sent as context to external LLMs
4. **Clear agent memory** in `/memory/default/` to remove cached identity references
5. **Restart server** to apply all changes with fresh context

**Critical**: External LLMs (Google, OpenAI, etc.) have no inherent knowledge of "Agent Zero" - if they respond with that identity, it's because the conversation history contains previous responses with that identity being sent as context.

### Docker/Production Deployment Identity Issues

**Key Learning**: When deploying identity changes to Docker/production environments:

- **Code changes deploy correctly** - Docker builds pull the right repository and include all prompt/personality changes
- **Persistent data is the problem** - Conversation history (`/tmp/chats/`) and agent memory (`/memory/default/`) persist between deployments
- **Symptoms**: New code is running but agent still uses old identity because old conversations are loaded as context
- **Solution**: Clear persistent storage in production:
  ```bash
  rm -rf /tmp/chats/*
  rm -rf /memory/default/*
  ```
- **Prevention**: Always clear these directories when making identity changes, both locally and in production
- **Docker volumes**: If using persistent volumes, they may need to be deleted and recreated for identity changes