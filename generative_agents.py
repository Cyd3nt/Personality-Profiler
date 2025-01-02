import random
import uuid
from datetime import datetime
from typing import List


class PersonalityTrait:
    def __init__(self, name: str, intensity: float):
        self.name = name
        self.intensity = intensity  # -1 to 1 scale


class Memory:
    def __init__(self, description: str, timestamp: datetime):
        self.id = str(uuid.uuid4())
        self.description = description
        self.timestamp = timestamp
        self.importance = self._calculate_importance()

    def _calculate_importance(self) -> float:
        # Recency, emotional intensity, and potential social impact
        return random.uniform(0.1, 1.0)


class GenerativeAgent:
    def __init__(self, name: str, age: int):
        self.id = str(uuid.uuid4())
        self.name = name
        self.age = age
        self.personality_traits = self._generate_personality()
        self.memories: List[Memory] = []
        self.current_goals = []

    def _generate_personality(self) -> List[PersonalityTrait]:
        trait_names = [
            "Openness", "Conscientiousness", "Extraversion",
            "Agreeableness", "Neuroticism"
        ]
        return [
            PersonalityTrait(name, random.uniform(-1, 1))
            for name in trait_names
        ]

    def add_memory(self, description: str):
        memory = Memory(description, datetime.now())
        self.memories.append(memory)
        self._reflect_on_memory(memory)

    def _reflect_on_memory(self, memory: Memory):
        # Simulate cognitive processing of memories
        if memory.importance > 0.7:
            print(f"{self.name} is deeply processing: {memory.description}")

    def interact_with(self, other_agent: 'GenerativeAgent'):
        # Simulate social interaction based on personality
        compatibility = self._calculate_social_compatibility(other_agent)
        interaction_outcome = self._generate_interaction_response(compatibility)
        return interaction_outcome

    def _calculate_social_compatibility(self, other_agent: 'GenerativeAgent') -> float:
        # Calculate social compatibility based on personality traits
        trait_differences = sum(
            abs(t1.intensity - t2.intensity)
            for t1, t2 in zip(self.personality_traits, other_agent.personality_traits)
        )
        return 1 - (trait_differences / len(self.personality_traits))

    def _generate_interaction_response(self, compatibility: float) -> str:
        responses = [
            "friendly and engaging",
            "polite but distant",
            "awkward and uncomfortable",
            "warm and welcoming"
        ]
        return random.choice(responses) if compatibility > 0.5 else random.choice(responses[2:])


def simulate_social_environment(agents: List[GenerativeAgent], days: int = 7):
    for day in range(days):
        print(f"\n--- Day {day + 1} Simulation ---")
        for agent in agents:
            # Random memory generation
            agent.add_memory(f"Experienced a notable event on day {day}")

        # Random interactions
        for _ in range(len(agents) * 2):
            agent1, agent2 = random.sample(agents, 2)
            interaction = agent1.interact_with(agent2)
            print(f"{agent1.name} interacted with {agent2.name}: {interaction}")


# Example Usage
def main():
    agents = [
        GenerativeAgent("Alice", 28),
        GenerativeAgent("Bob", 35),
        GenerativeAgent("Charlie", 42)
    ]
    simulate_social_environment(agents)


if __name__ == "__main__":
    main()
