import random
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class DialogueContext:
    topic: str
    mood: str
    formality_level: float
    previous_exchanges: List[Tuple[str, str]]
    speaker_role: str
    listener_role: str


class DialoguePatternLibrary:
    def __init__(self):
        self.patterns = {
            "empathetic_response": [
                "I understand how {emotion} that must make you feel.",
                "It sounds like you're feeling {emotion} about this.",
                "That must be really {emotion} for you.",
                "I can sense that this is {emotion} for you."
            ],
            "intellectual_discourse": [
                "That's an intriguing perspective. Have you considered {alternative}?",
                "Your point about {topic} reminds me of {connection}.",
                "This relates interestingly to {concept} in {field}.",
                "Let's explore the implications of {idea}."
            ],
            "emotional_support": [
                "I'm here to support you through this {situation}.",
                "It's perfectly normal to feel {emotion} in this situation.",
                "Would you like to talk more about how you're feeling?",
                "Your feelings about {topic} are valid and important."
            ],
            "problem_solving": [
                "What if we approached {problem} from {perspective}?",
                "Have you tried {solution} when dealing with {issue}?",
                "Let's break down {problem} into smaller steps.",
                "What would be the ideal outcome for {situation}?"
            ],
            "social_bonding": [
                "I've had similar experiences with {topic}.",
                "It's wonderful how {positive_aspect} brings people together.",
                "I really appreciate you sharing this with me.",
                "Your perspective on {topic} adds so much to our conversation."
            ]
        }

        self.transitions = {
            "topic_shift": [
                "Speaking of {new_topic}...",
                "That reminds me of something about {new_topic}...",
                "This relates to {new_topic} in an interesting way...",
                "Your point about {current_topic} makes me think about {new_topic}..."
            ],
            "emotional_shift": [
                "While that's {current_emotion}, there's also {new_emotion}...",
                "I understand the {current_emotion}, and yet...",
                "Looking at the {new_emotion} side of things...",
                "Balancing the {current_emotion} with {new_emotion}..."
            ],
            "perspective_shift": [
                "From another angle...",
                "Consider this perspective...",
                "Looking at it differently...",
                "Here's another way to think about it..."
            ]
        }

        self.meta_patterns = {
            "self_reflection": [
                "I notice I'm feeling {emotion} as we discuss this.",
                "This conversation is making me reflect on {topic}.",
                "I'm curious about my reaction to {topic}.",
                "I'm learning a lot about {topic} from our discussion."
            ],
            "relationship_building": [
                "I value your perspective on {topic}.",
                "Our conversations about {topic} are always enlightening.",
                "I appreciate how you {positive_action}.",
                "Thank you for sharing your thoughts on {topic}."
            ]
        }


