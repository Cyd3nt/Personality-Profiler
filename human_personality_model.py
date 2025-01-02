import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class PersonalityVector:
    # Core personality traits (Big Five + additional dimensions)
    openness: float
    conscientiousness: float
    extraversion: float
    agreeableness: float
    neuroticism: float
    adaptability: float
    resilience: float

    # Communication style
    verbal_expressiveness: float
    listening_style: float
    conflict_handling: float

    # Decision making
    risk_tolerance: float
    decision_speed: float
    analytical_tendency: float

    # Social patterns
    social_energy: float
    leadership_tendency: float
    empathy: float

    # Values and motivations
    achievement_drive: float
    growth_mindset: float
    helping_tendency: float

    def to_vector(self) -> np.ndarray:
        return np.array([
            self.openness, self.conscientiousness, self.extraversion,
            self.agreeableness, self.neuroticism, self.adaptability,
            self.resilience, self.verbal_expressiveness, self.listening_style,
            self.conflict_handling, self.risk_tolerance, self.decision_speed,
            self.analytical_tendency, self.social_energy, self.leadership_tendency,
            self.empathy, self.achievement_drive, self.growth_mindset,
            self.helping_tendency
        ])


@dataclass
class BehavioralResponse:
    situation: str
    response: str
    emotional_state: Dict[str, float]
    timestamp: datetime
    context: Dict[str, str]


