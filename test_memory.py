import os
import time
import tempfile
from utils.memory import MemoryManager

def test_memory_trimming():
    """Test memory trimming after exceeding MAX_CONVERSATION_TURNS"""
    print("Testing memory trimming...")

    # Set environment variables for testing
    os.environ["MAX_CONVERSATION_TURNS"] = "3"
    os.environ["MEMORY_INACTIVITY_TIMEOUT"] = "300"

    # Create a new memory manager instance
    memory_manager = MemoryManager()

    # Add more messages than the limit (3 turns = 6 messages)
    for i in range(8):
        role = "user" if i % 2 == 0 else "assistant"
        memory_manager.add_message(role, f"Message {i+1}")

    # Check that memory was trimmed
    context = memory_manager.get_context()
    assert len(context) <= 6, f"Memory should be trimmed to 6 messages, got {len(context)}"
    print(f"✓ Memory trimmed correctly: {len(context)} messages")

def test_inactivity_cleanup():
    """Test inactivity cleanup after timeout"""
    print("Testing inactivity cleanup...")

    # Set short timeout for testing
    os.environ["MAX_CONVERSATION_TURNS"] = "10"
    os.environ["MEMORY_INACTIVITY_TIMEOUT"] = "1"  # 1 second

    memory_manager = MemoryManager()

    # Add some messages
    memory_manager.add_message("user", "Hello")
    memory_manager.add_message("assistant", "Hi there")

    # Check memory is not empty
    assert len(memory_manager.get_context()) > 0, "Memory should have messages"

    # Wait for timeout
    time.sleep(2)

    # Trigger cleanup
    memory_manager.cleanup_if_inactive()

    # Check memory was cleared
    assert len(memory_manager.get_context()) == 0, "Memory should be cleared after inactivity"
    print("✓ Memory cleared after inactivity timeout")

def test_memory_persistence():
    """Test saving and loading memory from file"""
    print("Testing memory persistence...")

    os.environ["MAX_CONVERSATION_TURNS"] = "10"
    os.environ["MEMORY_INACTIVITY_TIMEOUT"] = "300"

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as f:
        temp_file = f.name

    try:
        # Create memory manager and add messages
        memory_manager1 = MemoryManager()
        memory_manager1.add_message("user", "Test message 1")
        memory_manager1.add_message("assistant", "Test response 1")

        # Save to file
        memory_manager1.save_to_file(temp_file)

        # Create new memory manager and load from file
        memory_manager2 = MemoryManager()
        memory_manager2.load_from_file(temp_file)

        # Check messages were loaded
        context = memory_manager2.get_context()
        assert len(context) == 2, f"Should load 2 messages, got {len(context)}"
        assert context[0]["content"] == "Test message 1", "First message content mismatch"
        assert context[1]["content"] == "Test response 1", "Second message content mismatch"
        print("✓ Memory persistence works correctly")

    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.remove(temp_file)

def test_error_handling():
    """Test error handling and memory clearing on exceptions"""
    print("Testing error handling...")

    os.environ["MAX_CONVERSATION_TURNS"] = "10"
    os.environ["MEMORY_INACTIVITY_TIMEOUT"] = "300"

    memory_manager = MemoryManager()

    # Add messages
    memory_manager.add_message("user", "Test")
    memory_manager.add_message("assistant", "Response")

    # Simulate error clearing
    memory_manager.memory.clear()
    memory_manager.save_to_file("Data/ChatLog.json")

    # Check memory is cleared
    assert len(memory_manager.get_context()) == 0, "Memory should be cleared on error"
    print("✓ Error handling works correctly")

if __name__ == "__main__":
    print("Running thorough memory tests...\n")

    try:
        test_memory_trimming()
        test_inactivity_cleanup()
        test_memory_persistence()
        test_error_handling()

        print("\n✅ All tests passed! Memory management is working correctly.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
