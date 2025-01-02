from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Set

import numpy as np


@dataclass
class MemoryTrace:
    content: str
    timestamp: datetime
    importance: float
    emotional_valence: float
    context: Dict[str, str]
    tags: Set[str]
    retrieval_count: int = 0
    last_accessed: Optional[datetime] = None
    associations: List[str] = None  # IDs of associated memories

    def __post_init__(self):
        """Validate memory trace attributes"""
        if not self.content:
            raise ValueError("Content must be a non-empty string")

        if not isinstance(self.timestamp, datetime):
            raise TypeError("Timestamp must be a datetime object")

        if not isinstance(self.importance, (int, float)) or not 0 <= self.importance <= 1:
            raise ValueError("Importance must be a float between 0 and 1")

        if not isinstance(self.emotional_valence, (int, float)) or not -1 <= self.emotional_valence <= 1:
            raise ValueError("Emotional valence must be a float between -1 and 1")

        if not isinstance(self.context, dict):
            raise TypeError("Context must be a dictionary")

        if not isinstance(self.tags, set):
            raise TypeError("Tags must be a set")

        if self.associations is None:
            self.associations = []
        elif not isinstance(self.associations, list):
            raise TypeError("Associations must be a list")

        if self.retrieval_count < 0:
            raise ValueError("Retrieval count cannot be negative")

        if self.last_accessed is not None and not isinstance(self.last_accessed, datetime):
            raise TypeError("Last accessed must be a datetime object")


@dataclass
class MemoryQuery:
    content: Optional[str] = None
    context: Optional[Dict[str, str]] = None
    time_range: Optional[Tuple[datetime, datetime]] = None
    tags: Optional[Set[str]] = None
    emotional_range: Optional[Tuple[float, float]] = None
    importance_threshold: Optional[float] = None


