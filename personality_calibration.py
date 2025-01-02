import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional

import numpy as np

from neurodivergent_traits import NeurodivergentTraits, SensoryProfile, CognitiveStyle, SocialCommunicationStyle


@dataclass
class PersonalityVector:
    # Big Five personality traits (OCEAN model)
    openness: float  # Openness to experience
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float

    # Additional personality dimensions
    risk_tolerance: float
    emotional_expressiveness: float
    decision_style: float  # analytical vs. intuitive
    social_adaptability: float
    value_alignment: Dict[str, float]  # core values and their strengths

    # Communication style
    communication_preferences: Dict[str, float]
    language_patterns: Dict[str, float]
    humor_style: Dict[str, float]

    # Neurodivergent traits
    sensory_profile: Optional[SensoryProfile] = None
    cognitive_style: Optional[CognitiveStyle] = None
    social_communication: Optional[SocialCommunicationStyle] = None

    def to_vector(self) -> np.ndarray:
        """Convert personality traits to a normalized vector"""
        basic_traits = [
            self.openness,
            self.conscientiousness,
            self.extraversion,
            self.agreeableness,
            self.neuroticism
        ]

        additional_traits = [
            self.risk_tolerance,
            self.emotional_expressiveness,
            self.decision_style,
            self.social_adaptability
        ]

        # Flatten dictionaries into vectors
        value_vector = list(self.value_alignment.values())
        comm_vector = list(self.communication_preferences.values())
        lang_vector = list(self.language_patterns.values())
        humor_vector = list(self.humor_style.values())

        # Add neurodivergent components if available
        nd_components = []
        if self.sensory_profile:
            nd_components.extend([
                self.sensory_profile.visual_sensitivity,
                self.sensory_profile.auditory_sensitivity,
                self.sensory_profile.tactile_sensitivity
            ])
        if self.cognitive_style:
            nd_components.extend([
                self.cognitive_style.detail_focus,
                self.cognitive_style.pattern_recognition,
                self.cognitive_style.cognitive_flexibility
            ])
        if self.social_communication:
            nd_components.extend([
                self.social_communication.nonverbal_understanding,
                self.social_communication.literal_interpretation,
                self.social_communication.social_energy_management
            ])

        # Combine all traits into a single vector
        return np.array(basic_traits + additional_traits +
                        value_vector + comm_vector + lang_vector +
                        humor_vector + nd_components)


