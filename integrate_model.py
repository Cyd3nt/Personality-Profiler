"""
Interactive CLI for integrating the emotional model with different LLMs.
Provides an easy workflow for testing and using the emotional model.
"""

import argparse
import json
import os
from typing import Dict, Optional

from emotional_model import EmotionalModel
from llm_adapters import create_adapter


class ModelIntegrator:
    def __init__(self):
        self.model = EmotionalModel()
        self.adapter = None
        self.config: Dict = {}
        self.load_config()

    def load_config(self):
        """Load API keys and configuration from config.json"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)

    def save_config(self):
        """Save API keys and configuration to config.json"""
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def setup_api_keys(self):
        """Interactive prompt to set up API keys"""
        print("\n=== API Key Setup ===")
        print("Enter API keys for the services you want to use (press Enter to skip):")

        # OpenAI
        key = input("OpenAI API Key: ").strip()
        if key:
            self.config['openai_api_key'] = key

        # Anthropic
        key = input("Anthropic API Key: ").strip()
        if key:
            self.config['anthropic_api_key'] = key

        # HuggingFace
        key = input("HuggingFace API Token: ").strip()
        if key:
            self.config['huggingface_token'] = key

        self.save_config()
        print("\nAPI keys saved successfully!")

    def select_model(self) -> Optional[str]:
        """Display menu to select LLM model type"""
        print("\n=== Select Model Type ===")
        print("1. OpenAI (GPT-3, GPT-4)")
        print("2. Anthropic (Claude)")
        print("3. HuggingFace")
        print("4. Setup API Keys")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ").strip()

        model_map = {
            "1": "openai",
            "2": "anthropic",
            "3": "huggingface"
        }

        if choice == "4":
            self.setup_api_keys()
            return self.select_model()
        elif choice == "5":
            return None
        elif choice in model_map:
            model_type = model_map[choice]
            # Check if API key is configured
            key_map = {
                "openai": "openai_api_key",
                "anthropic": "anthropic_api_key",
                "huggingface": "huggingface_token"
            }
            if key_map[model_type] not in self.config:
                print(f"\nWarning: No API key found for {model_type}.")
                setup = input("Would you like to set it up now? (y/n): ").strip().lower()
                if setup == 'y':
                    self.setup_api_keys()
            return model_type
        else:
            print("\nInvalid choice. Please try again.")
            return self.select_model()

    def test_emotional_response(self):
        """Interactive testing of emotional responses"""
        print("\n=== Test Emotional Responses ===")
        print("Enter emotional events to see how the model responds.")
        print("Type 'exit' to return to the main menu.")

        while True:
            event = input("\nEnter an event: ").strip()
            if event.lower() == 'exit':
                break

            intensity = input("Enter intensity (0.0-1.0, default 1.0): ").strip()
            try:
                intensity = float(intensity) if intensity else 1.0
            except ValueError:
                print("Invalid intensity. Using default 1.0")
                intensity = 1.0

            # Process the event
            state = self.adapter.process_event(event, intensity)

            # Display the emotional state
            print("\nEmotional State:")
            for emotion, value in state.to_dict().items():
                print(f"{emotion}: {value:.2f}")

            # Show model-specific output
            if isinstance(self.adapter, type(create_adapter("openai", self.model))):
                print("\nOpenAI System Message:")
                print(self.adapter.create_system_message(state)["content"])
            elif isinstance(self.adapter, type(create_adapter("anthropic", self.model))):
                print("\nAnthropic Prompt:")
                print(self.adapter.create_prompt(state, "Continue the conversation"))
            elif isinstance(self.adapter, type(create_adapter("huggingface", self.model))):
                print("\nHuggingFace Emotional Features:")
                print(self.adapter.format_for_tokenizer(state))

    def run(self):
        """Main interaction loop"""
        print("Welcome to the Emotional Model Integrator!")

        while True:
            model_type = self.select_model()
            if not model_type:
                break

            self.adapter = create_adapter(model_type, self.model)
            print(f"\nSuccessfully connected to {model_type.title()} adapter!")

            self.test_emotional_response()


def main():
    parser = argparse.ArgumentParser(description="Emotional Model Integration Tool")
    parser.add_argument("--setup", action="store_true", help="Run API key setup")
    args = parser.parse_args()

    integrator = ModelIntegrator()
    if args.setup:
        integrator.setup_api_keys()
    else:
        integrator.run()


if __name__ == "__main__":
    main()
