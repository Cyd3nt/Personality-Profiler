import random
from datetime import datetime, timedelta
from typing import Dict

from human_personality_model import PersonalityInterviewer, PersonalityVector, BehavioralResponse
from personality_calibration import PersonalityCalibration


class SyntheticPersonalityGenerator:
    def __init__(self):
        self.personality_types = {
            "analytical": {
                "openness": (0.6, 0.8),
                "conscientiousness": (0.7, 0.9),
                "extraversion": (0.3, 0.5),
                "agreeableness": (0.4, 0.6),
                "neuroticism": (0.2, 0.4),
                "verbal_expressiveness": (0.4, 0.6),
                "analytical_tendency": (0.8, 1.0),
                "social_energy": (0.3, 0.5),
                "learning_style": "systematic",
                "problem_solving": "methodical",
                "stress_response": "analytical"
            },
            "empathetic": {
                "openness": (0.5, 0.7),
                "conscientiousness": (0.6, 0.8),
                "extraversion": (0.6, 0.8),
                "agreeableness": (0.8, 1.0),
                "neuroticism": (0.3, 0.5),
                "verbal_expressiveness": (0.7, 0.9),
                "analytical_tendency": (0.4, 0.6),
                "social_energy": (0.7, 0.9),
                "learning_style": "collaborative",
                "problem_solving": "people-oriented",
                "stress_response": "supportive"
            },
            "creative": {
                "openness": (0.8, 1.0),
                "conscientiousness": (0.4, 0.6),
                "extraversion": (0.5, 0.7),
                "agreeableness": (0.5, 0.7),
                "neuroticism": (0.4, 0.6),
                "verbal_expressiveness": (0.7, 0.9),
                "analytical_tendency": (0.5, 0.7),
                "social_energy": (0.6, 0.8),
                "learning_style": "experiential",
                "problem_solving": "innovative",
                "stress_response": "adaptive"
            },
            "pragmatic": {
                "openness": (0.4, 0.6),
                "conscientiousness": (0.7, 0.9),
                "extraversion": (0.4, 0.6),
                "agreeableness": (0.5, 0.7),
                "neuroticism": (0.2, 0.4),
                "verbal_expressiveness": (0.5, 0.7),
                "analytical_tendency": (0.6, 0.8),
                "social_energy": (0.4, 0.6),
                "learning_style": "practical",
                "problem_solving": "efficient",
                "stress_response": "solution-focused"
            },
            "visionary": {
                "openness": (0.8, 1.0),
                "conscientiousness": (0.5, 0.7),
                "extraversion": (0.6, 0.8),
                "agreeableness": (0.6, 0.8),
                "neuroticism": (0.3, 0.5),
                "verbal_expressiveness": (0.8, 1.0),
                "analytical_tendency": (0.6, 0.8),
                "social_energy": (0.7, 0.9),
                "learning_style": "conceptual",
                "problem_solving": "strategic",
                "stress_response": "inspiring"
            },
            "adaptive": {
                "openness": (0.6, 0.8),
                "conscientiousness": (0.5, 0.7),
                "extraversion": (0.5, 0.7),
                "agreeableness": (0.7, 0.9),
                "neuroticism": (0.3, 0.5),
                "verbal_expressiveness": (0.6, 0.8),
                "analytical_tendency": (0.5, 0.7),
                "social_energy": (0.5, 0.7),
                "learning_style": "flexible",
                "problem_solving": "adaptable",
                "stress_response": "resilient"
            }
        }

        self.response_templates = {
            "openness": {
                "high": [
                    "I love exploring new ideas and experiences! I'm always eager to try something different.",
                    "Change excites me - it's an opportunity to learn and grow.",
                    "I actively seek out novel perspectives and creative solutions."
                ],
                "low": [
                    "I prefer sticking to what I know works well.",
                    "I'm cautious about new experiences and like to thoroughly research first.",
                    "I value tradition and proven methods over experimental approaches."
                ]
            },
            "social_behavior": {
                "extroverted": [
                    "I thrive in group settings and love organizing social events.",
                    "My ideal evening involves spending time with friends and meeting new people.",
                    "I get energized by social interactions and collaborative activities."
                ],
                "introverted": [
                    "I prefer small, intimate gatherings with close friends.",
                    "I need quiet time to recharge after social interactions.",
                    "I'm most productive when working independently in a calm environment."
                ]
            },
            "decision_making": {
                "analytical": [
                    "I carefully analyze all available data before making decisions.",
                    "I create pros and cons lists and evaluate multiple scenarios.",
                    "I prefer having complete information and time to process options."
                ],
                "intuitive": [
                    "I often trust my gut feeling when making decisions.",
                    "I can quickly assess situations and make effective choices.",
                    "I consider both emotional and logical factors in my decisions."
                ]
            }
        }

    def generate_random_trait_value(self, range_tuple: tuple) -> float:
        return random.uniform(range_tuple[0], range_tuple[1])

    def generate_personality_vector(self, personality_type: str) -> PersonalityVector:
        traits = self.personality_types[personality_type]
        return PersonalityVector(
            openness=self.generate_random_trait_value(traits["openness"]),
            conscientiousness=self.generate_random_trait_value(traits["conscientiousness"]),
            extraversion=self.generate_random_trait_value(traits["extraversion"]),
            agreeableness=self.generate_random_trait_value(traits["agreeableness"]),
            neuroticism=self.generate_random_trait_value(traits["neuroticism"]),
            adaptability=random.uniform(0.4, 0.8),
            resilience=random.uniform(0.5, 0.9),
            verbal_expressiveness=self.generate_random_trait_value(traits["verbal_expressiveness"]),
            listening_style=random.uniform(0.4, 0.9),
            conflict_handling=random.uniform(0.3, 0.8),
            risk_tolerance=random.uniform(0.2, 0.8),
            decision_speed=random.uniform(0.3, 0.9),
            analytical_tendency=self.generate_random_trait_value(traits["analytical_tendency"]),
            social_energy=self.generate_random_trait_value(traits["social_energy"]),
            leadership_tendency=random.uniform(0.3, 0.8),
            empathy=random.uniform(0.4, 0.9),
            achievement_drive=random.uniform(0.5, 0.9),
            growth_mindset=random.uniform(0.4, 0.9),
            helping_tendency=random.uniform(0.4, 0.9)
        )

    def generate_interview_response(self, question_category: str, personality_type: str) -> str:
        if question_category == "openness":
            templates = self.response_templates["openness"][
                "high" if self.personality_types[personality_type]["openness"][0] > 0.6 else "low"]
        elif question_category == "social_behavior":
            templates = self.response_templates["social_behavior"][
                "extroverted" if self.personality_types[personality_type]["extraversion"][0] > 0.6 else "introverted"]
        elif question_category == "decision_making":
            templates = self.response_templates["decision_making"][
                "analytical" if self.personality_types[personality_type]["analytical_tendency"][
                                    0] > 0.6 else "intuitive"]
        else:
            templates = self.response_templates["openness"]["high"]  # fallback

        return random.choice(templates)

    def generate_behavioral_response(self, personality_type: str) -> BehavioralResponse:
        situations = [
            {
                "type": "team_conflict",
                "scenario": "Team conflict resolution",
                "context": {
                    "severity": random.uniform(0.3, 0.8),
                    "stakeholders": ["team_members", "project_lead"],
                    "project_phase": "development",
                    "time_pressure": random.uniform(0.4, 0.9)
                }
            },
            {
                "type": "project_pressure",
                "scenario": "Project deadline pressure",
                "context": {
                    "deadline_proximity": random.uniform(0.7, 1.0),
                    "resource_constraints": random.uniform(0.4, 0.8),
                    "stakeholder_expectations": random.uniform(0.6, 0.9),
                    "team_morale": random.uniform(0.3, 0.7)
                }
            },
            {
                "type": "change_management",
                "scenario": "Unexpected change in requirements",
                "context": {
                    "change_magnitude": random.uniform(0.5, 1.0),
                    "available_time": random.uniform(0.2, 0.6),
                    "team_readiness": random.uniform(0.4, 0.8),
                    "business_impact": random.uniform(0.6, 0.9)
                }
            },
            {
                "type": "client_interaction",
                "scenario": "Client presentation feedback",
                "context": {
                    "client_satisfaction": random.uniform(0.3, 0.9),
                    "presentation_complexity": random.uniform(0.5, 0.8),
                    "stakeholder_level": random.uniform(0.6, 1.0),
                    "follow_up_required": random.uniform(0.4, 0.9)
                }
            },
            {
                "type": "innovation_challenge",
                "scenario": "Technical innovation opportunity",
                "context": {
                    "innovation_potential": random.uniform(0.6, 1.0),
                    "technical_complexity": random.uniform(0.7, 0.9),
                    "resource_availability": random.uniform(0.3, 0.7),
                    "risk_level": random.uniform(0.4, 0.8)
                }
            }
        ]

        responses = {
            "analytical": [
                {"action": "Analyzed the situation systematically", "effectiveness": (0.7, 0.9)},
                {"action": "Gathered data to inform decision", "effectiveness": (0.8, 0.95)},
                {"action": "Created a structured approach", "effectiveness": (0.75, 0.9)}
            ],
            "empathetic": [
                {"action": "Focused on team harmony", "effectiveness": (0.8, 0.95)},
                {"action": "Listened to all perspectives", "effectiveness": (0.85, 1.0)},
                {"action": "Found collaborative solutions", "effectiveness": (0.75, 0.9)}
            ],
            "creative": [
                {"action": "Proposed innovative solutions", "effectiveness": (0.7, 0.9)},
                {"action": "Explored alternative approaches", "effectiveness": (0.75, 0.95)},
                {"action": "Adapted flexibly to changes", "effectiveness": (0.8, 0.9)}
            ],
            "pragmatic": [
                {"action": "Prioritized tasks efficiently", "effectiveness": (0.8, 0.95)},
                {"action": "Managed resources effectively", "effectiveness": (0.75, 0.9)},
                {"action": "Minimized risks and maximized benefits", "effectiveness": (0.7, 0.85)}
            ],
            "visionary": [
                {"action": "Developed a strategic plan", "effectiveness": (0.75, 0.9)},
                {"action": "Inspired team members", "effectiveness": (0.8, 0.95)},
                {"action": "Encouraged creative thinking", "effectiveness": (0.7, 0.9)}
            ],
            "adaptive": [
                {"action": "Adjusted to changing circumstances", "effectiveness": (0.8, 0.95)},
                {"action": "Remained calm under pressure", "effectiveness": (0.75, 0.9)},
                {"action": "Found opportunities in challenges", "effectiveness": (0.7, 0.85)}
            ]
        }

        situation = random.choice(situations)
        response_data = random.choice(responses[personality_type])
        effectiveness = random.uniform(*response_data["effectiveness"])

        emotional_state = self._generate_emotional_state(
            personality_type,
            situation["type"],
            effectiveness
        )

        return BehavioralResponse(
            situation=situation["scenario"],
            response=response_data["action"],
            emotional_state=emotional_state,
            timestamp=datetime.now() - timedelta(days=random.randint(1, 30)),
            context={
                "location": "workplace",
                "participants": ["team_members", "stakeholders"],
                "project_phase": "development",
                "situation_type": situation["type"],
                "situation_context": situation["context"],
                "response_effectiveness": effectiveness
            }
        )

    def _generate_emotional_state(self, personality_type: str, situation_type: str, effectiveness: float) -> Dict[
        str, float]:
        """Generate emotional state based on personality type and situation"""
        base_emotions = {
            "stress": random.uniform(0.3, 0.7),
            "confidence": random.uniform(0.4, 0.8),
            "engagement": random.uniform(0.5, 0.9),
            "satisfaction": effectiveness,
            "energy": random.uniform(0.4, 0.8)
        }

        # Adjust emotions based on personality type
        if personality_type == "analytical":
            base_emotions["stress"] *= 0.8  # Lower stress due to systematic approach
            base_emotions["confidence"] *= 1.2  # Higher confidence in analysis
        elif personality_type == "empathetic":
            base_emotions["engagement"] *= 1.2  # Higher engagement with others
            base_emotions["energy"] *= 0.9  # Slightly lower energy due to emotional investment
        elif personality_type == "creative":
            base_emotions["confidence"] *= 1.1  # Higher confidence in creative solutions
            base_emotions["stress"] *= 0.9  # Lower stress due to adaptability
        elif personality_type == "pragmatic":
            base_emotions["stress"] *= 0.7  # Lower stress due to practical approach
            base_emotions["satisfaction"] *= 1.1  # Higher satisfaction with concrete results
        elif personality_type == "visionary":
            base_emotions["engagement"] *= 1.3  # Higher engagement with possibilities
            base_emotions["energy"] *= 1.2  # Higher energy from inspiration
        elif personality_type == "adaptive":
            base_emotions["stress"] *= 0.6  # Much lower stress due to adaptability
            base_emotions["confidence"] *= 1.1  # Higher confidence in handling change

        # Adjust emotions based on situation type
        if situation_type == "team_conflict":
            base_emotions["stress"] *= 1.2
            base_emotions["energy"] *= 0.9
        elif situation_type == "project_pressure":
            base_emotions["stress"] *= 1.3
            base_emotions["engagement"] *= 1.1
        elif situation_type == "change_management":
            base_emotions["confidence"] *= 0.9
            base_emotions["engagement"] *= 1.2
        elif situation_type == "client_interaction":
            base_emotions["stress"] *= 1.1
            base_emotions["energy"] *= 1.1
        elif situation_type == "innovation_challenge":
            base_emotions["engagement"] *= 1.2
            base_emotions["confidence"] *= 1.1

        # Normalize values to 0-1 range
        for emotion in base_emotions:
            base_emotions[emotion] = min(1.0, max(0.0, base_emotions[emotion]))

        return base_emotions