class MemoryNetwork:
    """Advanced associative memory network"""

    def __init__(self, capacity: int = 10000):
        self.memories: Dict[str, MemoryTrace] = {}
        self.capacity = capacity
        self.context_index = defaultdict(set)
        self.temporal_index = defaultdict(set)
        self.emotional_index = defaultdict(set)
        self.tag_index = defaultdict(set)
        self.importance_threshold = 0.3
        self.association_strength = defaultdict(float)

    def store_memory(self, memory: MemoryTrace) -> str:
        """Store a new memory and create associations"""
        # Validate memory trace
        if not isinstance(memory, MemoryTrace):
            raise TypeError("Memory must be a MemoryTrace object")

        # Additional validation of memory trace fields is handled by MemoryTrace.__post_init__

        # Generate unique ID
        memory_id = f"mem_{len(self.memories)}_{hash(memory.content)}"

        # Store memory
        self.memories[memory_id] = memory

        # Update indices
        self._update_indices(memory_id, memory)

        # Create associations
        self._create_associations(memory_id, memory)

        # Manage capacity
        self._manage_capacity()

        return memory_id

    def _update_indices(self, memory_id: str, memory: MemoryTrace) -> None:
        """Update all memory indices"""
        # Context index
        for context_key, context_value in memory.context.items():
            self.context_index[f"{context_key}:{context_value}"].add(memory_id)

        # Temporal index (by hour)
        hour_key = memory.timestamp.strftime("%Y%m%d%H")
        self.temporal_index[hour_key].add(memory_id)

        # Emotional index (discretized)
        emotion_key = round(memory.emotional_valence * 10) / 10
        self.emotional_index[emotion_key].add(memory_id)

        # Tag index
        for tag in memory.tags:
            self.tag_index[tag].add(memory_id)

    def _create_associations(self, memory_id: str, memory: MemoryTrace) -> None:
        """Create associations between memories"""
        for other_id, other_memory in self.memories.items():
            if other_id != memory_id:
                # Calculate association strength
                strength = self._calculate_association_strength(memory, other_memory)

                if strength > 0.3:  # Association threshold
                    memory.associations.append(other_id)
                    other_memory.associations.append(memory_id)
                    self.association_strength[(memory_id, other_id)] = strength
                    self.association_strength[(other_id, memory_id)] = strength

    def _calculate_association_strength(self,
                                        memory1: MemoryTrace,
                                        memory2: MemoryTrace) -> float:
        """Calculate association strength between two memories"""
        # Context similarity
        context_sim = len(set(memory1.context.items()) &
                          set(memory2.context.items())) / \
                      max(len(memory1.context), len(memory2.context))

        # Tag similarity
        tag_sim = len(memory1.tags & memory2.tags) / \
                  max(len(memory1.tags), len(memory2.tags)) if \
            (memory1.tags and memory2.tags) else 0

        # Temporal proximity (normalized to [0, 1])
        time_diff = abs((memory1.timestamp - memory2.timestamp).total_seconds())
        temporal_sim = 1 / (1 + time_diff / 3600)  # 1-hour scale

        # Emotional similarity
        emotional_sim = 1 - abs(memory1.emotional_valence -
                                memory2.emotional_valence)

        # Weighted combination
        weights = {
            "context": 0.3,
            "tags": 0.3,
            "temporal": 0.2,
            "emotional": 0.2
        }

        strength = (weights["context"] * context_sim +
                    weights["tags"] * tag_sim +
                    weights["temporal"] * temporal_sim +
                    weights["emotional"] * emotional_sim)

        return strength

    def _manage_capacity(self) -> None:
        """Manage memory capacity using importance-based forgetting"""
        if len(self.memories) > self.capacity:
            # Calculate memory scores
            memory_scores = {}
            for memory_id, memory in self.memories.items():
                # Score based on importance, recency, and retrieval count
                time_factor = 1 / (1 + (datetime.now() -
                                        memory.timestamp).total_seconds())
                score = (memory.importance * 0.4 +
                         time_factor * 0.3 +
                         (memory.retrieval_count / 10) * 0.3)
                memory_scores[memory_id] = score

            # Remove lowest scoring memories
            memories_to_remove = sorted(memory_scores.items(),
                                        key=lambda x: x[1])[:len(self.memories) -
                                                             self.capacity]

            for memory_id, _ in memories_to_remove:
                self._remove_memory(memory_id)

    def _remove_memory(self, memory_id: str) -> None:
        """Remove a memory and its references"""
        memory = self.memories[memory_id]

        # Remove from indices
        for context_key, context_value in memory.context.items():
            self.context_index[f"{context_key}:{context_value}"].discard(memory_id)

        hour_key = memory.timestamp.strftime("%Y%m%d%H")
        self.temporal_index[hour_key].discard(memory_id)

        emotion_key = round(memory.emotional_valence * 10) / 10
        self.emotional_index[emotion_key].discard(memory_id)

        for tag in memory.tags:
            self.tag_index[tag].discard(memory_id)

        # Remove associations
        for associated_id in memory.associations:
            if associated_id in self.memories:
                self.memories[associated_id].associations.remove(memory_id)
                del self.association_strength[(memory_id, associated_id)]
                del self.association_strength[(associated_id, memory_id)]

        # Remove memory
        del self.memories[memory_id]

    def retrieve_memories(self, query: MemoryQuery) -> List[Tuple[str, MemoryTrace]]:
        """Retrieve memories matching query parameters"""
        candidate_memories = set(self.memories.keys())

        # Apply filters
        if query.content:
            content_matches = {memory_id for memory_id, memory in
                               self.memories.items()
                               if query.content.lower() in
                               memory.content.lower()}
            candidate_memories &= content_matches

        if query.context:
            context_matches = set()
            for context_key, context_value in query.context.items():
                context_matches.update(
                    self.context_index[f"{context_key}:{context_value}"]
                )
            candidate_memories &= context_matches

        if query.time_range:
            start_time, end_time = query.time_range
            temporal_matches = set()
            current_time = start_time
            while current_time <= end_time:
                hour_key = current_time.strftime("%Y%m%d%H")
                temporal_matches.update(self.temporal_index[hour_key])
                current_time = current_time.replace(hour=current_time.hour + 1)
            candidate_memories &= temporal_matches

        if query.tags:
            tag_matches = set()
            for tag in query.tags:
                tag_matches.update(self.tag_index[tag])
            candidate_memories &= tag_matches

        if query.emotional_range:
            min_val, max_val = query.emotional_range
            emotional_matches = set()
            for val in np.arange(min_val, max_val + 0.1, 0.1):
                emotional_matches.update(
                    self.emotional_index[round(val * 10) / 10]
                )
            candidate_memories &= emotional_matches

        if query.importance_threshold is not None:
            importance_matches = {
                memory_id for memory_id, memory in self.memories.items()
                if memory.importance >= query.importance_threshold
            }
            candidate_memories &= importance_matches

        # Sort results by relevance
        results = [(memory_id, self.memories[memory_id])
                   for memory_id in candidate_memories]
        results.sort(key=lambda x: (-x[1].importance, -x[1].retrieval_count))

        # Update retrieval counts
        for memory_id, memory in results:
            memory.retrieval_count += 1
            memory.last_accessed = datetime.now()

        return results

    def get_associated_memories(self,
                                memory_id: str,
                                strength_threshold: float = 0.3,
                                max_results: int = 10) -> List[Tuple[str, float]]:
        """Get memories associated with a given memory"""
        if memory_id not in self.memories:
            return []

        # Get associations above threshold
        associations = [
            (other_id, self.association_strength[(memory_id, other_id)])
            for other_id in self.memories[memory_id].associations
            if self.association_strength[(memory_id, other_id)] >= strength_threshold
        ]

        # Sort by association strength
        associations.sort(key=lambda x: -x[1])
        return associations[:max_results]

    def get_memory_statistics(self) -> Dict[str, any]:
        """Get statistics about the memory network"""
        return {
            "total_memories": len(self.memories),
            "average_importance": np.mean([m.importance for m in self.memories.values()]),
            "average_retrieval_count": np.mean([m.retrieval_count for m in
                                                self.memories.values()]),
            "total_associations": sum(len(m.associations) for m in
                                      self.memories.values()) // 2,
            "memory_age_range": (
                min(m.timestamp for m in self.memories.values()),
                max(m.timestamp for m in self.memories.values())
            ) if self.memories else None
        }