class AdvancedDialogueGenerator:
    def __init__(self):
        self.pattern_library = DialoguePatternLibrary()
        self.conversation_memory = defaultdict(list)
        self.topic_transitions = {}
        self.emotional_states = []

    def generate_response(self,
                          input_text: str,
                          context: DialogueContext,
                          personality_vector: Dict[str, float]) -> str:
        """Generate a sophisticated response based on context and personality"""
        # Analyze input
        topics = self._extract_topics(input_text)
        emotional_tone = self._analyze_emotional_tone(input_text)

        # Select response strategy
        strategy = self._select_response_strategy(
            emotional_tone,
            personality_vector,
            context
        )

        # Generate base response
        base_response = self._generate_base_response(strategy, topics, context)

        # Enhance response
        enhanced_response = self._enhance_response(
            base_response,
            personality_vector,
            context
        )

        # Add meta-communication if appropriate
        final_response = self._add_meta_communication(
            enhanced_response,
            context,
            personality_vector
        )

        return final_response

    def _extract_topics(self, text: str) -> List[str]:
        """Extract main topics from text using keyword analysis"""
        # Simplified topic extraction - could be enhanced with NLP
        important_words = [word.lower() for word in text.split()
                           if len(word) > 3 and word.isalnum()]
        return list(set(important_words))

    def _analyze_emotional_tone(self, text: str) -> Dict[str, float]:
        """Analyze emotional tone of text"""
        emotions = {
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "interest": 0.0
        }

        # Simple keyword-based emotion detection
        emotion_keywords = {
            "joy": {"happy", "joy", "excited", "wonderful", "great"},
            "sadness": {"sad", "unhappy", "depressed", "down", "blue"},
            "anger": {"angry", "mad", "frustrated", "annoyed", "upset"},
            "fear": {"afraid", "scared", "worried", "anxious", "nervous"},
            "surprise": {"surprised", "shocked", "amazed", "unexpected"},
            "interest": {"interesting", "curious", "fascinated", "intrigued"}
        }

        words = text.lower().split()
        for emotion, keywords in emotion_keywords.items():
            emotion_count = sum(1 for word in words if word in keywords)
            emotions[emotion] = emotion_count / (len(words) + 1)  # Normalize

        return emotions

    def _select_response_strategy(self,
                                  emotional_tone: Dict[str, float],
                                  personality: Dict[str, float],
                                  context: DialogueContext) -> str:
        """Select appropriate response strategy based on context"""
        # Determine dominant emotion
        dominant_emotion = max(emotional_tone.items(), key=lambda x: x[1])[0]

        # Consider personality traits
        if personality["empathy"] > 0.7 and any(v > 0.3 for v in emotional_tone.values()):
            return "empathetic_response"
        elif personality["analytical_tendency"] > 0.7:
            return "intellectual_discourse"
        elif dominant_emotion in ["sadness", "fear"]:
            return "emotional_support"
        elif personality["problem_solving"] > 0.7:
            return "problem_solving"
        else:
            return "social_bonding"

    def _generate_base_response(self,
                                strategy: str,
                                topics: List[str],
                                context: DialogueContext) -> str:
        """Generate base response using selected strategy"""
        pattern = random.choice(self.pattern_library.patterns[strategy])

        # Fill in template with relevant information
        filled_pattern = pattern.format(
            emotion=context.mood,
            topic=topics[0] if topics else "this",
            alternative="a different approach",
            connection="a related concept",
            concept="an interesting idea",
            field="this area",
            idea="this thought",
            situation="experience",
            problem="the challenge",
            perspective="a new angle",
            solution="an alternative approach",
            issue="this situation",
            positive_aspect="this shared experience"
        )

        return filled_pattern

    def _enhance_response(self,
                          base_response: str,
                          personality: Dict[str, float],
                          context: DialogueContext) -> str:
        """Enhance response based on personality and context"""
        enhanced = base_response

        # Add personality-specific modifications
        if personality["verbal_expressiveness"] > 0.7:
            enhanced += " " + random.choice([
                "I find this particularly fascinating!",
                "This really captures my interest.",
                "What an engaging topic!"
            ])

        # Adjust formality
        if context.formality_level > 0.7:
            enhanced = enhanced.replace("thing", "matter")
            enhanced = enhanced.replace("get", "obtain")
            enhanced = enhanced.replace("about", "regarding")

        return enhanced

    def _add_meta_communication(self,
                                response: str,
                                context: DialogueContext,
                                personality: Dict[str, float]) -> str:
        """Add meta-communication elements if appropriate"""
        if personality["self_awareness"] > 0.7 and random.random() < 0.3:
            meta_pattern = random.choice(
                self.pattern_library.meta_patterns["self_reflection"]
            )
            response += " " + meta_pattern.format(
                emotion="thoughtful",
                topic=context.topic,
                positive_action="share your insights"
            )

        return response


def main():
    # Example usage
    generator = AdvancedDialogueGenerator()

    # Sample context
    context = DialogueContext(
        topic="artificial intelligence",
        mood="curious",
        formality_level=0.7,
        previous_exchanges=[],
        speaker_role="advisor",
        listener_role="learner"
    )

    # Sample personality
    personality = {
        "empathy": 0.8,
        "analytical_tendency": 0.7,
        "verbal_expressiveness": 0.9,
        "self_awareness": 0.8,
        "problem_solving": 0.7
    }

    # Generate response
    response = generator.generate_response(
        "I'm fascinated by how AI might change our future.",
        context,
        personality
    )

    print("Generated Response:", response)


if __name__ == "__main__":
    main()
