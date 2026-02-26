"""
Basic usage examples for LangChain WebSearch Tool.
"""

from langchain_websearch import WebSearchTool


def basic_search_example():
    """Basic search example."""
    # Set up your API keys (for testing, use environment variables in production)
    import os
    os.environ["QUERIT_API_KEY"] = "your-querit-api-key"
    
    # Initialize the tool
    search_tool = WebSearchTool()
    
    # Perform a search
    results = search_tool._run("latest Python programming news")
    print("Search Results:")
    print(results)


def agent_integration_example():
    """Example of integrating with LangChain agent."""
    import os
    
    try:
        from langchain.agents import initialize_agent
        from langchain.llms import OpenAI
        
        # Set up API keys
        os.environ["QUERIT_API_KEY"] = "your-querit-api-key"
        os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
        
        # Initialize tools
        search_tool = WebSearchTool()
        
        # Create agent
        agent = initialize_agent(
            tools=[search_tool],
            llm=OpenAI(temperature=0),
            agent="zero-shot-react-description",
            verbose=True
        )
        
        # Run agent with search capability
        result = agent.run(
            "What are the latest developments in artificial intelligence research?"
        )
        print("\nAgent Result:")
        print(result)
        
    except ImportError:
        print("LangChain OpenAI components not installed. Install with: pip install openai")


def advanced_configuration_example():
    """Example showing advanced configuration options."""
    # Set up API keys
    import os
    os.environ["QUERIT_API_KEY"] = "your-querit-api-key"
    
    # Configure tool with specific parameters
    search_tool = WebSearchTool(
        num_results=5
    )
    
    # Perform search
    results = search_tool._run("machine learning tutorials")
    print("Querit Search Results:")
    print(results)


if __name__ == "__main__":
    print("=== Basic Search Example ===")
    basic_search_example()
    
    print("\n=== Agent Integration Example ===")
    agent_integration_example()
    
    print("\n=== Advanced Configuration Example ===")
    advanced_configuration_example()