import random
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional

from advanced_dialogue import DialogueGenerator
from emotional_model import EmotionalCore
from human_personality_model import PersonalityVector
from memory_system import MemoryNetwork, MemoryTrace
from personality_calibration import PersonalityCalibration, PersonalityVector


@dataclass
class Memory:
    description: str
    timestamp: datetime
    importance: float
    emotion_tags: List[str]
    context: Dict[str, str]
    related_memories: List[str]  # Memory IDs
    retrieval_count: int = 0
    last_accessed: Optional[datetime] = None


@dataclass
class EmotionalState:
    valence: float  # Positive vs negative (-1 to 1)
    arousal: float  # Calm vs excited (-1 to 1)
    dominance: float  # Submissive vs dominant (-1 to 1)
    current_emotions: List[str]
    intensity: float  # 0 to 1


class DialogueGenerator:
    def __init__(self, personality: PersonalityVector):
        self.personality = personality
        self.dialogue_patterns = self._load_dialogue_patterns()

    def _load_dialogue_patterns(self) -> Dict[str, List[str]]:
        return {
            "greeting": [
                "Hello! How are you?",
                "Hi there!",
                "Greetings!",
                "Hey, nice to meet you!"
            ],
            "agreement": [
                "I completely agree with that.",
                "That's exactly right.",
                "You make a great point.",
                "I share your perspective on this."
            ],
            "disagreement": [
                "I see it differently.",
                "I'm not sure I agree.",
                "Let me offer a different perspective.",
                "I understand your point, but..."
            ],
            "question": [
                "What are your thoughts on this?",
                "How do you see it?",
                "What's your perspective?",
                "Could you elaborate on that?"
            ]
        }

    def generate_response(self,
                          context: str,
                          emotional_state: EmotionalState,
                          conversation_history: List[str]) -> str:
        """Generate a contextually appropriate dialogue response"""
        # Adjust response based on personality traits
        formality_level = self.personality.conscientiousness * 0.7 + \
                          self.personality.agreeableness * 0.3

        expressiveness = self.personality.verbal_expressiveness
        empathy_level = self.personality.empathy

        # Select base response pattern
        if "?" in context:
            base_pattern = random.choice(self.dialogue_patterns["question"])
        elif emotional_state.valence > 0.5:
            base_pattern = random.choice(self.dialogue_patterns["agreement"])
        elif emotional_state.valence < -0.5:
            base_pattern = random.choice(self.dialogue_patterns["disagreement"])
        else:
            base_pattern = random.choice(self.dialogue_patterns["greeting"])

        # Modify response based on personality and emotional state
        response = self._modify_response(base_pattern,
                                         formality_level,
                                         expressiveness,
                                         empathy_level,
                                         emotional_state)

        return response

    def _modify_response(self,
                         base_response: str,
                         formality: float,
                         expressiveness: float,
                         empathy: float,
                         emotional_state: EmotionalState) -> str:
        """Modify response based on personality traits and emotional state"""
        # Add emotional expressions based on state
        if emotional_state.intensity > 0.7:
            if emotional_state.valence > 0:
                base_response = f"I'm really excited! {base_response}"
            else:
                base_response = f"I must say, I'm concerned. {base_response}"

        # Add empathetic elements
        if empathy > 0.7:
            base_response += " How does that make you feel?"

        # Adjust expressiveness
        if expressiveness > 0.7:
            base_response += " " + random.choice([
                "This is fascinating!",
                "I'm really interested in your thoughts on this.",
                "There's so much to explore here!"
            ])

        # Adjust formality
        if formality > 0.7:
            base_response = base_response.replace("Hi", "Greetings")
            base_response = base_response.replace("Hey", "Hello")
        elif formality < 0.3:
            base_response = base_response.replace("Greetings", "Hey")
            base_response = base_response.replace("Hello", "Hi")

        return base_response


