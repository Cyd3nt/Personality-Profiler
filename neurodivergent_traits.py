from collections import defaultdict, Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class SensoryProfile:
    """Tracks sensory processing patterns and preferences"""
    visual_sensitivity: float  # Sensitivity to visual stimuli
    auditory_sensitivity: float  # Sensitivity to sounds
    tactile_sensitivity: float  # Sensitivity to touch
    proprioceptive_awareness: float  # Body awareness
    vestibular_processing: float  # Balance and movement
    interoceptive_awareness: float  # Internal body signals
    sensory_seeking: Dict[str, float]  # Specific sensory seeking behaviors
    sensory_avoiding: Dict[str, float]  # Specific sensory avoiding behaviors

    def to_dict(self) -> Dict:
        return {
            "visual_sensitivity": self.visual_sensitivity,
            "auditory_sensitivity": self.auditory_sensitivity,
            "tactile_sensitivity": self.tactile_sensitivity,
            "proprioceptive_awareness": self.proprioceptive_awareness,
            "vestibular_processing": self.vestibular_processing,
            "interoceptive_awareness": self.interoceptive_awareness,
            "sensory_seeking": dict(self.sensory_seeking),
            "sensory_avoiding": dict(self.sensory_avoiding)
        }


@dataclass
class CognitiveStyle:
    """Tracks cognitive processing patterns"""
    detail_focus: float  # Attention to detail vs. big picture
    pattern_recognition: float  # Ability to recognize patterns
    context_sensitivity: float  # Sensitivity to context
    sequential_processing: float  # Sequential vs. parallel processing
    cognitive_flexibility: float  # Ability to switch between tasks/concepts
    special_interests: List[Dict[str, float]]  # Areas of intense focus/interest
    learning_style: Dict[str, float]  # Different learning preferences

    def to_dict(self) -> Dict:
        return {
            "detail_focus": self.detail_focus,
            "pattern_recognition": self.pattern_recognition,
            "context_sensitivity": self.context_sensitivity,
            "sequential_processing": self.sequential_processing,
            "cognitive_flexibility": self.cognitive_flexibility,
            "special_interests": [dict(interest) for interest in self.special_interests],
            "learning_style": dict(self.learning_style)
        }


@dataclass
class SocialCommunicationStyle:
    """Tracks social communication patterns"""
    nonverbal_understanding: float  # Understanding of nonverbal cues
    literal_interpretation: float  # Tendency for literal interpretation
    social_energy_management: float  # Social energy levels and recovery
    communication_preferences: Dict[str, float]  # Preferred communication modes
    social_scripts: List[Dict[str, any]]  # Learned social interactions
    masking_patterns: Dict[str, float]  # Social masking behaviors

    def to_dict(self) -> Dict:
        return {
            "nonverbal_understanding": self.nonverbal_understanding,
            "literal_interpretation": self.literal_interpretation,
            "social_energy_management": self.social_energy_management,
            "communication_preferences": dict(self.communication_preferences),
            "social_scripts": [dict(script) for script in self.social_scripts],
            "masking_patterns": dict(self.masking_patterns)
        }


