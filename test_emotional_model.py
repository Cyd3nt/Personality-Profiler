import unittest
from datetime import datetime

from emotional_model import EmotionalCore, EmotionalModel


class TestEmotionalCore(unittest.TestCase):
    def setUp(self):
        self.personality = {
            "optimism": 0.5,
            "energy_level": 0.6,
            "confidence": 0.4,
            "baseline_mood": 0.3,
            "emotional_stability": 0.7,
            "openness": 0.6,
            "neuroticism": 0.4,
            "conscientiousness": 0.7,
            "extraversion": 0.5,
            "agreeableness": 0.6
        }
        self.core = EmotionalCore(self.personality)
        self.base_time = datetime.now()

    def test_initialization(self):
        """Test initial emotional state and dimensions"""
        # Test emotional dimensions
        self.assertIn("valence", self.core.emotion_dimensions)
        self.assertIn("arousal", self.core.emotion_dimensions)
        self.assertIn("dominance", self.core.emotion_dimensions)

        # Test current state initialization
        self.assertEqual(self.core.current_state["valence"], self.personality["optimism"])
        self.assertEqual(self.core.current_state["arousal"], self.personality["energy_level"])
        self.assertEqual(self.core.current_state["dominance"], self.personality["confidence"])

        # Test baseline calculation
        self.assertAlmostEqual(self.core.mood_baseline["valence"], self.personality["optimism"] * 0.7)
        self.assertAlmostEqual(self.core.mood_baseline["arousal"], self.personality["energy_level"] * 0.5)
        self.assertAlmostEqual(self.core.mood_baseline["dominance"], self.personality["confidence"] * 0.6)

        # Test regulation strategies
        self.assertEqual(self.core.regulation_strategies["reappraisal"], self.personality["openness"])
        self.assertEqual(self.core.regulation_strategies["suppression"], self.personality["neuroticism"])

    def test_process_emotional_event(self):
        """Test processing emotional events"""
        context = {
            "location": "work",
            "activity": "achievement",
            "social_context": "team"
        }

        # Process a very positive event
        response = self.core.process_emotional_event(
            event="Great success! Won the project award and the team is happy",
            context=context,
            intensity=0.8
        )

        # Check response contains expected keys
        self.assertIn("valence", response)
        self.assertIn("arousal", response)
        self.assertIn("dominance", response)
        self.assertIn("current_mood", response)
        self.assertIn("emotional_stability", response)

        # Verify positive response
        self.assertGreater(response["valence"], 0.3)
        self.assertGreater(response["joy"], 0.2)
        self.assertLess(response["sadness"], 0.1)

        # Check emotional memory was stored
        self.assertEqual(len(self.core.emotional_memory), 1)
        memory = self.core.emotional_memory[0]
        self.assertEqual(memory.trigger, "Great success! Won the project award and the team is happy")
        self.assertEqual(memory.context, context)
        self.assertEqual(memory.intensity, 0.8)

        # Store the positive response values
        positive_valence = response["valence"]
        positive_joy = response["joy"]
        positive_sadness = response["sadness"]
        positive_anger = response["anger"]

        # Process a very negative event
        response2 = self.core.process_emotional_event(
            event="Terrible failure. Project rejected and team is frustrated and angry",
            context={"location": "work", "activity": "review"},
            intensity=0.6
        )

        # Check emotional state changed appropriately
        self.assertLess(response2["valence"], positive_valence)  # Should be more negative
        self.assertLess(response2["joy"], positive_joy)  # Should have less joy
        self.assertGreater(response2["sadness"], positive_sadness)  # Should have more sadness
        self.assertGreater(response2["anger"], positive_anger)  # Should have more anger
        self.assertEqual(len(self.core.emotional_memory), 2)

    def test_emotional_regulation(self):
        """Test emotional regulation strategies"""
        # Process an intense negative event
        response = self.core.process_emotional_event(
            event="failure",
            context={"location": "work", "activity": "project"},
            intensity=0.9
        )

        # Check that regulation strategies modulated the response
        # Higher emotional stability should lead to less extreme responses
        self.assertLess(abs(response["valence"]), 0.9)

        # Process multiple events to test cumulative regulation
        for _ in range(3):
            self.core.process_emotional_event(
                event="minor_setback",
                context={"location": "work"},
                intensity=0.4
            )

        # Check emotional stability remains within bounds
        self.assertGreaterEqual(self.core.current_state["emotional_stability"], 0.0)
        self.assertLessEqual(self.core.current_state["emotional_stability"], 1.0)

    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        # Test invalid intensity
        with self.assertRaises(ValueError):
            self.core.process_emotional_event(
                event="test",
                context={},
                intensity=1.5
            )

        # Test invalid context
        with self.assertRaises(TypeError):
            self.core.process_emotional_event(
                event="test",
                context="invalid",
                intensity=0.5
            )

        # Test empty event
        with self.assertRaises(ValueError):
            self.core.process_emotional_event(
                event="",
                context={},
                intensity=0.5
            )


