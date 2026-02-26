# PyPI Publishing Guide

## Pre-release Preparation

### 1. Update Project Information
Check and update information in the following files:
- Version number and author information in `pyproject.toml`
- Usage instructions in `README.md`
- Version change records in `CHANGELOG.md`

### 2. Ensure All Tests Pass
```bash
# Run tests
export QUERIT_API_KEY="your-querit-api-key" && python3 -m pytest tests/

# Check code formatting
python3 -m black src/ tests/ --check
python3 -m flake8 src/ tests/
```

## Publishing to PyPI

### 1. Build the Package
```bash
# Clean previous builds
rm -rf build/ dist/ src/*.egg-info/

# Build the package
python3 -m build
```

### 2. Check Package Contents
```bash
# Check built files
ls -la dist/

# Test installation
python3 -m pip install dist/langchain_websearch-*.whl --force-reinstall
```

### 3. Upload to PyPI

#### Method 1: Using twine (Recommended)
```bash
# Upload to test PyPI
python3 -m twine upload --repository testpypi dist/*

# Upload to production PyPI
python3 -m twine upload dist/*
```

#### Method 2: Using GitHub Actions (Automated Publishing)
Create `.github/workflows/publish.yml` file to automate the publishing process

## Verify the Release

### 1. Test New Version Installation
```bash
# Test installation from PyPI
python3 -m pip uninstall langchain-querit -y
python3 -m pip install langchain-querit
```

### 2. Verify Functionality
```python
from langchain_websearch import WebSearchTool, __version__
print(f"Version: {__version__}")
tool = WebSearchTool()
print(f"Tool name: {tool.name}")
```

## Version Upgrade Process

### 1. Update Version Number
Follow semantic versioning:
- **MAJOR** version: Incompatible API changes
- **MINOR** version: Backward-compatible functionality additions
- **PATCH** version: Backward-compatible bug fixes

### 2. Update Changelog
Record changes in the new version in `CHANGELOG.md`

## Testing Notes
- Ensure all tests are run before publishing
- Tests should include real API calls
- Verify behavior with different parameter configurations
- Check edge cases (such as empty queries)
- Test with actual Querit API key

## Release Checklist
- [ ] All tests pass with valid API key
- [ ] Code quality checks pass (black, flake8)
- [ ] Documentation is up to date
- [ ] Version number updated
- [ ] Changelog updated
- [ ] Package builds successfully
- [ ] Test installation works
- [ ] PyPI upload successful