def main():
    # Example usage
    memory_network = MemoryNetwork()

    # Create some sample memories
    memories = [
        MemoryTrace(
            content="Had a great conversation about AI",
            timestamp=datetime.now(),
            importance=0.8,
            emotional_valence=0.7,
            context={"location": "office", "activity": "meeting"},
            tags={"AI", "work", "conversation"}
        ),
        MemoryTrace(
            content="Felt anxious about the presentation",
            timestamp=datetime.now(),
            importance=0.6,
            emotional_valence=-0.4,
            context={"location": "office", "activity": "presentation"},
            tags={"work", "presentation", "anxiety"}
        )
    ]

    # Store memories
    for memory in memories:
        memory_id = memory_network.store_memory(memory)
        print(f"\nStored memory: {memory_id}")
        print(f"Content: {memory.content}")

    # Query memories
    query = MemoryQuery(
        context={"location": "office"},
        tags={"work"},
        importance_threshold=0.5
    )

    print("\nRetrieving memories:")
    results = memory_network.retrieve_memories(query)
    for memory_id, memory in results:
        print(f"\nMemory ID: {memory_id}")
        print(f"Content: {memory.content}")
        print(f"Importance: {memory.importance}")
        print(f"Emotional Valence: {memory.emotional_valence}")

    # Get statistics
    print("\nMemory Network Statistics:")
    stats = memory_network.get_memory_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
