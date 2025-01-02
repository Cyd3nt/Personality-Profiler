import unittest

from neurodivergent_traits import NeurodivergentTraits


class TestNeurodivergentTraits(unittest.TestCase):
    def setUp(self):
        self.traits = NeurodivergentTraits()

    def test_initialization(self):
        """Test that initialization creates proper baseline data"""
        # Check stim patterns
        for stim_type in ["hand_flapping", "rocking", "pacing", "fidgeting"]:
            self.assertGreaterEqual(
                len(self.traits.stim_patterns[stim_type]),
                self.traits.MIN_DATA_POINTS,
                f"Stim pattern {stim_type} doesn't have minimum data points"
            )

        # Check executive functions
        for function in self.traits.executive_function:
            self.assertGreaterEqual(
                len(self.traits._exec_function_history[function]),
                self.traits.MIN_DATA_POINTS,
                f"Executive function {function} doesn't have minimum data points"
            )

        # Check processing speed
        for speed_type in self.traits.processing_speed:
            self.assertGreaterEqual(
                len(self.traits._processing_history[speed_type]),
                self.traits.MIN_DATA_POINTS,
                f"Processing speed {speed_type} doesn't have minimum data points"
            )

        # Check attention patterns
        for pattern in ["sustained", "selective", "divided"]:
            self.assertGreaterEqual(
                len(self.traits.attention_patterns[pattern]),
                self.traits.MIN_DATA_POINTS,
                f"Attention pattern {pattern} doesn't have minimum data points"
            )

    def test_data_point_validation(self):
        """Test the data point validation logic"""
        # Test with insufficient data
        self.assertFalse(
            self.traits._validate_data_points([1, 2], "test_category"),
            "Validation should fail with insufficient data points"
        )

        # Test with minimum data
        self.assertTrue(
            self.traits._validate_data_points([1, 2, 3], "test_category"),
            "Validation should pass with minimum data points"
        )

        # Test with more than minimum data
        self.assertTrue(
            self.traits._validate_data_points([1, 2, 3, 4], "test_category"),
            "Validation should pass with more than minimum data points"
        )

    def test_stim_pattern_management(self):
        """Test adding and managing stim patterns"""
        stim_type = "hand_flapping"
        initial_count = len(self.traits.stim_patterns[stim_type])

        # Add new patterns
        for i in range(self.traits.MAX_DATA_POINTS + 10):
            self.traits.add_stim_pattern(
                stim_type=stim_type,
                pattern={"duration": 30, "intensity": 0.8},
                context={"location": "home", "time": "evening"}
            )

        # Check that we don't exceed max points
        self.assertLessEqual(
            len(self.traits.stim_patterns[stim_type]),
            self.traits.MAX_DATA_POINTS,
            "Stim patterns should not exceed maximum limit"
        )

        # Check that we maintain minimum points
        self.assertGreaterEqual(
            len(self.traits.stim_patterns[stim_type]),
            self.traits.MIN_DATA_POINTS,
            "Stim patterns should maintain minimum data points"
        )

    def test_executive_function_tracking(self):
        """Test executive function observation tracking"""
        function_type = "task_switching"

        # Add observations
        performances = [0.7, 0.8, 0.9, 0.6, 0.8]
        for perf in performances:
            self.traits.add_executive_function_observation(
                function_type=function_type,
                performance=perf,
                context={"task": "coding"},
                difficulty_level=0.8
            )

        # Check history maintenance
        self.assertGreaterEqual(
            len(self.traits._exec_function_history[function_type]),
            self.traits.MIN_DATA_POINTS,
            "Executive function history should maintain minimum points"
        )

        # Check current value calculation
        current_value = self.traits.executive_function[function_type]
        self.assertGreater(current_value, 0,
                           "Executive function value should be updated")

    def test_processing_speed_tracking(self):
        """Test processing speed observation tracking"""
        speed_type = "verbal"

        # Add observations with varying complexity
        test_data = [
            (0.8, 0.9, 0.7),  # speed, accuracy, complexity
            (0.7, 0.8, 0.6),
            (0.9, 0.95, 0.8),
            (0.6, 0.85, 0.5)
        ]

        for speed, accuracy, complexity in test_data:
            self.traits.add_processing_speed_observation(
                processing_type=speed_type,
                speed=speed,
                accuracy=accuracy,
                complexity=complexity
            )

        # Check history maintenance
        self.assertGreaterEqual(
            len(self.traits._processing_history[speed_type]),
            self.traits.MIN_DATA_POINTS,
            "Processing speed history should maintain minimum points"
        )

        # Verify speed adjustments
        current_speed = self.traits.processing_speed[speed_type]
        self.assertGreater(current_speed, 0,
                           "Processing speed should be updated")

    def test_attention_pattern_tracking(self):
        """Test attention pattern tracking"""
        attention_type = "sustained"

        # Add observations with varying distractions
        test_data = [
            (60, 0.9, ["noise"]),
            (45, 0.8, ["noise", "movement"]),
            (30, 0.7, ["noise", "movement", "conversation"]),
            (90, 0.95, [])
        ]

        for duration, quality, distractions in test_data:
            self.traits.add_attention_observation(
                attention_type=attention_type,
                duration=duration,
                quality=quality,
                distractions=distractions
            )

        # Check pattern maintenance
        self.assertGreaterEqual(
            len(self.traits.attention_patterns[attention_type]),
            self.traits.MIN_DATA_POINTS,
            "Attention patterns should maintain minimum points"
        )

        # Test distraction penalty
        scores = self.traits.attention_patterns[attention_type]
        self.assertGreater(scores[-1], scores[-3],
                           "No distractions should result in higher score")

    def test_trend_calculation(self):
        """Test trend calculation methods"""
        # Test with exactly minimum points
        min_data = [0.5, 0.6, 0.7]
        trend = self.traits._calculate_trend(min_data)
        self.assertGreater(trend, 0,
                           "Trend should be positive for increasing values")

        # Test with more than minimum points
        more_data = [0.5, 0.6, 0.7, 0.8, 0.9]
        trend = self.traits._calculate_trend(more_data)
        self.assertGreater(trend, 0,
                           "Trend should be positive for increasing values")

        # Test with decreasing values
        decreasing_data = [0.9, 0.8, 0.7, 0.6, 0.5]
        trend = self.traits._calculate_trend(decreasing_data)
        self.assertLess(trend, 0,
                        "Trend should be negative for decreasing values")

    def test_recent_change_calculation(self):
        """Test recent change calculation"""
        # Test with minimum points
        min_data = [0.5, 0.6, 0.7]
        change = self.traits._calculate_recent_change(min_data)
        self.assertGreater(change, 0,
                           "Change should be positive for increasing values")

        # Test with more points
        more_data = [0.5, 0.6, 0.7, 0.8, 0.9, 0.7]
        change = self.traits._calculate_recent_change(more_data)
        self.assertIsInstance(change, float,
                              "Change calculation should return float")

    def test_trait_summary(self):
        """Test trait summary generation"""
        # Add some test data
        self.traits.add_stim_pattern(
            "hand_flapping",
            {"duration": 30, "intensity": 0.8},
            {"location": "home"}
        )

        self.traits.add_executive_function_observation(
            "task_switching",
            0.8,
            {"task": "coding"},
            0.7
        )

        self.traits.add_processing_speed_observation(
            "verbal",
            0.9,
            0.95,
            0.8
        )

        self.traits.add_attention_observation(
            "sustained",
            60,
            0.9,
            ["noise"]
        )

        # Get summary
        summary = self.traits.get_trait_summary()

        # Check summary structure
        self.assertIn("executive_function", summary)
        self.assertIn("processing_speed", summary)
        self.assertIn("attention_patterns", summary)
        self.assertIn("stim_patterns", summary)

        # Check data validation in summary
        self.assertTrue(all(len(v) >= self.traits.MIN_DATA_POINTS
                            for v in self.traits.attention_patterns.values()))
        self.assertTrue(all(len(v) >= self.traits.MIN_DATA_POINTS
                            for v in self.traits._exec_function_history.values()))
        self.assertTrue(all(len(v) >= self.traits.MIN_DATA_POINTS
                            for v in self.traits._processing_history.values()))


if __name__ == '__main__':
    unittest.main()