def generate_synthetic_dataset(num_personalities: int = 5):
    generator = SyntheticPersonalityGenerator()
    personality_types = list(generator.personality_types.keys())
    dataset = []

    for _ in range(num_personalities):
        personality_type = random.choice(personality_types)
        vector = generator.generate_personality_vector(personality_type)

        personality_data = {
            "type": personality_type,
            "vector": {
                attr: getattr(vector, attr)
                for attr in dir(vector)
                if not attr.startswith('_') and isinstance(getattr(vector, attr), (int, float, str, dict))
            },
            "interview_responses": {},
            "behavioral_responses": []
        }

        # Generate interview responses
        interviewer = PersonalityInterviewer()
        for category, questions in interviewer.questions.items():
            personality_data["interview_responses"][category] = [
                generator.generate_interview_response(category, personality_type)
                for _ in questions
            ]

        # Generate behavioral responses
        for _ in range(5):  # 5 behavioral observations per personality
            behavior = generator.generate_behavioral_response(personality_type)
            personality_data["behavioral_responses"].append({
                "situation": behavior.situation,
                "response": behavior.response,
                "emotional_state": behavior.emotional_state,
                "timestamp": behavior.timestamp.isoformat(),
                "context": behavior.context
            })

        dataset.append(personality_data)

    return dataset


