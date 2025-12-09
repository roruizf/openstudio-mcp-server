# Contributing to OpenStudio MCP Server

Thank you for your interest in contributing to the OpenStudio MCP Server!

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in [GitHub Issues](https://github.com/roruizf/openstudio-mcp-server/issues)
2. If not, create a new issue with:
   - Clear description of the problem
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Docker version, OpenStudio version)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/roruizf/openstudio-mcp-server.git
   cd openstudio-mcp-server
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style and patterns
   - Add tests if applicable
   - Update documentation

4. **Test your changes**
   ```bash
   # Build Docker image
   docker build -t openstudio-mcp-dev -f .devcontainer/Dockerfile .

   # Test in Claude Desktop
   # Follow USER_GUIDE.md instructions
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: description of your changes"
   ```

6. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a PR on GitHub.

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Add docstrings to all public functions
- Keep functions focused and single-purpose

### Commit Messages

Use conventional commits format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### Adding New Tools

See [DEVELOPER_NOTES.md](DEVELOPER_NOTES.md) for detailed instructions on:
- Creating new MCP tool wrappers
- Integrating OpenStudio-Toolkit functions
- Error handling patterns
- Testing procedures

**Critical Requirements for New Tools:**

1. **JSON Serialization**
   - ALL tool returns MUST use `ensure_json_response()` wrapper
   - Import: `from openstudio_mcp_server.utils.json_utils import ensure_json_response`
   - Never use `str()` on lists or dicts - always use proper JSON serialization

   ```python
   # CORRECT
   return ensure_json_response(result)

   # WRONG - Can cause JSON parsing errors
   return json.dumps(result)  # Missing edge case handling
   return str(result)          # Creates invalid JSON
   ```

2. **Parameter Matching**
   - Verify exact parameter names when calling wrapped functions
   - Use explicit parameters or `**kwargs` for flexibility
   - Test with actual function signatures before committing

   ```python
   # CORRECT - Explicit matching
   toolkit_function(
       osm_model=model,
       osm_file_path=path  # ← Verify this exact name
   )

   # WRONG - Assumed parameter name
   toolkit_function(
       osm_model=model,
       file_path=path  # ← May not match actual signature
   )
   ```

3. **Error Handling**
   - Catch specific exceptions (ValueError, FileNotFoundError, etc.)
   - Return structured error responses
   - Use `ensure_json_response()` for both success AND error paths

   ```python
   try:
       result = manager.do_operation()
       return ensure_json_response(result)
   except ValueError as e:
       return ensure_json_response({"status": "error", "error": str(e)})
   except Exception as e:
       logger.error(f"Unexpected error: {e}", exc_info=True)
       return ensure_json_response({"status": "error", "error": str(e)})
   ```

### Documentation

- Update README.md if adding new features
- Add examples to USER_GUIDE.md
- Document technical details in DEVELOPER_NOTES.md
- Include docstrings in code

## Questions?

- **Discussions**: [GitHub Discussions](https://github.com/roruizf/openstudio-mcp-server/discussions)
- **Issues**: [GitHub Issues](https://github.com/roruizf/openstudio-mcp-server/issues)

Thank you for contributing!
