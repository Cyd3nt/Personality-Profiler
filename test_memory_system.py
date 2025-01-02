import unittest
from datetime import datetime, timedelta

from memory_system import MemoryNetwork, MemoryTrace


class TestMemoryNetwork(unittest.TestCase):
    def setUp(self):
        self.memory_network = MemoryNetwork()
        self.base_time = datetime.now()

    def test_initialization(self):
        """Test memory network initialization"""
        self.assertEqual(len(self.memory_network.memories), 0)
        self.assertEqual(len(self.memory_network.context_index), 0)
        self.assertEqual(len(self.memory_network.temporal_index), 0)
        self.assertEqual(len(self.memory_network.emotional_index), 0)
        self.assertEqual(len(self.memory_network.tag_index), 0)
        self.assertEqual(self.memory_network.capacity, 10000)

    def test_store_memory(self):
        """Test storing memories and index updates"""
        # Create a memory trace
        memory = MemoryTrace(
            content="Completed project milestone",
            timestamp=self.base_time,
            importance=0.8,
            emotional_valence=0.7,
            context={
                "location": "work",
                "activity": "project",
                "outcome": "success"
            },
            tags={"achievement", "work", "milestone"}
        )

        # Store memory
        memory_id = self.memory_network.store_memory(memory)

        # Check memory was stored
        self.assertIn(memory_id, self.memory_network.memories)
        self.assertEqual(self.memory_network.memories[memory_id], memory)

        # Check indices were updated
        self.assertIn("location:work", self.memory_network.context_index)
        self.assertIn("activity:project", self.memory_network.context_index)
        self.assertIn("outcome:success", self.memory_network.context_index)

        hour_key = memory.timestamp.strftime("%Y%m%d%H")
        self.assertIn(hour_key, self.memory_network.temporal_index)

        emotion_key = round(memory.emotional_valence * 10) / 10
        self.assertIn(emotion_key, self.memory_network.emotional_index)

        for tag in memory.tags:
            self.assertIn(tag, self.memory_network.tag_index)

    def test_memory_associations(self):
        """Test memory association creation and strength calculation"""
        # Create two related memories
        memory1 = MemoryTrace(
            content="Started new project",
            timestamp=self.base_time,
            importance=0.7,
            emotional_valence=0.6,
            context={"location": "work", "activity": "project"},
            tags={"project", "work", "planning"}
        )

        memory2 = MemoryTrace(
            content="Project team meeting",
            timestamp=self.base_time + timedelta(hours=1),
            importance=0.6,
            emotional_valence=0.5,
            context={"location": "work", "activity": "meeting"},
            tags={"project", "work", "team"}
        )

        # Store memories
        id1 = self.memory_network.store_memory(memory1)
        id2 = self.memory_network.store_memory(memory2)

        # Check associations were created
        self.assertIn(id2, memory1.associations)
        self.assertIn(id1, memory2.associations)

        # Check association strength
        strength = self.memory_network.association_strength[(id1, id2)]
        self.assertGreater(strength, 0.3)  # Above association threshold

    def test_memory_capacity(self):
        """Test memory capacity management"""
        # Create memories up to capacity
        for i in range(self.memory_network.capacity + 5):
            memory = MemoryTrace(
                content=f"Test memory {i}",
                timestamp=self.base_time + timedelta(minutes=i),
                importance=0.5,
                emotional_valence=0.0,
                context={"test": "capacity"},
                tags={"test"}
            )
            self.memory_network.store_memory(memory)

        # Check capacity is maintained
        self.assertLessEqual(
            len(self.memory_network.memories),
            self.memory_network.capacity
        )

    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        # Test invalid memory trace
        with self.assertRaises(ValueError):
            invalid_memory = MemoryTrace(
                content="",  # Empty content
                timestamp=self.base_time,
                importance=0.5,
                emotional_valence=0.0,
                context={},
                tags=set()
            )
            self.memory_network.store_memory(invalid_memory)

        with self.assertRaises(ValueError):
            invalid_memory = MemoryTrace(
                content="Test",
                timestamp=self.base_time,
                importance=1.5,  # Invalid importance
                emotional_valence=0.0,
                context={},
                tags=set()
            )
            self.memory_network.store_memory(invalid_memory)

        with self.assertRaises(ValueError):
            invalid_memory = MemoryTrace(
                content="Test",
                timestamp=self.base_time,
                importance=0.5,
                emotional_valence=2.0,  # Invalid valence
                context={},
                tags=set()
            )
            self.memory_network.store_memory(invalid_memory)

        # Test invalid context
        with self.assertRaises(TypeError):
            invalid_memory = MemoryTrace(
                content="Test",
                timestamp=self.base_time,
                importance=0.5,
                emotional_valence=0.0,
                context="invalid",  # Should be dict
                tags=set()
            )
            self.memory_network.store_memory(invalid_memory)


if __name__ == '__main__':
    unittest.main()
