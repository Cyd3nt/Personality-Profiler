"""
LLM/AI Model Adapters for the Emotional Model

This module provides adapter classes to integrate the emotional model with various LLM/AI models.
It includes standardized interfaces and utility functions for emotional state processing.
"""

import json
from dataclasses import dataclass
from typing import Dict, List, Any

from emotional_model import EmotionalModel


@dataclass
class EmotionalState:
    """Represents an emotional state that can be passed to LLMs"""
    joy: float
    sadness: float
    anger: float
    fear: float
    trust: float
    surprise: float
    valence: float
    arousal: float
    dominance: float

    def to_dict(self) -> Dict[str, float]:
        """Convert emotional state to dictionary format"""
        return {
            "joy": self.joy,
            "sadness": self.sadness,
            "anger": self.anger,
            "fear": self.fear,
            "trust": self.trust,
            "surprise": self.surprise,
            "valence": self.valence,
            "arousal": self.arousal,
            "dominance": self.dominance
        }

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'EmotionalState':
        """Create EmotionalState from dictionary"""
        return cls(**data)


class BaseLLMAdapter:
    """Base adapter class for LLM integration"""

    def __init__(self, emotional_model: EmotionalModel):
        self.emotional_model = emotional_model

    def process_event(self, event: str, intensity: float = 1.0) -> EmotionalState:
        """Process an event and return emotional state"""
        response = self.emotional_model.process_emotional_event(event, intensity)
        return EmotionalState(**response)

    def get_current_state(self) -> EmotionalState:
        """Get current emotional state"""
        state = self.emotional_model.get_current_state()
        return EmotionalState(**state)


class OpenAIAdapter(BaseLLMAdapter):
    """Adapter for OpenAI models (GPT-3, GPT-4)"""

    def format_for_prompt(self, state: EmotionalState) -> str:
        """Format emotional state for OpenAI prompt"""
        emotions = [f"{k}: {v:.2f}" for k, v in state.to_dict().items()]
        return (
                "Current emotional state:\n" +
                "\n".join(emotions)
        )

    def create_system_message(self, state: EmotionalState) -> Dict[str, str]:
        """Create system message with emotional context"""
        return {
            "role": "system",
            "content": f"You are an AI assistant with the following emotional state:\n{self.format_for_prompt(state)}\n"
                       f"Let this emotional state influence your responses appropriately."
        }


class AnthropicAdapter(BaseLLMAdapter):
    """Adapter for Anthropic models (Claude)"""

    def format_for_prompt(self, state: EmotionalState) -> str:
        """Format emotional state for Claude prompt"""
        return json.dumps(state.to_dict(), indent=2)

    def create_prompt(self, state: EmotionalState, message: str) -> str:
        """Create a Claude-style prompt with emotional context"""
        return (
            f"Human: The following JSON represents my current emotional state:\n"
            f"{self.format_for_prompt(state)}\n\n"
            f"Please respond to the following message while taking this emotional context into account:\n"
            f"{message}\n\n"
            "Assistant:"
        )


class HuggingFaceAdapter(BaseLLMAdapter):
    """Adapter for HuggingFace models"""

    def format_for_tokenizer(self, state: EmotionalState) -> Dict[str, List[float]]:
        """Format emotional state for HuggingFace tokenizer"""
        return {
            "emotional_state": list(state.to_dict().values())
        }

    def create_model_inputs(self, state: EmotionalState,
                            tokenizer: Any, text: str) -> Dict[str, Any]:
        """Create model inputs with emotional context"""
        # Encode the text
        encoded = tokenizer(text, return_tensors="pt")

        # Add emotional state as additional features
        emotional_features = self.format_for_tokenizer(state)

        return {
            **encoded,
            "emotional_features": emotional_features
        }


def create_adapter(model_type: str, emotional_model: EmotionalModel) -> BaseLLMAdapter:
    """Factory function to create appropriate adapter based on model type"""
    adapters = {
        "openai": OpenAIAdapter,
        "anthropic": AnthropicAdapter,
        "huggingface": HuggingFaceAdapter
    }

    adapter_class = adapters.get(model_type.lower())
    if not adapter_class:
        raise ValueError(f"Unsupported model type: {model_type}")

    return adapter_class(emotional_model)
