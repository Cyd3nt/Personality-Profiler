import json
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np


class AdaptiveQuestionGenerator:
    def __init__(self):
        self.question_templates = {
            "high_score": [
                "Given your strong {trait}, how do you handle situations where {scenario}?",
                "Your responses indicate high {trait}. Can you describe a time when {scenario}?",
                "With your elevated {trait}, what strategies do you use when {scenario}?",
                "How does your high level of {trait} influence your approach to {scenario}?",
                "Considering your strong {trait}, how would you react if {scenario}?"
            ],
            "low_score": [
                "With your more reserved {trait}, how do you approach situations where {scenario}?",
                "Given your measured {trait}, what challenges do you face when {scenario}?",
                "How do you compensate when your lower {trait} affects {scenario}?",
                "What strategies help you manage situations requiring {trait} when {scenario}?",
                "How does your moderate level of {trait} impact your response to {scenario}?"
            ],
            "mixed_score": [
                "How does the combination of your {trait1} and {trait2} influence {scenario}?",
                "When facing {scenario}, how do you balance your {trait1} with your {trait2}?",
                "Given your contrasting {trait1} and {trait2}, how do you handle {scenario}?",
                "How do your {trait1} and {trait2} work together when you {scenario}?",
                "What strategies do you use to leverage both {trait1} and {trait2} in {scenario}?"
            ]
        }

        self.scenario_templates = {
            "moral_fairness": [
                "you need to make a decision that affects multiple people differently",
                "you witness unfair treatment of others",
                "you must distribute limited resources",
                "you face a conflict between equality and efficiency",
                "you need to balance competing interests"
            ],
            "moral_care": [
                "others are in need but helping comes at a personal cost",
                "you must choose between helping one person significantly or many people slightly",
                "you witness someone in emotional distress",
                "you need to balance self-care with caring for others",
                "you see someone struggling but they haven't asked for help"
            ],
            "moral_loyalty": [
                "group interests conflict with personal values",
                "you must choose between loyalty to different groups",
                "your group makes a decision you disagree with",
                "maintaining loyalty requires personal sacrifice",
                "you discover misconduct within your group"
            ],
            "moral_authority": [
                "authority figures make questionable decisions",
                "rules conflict with what you believe is right",
                "you must choose between following protocol and achieving better results",
                "traditional practices seem outdated or harmful",
                "you disagree with established hierarchies"
            ],
            "moral_sanctity": [
                "cultural traditions conflict with modern values",
                "you must compromise on personal principles",
                "sacred values are challenged by practical needs",
                "you face pressure to violate your moral standards",
                "others disrespect what you consider sacred"
            ],
            "moral_responsibility": [
                "taking responsibility might harm your interests",
                "you must choose between different obligations",
                "others fail to take responsibility for their actions",
                "you need to balance multiple commitments",
                "accepting blame could have serious consequences"
            ],
            "moral_honesty": [
                "telling the truth might hurt someone",
                "you discover others being dishonest",
                "being honest could damage relationships",
                "you face pressure to hide information",
                "complete honesty conflicts with loyalty"
            ],
            "moral_courage": [
                "standing up for beliefs risks personal consequences",
                "you witness wrongdoing by powerful people",
                "speaking up could harm your relationships",
                "you must choose between safety and doing right",
                "others pressure you to stay silent"
            ],
            "moral_wisdom": [
                "you face complex ethical dilemmas",
                "different moral principles conflict",
                "you must make decisions with incomplete information",
                "you need to balance short-term and long-term consequences",
                "cultural differences create ethical uncertainty"
            ],
            "moral_temperance": [
                "you face temptation to excess",
                "others pressure you to extremes",
                "moderation seems inadequate",
                "you must balance different needs",
                "restraint conflicts with immediate desires"
            ]
        }

    def generate_adaptive_questions(self, personality_scores: Dict[str, float],
                                    previous_responses: Dict[str, List[str]],
                                    num_questions: int = 50) -> List[Dict[str, str]]:
        """
        Generate adaptive questions based on personality scores and previous responses.
        
        Args:
            personality_scores: Dictionary of trait scores (0-1)
            previous_responses: Dictionary of previous question responses
            num_questions: Number of follow-up questions to generate
            
        Returns:
            List of generated questions with their categories
        """
        adaptive_questions = []

        # Find notable traits (high and low scores)
        high_traits = {k: v for k, v in personality_scores.items() if v >= 0.7}
        low_traits = {k: v for k, v in personality_scores.items() if v <= 0.3}

        # Generate single-trait questions
        for trait, score in high_traits.items():
            template = np.random.choice(self.question_templates["high_score"])
            scenario = np.random.choice(self.scenario_templates.get(trait, ["you face a challenging situation"]))
            question = template.format(trait=trait.replace("_", " "), scenario=scenario)
            adaptive_questions.append({"category": trait, "question": question, "type": "high_score"})

        for trait, score in low_traits.items():
            template = np.random.choice(self.question_templates["low_score"])
            scenario = np.random.choice(self.scenario_templates.get(trait, ["you face a challenging situation"]))
            question = template.format(trait=trait.replace("_", " "), scenario=scenario)
            adaptive_questions.append({"category": trait, "question": question, "type": "low_score"})

        # Generate questions about trait interactions
        trait_pairs = self._get_interesting_trait_pairs(personality_scores)
        for trait1, trait2 in trait_pairs:
            template = np.random.choice(self.question_templates["mixed_score"])
            scenario = np.random.choice(self.scenario_templates.get(trait1, ["you face a challenging situation"]))
            question = template.format(
                trait1=trait1.replace("_", " "),
                trait2=trait2.replace("_", " "),
                scenario=scenario
            )
            adaptive_questions.append({
                "category": f"{trait1}_{trait2}_interaction",
                "question": question,
                "type": "trait_interaction"
            })

        # Ensure we have enough questions
        while len(adaptive_questions) < num_questions:
            # Add more questions by mixing and matching traits and scenarios
            trait = np.random.choice(list(personality_scores.keys()))
            template = np.random.choice(self.question_templates["mixed_score"])
            scenario = np.random.choice(self.scenario_templates.get(trait, ["you face a challenging situation"]))
            other_trait = np.random.choice(list(personality_scores.keys()))

            question = template.format(
                trait1=trait.replace("_", " "),
                trait2=other_trait.replace("_", " "),
                scenario=scenario
            )
            adaptive_questions.append({
                "category": f"{trait}_{other_trait}_interaction",
                "question": question,
                "type": "supplementary"
            })

        return adaptive_questions[:num_questions]

    def _get_interesting_trait_pairs(self, personality_scores: Dict[str, float]) -> List[Tuple[str, str]]:
        """Find interesting pairs of traits based on scores."""
        pairs = []
        traits = list(personality_scores.keys())

        for i, trait1 in enumerate(traits):
            for trait2 in traits[i + 1:]:
                score1 = personality_scores[trait1]
                score2 = personality_scores[trait2]

                # Look for contrasting traits or strong correlations
                if abs(score1 - score2) > 0.4 or abs(score1 - score2) < 0.1:
                    pairs.append((trait1, trait2))

        return pairs[:10]  # Limit to top 10 most interesting pairs

    def save_adaptive_questions(self, questions: List[Dict[str, str]], session_id: str):
        """Save generated adaptive questions to a file."""
        output_dir = Path("output/adaptive_questions")
        output_dir.mkdir(exist_ok=True)

        filename = output_dir / f"adaptive_questions_{session_id}.json"
        with open(filename, 'w') as f:
            json.dump(questions, f, indent=4)

        return filename
