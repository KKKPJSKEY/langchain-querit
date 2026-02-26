# LangChain WebSearch Tool

A powerful LangChain tool for web search functionality using Querit Search API.

## 🔍 Features

- **Querit Search API Integration**: Powered by Querit Search API
- **API Key Management**: Secure API key handling with environment variables
- **LangChain Integration**: Seamlessly integrates with LangChain agents and chains
- **Structured Results**: Returns formatted search results with metadata
- **Async Support**: Asynchronous version available
- **Flexible Configuration**: Customizable search parameters

## 🚀 Quick Start

### Installation

```bash
pip install langchain-querit
```

### Basic Usage

```python
import os
from langchain_websearch import WebSearchTool

# Set your API key (recommended: use environment variables)
os.environ["QUERIT_API_KEY"] = "your-querit-api-key"

# Initialize the tool
search_tool = WebSearchTool()

# Perform a search
results = search_tool._run("latest Python programming news")
print(results)
```

### Advanced Configuration

```python
from langchain_websearch import WebSearchTool

# Configure with specific parameters
search_tool = WebSearchTool(
    num_results=5  # Number of results to return
)

# Use with custom query
results = search_tool._run("machine learning tutorials")
print(results)
```

## 🧪 Testing

To run tests with your API key:

```bash
export QUERIT_API_KEY="your-querit-api-key" && python3 -m pytest tests/
```

For verbose test output:

```bash
export QUERIT_API_KEY="your-querit-api-key" && python3 tests/test_basic.py
```

## ⚙️ Configuration

### Environment Variables

- `QUERIT_API_KEY`: Your Querit Search API key (required)

### WebSearchTool Parameters

- `num_results`: Number of results to return (default: 10, range: 1-50)
- `region`: Search region/language (default: "en-US", currently not used)
- `safe_search`: Enable safe search filtering (default: True, currently not used)

## 📚 Documentation

For full API reference and examples, see the [examples directory](examples/).

### Example Usage

Check [`examples/basic_usage.py`](examples/basic_usage.py) for complete usage examples including LangChain agent integration.

## 🔧 Development

### Development Setup

```bash
# Clone the repository
git clone https://github.com/KKKPJSKEY/langchain-querit.git
cd langchain-querit

# Install in development mode
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
export QUERIT_API_KEY="your-querit-api-key" && pytest tests/

# Run with coverage
export QUERIT_API_KEY="your-querit-api-key" && pytest --cov=src tests/

# Run specific test file
export QUERIT_API_KEY="your-querit-api-key" && python3 tests/test_basic.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

## 🔗 Links

- [Querit API Documentation](https://api.querit.ai/docs)
- [LangChain Documentation](https://python.langchain.com/docs/)
- [Issue Tracker](https://github.com/KKKPJSKEY/langchain-querit/issues)