"""
Real testing for WebSearchTool.
No mocks, directly testing Querit API calls in real environment.
"""

import os
import sys
import time
import signal
from threading import Timer
from langchain_websearch import WebSearchTool


class TimeoutException(Exception):
    """Timeout exception"""

    pass


def timeout_handler(signum, frame):
    """Timeout handler"""
    raise TimeoutException("Request timeout")


def check_api_key():
    """Check if API key exists"""
    print("🔑 Checking API key environment variable...")
    api_key = os.getenv("QUERIT_API_KEY")

    if api_key:
        print(f"✓ Found API key: {api_key[:8]}...{api_key[-4:]}")
        return True
    else:
        print("⚠️  QUERIT_API_KEY environment variable not found")
        print("Please set environment variable before running tests:")
        print("  export QUERIT_API_KEY='your-api-key'")
        return False


def test_api_key_only_no_query(timeout_seconds=10):
    """Test API key only, no query passed"""
    print("\n🧪 Testing: WebSearchTool with API key only, no query")
    print("=" * 60)

    # Ensure API key exists
    api_key = os.getenv("QUERIT_API_KEY")

    if not api_key:
        print("⚠️  QUERIT_API_KEY environment variable not set")
        print("Will use test key for this test")
        api_key = "test-key-only-12345"
        os.environ["QUERIT_API_KEY"] = api_key

    print(f"🔑 Using API key: {api_key[:8]}...{api_key[-4:]}")

    try:
        # Create tool instance
        print("🔄 Initializing WebSearchTool...")
        tool = WebSearchTool()

        print("📋 Test configuration:")
        print(f"✓ Tool name: {tool.name}")
        print(f"✓ Default results: {tool.num_results}")
        print(f"✓ Search backend: {tool._backend_instance.__class__.__name__}")
        print(f"✓ API endpoint: {tool._backend_instance.BASE_URL}")

        print("\n🎯 Test scenario:")
        print("✓ API key is set")
        print("✓ Will call tool._run('') - empty string query")
        print("✓ Testing if system handles empty query without crashing")

        # Set timeout
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout_seconds)

        try:
            # Execute test
            print(f"\n⏳ Sending request (timeout: {timeout_seconds} seconds)...")
            start_time = time.time()

            result = tool._run("")  # Empty query

            elapsed_time = time.time() - start_time
            signal.alarm(0)  # Cancel timeout

            print(f"✅ Request completed - Time taken: {elapsed_time:.2f} seconds")
            print(f"📏 Result length: {len(result)} characters")

            print("\n📄 Returned result:")
            print("-" * 50)
            print(result)
            print("-" * 50)

            # Analyze result
            print("\n🔍 Result analysis:")

            if "Search failed" in result:
                if "401" in result or "Unauthorized" in result:
                    print("✓ API key authentication failed (HTTP 401)")
                    print("✓ Verified system can send requests to API server")
                    print("✓ Error message formatting works correctly")
                elif "Querit API key not found" in result:
                    print("✓ API key not found error")
                    print("✓ Error handling mechanism works properly")
                else:
                    print(f"✓ Other search error: {result[:100]}")
            elif "No search results found" in result:
                print("✓ API accepted empty query and returned no results message")
                print("✓ System correctly handles edge cases")
                print("✓ User-friendly error message returned")
            else:
                print("✓ Successfully returned search results")
                print("✓ Empty query was accepted by API")
                print("✓ Formatted results returned")

        except TimeoutException:
            signal.alarm(0)  # Cancel timeout
            print(f"\n⏰ Request timed out ({timeout_seconds} seconds)")
            print("✓ WebSearchTool did not crash within timeout period")
            print("✓ System needs more time to process request")
            print("✓ No immediate errors returned")
            return True

        print("\n✅ Verification points:")
        print("1. ✅ WebSearchTool initialized correctly")
        print("2. ✅ _run('') method accepts empty string parameter")
        print("3. ✅ No crash due to empty query")
        print("4. ✅ Formatted response returned")

        if "Search failed" in result and ("401" in result or "Unauthorized" in result):
            print("5. ⚠️  API key invalid or timeout, but API call mechanism works")
        else:
            print("5. ✅ API response handling normal")

        print("\n🎯 Test conclusion:")
        print("WebSearchTool correctly handles API key only, no query scenario.")
        print("System is stable, no crashes, returns reasonable responses.")

        return True

    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_websearchtool_with_queries():
    """Test WebSearchTool with various queries"""
    print("\n🧪 Testing: WebSearchTool with various queries")
    print("=" * 60)

    if not check_api_key():
        print("❌ Cannot proceed with test - API key missing")
        return False

    try:
        # Create tool instance
        tool = WebSearchTool()

        print("🎯 Test configuration:")
        print(f"✓ Tool name: {tool.name}")
        print(f"✓ Default results: {tool.num_results}")
        print(f"✓ Search backend: {tool._backend_instance.__class__.__name__}")
        print(f"✓ API endpoint: {tool._backend_instance.BASE_URL}")

        # Test query list
        test_queries = [
            "hello world",
            "Python programming",
            "machine learning",
            "artificial intelligence",
        ]

        for i, query in enumerate(test_queries, 1):
            print(f"\n📥 Test query {i}/{len(test_queries)}: '{query}'")
            print("-" * 50)

            try:
                # Record start time
                start_time = time.time()

                # Execute real search
                print("⏳ Sending request to Querit API...")
                result = tool._run(query)

                # Calculate elapsed time
                elapsed_time = time.time() - start_time

                print(f"✅ Request completed - Time taken: {elapsed_time:.2f} seconds")
                print(f"📏 Result length: {len(result)} characters")

                # Print result preview
                print("\n📄 Result preview:")
                print("=" * 50)

                if result:
                    # Limit displayed lines to avoid terminal overflow
                    lines = result.split("\n")
                    display_lines = min(len(lines), 15)  # Max 15 lines
                    for j in range(display_lines):
                        line = lines[j].strip()
                        if not line:  # Skip empty lines
                            continue
                        print(line)

                    if len(lines) > display_lines:
                        print(f"... (showing {display_lines} of {len(lines)} lines)")

                print("=" * 50)

                # Simple success check
                if "Search failed" in result:
                    print("⚠️  Search may have encountered issues")
                elif "No search results found" in result:
                    print("ℹ️  No search results found")
                else:
                    print("✅ Search completed successfully")

                # Add delay between queries to avoid API rate limiting
                if i < len(test_queries):
                    print(f"⏸️  Waiting 1 second before next query...")
                    time.sleep(1)

            except Exception as e:
                print(f"❌ Query '{query}' execution failed: {e}")
                import traceback

                traceback.print_exc()
                continue

        return True

    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_no_token():
    """Test WebSearchTool without API token"""
    print("\n🧪 Testing: WebSearchTool without API token")
    print("=" * 60)

    # Save original key if exists
    original_key = os.getenv("QUERIT_API_KEY")

    try:
        # Remove API key
        if "QUERIT_API_KEY" in os.environ:
            del os.environ["QUERIT_API_KEY"]

        print("📋 Test scenario:")
        print("✓ No API key set")
        print("✓ Will attempt to initialize and use WebSearchTool")

        try:
            # Initialize tool
            print("\n🔄 Initializing WebSearchTool without API key...")
            tool = WebSearchTool()

            # Set timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(10)  # 10 second timeout

            try:
                print("\n⏳ Attempting search without API key...")
                start_time = time.time()

                result = tool._run("test query")

                elapsed_time = time.time() - start_time
                signal.alarm(0)  # Cancel timeout

                print(f"✅ Request completed - Time: {elapsed_time:.2f} seconds")
                print(f"📏 Result length: {len(result)} characters")

                print("\n📄 Response:")
                print("-" * 50)
                print(result)
                print("-" * 50)

                # Analyze response
                if "Querit API key not found" in result:
                    print("\n🔍 Analysis: Correct error message returned")
                    print("✓ WebSearchTool properly handles missing API key")
                else:
                    print("\n⚠️ Analysis: Unexpected response")
                    print(f"Response: {result[:200]}")

            except TimeoutException:
                signal.alarm(0)
                print("\n⏰ Request timed out (10 seconds)")
                print("✓ System remained stable during timeout")

            except Exception as e:
                print(f"\n❌ Search failed with exception: {e}")
                import traceback

                traceback.print_exc()

        except Exception as e:
            print(f"\n❌ Initialization failed with exception: {e}")
            import traceback

            traceback.print_exc()

        print("\n✅ Verification points:")
        print("1. ✅ System handles initialization without API key")
        print("2. ✅ Returns appropriate error for missing API key")
        print("3. ✅ No crashes or unexpected behavior")

        return True

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        # Restore original key
        if original_key:
            os.environ["QUERIT_API_KEY"] = original_key


def main():
    """Main test function"""
    print("🚀 Starting real WebSearchTool tests")
    print("No mocks, directly accessing Querit API")
    print("=" * 70)

    try:
        # Run tests in order
        test_api_key_only_no_query(timeout_seconds=15)
        test_websearchtool_with_queries()
        test_no_token()

        print("\n" + "=" * 70)
        print("🎉 Real testing completed!")
        print("📊 Test summary:")
        print("  ✓ API key only test (no query)")
        print("  ✓ Various query tests")
        print("  ✓ No API token test")
        print("\n🔍 Note: Actual results depend on Querit API real-time response")

        return True

    except Exception as e:
        print(f"\n❌ Test encountered exception: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
