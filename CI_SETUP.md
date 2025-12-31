# CI/CD Setup Documentation

This document describes the CI/CD pipeline setup for the Ferbos Query Executor integration.

## Overview

The CI pipeline ensures code quality through:
- **Linting**: Code style and quality checks
- **Unit Tests**: Comprehensive test coverage
- **Integration Tests**: Smoke tests for basic functionality
- **Validation**: Manifest and HACS configuration checks

## Requirements

### Entry Criteria
- PR raised in Git repository
- All code changes committed to feature branch

### Exit Criteria
- ✅ **2 peer approvals** required
- ✅ **All CI tests pass**:
  - Lint checks
  - Unit tests (Python 3.10, 3.11, 3.12)
  - Integration smoke tests
  - Manifest validation
  - HACS configuration check

### Artifacts
- PR approvals (tracked in GitHub)
- CI logs (available in GitHub Actions)
- Coverage reports (Codecov, if configured)

## CI Pipeline Jobs

### 1. Lint Code (`lint`)
- **Purpose**: Check code style and quality
- **Tools**: Ruff linter and formatter
- **Runs on**: Ubuntu Latest
- **Python**: 3.11
- **Checks**:
  - Code style violations
  - Import organization
  - Code complexity
  - Formatting consistency

### 2. Unit Tests (`unit-tests`)
- **Purpose**: Test individual components
- **Framework**: pytest with pytest-cov
- **Runs on**: Ubuntu Latest
- **Python Versions**: 3.10, 3.11, 3.12
- **Coverage**: Code coverage reporting enabled
- **Location**: `tests/test_*.py` (excluding `test_integration.py`)

### 3. Integration Smoke Tests (`integration-tests`)
- **Purpose**: Basic integration functionality verification
- **Framework**: pytest with smoke markers
- **Runs on**: Ubuntu Latest
- **Python**: 3.11
- **Tests**:
  - Manifest validation
  - HACS configuration
  - Module imports
  - Basic setup functions

### 4. Validate Manifest (`validate-manifest`)
- **Purpose**: Ensure manifest.json is valid
- **Checks**:
  - JSON validity
  - Required fields present
  - Codeowners format

### 5. Check HACS (`check-hacs`)
- **Purpose**: Validate HACS configuration
- **Checks**:
  - JSON validity
  - Required fields
  - Domain configuration

## Running Tests Locally

### Prerequisites
```bash
pip install -r requirements-dev.txt
```

### Run Linter
```bash
ruff check custom_components/ferbos_query_executor/
ruff format --check custom_components/ferbos_query_executor/
```

### Run Unit Tests
```bash
pytest tests/ -v --cov=custom_components/ferbos_query_executor
```

### Run Integration Tests
```bash
pytest tests/test_integration.py -v -m smoke
```

### Run All Tests
```bash
pytest tests/ -v
```

## Branch Protection

Configure branch protection rules in GitHub:
1. Go to **Settings** → **Branches**
2. Add rule for `main` and `develop`
3. Configure:
   - Require 2 pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

See `.github/BRANCH_PROTECTION.md` for detailed configuration.

## Troubleshooting

### CI Fails on Lint
- Run `ruff check` locally to see errors
- Run `ruff format` to auto-fix formatting issues
- Check `ruff.toml` for configuration

### CI Fails on Tests
- Run `pytest tests/ -v` locally
- Check test output for specific failures
- Ensure all dependencies are installed

### Status Checks Not Appearing
- Verify workflow file is in `.github/workflows/ci.yml`
- Check that workflow runs on `pull_request` events
- Ensure job names match branch protection requirements

## Responsible Parties

- **Dev Team**: Create PRs, address review feedback, ensure tests pass
- **Repository Maintainer**: Configure branch protection, review PRs, merge approved PRs

## Next Steps

1. Configure branch protection rules in GitHub (see `.github/BRANCH_PROTECTION.md`)
2. Set up Codecov (optional) for coverage tracking
3. Add additional test cases as needed
4. Configure repository settings for required reviewers

## Related Files

- `.github/workflows/ci.yml` - CI workflow definition
- `pytest.ini` - Test configuration
- `ruff.toml` - Linter configuration
- `requirements-dev.txt` - Development dependencies
- `.github/PULL_REQUEST_TEMPLATE.md` - PR template
- `CONTRIBUTING.md` - Contribution guidelines