class PersonalityCalibration:
    def __init__(self):
        self.interview_responses: Dict[str, List[str]] = defaultdict(list)
        self.behavioral_observations: List[Dict] = []
        self.interaction_history: List[Dict] = []
        self.personality_vector: Optional[PersonalityVector] = None
        self.confidence_scores: Dict[str, float] = {}
        self.neurodivergent_traits = NeurodivergentTraits()

    def add_interview_response(self, question_id: str, response: str) -> None:
        """Add a response from the personality interview"""
        self.interview_responses[question_id].append(response)

        # Check for neurodivergent patterns in response
        if "sensory" in question_id:
            self._process_sensory_response(response)
        elif "cognitive" in question_id:
            self._process_cognitive_response(response)
        elif "social" in question_id:
            self._process_social_response(response)

        self._update_personality_model()

    def add_behavioral_observation(self,
                                   context: str,
                                   behavior: str,
                                   timestamp: datetime,
                                   emotional_state: Optional[Dict] = None) -> None:
        """Add an observed behavior to improve personality modeling"""
        observation = {
            "context": context,
            "behavior": behavior,
            "timestamp": timestamp,
            "emotional_state": emotional_state
        }
        self.behavioral_observations.append(observation)
        self._update_personality_model()

    def add_interaction(self,
                        interaction_type: str,
                        content: str,
                        response: str,
                        context: Dict,
                        outcome: Optional[str] = None) -> None:
        """Add an interaction to improve personality modeling"""
        interaction = {
            "type": interaction_type,
            "content": content,
            "response": response,
            "context": context,
            "outcome": outcome,
            "timestamp": datetime.now()
        }
        self.interaction_history.append(interaction)
        self._update_personality_model()

    def _analyze_language_patterns(self, text_samples: List[str]) -> Dict[str, float]:
        """Analyze language patterns from text samples"""
        patterns = {
            "formality": 0.0,
            "complexity": 0.0,
            "emotionality": 0.0,
            "assertiveness": 0.0,
            "detail_orientation": 0.0
        }

        # Implement sophisticated language pattern analysis here
        # This would involve NLP techniques to analyze:
        # - Vocabulary complexity
        # - Sentence structure
        # - Use of emotional language
        # - Communication style markers
        # - etc.

        return patterns

    def _analyze_values(self,
                        responses: List[str],
                        behaviors: List[Dict]) -> Dict[str, float]:
        """Analyze core values from responses and behaviors"""
        values = {
            "achievement": 0.0,
            "benevolence": 0.0,
            "tradition": 0.0,
            "security": 0.0,
            "self_direction": 0.0,
            "stimulation": 0.0,
            "hedonism": 0.0,
            "power": 0.0,
            "universalism": 0.0
        }

        # Implement value analysis based on:
        # - Explicit value statements in responses
        # - Behavioral patterns indicating values
        # - Decision-making patterns
        # - Emotional reactions to value-related situations

        return values

    def _analyze_humor_style(self,
                             responses: List[str],
                             interactions: List[Dict]) -> Dict[str, float]:
        """Analyze humor style from responses and interactions"""
        humor_style = {
            "affiliative": 0.0,  # Use humor to enhance relationships
            "self_enhancing": 0.0,  # Use humor to cope with stress
            "aggressive": 0.0,  # Use humor to criticize or manipulate
            "self_defeating": 0.0,  # Use humor at own expense
            "wit_level": 0.0,  # Cleverness and intellectual humor
            "sarcasm": 0.0,  # Use of irony and sarcasm
            "playfulness": 0.0  # General playful attitude
        }

        # Implement humor style analysis based on:
        # - Types of jokes made
        # - Reactions to different types of humor
        # - Context of humor usage
        # - Frequency of humor attempts

        return humor_style

    def _calculate_confidence_scores(self) -> Dict[str, float]:
        """Calculate confidence scores for different personality aspects"""
        scores = {}

        # Calculate based on:
        # - Amount and consistency of data
        # - Time span of observations
        # - Diversity of contexts
        # - Agreement between different data sources

        return scores

    def _process_sensory_response(self, response: str) -> None:
        """Process response for sensory processing patterns"""
        # Example analysis - would be more sophisticated in practice
        keywords = {
            "bright": ("visual", "avoiding"),
            "loud": ("auditory", "avoiding"),
            "quiet": ("auditory", "seeking"),
            "touch": ("tactile", None),
            "texture": ("tactile", None),
            "movement": ("vestibular", None)
        }

        for keyword, (sense_type, default_response) in keywords.items():
            if keyword in response.lower():
                # Analyze intensity and response type
                intensity = 0.7  # Would be calculated based on language analysis
                response_type = default_response or ("seeking" if "like" in response.lower() else "avoiding")

                self.neurodivergent_traits.add_sensory_observation(
                    stimulus_type=sense_type,
                    response=response_type,
                    intensity=intensity,
                    context={"source": "interview"},
                    timestamp=datetime.now()
                )

    def _process_cognitive_response(self, response: str) -> None:
        """Process response for cognitive patterns"""
        # Example cognitive pattern detection
        if "detail" in response.lower():
            self.neurodivergent_traits.add_cognitive_observation(
                observation_type="detail_focus",
                behavior=response,
                context={"source": "interview"},
                performance=0.8 if "good" in response.lower() else 0.4
            )

        # Check for special interests
        interest_keywords = ["passion", "fascinate", "love", "expert", "focus"]
        if any(keyword in response.lower() for keyword in interest_keywords):
            self.neurodivergent_traits.add_cognitive_observation(
                observation_type="special_interest",
                behavior=response,
                context={"source": "interview"},
                special_interest={
                    "topic": "unknown",  # Would be extracted from response
                    "intensity": 0.9 if "always" in response.lower() else 0.6
                }
            )

    def _process_social_response(self, response: str) -> None:
        """Process response for social communication patterns"""
        # Example social pattern detection
        if any(word in response.lower() for word in ["exhausting", "tired", "drain"]):
            self.neurodivergent_traits.add_social_observation(
                interaction_type="general",
                behavior=response,
                context={"source": "interview"},
                energy_impact=-0.7,
                masking_effort=0.8 if "pretend" in response.lower() else 0.4
            )

    def _update_personality_model(self) -> None:
        """Update the personality model based on all available data"""
        # Analyze language patterns from all text data
        text_samples = (
                [resp for responses in self.interview_responses.values()
                 for resp in responses] +
                [inter["content"] for inter in self.interaction_history] +
                [inter["response"] for inter in self.interaction_history]
        )
        language_patterns = self._analyze_language_patterns(text_samples)

        # Analyze values from responses and behaviors
        values = self._analyze_values(
            text_samples,
            self.behavioral_observations
        )

        # Analyze humor style
        humor_style = self._analyze_humor_style(
            text_samples,
            self.interaction_history
        )

        # Update confidence scores
        self.confidence_scores = self._calculate_confidence_scores()

        # Get neurodivergent trait summary
        nd_summary = self.neurodivergent_traits.get_trait_summary()

        # Create or update personality vector with neurodivergent traits
        self.personality_vector = PersonalityVector(
            # Basic traits (would be calculated from all available data)
            openness=0.0,  # placeholder
            conscientiousness=0.0,
            extraversion=0.0,
            agreeableness=0.0,
            neuroticism=0.0,

            # Additional traits
            risk_tolerance=0.0,
            emotional_expressiveness=0.0,
            decision_style=0.0,
            social_adaptability=0.0,

            # Complex trait dictionaries
            value_alignment=values,
            communication_preferences={
                "direct_vs_indirect": 0.0,
                "formal_vs_casual": 0.0,
                "emotional_vs_neutral": 0.0,
                "concise_vs_elaborate": 0.0
            },
            language_patterns=language_patterns,
            humor_style=humor_style,

            # Neurodivergent traits
            sensory_profile=SensoryProfile(**nd_summary["sensory_profile"]),
            cognitive_style=CognitiveStyle(**nd_summary["cognitive_style"]),
            social_communication=SocialCommunicationStyle(**nd_summary["social_communication"])
        )

    def get_personality_snapshot(self) -> Dict:
        """Get current personality model with confidence scores"""
        if not self.personality_vector:
            return {}

        # Convert neurodivergent traits to dictionaries
        personality_dict = vars(self.personality_vector)
        if personality_dict["sensory_profile"]:
            personality_dict["sensory_profile"] = \
                personality_dict["sensory_profile"].to_dict()
        if personality_dict["cognitive_style"]:
            personality_dict["cognitive_style"] = \
                personality_dict["cognitive_style"].to_dict()
        if personality_dict["social_communication"]:
            personality_dict["social_communication"] = \
                personality_dict["social_communication"].to_dict()

        return {
            "personality_vector": personality_dict,
            "confidence_scores": self.confidence_scores,
            "data_points": {
                "interviews": len(self.interview_responses),
                "behaviors": len(self.behavioral_observations),
                "interactions": len(self.interaction_history)
            },
            "last_updated": datetime.now().isoformat(),
            "neurodivergent_traits": self.neurodivergent_traits.get_trait_summary()
        }

    def save_calibration_data(self, filepath: str) -> None:
        """Save calibration data to file"""
        data = {
            "interview_responses": dict(self.interview_responses),
            "behavioral_observations": [
                {**obs, "timestamp": obs["timestamp"].isoformat()}
                for obs in self.behavioral_observations
            ],
            "interaction_history": [
                {**inter, "timestamp": inter["timestamp"].isoformat()}
                for inter in self.interaction_history
            ],
            "personality_snapshot": self.get_personality_snapshot()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load_calibration_data(self, filepath: str) -> None:
        """Load calibration data from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.interview_responses = defaultdict(list, data["interview_responses"])
        self.behavioral_observations = [
            {**obs, "timestamp": datetime.fromisoformat(obs["timestamp"])}
            for obs in data["behavioral_observations"]
        ]
        self.interaction_history = [
            {**inter, "timestamp": datetime.fromisoformat(inter["timestamp"])}
            for inter in data["interaction_history"]
        ]

        # Update personality model with loaded data
        self._update_personality_model()


def main():
    # Example usage
    calibration = PersonalityCalibration()

    # Add some example interview responses
    calibration.add_interview_response(
        "sensory_preferences",
        "I find bright lights and loud noises overwhelming, but I love certain textures"
    )

    calibration.add_interview_response(
        "cognitive_style",
        "I'm extremely detail-oriented and can spot patterns that others miss. " +
        "I have an intense passion for programming and can focus on it for hours"
    )

    calibration.add_interview_response(
        "social_interaction",
        "Social situations can be exhausting, especially when I have to maintain small talk. " +
        "I often have to consciously think about body language"
    )

    # Get and display personality snapshot
    snapshot = calibration.get_personality_snapshot()
    print("\nPersonality Snapshot:")
    print(json.dumps(snapshot, indent=2))


if __name__ == "__main__":
    main()
