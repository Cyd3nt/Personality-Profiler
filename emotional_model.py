from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass
class EmotionalDimension:
    name: str
    value: float  # -1 to 1
    volatility: float  # How quickly this dimension changes
    persistence: float  # How long changes last


@dataclass
class EmotionalMemory:
    trigger: str
    emotion_state: Dict[str, float]
    intensity: float
    timestamp: datetime
    context: Dict[str, str]
    duration: float  # How long the emotional state lasted


class EmotionalCore:
    """Advanced emotional modeling system"""

    def __init__(self, personality: Dict[str, float]):
        """Initialize emotional core with personality traits"""
        self.personality = personality
        self.emotion_dimensions = ["valence", "arousal", "dominance"]

        # Initialize current emotional state
        self.current_state = {
            "valence": personality["optimism"],
            "arousal": personality["energy_level"],
            "dominance": personality["confidence"],
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "trust": 0.0,
            "surprise": 0.0,
            "emotional_stability": personality["emotional_stability"]
        }

        # Calculate baseline mood values
        self.mood_baseline = {
            "valence": personality["optimism"] * 0.7,
            "arousal": personality["energy_level"] * 0.5,
            "dominance": personality["confidence"] * 0.6
        }

        # Initialize regulation strategies
        self.regulation_strategies = {
            "reappraisal": personality["openness"],
            "suppression": personality["neuroticism"]
        }

        # Initialize emotional memory
        self.emotional_memory = []
        self.memory_capacity = 100
        self.last_response = None

    def _regulate_emotions(self, response: Dict[str, float]) -> Dict[str, float]:
        """Apply emotional regulation strategies based on personality"""
        regulated = response.copy()

        # Apply reappraisal (cognitive change)
        reappraisal_strength = self.regulation_strategies["reappraisal"]
        if reappraisal_strength > 0.5:
            # Reduce intensity of negative emotions
            for emotion in ["sadness", "anger", "fear"]:
                regulated[emotion] *= (1 - (reappraisal_strength - 0.5))
            # Enhance positive emotions slightly
            for emotion in ["joy", "trust"]:
                regulated[emotion] *= (1 + (reappraisal_strength - 0.5) * 0.5)

        # Apply suppression (response modulation)
        suppression_strength = self.regulation_strategies["suppression"]
        if suppression_strength > 0.5:
            # Reduce overall emotional expressivity
            for emotion in regulated:
                if emotion not in ["valence", "arousal", "dominance"]:
                    regulated[emotion] *= (1 - (suppression_strength - 0.5) * 0.7)

        # Ensure values stay within bounds
        for key in regulated:
            regulated[key] = max(-1.0, min(1.0, regulated[key]))

        return regulated

    def _update_emotional_state(self, response: Dict[str, float]) -> None:
        """Update current emotional state based on new response"""
        # Calculate emotional momentum (how much previous state influences current)
        stability = self.personality.get("emotional_stability", 0.5)
        momentum = 0.3 + (stability * 0.4)  # 0.3 to 0.7 based on stability

        # Update each emotion dimension
        for key in self.current_state:
            if key in response:
                self.current_state[key] = (momentum * self.current_state[key] +
                                           (1 - momentum) * response[key])

        # Store last response
        self.last_response = response.copy()

    def _store_emotional_memory(self, event: str, response: Dict[str, float], context: Dict[str, Any] = None,
                                intensity: float = 0.0) -> None:
        """Store emotional event in memory"""
        memory = EmotionalMemory(
            trigger=event,
            emotion_state=response,
            intensity=intensity,
            timestamp=datetime.now(),
            context=context or {},
            duration=0.0
        )
        self.emotional_memory.append(memory)
        if len(self.emotional_memory) > self.memory_capacity:
            self.emotional_memory.pop(0)

    def process_emotional_event(self, event: str, context: Dict[str, Any] = None, intensity: float = 0.8) -> Dict[
        str, float]:
        """Process an emotional event and return the emotional response
        
        Args:
            event: String describing the emotional event
            context: Optional context dictionary for the event
            intensity: Intensity of the emotional response (0.0 to 1.0)
            
        Returns:
            Dictionary containing emotional response values
            
        Raises:
            ValueError: If event is not a string or intensity is invalid
        """
        # Validate event
        if not isinstance(event, str):
            raise ValueError("Event must be a string")
        if not event.strip():
            raise ValueError("Event cannot be empty")

        # Validate context
        if context is not None and not isinstance(context, dict):
            raise TypeError("Context must be a dictionary")

        # Validate and extract intensity
        if context is None:
            context = {}

        if isinstance(intensity, dict):
            intensity = intensity.get('intensity', 0.8)

        try:
            intensity = float(intensity)
        except (TypeError, ValueError):
            raise ValueError("Intensity must be a number between 0 and 1")

        if not (0 <= intensity <= 1):
            raise ValueError(f"Intensity must be between 0 and 1, got {intensity}")

        # Generate initial emotional response
        response = self._generate_emotional_response(event, intensity)

        # Apply emotional regulation
        response = self._regulate_emotions(response)

        # Add required fields
        response["current_mood"] = self.current_state["valence"]
        response["emotional_stability"] = self.personality["emotional_stability"]

        # Update emotional state
        self._update_emotional_state(response)

        # Store emotional memory
        self._store_emotional_memory(event, response, context, intensity)

        return response

    def _generate_emotional_response(self,
                                     event: str,
                                     intensity: float) -> Dict[str, float]:
        """Generate initial emotional response to event"""
        response = {
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "trust": 0.0,
            "surprise": 0.0,
            "valence": 0.0,
            "arousal": 0.0,
            "dominance": 0.0
        }

        # First pass: detect surprise indicators
        surprise_detected = False
        exclamation_count = event.count('!')
        if exclamation_count > 0:
            surprise_detected = True
            response["surprise"] = min(0.2 * float(exclamation_count), 0.6) * intensity

        # Special handling for surprise phrases
        surprise_phrases = [
            "wow", "whoa", "oh my", "oh no", "oh wow", "unexpected", "suddenly",
            "can't believe", "cant believe", "amazing", "incredible", "unbelievable"
        ]

        event_lower = event.lower()
        words = event_lower.split()

        # Check for surprise phrases
        for phrase in surprise_phrases:
            if phrase in event_lower:
                surprise_detected = True
                response["surprise"] = max(response["surprise"], 0.4 * intensity)
                break

        # Track emotional content for surprise context
        joy_detected = False
        negative_detected = False

        # Calculate emotional response for each dimension
        total_intensity = 0.0

        # Emotional keyword sets with intensities
        emotion_keywords = {
            "joy": {
                "words": ["happy", "joy", "excited", "wonderful", "great", "success", "won", "award", "achievement"],
                "base_intensity": 0.8,
                "positive": True
            },
            "sadness": {
                "words": ["sad", "unhappy", "depressed", "down", "blue", "failure", "disappointed", "terrible", "awful",
                          "bad"],
                "base_intensity": 0.7,
                "positive": False
            },
            "anger": {
                "words": ["angry", "mad", "frustrated", "annoyed", "upset", "furious", "terrible", "hate", "rage"],
                "base_intensity": 0.6,
                "positive": False
            },
            "fear": {
                "words": ["afraid", "scared", "worried", "anxious", "nervous", "terrified", "fear", "dread", "panic"],
                "base_intensity": 0.7,
                "positive": False
            },
            "trust": {
                "words": ["trust", "reliable", "honest", "faithful", "confident", "secure", "safe", "certain"],
                "base_intensity": 0.6,
                "positive": True
            }
        }

        # Word intensities
        word_intensities = {
            "very": 1.5,
            "extremely": 2.0,
            "somewhat": 0.5,
            "slightly": 0.3,
            "really": 1.8,
            "absolutely": 2.0,
            "so": 1.5,
            "totally": 1.8,
            "completely": 2.0
        }

        # Calculate base intensity modifier
        intensity_modifier = 1.0
        for word in words:
            if word in word_intensities:
                intensity_modifier *= word_intensities[word]

        # Process each emotion
        for emotion, data in emotion_keywords.items():
            emotion_intensity = 0.0
            matches = 0

            # Check for keywords
            for word in words:
                if word in data["words"]:
                    emotion_intensity += data["base_intensity"]
                    total_intensity += data["base_intensity"]
                    matches += 1

                    if data["positive"]:
                        joy_detected = True
                    else:
                        negative_detected = True

            if matches > 0:
                # Scale by number of matches and apply intensity modifiers
                base_intensity = (emotion_intensity / matches) * intensity * intensity_modifier
                response[emotion] = min(1.0, base_intensity)

        # Handle surprise context
        if surprise_detected:
            if "wow" in event_lower or "amazing" in event_lower or "incredible" in event_lower:
                response["joy"] = max(response["joy"], 0.5 * intensity)
            if "oh no" in event_lower or "terrible" in event_lower:
                response["fear"] = max(response["fear"], 0.5 * intensity)

        # If no emotions detected, provide subtle baseline response
        if total_intensity == 0:
            response["trust"] = 0.1 * intensity

        # Calculate core dimensions
        positive_emotions = response["joy"] + response["trust"]
        negative_emotions = response["sadness"] + response["anger"] + response["fear"]

        response["valence"] = (positive_emotions - negative_emotions) * intensity
        response["arousal"] = (response["anger"] + response["fear"] + response["surprise"] + response[
            "joy"]) * intensity
        response["dominance"] = (response["trust"] - response["fear"] + 0.5 * response["joy"] - 0.5 * response[
            "sadness"]) * intensity

        # Normalize responses to prevent extreme values
        for emotion in response:
            response[emotion] = max(-1.0, min(1.0, response[emotion]))

        return response

    def get_current_state(self) -> Dict[str, float]:
        """Return current emotional state"""
        return self.current_state.copy()