def main():
    print("Generating synthetic personality dataset...")
    dataset = generate_synthetic_dataset()

    print("\nGenerated Personalities:")
    for i, personality in enumerate(dataset, 1):
        print(f"\nPersonality {i} ({personality['type']}):")
        print("Sample interview responses:")
        for category, responses in list(personality['interview_responses'].items())[:2]:
            print(f"  {category}: {responses[0]}")
        print("Sample behavioral response:")
        print(f"  Situation: {personality['behavioral_responses'][0].situation}")
        print(f"  Response: {personality['behavioral_responses'][0].response}")

        # Initialize calibration with synthetic data
        calibration = PersonalityCalibration()
        for category, responses in personality['interview_responses'].items():
            for i, response in enumerate(responses):
                calibration.add_interview_response(f"{category}_{i}", response)

        for behavior in personality['behavioral_responses']:
            calibration.add_behavioral_observation(
                context=behavior.situation,
                behavior=behavior.response,
                timestamp=behavior.timestamp,
                emotional_state=behavior.emotional_state
            )

        # Generate and print confidence scores
        calibration._calculate_confidence_scores()
        print("\nConfidence Scores:")
        for trait, score in list(calibration.confidence_scores.items())[:3]:
            print(f"  {trait}: {score:.2f}")


if __name__ == "__main__":
    main()