class PersonalityInterviewer:
    def __init__(self):
        self.questions = self._load_interview_questions()
        self.responses: List[Tuple[str, str]] = []
        self.behavioral_observations: List[BehavioralResponse] = []
        self.personality_vector: Optional[PersonalityVector] = None

    def _load_interview_questions(self) -> Dict[str, List[str]]:
        """Load structured interview questions for personality assessment"""
        return {
            "openness": [
                "How do you typically react to new ideas or experiences?",
                "What's your approach to trying new things?",
                "How important is creativity in your daily life?"
            ],
            "social_behavior": [
                "How do you prefer to spend your free time?",
                "What's your ideal social gathering like?",
                "How do you handle conflicts with others?"
            ],
            "decision_making": [
                "Can you describe your process for making important decisions?",
                "How do you handle uncertainty?",
                "What factors do you consider when taking risks?"
            ],
            "emotional_patterns": [
                "How do you typically handle stress?",
                "What brings you the most joy in life?",
                "How do you process difficult emotions?"
            ],
            "behavioral_scenarios": [
                "How would you handle a situation where someone disagrees with you strongly?",
                "What would you do if you found someone's lost wallet?",
                "How would you react to an unexpected change in plans?"
            ]
        }

    def conduct_interview(self, response_callback) -> None:
        """Conduct an interactive interview to gather personality data"""
        print("\nPersonality Assessment Interview")
        print("================================")

        for category, questions in self.questions.items():
            print(f"\n{category.replace('_', ' ').title()} Assessment:")
            for question in questions:
                response = response_callback(question)
                self.responses.append((question, response))
                self._analyze_response(category, response)

    def _analyze_response(self, category: str, response: str) -> None:
        """Analyze interview responses to build personality profile"""
        # Sentiment analysis of response
        sentiment_score = self._calculate_sentiment(response)

        # Extract behavioral indicators
        behavioral_indicators = self._extract_behavioral_indicators(response)

        # Record behavioral response
        self.behavioral_observations.append(
            BehavioralResponse(
                situation=category,
                response=response,
                emotional_state={"valence": sentiment_score},
                timestamp=datetime.now(),
                context=behavioral_indicators
            )
        )

    def _calculate_sentiment(self, text: str) -> float:
        """Simple sentiment analysis (replace with more sophisticated NLP)"""
        positive_words = {'happy', 'good', 'great', 'excellent', 'positive', 'enjoy', 'love'}
        negative_words = {'sad', 'bad', 'terrible', 'negative', 'hate', 'dislike', 'angry'}

        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        if positive_count + negative_count == 0:
            return 0.0
        return (positive_count - negative_count) / (positive_count + negative_count)

    def _extract_behavioral_indicators(self, text: str) -> Dict[str, str]:
        """Extract behavioral indicators from response"""
        indicators = {
            "decision_style": self._analyze_decision_style(text),
            "social_orientation": self._analyze_social_orientation(text),
            "emotional_expression": self._analyze_emotional_expression(text)
        }
        return indicators

    def _analyze_decision_style(self, text: str) -> str:
        analytical_keywords = {'think', 'analyze', 'consider', 'evaluate', 'plan'}
        intuitive_keywords = {'feel', 'sense', 'intuition', 'gut', 'instinct'}

        words = text.lower().split()
        analytical_count = sum(1 for word in words if word in analytical_keywords)
        intuitive_count = sum(1 for word in words if word in intuitive_keywords)

        if analytical_count > intuitive_count:
            return "analytical"
        elif intuitive_count > analytical_count:
            return "intuitive"
        return "balanced"

    def _analyze_social_orientation(self, text: str) -> str:
        extroverted_keywords = {'people', 'social', 'together', 'group', 'talk'}
        introverted_keywords = {'alone', 'quiet', 'private', 'space', 'solitude'}

        words = text.lower().split()
        extroverted_count = sum(1 for word in words if word in extroverted_keywords)
        introverted_count = sum(1 for word in words if word in introverted_keywords)

        if extroverted_count > introverted_count:
            return "extroverted"
        elif introverted_count > extroverted_count:
            return "introverted"
        return "ambivert"

    def _analyze_emotional_expression(self, text: str) -> str:
        emotional_keywords = {'feel', 'emotion', 'happy', 'sad', 'angry'}
        rational_keywords = {'think', 'logical', 'rational', 'reason', 'analyze'}

        words = text.lower().split()
        emotional_count = sum(1 for word in words if word in emotional_keywords)
        rational_count = sum(1 for word in words if word in rational_keywords)

        if emotional_count > rational_count:
            return "emotionally_expressive"
        elif rational_count > emotional_count:
            return "rationally_focused"
        return "balanced"

    def generate_personality_vector(self) -> PersonalityVector:
        """Generate personality vector from interview responses and observations"""
        trait_scores = defaultdict(list)

        # Analyze behavioral observations
        for observation in self.behavioral_observations:
            # Decision making style
            if observation.context["decision_style"] == "analytical":
                trait_scores["analytical_tendency"].append(0.8)
                trait_scores["risk_tolerance"].append(0.4)
            elif observation.context["decision_style"] == "intuitive":
                trait_scores["analytical_tendency"].append(0.3)
                trait_scores["risk_tolerance"].append(0.7)

            # Social orientation
            if observation.context["social_orientation"] == "extroverted":
                trait_scores["extraversion"].append(0.8)
                trait_scores["social_energy"].append(0.8)
            elif observation.context["social_orientation"] == "introverted":
                trait_scores["extraversion"].append(0.3)
                trait_scores["social_energy"].append(0.3)

            # Emotional expression
            if observation.context["emotional_expression"] == "emotionally_expressive":
                trait_scores["empathy"].append(0.8)
                trait_scores["verbal_expressiveness"].append(0.8)
            elif observation.context["emotional_expression"] == "rationally_focused":
                trait_scores["analytical_tendency"].append(0.8)
                trait_scores["verbal_expressiveness"].append(0.4)

        # Calculate average scores
        def avg_score(trait: str, default: float = 0.5) -> float:
            scores = trait_scores.get(trait, [])
            return sum(scores) / len(scores) if scores else default

        self.personality_vector = PersonalityVector(
            openness=avg_score("openness"),
            conscientiousness=avg_score("conscientiousness"),
            extraversion=avg_score("extraversion"),
            agreeableness=avg_score("agreeableness"),
            neuroticism=avg_score("neuroticism"),
            adaptability=avg_score("adaptability"),
            resilience=avg_score("resilience"),
            verbal_expressiveness=avg_score("verbal_expressiveness"),
            listening_style=avg_score("listening_style"),
            conflict_handling=avg_score("conflict_handling"),
            risk_tolerance=avg_score("risk_tolerance"),
            decision_speed=avg_score("decision_speed"),
            analytical_tendency=avg_score("analytical_tendency"),
            social_energy=avg_score("social_energy"),
            leadership_tendency=avg_score("leadership_tendency"),
            empathy=avg_score("empathy"),
            achievement_drive=avg_score("achievement_drive"),
            growth_mindset=avg_score("growth_mindset"),
            helping_tendency=avg_score("helping_tendency")
        )

        return self.personality_vector

    def save_personality_profile(self, filename: str) -> None:
        """Save the complete personality profile to a file"""
        if not self.personality_vector:
            raise ValueError("Personality vector not generated yet")

        profile = {
            "personality_vector": {
                k: v for k, v in self.personality_vector.__dict__.items()
            },
            "behavioral_observations": [
                {
                    "situation": obs.situation,
                    "response": obs.response,
                    "emotional_state": obs.emotional_state,
                    "timestamp": obs.timestamp.isoformat(),
                    "context": obs.context
                }
                for obs in self.behavioral_observations
            ],
            "interview_responses": self.responses
        }

        with open(filename, 'w') as f:
            json.dump(profile, f, indent=2)

    def load_personality_profile(self, filename: str) -> None:
        """Load a personality profile from a file"""
        with open(filename, 'r') as f:
            profile = json.load(f)

        self.personality_vector = PersonalityVector(**profile["personality_vector"])

        self.behavioral_observations = [
            BehavioralResponse(
                situation=obs["situation"],
                response=obs["response"],
                emotional_state=obs["emotional_state"],
                timestamp=datetime.fromisoformat(obs["timestamp"]),
                context=obs["context"]
            )
            for obs in profile["behavioral_observations"]
        ]

        self.responses = profile["interview_responses"]


def interactive_interview():
    """Run an interactive interview session"""
    interviewer = PersonalityInterviewer()

    def get_user_response(question: str) -> str:
        print(f"\nQ: {question}")
        return input("A: ")

    interviewer.conduct_interview(get_user_response)
    personality_vector = interviewer.generate_personality_vector()

    print("\nPersonality Profile Generated:")
    for trait, value in personality_vector.__dict__.items():
        print(f"{trait.replace('_', ' ').title()}: {value:.2f}")

    # Save the profile
    interviewer.save_personality_profile("personality_profile.json")
    print("\nProfile saved to personality_profile.json")


if __name__ == "__main__":
    interactive_interview()
