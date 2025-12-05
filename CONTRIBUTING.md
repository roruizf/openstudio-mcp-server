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

### Documentation

- Update README.md if adding new features
- Add examples to USER_GUIDE.md
- Document technical details in DEVELOPER_NOTES.md
- Include docstrings in code

## Questions?

- **Discussions**: [GitHub Discussions](https://github.com/roruizf/openstudio-mcp-server/discussions)
- **Issues**: [GitHub Issues](https://github.com/roruizf/openstudio-mcp-server/issues)

Thank you for contributing!