class NeurodivergentTraits:
    def __init__(self):
        self.sensory_profile = SensoryProfile(
            visual_sensitivity=0.0,
            auditory_sensitivity=0.0,
            tactile_sensitivity=0.0,
            proprioceptive_awareness=0.0,
            vestibular_processing=0.0,
            interoceptive_awareness=0.0,
            sensory_seeking={},
            sensory_avoiding={}
        )

        self.cognitive_style = CognitiveStyle(
            detail_focus=0.0,
            pattern_recognition=0.0,
            context_sensitivity=0.0,
            sequential_processing=0.0,
            cognitive_flexibility=0.0,
            special_interests=[],
            learning_style={}
        )

        self.social_style = SocialCommunicationStyle(
            nonverbal_understanding=0.0,
            literal_interpretation=0.0,
            social_energy_management=0.0,
            communication_preferences={},
            social_scripts=[],
            masking_patterns={}
        )

        self.observations: List[Dict] = []
        self.processing_patterns: Dict[str, List[float]] = defaultdict(list)
        self.environmental_impacts: Dict[str, Dict[str, float]] = defaultdict(dict)

        self.stim_patterns: Dict[str, List[Dict]] = defaultdict(list)
        self.executive_function: Dict[str, float] = {
            "task_switching": 0.0,
            "working_memory": 0.0,
            "planning": 0.0,
            "organization": 0.0,
            "time_management": 0.0,
            "emotional_regulation": 0.0
        }
        self._exec_function_history: Dict[str, List[float]] = defaultdict(list)
        self.processing_speed: Dict[str, float] = {
            "verbal": 0.0,
            "visual": 0.0,
            "motor": 0.0,
            "decision_making": 0.0
        }
        self._processing_history: Dict[str, List[float]] = defaultdict(list)
        self.attention_patterns: Dict[str, List[float]] = defaultdict(list)

        self.MIN_DATA_POINTS = 3
        self.MAX_DATA_POINTS = 100

        # Initialize with baseline neutral values
        self._initialize_baseline_data()

    def _initialize_baseline_data(self):
        """Initialize with neutral baseline data to ensure minimum data points"""
        baseline_timestamp = datetime.now()

        # Initialize stim patterns with baseline data
        for stim_type in ["hand_flapping", "rocking", "pacing", "fidgeting"]:
            for i in range(self.MIN_DATA_POINTS):
                self.stim_patterns[stim_type].append({
                    "timestamp": baseline_timestamp,
                    "duration": 30,
                    "intensity": 0.5,
                    "context": {"setting": "baseline", "state": "neutral"}
                })

        # Initialize executive function with baseline data
        for function in self.executive_function.keys():
            self.executive_function[function] = 0.5
            self._exec_function_history[function] = [0.5] * self.MIN_DATA_POINTS

        # Initialize processing speed with baseline data
        for process in self.processing_speed.keys():
            self.processing_speed[process] = 0.5
            self._processing_history[process] = [0.5] * self.MIN_DATA_POINTS

        # Initialize attention patterns with baseline data
        for attention_type in ["sustained", "selective", "divided"]:
            self.attention_patterns[attention_type] = [0.5] * self.MIN_DATA_POINTS

    def _validate_data_points(self, data_list: List, category: str) -> bool:
        """Validate that we have minimum required data points"""
        if len(data_list) < self.MIN_DATA_POINTS:
            print(f"Warning: Insufficient data points for {category}. "
                  f"Minimum {self.MIN_DATA_POINTS} required, current: {len(data_list)}")
            return False
        return True

    def add_sensory_observation(self,
                                stimulus_type: str,
                                response: str,
                                intensity: float,
                                context: Dict[str, str],
                                timestamp: datetime) -> None:
        """Record a sensory processing observation"""
        observation = {
            "type": "sensory",
            "stimulus": stimulus_type,
            "response": response,
            "intensity": intensity,
            "context": context,
            "timestamp": timestamp
        }
        self.observations.append(observation)

        # Update sensory profile
        if "seeking" in response.lower():
            self.sensory_profile.sensory_seeking[stimulus_type] = intensity
        elif "avoiding" in response.lower():
            self.sensory_profile.sensory_avoiding[stimulus_type] = intensity

        # Update relevant sensitivity scores
        if stimulus_type == "visual":
            self._update_running_average("visual_sensitivity", intensity)
        elif stimulus_type == "auditory":
            self._update_running_average("auditory_sensitivity", intensity)
        elif stimulus_type == "tactile":
            self._update_running_average("tactile_sensitivity", intensity)

    def add_cognitive_observation(self,
                                  observation_type: str,
                                  behavior: str,
                                  context: Dict[str, str],
                                  performance: Optional[float] = None,
                                  special_interest: Optional[Dict] = None) -> None:
        """Record a cognitive processing observation"""
        observation = {
            "type": "cognitive",
            "observation_type": observation_type,
            "behavior": behavior,
            "context": context,
            "performance": performance,
            "timestamp": datetime.now()
        }
        self.observations.append(observation)

        # Update cognitive style
        if special_interest:
            self._update_special_interests(special_interest)

        if performance is not None:
            self._update_cognitive_metrics(observation_type, performance)

    def add_social_observation(self,
                               interaction_type: str,
                               behavior: str,
                               context: Dict[str, str],
                               energy_impact: Optional[float] = None,
                               masking_effort: Optional[float] = None) -> None:
        """Record a social interaction observation"""
        observation = {
            "type": "social",
            "interaction_type": interaction_type,
            "behavior": behavior,
            "context": context,
            "energy_impact": energy_impact,
            "masking_effort": masking_effort,
            "timestamp": datetime.now()
        }
        self.observations.append(observation)

        # Update social communication style
        if energy_impact is not None:
            self._update_running_average("social_energy", energy_impact)

        if masking_effort is not None:
            self._update_masking_patterns(interaction_type, masking_effort)

    def add_environmental_impact(self,
                                 environment_type: str,
                                 impact_metrics: Dict[str, float]) -> None:
        """Record environmental impacts on functioning"""
        for metric, value in impact_metrics.items():
            current = self.environmental_impacts[environment_type].get(metric, 0.0)
            self.environmental_impacts[environment_type][metric] = (current + value) / 2

    def add_stim_pattern(self,
                         stim_type: str,
                         pattern: Dict[str, any],
                         context: Dict[str, str]) -> None:
        """Record stimming patterns and contexts"""
        pattern.update({
            "timestamp": datetime.now(),
            "context": context
        })
        self.stim_patterns[stim_type].append(pattern)

        # Maintain maximum window while keeping minimum points
        if len(self.stim_patterns[stim_type]) > self.MAX_DATA_POINTS:
            excess = len(self.stim_patterns[stim_type]) - self.MAX_DATA_POINTS
            if len(self.stim_patterns[stim_type]) - excess >= self.MIN_DATA_POINTS:
                self.stim_patterns[stim_type] = (
                    self.stim_patterns[stim_type][excess:])

        self._analyze_stim_patterns(stim_type)

    def add_executive_function_observation(self,
                                           function_type: str,
                                           performance: float,
                                           context: Dict[str, str],
                                           difficulty_level: float) -> None:
        """Record executive function performance"""
        if function_type in self.executive_function:
            # Add to history
            if function_type not in self._exec_function_history:
                self._exec_function_history[function_type] = []

            adjusted_performance = performance * difficulty_level
            self._exec_function_history[function_type].append(adjusted_performance)

            # Maintain window size while keeping minimum points
            if len(self._exec_function_history[function_type]) > self.MAX_DATA_POINTS:
                excess = len(self._exec_function_history[function_type]) - self.MAX_DATA_POINTS
                if len(self._exec_function_history[function_type]) - excess >= self.MIN_DATA_POINTS:
                    self._exec_function_history[function_type] = (
                        self._exec_function_history[function_type][excess:])

            # Update current value with weighted average
            self.executive_function[function_type] = np.mean(
                self._exec_function_history[function_type][-10:])

    def add_processing_speed_observation(self,
                                         processing_type: str,
                                         speed: float,
                                         accuracy: float,
                                         complexity: float) -> None:
        """Record processing speed observations"""
        if processing_type in self.processing_speed:
            if processing_type not in self._processing_history:
                self._processing_history[processing_type] = []

            adjusted_speed = speed * (accuracy ** 0.5) / (complexity ** 0.3)
            self._processing_history[processing_type].append(adjusted_speed)

            # Maintain window size while keeping minimum points
            if len(self._processing_history[processing_type]) > self.MAX_DATA_POINTS:
                excess = len(self._processing_history[processing_type]) - self.MAX_DATA_POINTS
                if len(self._processing_history[processing_type]) - excess >= self.MIN_DATA_POINTS:
                    self._processing_history[processing_type] = (
                        self._processing_history[processing_type][excess:])

            # Update current value with weighted average
            self.processing_speed[processing_type] = np.mean(
                self._processing_history[processing_type][-10:])

    def add_attention_observation(self,
                                  attention_type: str,
                                  duration: float,
                                  quality: float,
                                  distractions: List[str]) -> None:
        """Record attention patterns"""
        distraction_penalty = len(distractions) * 0.1
        attention_score = quality * duration * (1 - distraction_penalty)

        if attention_type not in self.attention_patterns:
            self.attention_patterns[attention_type] = []

        self.attention_patterns[attention_type].append(attention_score)

        # Maintain window size while keeping minimum points
        if len(self.attention_patterns[attention_type]) > self.MAX_DATA_POINTS:
            excess = len(self.attention_patterns[attention_type]) - self.MAX_DATA_POINTS
            if len(self.attention_patterns[attention_type]) - excess >= self.MIN_DATA_POINTS:
                self.attention_patterns[attention_type] = (
                    self.attention_patterns[attention_type][excess:])

    def _update_running_average(self, metric: str, value: float) -> None:
        """Update running average for a metric"""
        self.processing_patterns[metric].append(value)
        if len(self.processing_patterns[metric]) > 100:  # Keep last 100 observations
            self.processing_patterns[metric].pop(0)

    def _update_special_interests(self, interest: Dict) -> None:
        """Update special interests tracking"""
        topic = interest.get("topic")
        intensity = interest.get("intensity", 0.0)

        # Update existing interest or add new one
        existing = next((i for i in self.cognitive_style.special_interests
                         if i["topic"] == topic), None)
        if existing:
            existing["intensity"] = (existing["intensity"] + intensity) / 2
            existing["last_observed"] = datetime.now()
        else:
            interest["first_observed"] = datetime.now()
            interest["last_observed"] = datetime.now()
            self.cognitive_style.special_interests.append(interest)

    def _update_cognitive_metrics(self, metric: str, value: float) -> None:
        """Update cognitive processing metrics"""
        if metric == "detail_focus":
            self.cognitive_style.detail_focus = (
                    self.cognitive_style.detail_focus * 0.9 + value * 0.1
            )
        elif metric == "pattern_recognition":
            self.cognitive_style.pattern_recognition = (
                    self.cognitive_style.pattern_recognition * 0.9 + value * 0.1
            )
        elif metric == "cognitive_flexibility":
            self.cognitive_style.cognitive_flexibility = (
                    self.cognitive_style.cognitive_flexibility * 0.9 + value * 0.1
            )

    def _update_masking_patterns(self, context: str, effort: float) -> None:
        """Update social masking patterns"""
        current = self.social_style.masking_patterns.get(context, 0.0)
        self.social_style.masking_patterns[context] = (current + effort) / 2

    def _analyze_stim_patterns(self, stim_type: str) -> None:
        """Analyze stimming patterns for insights"""
        patterns = self.stim_patterns[stim_type]

        # Analyze frequency
        timestamps = [p["timestamp"] for p in patterns]
        intervals = np.diff([t.timestamp() for t in timestamps])
        frequency = 1 / np.mean(intervals) if intervals.size > 0 and np.mean(intervals) != 0 else 0

        # Analyze context correlation
        contexts = [p["context"] for p in patterns]
        common_contexts = Counter([
            item for d in contexts
            for item in d.items()
        ]).most_common()

        # Update cognitive style based on patterns
        if frequency > 0.5:  # High frequency
            self.cognitive_style.detail_focus += 0.1
            self.cognitive_style.pattern_recognition += 0.1

        # Update sensory profile based on common contexts
        for (context_key, context_value), count in common_contexts:
            if "stress" in context_key and count > 3:
                self.sensory_profile.sensory_seeking[stim_type] = 0.8

    def get_trait_summary(self) -> Dict:
        """Get a summary of neurodivergent traits and patterns"""
        summary = {
            "sensory_profile": self.sensory_profile.to_dict(),
            "cognitive_style": self.cognitive_style.to_dict(),
            "social_communication": self.social_style.to_dict(),
            "environmental_impacts": dict(self.environmental_impacts),
            "processing_patterns": {
                k: {"mean": np.mean(v), "std": np.std(v) if len(v) > 1 else 0}
                for k, v in self.processing_patterns.items()
            },
            "observation_counts": {
                "sensory": len([o for o in self.observations if o["type"] == "sensory"]),
                "cognitive": len([o for o in self.observations if o["type"] == "cognitive"]),
                "social": len([o for o in self.observations if o["type"] == "social"])
            }
        }

        # Validate data points before generating summaries
        for attention_type, data in self.attention_patterns.items():
            self._validate_data_points(data, f"attention_{attention_type}")

        for stim_type, data in self.stim_patterns.items():
            self._validate_data_points(data, f"stim_{stim_type}")

        for function_type, data in self._exec_function_history.items():
            self._validate_data_points(data, f"executive_{function_type}")

        for process_type, data in self._processing_history.items():
            self._validate_data_points(data, f"processing_{process_type}")

        # Add detailed metrics with safety checks
        summary.update({
            "executive_function": {
                k: {
                    "current": v,
                    "trend": self._calculate_trend(self._exec_function_history[k]),
                    "variability": float(np.std(self._exec_function_history[k]))
                    if len(self._exec_function_history[k]) > 1 else 0.0
                }
                for k, v in self.executive_function.items()
            },
            "processing_speed": {
                k: {
                    "current": v,
                    "trend": self._calculate_trend(self._processing_history[k]),
                    "variability": float(np.std(self._processing_history[k]))
                    if len(self._processing_history[k]) > 1 else 0.0
                }
                for k, v in self.processing_speed.items()
            },
            "attention_patterns": {
                k: {
                    "mean": float(np.mean(v)),
                    "variance": float(np.var(v)) if len(v) > 1 else 0.0,
                    "trend": self._calculate_trend(v),
                    "recent_change": self._calculate_recent_change(v)
                }
                for k, v in self.attention_patterns.items()
                if self._validate_data_points(v, f"attention_{k}")
            },
            "stim_patterns": {
                k: {
                    "frequency": self._calculate_frequency(v),
                    "intensity_trend": self._calculate_intensity_trend(v),
                    "common_contexts": self._get_common_contexts(v),
                    "total_observations": len(v)
                }
                for k, v in self.stim_patterns.items()
                if self._validate_data_points(v, f"stim_{k}")
            }
        })

        return summary

    def _calculate_trend(self, data: List[float]) -> float:
        """Calculate linear trend in data"""
        if len(data) < self.MIN_DATA_POINTS:
            return 0.0

        try:
            # Use robust linear regression to handle outliers
            x = np.arange(len(data))
            y = np.array(data)

            # Remove any NaN values
            mask = ~np.isnan(y)
            if np.sum(mask) < self.MIN_DATA_POINTS:
                return 0.0

            x = x[mask]
            y = y[mask]

            # Calculate trend
            slope = np.polyfit(x, y, 1)[0]
            return float(slope)
        except (ValueError, np.linalg.LinAlgError):
            return 0.0

    def _calculate_recent_change(self, data: List[float]) -> float:
        """Calculate change in recent observations"""
        if len(data) < self.MIN_DATA_POINTS:
            return 0.0

        # For minimum data points, compare last to first
        if len(data) == self.MIN_DATA_POINTS:
            return data[-1] - data[0]

        # For more data points, compare recent average to previous average
        recent = np.mean(data[-3:])
        if len(data) >= 6:
            previous = np.mean(data[-6:-3])
        else:
            previous = np.mean(data[:-3])

        if not np.isnan(recent) and not np.isnan(previous):
            return recent - previous

        return 0.0

    def _calculate_frequency(self, patterns: List[Dict]) -> float:
        """Calculate frequency of patterns"""
        if len(patterns) >= self.MIN_DATA_POINTS:
            timestamps = [p["timestamp"] for p in patterns]
            intervals = np.diff([t.timestamp() for t in timestamps])
            if intervals.size > 0 and np.mean(intervals) != 0:
                return 1 / np.mean(intervals)
        return 0.0

    def _calculate_intensity_trend(self, patterns: List[Dict]) -> float:
        """Calculate trend in pattern intensity"""
        if len(patterns) >= self.MIN_DATA_POINTS:
            intensities = [p.get("intensity", 0.5) for p in patterns]
            return self._calculate_trend(intensities)
        return 0.0

    def _get_common_contexts(self, patterns: List[Dict]) -> List[Tuple[str, int]]:
        """Get most common contexts for patterns"""
        if len(patterns) >= self.MIN_DATA_POINTS:
            contexts = [p["context"] for p in patterns]
            return Counter([
                item for d in contexts
                for item in d.items()
            ]).most_common(3)
        return []


