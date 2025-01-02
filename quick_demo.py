"""
Quick demo of the emotional model integration with different LLMs.
"""

from emotional_model import EmotionalModel
from llm_adapters import create_adapter


def run_demo():
    print("=== Emotional Model Integration Demo ===\n")

    # Create model and test events
    model = EmotionalModel()
    events = [
        ("I just won a major award!", 1.0),
        ("I'm feeling quite anxious about tomorrow.", 0.7),
        ("This is absolutely amazing news!", 0.9),
        ("We need to rethink our approach.", 0.6)
    ]

    # Demo each adapter
    adapters = ["openai", "anthropic", "huggingface"]

    for adapter_type in adapters:
        print(f"\n=== {adapter_type.title()} Integration ===")
        adapter = create_adapter(adapter_type, model)

        for event, intensity in events:
            print(f"\nEvent: '{event}' (intensity: {intensity})")
            state = adapter.process_event(event, intensity)

            print("\nEmotional State:")
            for emotion, value in state.to_dict().items():
                print(f"{emotion}: {value:.2f}")

            # Show adapter-specific output
            if adapter_type == "openai":
                print("\nOpenAI System Message:")
                print(adapter.create_system_message(state)["content"])
            elif adapter_type == "anthropic":
                print("\nAnthropic Prompt:")
                print(adapter.create_prompt(state, "How should we proceed?"))
            else:  # huggingface
                print("\nHuggingFace Emotional Features:")
                print(adapter.format_for_tokenizer(state))

            print("\n" + "-" * 50)

        print("\n" + "=" * 50)


if __name__ == "__main__":
    run_demo()
