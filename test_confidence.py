#!/usr/bin/env python3

# Import the real FirstLayerDMM for API testing
from Backend.Model import FirstLayerDMM

def test_intent_detection():
    test_queries = [
        "open chrome",
        "play music",
        "what is the weather",
        "add a todo to buy groceries",
        "hello",
        "some random query"
    ]

    print("Testing Intent Detection with Confidence Scoring:")
    print("=" * 60)

    for query in test_queries:
        print(f"\nQuery: '{query}'")
        try:
            result = FirstLayerDMM(query)
            print(f"Result: {result}")
            print(f"Type: {type(result)}")

            if result and isinstance(result, list) and len(result) > 0:
                first_item = result[0]
                print(f"First item: {first_item}")
                print(f"First item type: {type(first_item)}")

                if isinstance(first_item, dict):
                    intent = first_item.get('intent')
                    confidence = first_item.get('confidence')
                    print(f"Intent: {intent}")
                    print(f"Confidence: {confidence}")
                    print(f"Confidence type: {type(confidence)}")

                    # Test confidence thresholds
                    if confidence >= 0.75:
                        print("→ Would execute directly (high confidence)")
                    elif confidence >= 0.45:
                        print("→ Would ask for clarification (medium confidence)")
                    else:
                        print("→ Would ask to rephrase (low confidence)")
                else:
                    print("ERROR: First item is not a dict!")
            else:
                print("ERROR: Result is not a list or is empty!")

        except Exception as e:
            print(f"ERROR: {e}")

        print("-" * 40)

def test_main_logic():
    print("\n\nTesting Main Logic Flow:")
    print("=" * 40)

    # Test the confidence thresholds
    test_cases = [
        {"intent": "open chrome", "confidence": 0.85},
        {"intent": "general what is weather", "confidence": 0.60},
        {"intent": "general random query", "confidence": 0.35}
    ]

    HIGH_CONFIDENCE = 0.75
    LOW_CONFIDENCE = 0.45

    for case in test_cases:
        intent = case["intent"]
        confidence = case["confidence"]
        print(f"\nIntent: {intent}, Confidence: {confidence}")

        if confidence >= HIGH_CONFIDENCE:
            print("→ Execute directly")
        elif confidence >= LOW_CONFIDENCE:
            print("→ Ask clarification")
        else:
            print("→ Ask to rephrase")

if __name__ == "__main__":
    test_intent_detection()
    test_main_logic()
