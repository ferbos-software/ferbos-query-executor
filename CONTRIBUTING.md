# Contributing to Ferbos Query Executor

Thank you for your interest in contributing! This document outlines the process for contributing code changes.

## Development Workflow

### 1. Create a Branch
- Create a feature branch from `main` or `develop`
- Use descriptive branch names (e.g., `feature/add-new-endpoint`, `fix/query-error-handling`)

### 2. Make Changes
- Write clean, well-documented code
- Follow the existing code style
- Add unit tests for new functionality
- Update documentation as needed

### 3. Run Tests Locally
Before submitting a PR, ensure all tests pass locally:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run linter
ruff check custom_components/ferbos_query_executor/

# Run formatter check
ruff format --check custom_components/ferbos_query_executor/

# Run unit tests
pytest tests/ -v

# Run integration smoke tests
pytest tests/test_integration.py -v -m smoke
```

### 4. Create a Pull Request
- Push your branch to the repository
- Create a Pull Request (PR) with a clear description
- Fill out the PR template completely
- Link any related issues

## Code Review Process

### Requirements
- **2 peer approvals** are required before merging
- **All CI tests must pass** (unit tests, linters, integration smoke tests)
- Repository maintainer approval may be required for significant changes

### Review Checklist
Reviewers will check:
- Code quality and style
- Test coverage
- Documentation completeness
- Security considerations
- Performance implications
- Backward compatibility

### CI Pipeline
The CI pipeline automatically runs:
1. **Lint**: Code quality checks (Ruff)
2. **Unit Tests**: Test suite across Python 3.10, 3.11, 3.12
3. **Integration Tests**: Smoke tests for basic functionality
4. **Manifest Validation**: Ensures manifest.json is valid
5. **HACS Check**: Validates HACS configuration

All checks must pass before merging.

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Maximum line length: 88 characters (enforced by Ruff)
- Use async/await for asynchronous operations
- Add docstrings to public functions and classes

## Testing Guidelines

### Unit Tests
- Test individual functions and methods
- Use mocks for external dependencies
- Aim for high code coverage
- Mark tests with `@pytest.mark.unit`

### Integration Tests
- Test basic integration functionality
- Verify manifest and configuration files
- Mark tests with `@pytest.mark.integration` and `@pytest.mark.smoke`

## Branch Protection

The `main` and `develop` branches are protected with:
- Require pull request reviews before merging
- Require 2 approving reviews
- Require status checks to pass before merging
- Require branches to be up to date before merging

## Getting Help

If you have questions:
- Open an issue for discussion
- Check existing documentation
- Review similar PRs for examples

## Commit Messages

Use clear, descriptive commit messages:
- Start with a verb (Add, Fix, Update, Remove)
- Be specific about what changed
- Reference issue numbers if applicable

Example:
```
Add error handling for database connection failures

- Handle SQLite connection errors gracefully
- Return proper error codes to clients
- Add unit tests for error scenarios

Fixes #123
```

Thank you for contributing! 🎉