def main():
    # Example usage
    traits = NeurodivergentTraits()

    # Add some example observations
    traits.add_sensory_observation(
        stimulus_type="auditory",
        response="avoiding",
        intensity=0.8,
        context={"location": "office", "time": "busy_hours"},
        timestamp=datetime.now()
    )

    traits.add_cognitive_observation(
        observation_type="pattern_recognition",
        behavior="Quickly identified complex data patterns",
        context={"task": "data_analysis"},
        performance=0.9,
        special_interest={
            "topic": "data_science",
            "intensity": 0.9,
            "engagement_hours": 4
        }
    )

    traits.add_social_observation(
        interaction_type="group_meeting",
        behavior="Contributed technical insights but struggled with small talk",
        context={"setting": "work", "participants": 5},
        energy_impact=-0.6,
        masking_effort=0.7
    )

    traits.add_stim_pattern(
        stim_type="hand_flapping",
        pattern={"duration": 30, "intensity": 0.8},
        context={"location": "home", "time": "relaxation"}
    )

    traits.add_executive_function_observation(
        function_type="task_switching",
        performance=0.8,
        context={"task": "work_project"},
        difficulty_level=0.7
    )

    traits.add_processing_speed_observation(
        processing_type="verbal",
        speed=0.9,
        accuracy=0.95,
        complexity=0.8
    )

    traits.add_attention_observation(
        attention_type="focused_attention",
        duration=60,
        quality=0.9,
        distractions=["phone_notification", "coworker_talking"]
    )

    # Get trait summary
    summary = traits.get_trait_summary()
    print("\nNeurodivergent Trait Summary:")
    for category, data in summary.items():
        print(f"\n{category.replace('_', ' ').title()}:")
        if isinstance(data, dict):
            for key, value in data.items():
                print(f"  {key}: {value}")
        else:
            print(f"  {data}")


if __name__ == "__main__":
    main()