class TestEmotionalModel(unittest.TestCase):
    def setUp(self):
        self.personality = {
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
        self.model = EmotionalModel(self.personality)

    def test_process_emotional_event(self):
        """Test basic emotional event processing"""
        event = "I am very happy today"
        context = {"location": "home", "time": datetime.now()}
        response = self.model.process_emotional_event(event, context)

        self.assertGreater(response["joy"], 0)
        self.assertGreaterEqual(response["valence"], 0)
        self.assertLess(response["sadness"], response["joy"])

    def test_negative_emotions(self):
        """Test processing of negative emotional events"""
        events = [
            "I am very sad and angry today",
            "This is terrible and frustrating",
            "I am scared and worried about tomorrow"
        ]

        for event in events:
            context = {"location": "home", "time": datetime.now()}
            response = self.model.process_emotional_event(event, context)

            # Check that negative emotions are properly represented
            self.assertGreater(response["sadness"] + response["anger"] + response["fear"], 0)
            self.assertLess(response["valence"], 0)
            self.assertLess(response["joy"], 0.2)  # Should have minimal joy

    def test_mixed_emotions(self):
        """Test processing of events with mixed emotions"""
        events = [
            "I am happy but also nervous about the presentation",
            "The success was great but I'm worried about maintaining it",
            "I trust them but I'm slightly afraid of change"
        ]

        for event in events:
            context = {"location": "work", "time": datetime.now()}
            response = self.model.process_emotional_event(event, context)

            # Check for presence of both positive and negative emotions
            positive_emotions = response["joy"] + response["trust"]
            negative_emotions = response["sadness"] + response["anger"] + response["fear"]

            self.assertGreater(positive_emotions, 0)
            self.assertGreater(negative_emotions, 0)
            self.assertNotEqual(response["valence"], 0)  # Should not be neutral

    def test_neutral_events(self):
        """Test processing of neutral or ambiguous events"""
        events = [
            "The weather is changing",
            "I am going to the store",
            "The book is on the table"
        ]

        for event in events:
            context = {"location": "home", "time": datetime.now()}
            response = self.model.process_emotional_event(event, context)

            # Check that neutral events produce minimal emotional response
            for emotion in ["joy", "sadness", "anger", "fear", "trust"]:
                self.assertLess(abs(response[emotion]), 0.3)

            self.assertGreater(response["valence"], -0.3)
            self.assertLess(response["valence"], 0.3)

    def test_intensity_scaling(self):
        """Test that emotional intensity properly scales responses"""
        event = "I am extremely happy and excited about winning the award!"
        context = {"location": "work", "time": datetime.now(), "intensity": 1.0}
        high_intensity_response = self.model.process_emotional_event(event, context)

        context["intensity"] = 0.5
        medium_intensity_response = self.model.process_emotional_event(event, context)

        context["intensity"] = 0.2
        low_intensity_response = self.model.process_emotional_event(event, context)

        # Check that responses scale with intensity
        self.assertGreater(high_intensity_response["joy"], medium_intensity_response["joy"])
        self.assertGreater(medium_intensity_response["joy"], low_intensity_response["joy"])

        # Check that valence maintains the same sign but scales
        self.assertGreater(abs(high_intensity_response["valence"]),
                           abs(medium_intensity_response["valence"]))
        self.assertGreater(abs(medium_intensity_response["valence"]),
                           abs(low_intensity_response["valence"]))

    def test_emotional_memory_integration(self):
        """Test that consecutive emotional events influence each other"""
        context = {"location": "home", "time": datetime.now()}

        # Process a sequence of related events
        events = [
            "Today was a wonderful day!",  # Strong positive
            "Everything is going perfectly well",  # Moderate positive
            "Things are good but I'm a bit tired"  # Mild positive with slight negative
        ]

        responses = []
        for event in events:
            response = self.model.process_emotional_event(event, context)
            responses.append(response)

        # Check that emotional changes are smooth
        for i in range(1, len(responses)):
            # Check that changes between states are not too extreme
            self.assertLess(
                abs(responses[i]["valence"] - responses[i - 1]["valence"]),
                0.5,  # Maximum allowed change between states
                f"Too large change in valence between states {i - 1} and {i}"
            )

            # Check that emotional momentum is maintained
            self.assertGreater(
                responses[i]["valence"],
                0,  # Should stay positive throughout
                f"Lost positive momentum in state {i}"
            )

    def test_surprise_emotion(self):
        """Test surprise emotion which can be either positive or negative"""
        positive_surprise = "Wow! I just got an unexpected award!"
        negative_surprise = "Oh no! Something terrible happened!"
        neutral_surprise = "Oh! That was completely unexpected."

        context = {"location": "work", "time": datetime.now()}

        pos_response = self.model.process_emotional_event(positive_surprise, context)
        neg_response = self.model.process_emotional_event(negative_surprise, context)
        neut_response = self.model.process_emotional_event(neutral_surprise, context)

        # Check that surprise is present in all cases
        self.assertGreater(pos_response["surprise"], 0)
        self.assertGreater(neg_response["surprise"], 0)
        self.assertGreater(neut_response["surprise"], 0)

        # Check associated emotions
        self.assertGreater(pos_response["joy"], 0)
        self.assertGreater(neg_response["fear"] + neg_response["sadness"], 0)

        # Check relative valence
        self.assertGreater(pos_response["valence"], neut_response["valence"])
        self.assertLess(neg_response["valence"], neut_response["valence"])

    def test_boundary_conditions(self):
        """Test extreme emotional events and boundary conditions"""
        extreme_events = [
            "This is the absolute worst thing that has ever happened to me!",
            "I am experiencing the greatest joy and success of my entire life!",
            "I am completely terrified and utterly devastated"
        ]

        for event in extreme_events:
            context = {"location": "home", "time": datetime.now(), "intensity": 1.0}
            response = self.model.process_emotional_event(event, context)

            # Check that no emotional values exceed bounds
            for emotion in response:
                self.assertGreaterEqual(response[emotion], -1.0)
                self.assertLessEqual(response[emotion], 1.0)


if __name__ == '__main__':
    unittest.main()
