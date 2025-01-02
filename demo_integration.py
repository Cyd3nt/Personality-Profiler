"""
Demo script to showcase the emotional model integration with different LLMs.
"""

from emotional_model import EmotionalModel
from llm_adapters import create_adapter


def demo_openai():
    """Demonstrate OpenAI integration"""
    print("\n=== OpenAI Integration Demo ===")
    model = EmotionalModel()
    adapter = create_adapter("openai", model)

    # Test various emotional events
    events = [
        ("I just won a major award!", 1.0),
        ("I'm feeling a bit nervous about the presentation.", 0.7),
        ("That's absolutely incredible news!", 0.9),
        ("I'm disappointed with the results.", 0.6)
    ]

    for event, intensity in events:
        print(f"\nProcessing event: '{event}' (intensity: {intensity})")
        state = adapter.process_event(event, intensity)

        print("\nEmotional State:")
        for emotion, value in state.to_dict().items():
            print(f"{emotion}: {value:.2f}")

        print("\nGenerated OpenAI System Message:")
        print(adapter.create_system_message(state)["content"])
        print("\n" + "=" * 50)


def demo_anthropic():
    """Demonstrate Anthropic integration"""
    print("\n=== Anthropic Integration Demo ===")
    model = EmotionalModel()
    adapter = create_adapter("anthropic", model)

    # Test various emotional events
    events = [
        ("This is such a beautiful day!", 0.8),
        ("I'm worried about the upcoming deadline.", 0.7),
        ("We achieved all our goals this quarter!", 0.9),
        ("The project faced some unexpected challenges.", 0.6)
    ]

    for event, intensity in events:
        print(f"\nProcessing event: '{event}' (intensity: {intensity})")
        state = adapter.process_event(event, intensity)

        print("\nEmotional State:")
        for emotion, value in state.to_dict().items():
            print(f"{emotion}: {value:.2f}")

        print("\nGenerated Anthropic Prompt:")
        print(adapter.create_prompt(state, "How should we proceed?"))
        print("\n" + "=" * 50)


def demo_huggingface():
    """Demonstrate HuggingFace integration"""
    print("\n=== HuggingFace Integration Demo ===")
    model = EmotionalModel()
    adapter = create_adapter("huggingface", model)

    # Test various emotional events
    events = [
        ("Great success on the latest experiment!", 0.9),
        ("The results were quite unexpected.", 0.7),
        ("We need to rethink our approach.", 0.6),
        ("Everyone loved the presentation!", 0.8)
    ]

    for event, intensity in events:
        print(f"\nProcessing event: '{event}' (intensity: {intensity})")
        state = adapter.process_event(event, intensity)

        print("\nEmotional State:")
        for emotion, value in state.to_dict().items():
            print(f"{emotion}: {value:.2f}")

        print("\nHuggingFace Emotional Features:")
        print(adapter.format_for_tokenizer(state))
        print("\n" + "=" * 50)


def main():
    print("Welcome to the Emotional Model Integration Demo!")
    print("This demo will showcase how the emotional model works with different LLMs.")

    while True:
        print("\nSelect a demo to run:")
        print("1. OpenAI Integration")
        print("2. Anthropic Integration")
        print("3. HuggingFace Integration")
        print("4. Run All Demos")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            demo_openai()
        elif choice == "2":
            demo_anthropic()
        elif choice == "3":
            demo_huggingface()
        elif choice == "4":
            demo_openai()
            demo_anthropic()
            demo_huggingface()
        elif choice == "5":
            print("\nThank you for trying the demo!")
            break
        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()
