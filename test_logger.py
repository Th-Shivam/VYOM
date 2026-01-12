#!/usr/bin/env python3
"""
Test script for the VYOM logging system
"""
import os
import sys
from utils.logger import get_logger

def test_logger():
    """Test the logger functionality"""
    print("Testing VYOM Logger...")

    # Test logger initialization
    logger = get_logger()
    print("✓ Logger initialized successfully")

    # Test different log levels
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")

    print("✓ All log levels tested")

    # Test log level configuration
    current_level = os.getenv("LOG_LEVEL", "INFO")
    print(f"✓ Current log level: {current_level}")

    print("Logger test completed successfully!")

if __name__ == "__main__":
    test_logger()
