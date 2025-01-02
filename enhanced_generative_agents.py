import random
import uuid
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Optional


@dataclass
class Observation:
    timestamp: datetime
    description: str
    importance: float
    location: str
    entities_involved: List[str]


class Memory:
    def __init__(self, description: str, timestamp: datetime, location: str):
        self.id = str(uuid.uuid4())
        self.description = description
        self.timestamp = timestamp
        self.location = location
        self.importance = self._calculate_importance()
        self.last_accessed = timestamp
        self.access_count = 0
        self.related_memories: List[str] = []  # IDs of related memories

    def _calculate_importance(self) -> float:
        # Implement the importance calculation based on:
        # - Recency
        # - Emotional significance
        # - Relevance to current goals
        # - Social impact
        base_importance = random.uniform(0.3, 0.8)
        return base_importance

    def access(self):
        self.last_accessed = datetime.now()
        self.access_count += 1


class Plan:
    def __init__(self, description: str, priority: float, deadline: Optional[datetime] = None):
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.status = "pending"  # pending, in_progress, completed, failed
        self.sub_tasks: List[str] = []


class GenerativeAgent:
    def __init__(self, name: str, age: int, archetype: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.age = age
        self.archetype = archetype
        self.personality = self._generate_personality()
        self.memories: List[Memory] = []
        self.current_location = "home"
        self.daily_schedule = self._generate_schedule()
        self.current_plan: Optional[Plan] = None
        self.observation_queue = deque(maxlen=50)  # Recent observations
        self.relationships: Dict[str, float] = {}  # Other agent IDs -> relationship strength
        self.emotional_state = {
            "valence": 0.0,  # -1 to 1
            "arousal": 0.0,  # -1 to 1
            "dominance": 0.0  # -1 to 1
        }

    def _generate_personality(self) -> Dict[str, float]:
        """Generate personality traits based on archetype and random variation"""
        base_traits = {
            "openness": 0.0,
            "conscientiousness": 0.0,
            "extraversion": 0.0,
            "agreeableness": 0.0,
            "neuroticism": 0.0,
            "empathy": 0.0,
            "creativity": 0.0,
            "ambition": 0.0
        }

        # Adjust traits based on archetype
        if self.archetype == "scholar":
            base_traits.update({
                "openness": 0.8,
                "conscientiousness": 0.7,
                "creativity": 0.6
            })
        elif self.archetype == "caregiver":
            base_traits.update({
                "empathy": 0.9,
                "agreeableness": 0.8,
                "conscientiousness": 0.6
            })
        # Add random variation
        return {k: min(1.0, max(-1.0, v + random.uniform(-0.2, 0.2)))
                for k, v in base_traits.items()}

    def _generate_schedule(self) -> Dict[int, str]:
        """Generate a daily schedule based on personality and archetype"""
        schedule = {}
        # 24-hour schedule with hourly activities
        for hour in range(24):
            if 0 <= hour < 6:
                schedule[hour] = "sleeping"
            elif 6 <= hour < 8:
                schedule[hour] = "morning_routine"
            elif 8 <= hour < 17:
                schedule[hour] = self._get_daytime_activity()
            elif 17 <= hour < 22:
                schedule[hour] = self._get_evening_activity()
            else:
                schedule[hour] = "preparing_for_bed"
        return schedule

    def _get_daytime_activity(self) -> str:
        if self.archetype == "scholar":
            return random.choice(["studying", "researching", "teaching", "writing"])
        elif self.archetype == "caregiver":
            return random.choice(["caring", "helping", "supporting", "organizing"])
        return "working"

    def _get_evening_activity(self) -> str:
        if self.personality["extraversion"] > 0.5:
            return random.choice(["socializing", "hobby", "entertainment"])
        return random.choice(["reading", "relaxing", "personal_time"])

    def observe(self, observation: Observation):
        """Process and store new observations"""
        self.observation_queue.append(observation)
        if observation.importance > 0.5:
            self._create_memory_from_observation(observation)

    def _create_memory_from_observation(self, observation: Observation):
        """Convert an observation into a long-term memory"""
        memory = Memory(
            description=observation.description,
            timestamp=observation.timestamp,
            location=observation.location
        )
        self.memories.append(memory)
        self._reflect_on_memory(memory)

    def _reflect_on_memory(self, memory: Memory):
        """Process memory and update agent's state based on its content"""
        # Update emotional state based on memory content
        if "positive" in memory.description.lower():
            self.emotional_state["valence"] = min(1.0, self.emotional_state["valence"] + 0.1)
        elif "negative" in memory.description.lower():
            self.emotional_state["valence"] = max(-1.0, self.emotional_state["valence"] - 0.1)

        # Link related memories
        self._find_related_memories(memory)

    def _find_related_memories(self, new_memory: Memory):
        """Find and link related memories based on content similarity"""
        for memory in self.memories[-50:]:  # Look at recent memories
            if memory.id != new_memory.id:
                # Simple keyword-based similarity for demonstration
                if any(word in memory.description.lower()
                       for word in new_memory.description.lower().split()):
                    memory.related_memories.append(new_memory.id)
                    new_memory.related_memories.append(memory.id)

    def plan_next_action(self) -> Optional[Plan]:
        """Decide on the next action based on current state and goals"""
        current_hour = datetime.now().hour
        scheduled_activity = self.daily_schedule.get(current_hour, "free_time")

        # Create a plan based on scheduled activity
        if scheduled_activity != self.current_plan:
            self.current_plan = Plan(
                description=f"Engage in {scheduled_activity}",
                priority=0.7
            )
        return self.current_plan

    def interact_with(self, other_agent: 'GenerativeAgent') -> str:
        """Generate interaction based on both agents' states"""
        # Calculate social compatibility
        compatibility = self._calculate_social_compatibility(other_agent)

        # Update relationship strength
        if other_agent.id not in self.relationships:
            self.relationships[other_agent.id] = 0.0

        interaction_quality = self._generate_interaction_quality(compatibility)
        self.relationships[other_agent.id] = min(1.0,
                                                 self.relationships[other_agent.id] + interaction_quality * 0.1)

        return self._generate_interaction_description(other_agent, interaction_quality)

    def _calculate_social_compatibility(self, other_agent: 'GenerativeAgent') -> float:
        """Calculate social compatibility based on personality traits and current states"""
        trait_compatibility = sum(
            1 - abs(self.personality[trait] - other_agent.personality[trait])
            for trait in self.personality
        ) / len(self.personality)

        emotional_compatibility = 1 - abs(
            self.emotional_state["valence"] - other_agent.emotional_state["valence"]
        ) / 2

        return (trait_compatibility * 0.7 + emotional_compatibility * 0.3)

    def _generate_interaction_quality(self, compatibility: float) -> float:
        """Generate interaction quality based on compatibility and random factors"""
        base_quality = compatibility * 0.8 + random.uniform(0, 0.2)
        return max(0.0, min(1.0, base_quality))

    def _generate_interaction_description(self, other_agent: 'GenerativeAgent',
                                          quality: float) -> str:
        """Generate a description of the interaction"""
        if quality > 0.8:
            return f"Had a deeply meaningful conversation with {other_agent.name}"
        elif quality > 0.6:
            return f"Enjoyed a pleasant interaction with {other_agent.name}"
        elif quality > 0.4:
            return f"Had a neutral exchange with {other_agent.name}"
        else:
            return f"Experienced some tension while interacting with {other_agent.name}"


def simulate_social_environment(agents: List[GenerativeAgent], days: int = 7):
    """Run a multi-day simulation of agent interactions"""
    print(f"\nStarting {days}-day simulation with {len(agents)} agents...")

    for day in range(days):
        print(f"\n=== Day {day + 1} ===")
        current_time = datetime(2024, 1, 1) + timedelta(days=day)

        # Morning reflection
        for agent in agents:
            print(f"\n{agent.name}'s Morning Reflection:")
            plan = agent.plan_next_action()
            if plan:
                print(f"- Planning to: {plan.description}")

        # Daily interactions
        for hour in range(9, 18):  # 9 AM to 6 PM
            current_time = current_time.replace(hour=hour)

            # Random interactions
            for _ in range(len(agents) // 2):
                agent1, agent2 = random.sample(agents, 2)

                # Create observation
                interaction_desc = agent1.interact_with(agent2)
                observation = Observation(
                    timestamp=current_time,
                    description=interaction_desc,
                    importance=random.uniform(0.3, 0.9),
                    location="common_area",
                    entities_involved=[agent1.name, agent2.name]
                )

                # Both agents observe the interaction
                agent1.observe(observation)
                agent2.observe(observation)

                print(f"\n{current_time.strftime('%H:%M')} - {interaction_desc}")

        # Evening reflection
        print("\nEvening Reflections:")
        for agent in agents:
            print(f"\n{agent.name}'s Status:")
            print(f"- Emotional state: {agent.emotional_state}")
            print(f"- Recent memories: {len(agent.memories[-5:]) if agent.memories else 0} new memories")
            print(f"- Relationship updates: {len(agent.relationships)} connections")


def main():
    # Create agents with different archetypes
    agents = [
        GenerativeAgent("Alice", 28, "scholar"),
        GenerativeAgent("Bob", 35, "caregiver"),
        GenerativeAgent("Charlie", 42, "scholar"),
        GenerativeAgent("Diana", 31, "caregiver")
    ]

    # Run simulation
    simulate_social_environment(agents, days=3)


if __name__ == "__main__":
    main()