class EmotionalModel:
    """Main class that integrates emotional processing components"""

    def __init__(self, personality: Dict[str, float]):
        self.core = EmotionalCore(personality)
        self.memory_system = []
        self.current_context = None

    def process_emotional_event(self, event: str, context: Dict[str, Any] = None, intensity: float = 0.8) -> Dict[
        str, float]:
        """Process an emotional event and return the emotional response"""
        # Validate context
        if context is not None and not isinstance(context, dict):
            raise TypeError("Context must be a dictionary")

        # Extract intensity from context if provided
        if context and 'intensity' in context:
            intensity = context['intensity']

        # Process event through emotional core
        response = self.core.process_emotional_event(event, context, intensity)

        # Add current mood and emotional stability
        response["current_mood"] = self.core.current_state["valence"]
        response["emotional_stability"] = self.core.personality["emotional_stability"]

        # Store in memory system
        self.memory_system.append({
            "event": event,
            "context": context,
            "response": response,
            "timestamp": datetime.now()
        })

        return response

    def _regulate_emotions(self, response: Dict[str, float]) -> Dict[str, float]:
        """Regulate emotional response based on personality traits"""
        regulated = response.copy()

        # Get personality traits
        stability = self.core.personality.get("emotional_stability", 0.5)
        neuroticism = self.core.personality.get("neuroticism", 0.5)

        # Apply emotional stability
        for emotion in regulated:
            if emotion not in ["current_mood", "emotional_stability"]:
                # More stable personalities have more moderated responses
                regulated[emotion] *= (1.0 - (stability * 0.5))

                # More neurotic personalities have more intense negative emotions
                if emotion in ["sadness", "fear", "anger"] and neuroticism > 0.5:
                    regulated[emotion] *= (1.0 + (neuroticism - 0.5))

        return regulated

    def get_emotional_state(self) -> Dict[str, float]:
        """Get current emotional state"""
        return self.core.get_current_state()


def main():
    # Example usage
    personality = {
        "optimism": 0.7,
        "energy_level": 0.6,
        "confidence": 0.5,
        "baseline_mood": 0.6,
        "emotional_stability": 0.7,
        "openness": 0.8,
        "neuroticism": 0.3,
        "conscientiousness": 0.7,
        "extraversion": 0.6,
        "agreeableness": 0.8
    }

    emotional_core = EmotionalCore(personality)

    # Process some emotional events
    events = [
        ("I'm really excited about this new project!", 0.8),
        ("That comment made me feel uncomfortable.", 0.6),
        ("I'm worried about the upcoming deadline.", 0.7)
    ]

    print("\nProcessing emotional events:")
    for event, intensity in events:
        print(f"\nEvent: {event}")
        response = emotional_core.process_emotional_event(event, intensity=intensity)
        print("Emotional state:", response)

    print("\nEmotional Summary:")
    summary = emotional_core.get_current_state()
    for key, value in summary.items():
        print(f"{key}: {value}")

    emotional_model = EmotionalModel(personality)
    print("\nEmotional Model:")
    print(emotional_model.process_emotional_event("I'm really happy today!", intensity=0.9))


if __name__ == "__main__":
    main()