class EnhancedAgent:
    def __init__(self):
        self.memory_network = MemoryNetwork()
        self.personality_calibration = PersonalityCalibration()
        self.emotional_core = EmotionalCore()
        self.dialogue_generator = DialogueGenerator(PersonalityVector())

    def process_interaction(self,
                            content: str,
                            context: Dict[str, str],
                            emotional_state: Optional[Dict[str, float]] = None) -> str:
        """Process an interaction and generate a response"""
        # Update personality model with interaction
        self.personality_calibration.add_interaction(
            interaction_type="conversation",
            content=content,
            response="",  # Will be filled after generation
            context=context
        )

        # Create memory trace
        memory = MemoryTrace(
            content=content,
            timestamp=datetime.now(),
            importance=self._calculate_importance(content, context),
            emotional_valence=self.emotional_core.analyze_emotional_valence(content),
            context=context,
            tags=self._extract_tags(content, context)
        )
        memory_id = self.memory_network.store_memory(memory)

        # Update emotional state
        if emotional_state:
            self.emotional_core.update_emotional_state(emotional_state)

        # Generate response based on personality and emotional state
        personality = self.personality_calibration.get_personality_snapshot()
        emotional_state = self.emotional_core.get_emotional_state()
        response = self.dialogue_generator.generate_response(
            content=content,
            context=context,
            emotional_state=emotional_state,
            conversation_history=[]
        )

        # Store response in interaction history
        self.personality_calibration.add_interaction(
            interaction_type="conversation",
            content=content,
            response=response,
            context=context
        )

        return response

    def learn_from_observation(self,
                               behavior: str,
                               context: str,
                               emotional_state: Optional[Dict[str, float]] = None) -> None:
        """Learn from observed behavior"""
        # Add behavioral observation
        self.personality_calibration.add_behavioral_observation(
            context=context,
            behavior=behavior,
            timestamp=datetime.now(),
            emotional_state=emotional_state
        )

        # Create memory trace
        memory = MemoryTrace(
            content=behavior,
            timestamp=datetime.now(),
            importance=self._calculate_importance(behavior, {"context": context}),
            emotional_valence=self.emotional_core.analyze_emotional_valence(behavior),
            context={"context": context},
            tags=self._extract_tags(behavior, {"context": context})
        )
        self.memory_network.store_memory(memory)

        # Update emotional model if emotional state provided
        if emotional_state:
            self.emotional_core.update_emotional_state(emotional_state)

    def _calculate_importance(self, content: str, context: Dict[str, str]) -> float:
        """Calculate importance of a memory or interaction"""
        # Implement importance calculation based on:
        # - Emotional intensity
        # - Relevance to core values
        # - Novelty
        # - Context significance
        return 0.5  # Placeholder

    def _extract_tags(self, content: str, context: Dict[str, str]) -> set:
        """Extract relevant tags from content and context"""
        # Implement tag extraction based on:
        # - Key topics
        # - Emotional themes
        # - Context categories
        # - Behavioral patterns
        return {"placeholder_tag"}

    def save_agent_state(self, directory: str) -> None:
        """Save complete agent state"""
        import os
        os.makedirs(directory, exist_ok=True)

        # Save each component
        self.memory_network.save_memory_data(f"{directory}/memory_network.json")
        self.personality_calibration.save_calibration_data(
            f"{directory}/personality_calibration.json"
        )
        self.emotional_core.save_emotional_state(
            f"{directory}/emotional_state.json"
        )

    def load_agent_state(self, directory: str) -> None:
        """Load complete agent state"""
        # Load each component
        self.memory_network.load_memory_data(f"{directory}/memory_network.json")
        self.personality_calibration.load_calibration_data(
            f"{directory}/personality_calibration.json"
        )
        self.emotional_core.load_emotional_state(
            f"{directory}/emotional_state.json"
        )


def main():
    # Create a sample personality vector
    personality = PersonalityVector(
        openness=0.8,
        conscientiousness=0.7,
        extraversion=0.6,
        agreeableness=0.8,
        neuroticism=0.3,
        adaptability=0.7,
        resilience=0.8,
        verbal_expressiveness=0.9,
        listening_style=0.7,
        conflict_handling=0.6,
        risk_tolerance=0.5,
        decision_speed=0.6,
        analytical_tendency=0.7,
        social_energy=0.6,
        leadership_tendency=0.5,
        empathy=0.8,
        achievement_drive=0.7,
        growth_mindset=0.8,
        helping_tendency=0.9
    )

    # Create an agent with this personality
    agent = EnhancedAgent()

    # Simulate some interactions
    print("\nSimulating interactions with Alice:")

    inputs = [
        "Hello! How are you today?",
        "What do you think about artificial intelligence?",
        "That's an interesting perspective. Do you enjoy learning new things?",
        "I've had a really difficult day today.",
        "Thank you for listening to me."
    ]

    for user_input in inputs:
        print(f"\nUser: {user_input}")
        response = agent.process_interaction(user_input, {})
        print(f"Alice: {response}")

    # Generate insights
    print("\nConversation Insights:")
    # insights = agent.reflect_on_conversation()
    # for key, value in insights.items():
    #     print(f"{key}: {value}")


if __name__ == "__main__":
    main()
