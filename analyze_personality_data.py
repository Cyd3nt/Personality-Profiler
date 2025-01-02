import json
from collections import defaultdict
from typing import Dict, List, Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


class PersonalityAnalyzer:
    def __init__(self, dataset: List[Dict]):
        self.dataset = dataset

    def analyze_behavioral_patterns(self) -> Dict[str, Dict[str, float]]:
        """Analyze behavioral response patterns for each personality type"""
        patterns = defaultdict(lambda: defaultdict(list))

        for person in self.dataset:
            ptype = person['type']
            for behavior in person['behavioral_responses']:
                situation_type = behavior['situation']
                effectiveness = behavior.get('context', {}).get('response_effectiveness', 0)
                patterns[ptype][situation_type].append(effectiveness)

        # Calculate average effectiveness for each situation type
        return {
            ptype: {
                situation: np.mean(scores) if scores else 0
                for situation, scores in situations.items()
            }
            for ptype, situations in patterns.items()
        }

    def analyze_emotional_trends(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """Analyze emotional response patterns"""
        trends = defaultdict(lambda: defaultdict(list))

        for person in self.dataset:
            ptype = person['type']
            for behavior in person['behavioral_responses']:
                for emotion, value in behavior.get('emotional_state', {}).items():
                    if isinstance(value, (int, float)):
                        trends[ptype][emotion].append(value)

        return {
            ptype: {
                emotion: {
                    'mean': float(np.mean(values)) if values else 0,
                    'std': float(np.std(values)) if values else 0,
                    'min': float(np.min(values)) if values else 0,
                    'max': float(np.max(values)) if values else 0
                }
                for emotion, values in emotions.items()
            }
            for ptype, emotions in trends.items()
        }

    def analyze_trait_correlations(self) -> pd.DataFrame:
        """Analyze correlations between personality traits"""
        trait_data = defaultdict(list)

        for person in self.dataset:
            for trait, value in person['vector'].items():
                if isinstance(value, (int, float)):
                    trait_data[trait].append(value)

        df = pd.DataFrame(trait_data)
        return df.corr()

    def visualize_personality_space(self, output_file: str = 'personality_space.png'):
        """Visualize personality types in 2D space using PCA"""
        vectors = []
        types = []

        for person in self.dataset:
            vector = [v for v in person['vector'].values() if isinstance(v, (int, float))]
            if vector:
                vectors.append(vector)
                types.append(person['type'])

        if not vectors:
            return

        # Standardize and reduce dimensionality
        scaler = StandardScaler()
        pca = PCA(n_components=2)
        vectors_2d = pca.fit_transform(scaler.fit_transform(vectors))

        # Plot
        plt.figure(figsize=(10, 8))
        for ptype in set(types):
            mask = [t == ptype for t in types]
            points = vectors_2d[mask]
            plt.scatter(points[:, 0], points[:, 1], label=ptype, alpha=0.6)

        plt.xlabel('First Principal Component')
        plt.ylabel('Second Principal Component')
        plt.title('Personality Types in 2D Space')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_file)
        plt.close()


class PersonalityDataAnalyzer(PersonalityAnalyzer):
    def __init__(self, dataset_path: str):
        super().__init__(self._load_dataset(dataset_path))
        self.personality_vectors = []
        self.behavioral_patterns = defaultdict(list)
        self.emotional_trends = defaultdict(list)
        self.response_effectiveness = defaultdict(list)

    def _load_dataset(self, path: str) -> List[Dict]:
        """Load personality dataset from JSON file"""
        with open(path, 'r') as f:
            return json.load(f)

    def analyze_personality_distribution(self) -> Dict[str, float]:
        """Analyze distribution of personality types"""
        type_counts = defaultdict(int)
        for person in self.dataset:
            type_counts[person['type']] += 1

        total = len(self.dataset)
        return {ptype: count / total for ptype, count in type_counts.items()}

    def generate_personality_profiles(self) -> Dict[str, Dict[str, Any]]:
        """Generate detailed profiles for each personality type"""
        profiles = defaultdict(lambda: {
            'traits': defaultdict(list),
            'behaviors': defaultdict(list),
            'emotions': defaultdict(list)
        })

        for person in self.dataset:
            ptype = person['type']

            # Aggregate trait values
            for trait, value in person['vector'].items():
                if isinstance(value, (int, float)):
                    profiles[ptype]['traits'][trait].append(value)

            # Aggregate behavioral responses
            for behavior in person['behavioral_responses']:
                profiles[ptype]['behaviors'][behavior['situation']].append(behavior['response'])

                # Aggregate emotional states
                for emotion, value in behavior.get('emotional_state', {}).items():
                    profiles[ptype]['emotions'][emotion].append(value)

        # Calculate averages and patterns
        return {
            ptype: {
                'traits': {
                    trait: np.mean(values)
                    for trait, values in profile['traits'].items()
                },
                'common_behaviors': {
                    situation: max(set(responses), key=responses.count)
                    for situation, responses in profile['behaviors'].items()
                },
                'emotional_profile': {
                    emotion: np.mean(values)
                    for emotion, values in profile['emotions'].items()
                }
            }
            for ptype, profile in profiles.items()
        }


def main():
    # Generate synthetic data
    from generate_synthetic_data import generate_synthetic_dataset
    dataset = generate_synthetic_dataset(num_personalities=50)

    # Save dataset
    output_path = 'personality_dataset.json'
    with open(output_path, 'w') as f:
        json.dump(dataset, f, indent=2, default=str)

    # Analyze data
    analyzer = PersonalityDataAnalyzer(output_path)

    print("\nPersonality Type Distribution:")
    distribution = analyzer.analyze_personality_distribution()
    for ptype, freq in distribution.items():
        print(f"  {ptype}: {freq:.1%}")

    print("\nBehavioral Pattern Analysis:")
    patterns = analyzer.analyze_behavioral_patterns()
    for ptype, situations in patterns.items():
        print(f"\n{ptype.title()} Type:")
        for situation, effectiveness in situations.items():
            print(f"  {situation}: {effectiveness:.2f} effectiveness")

    print("\nEmotional Trend Analysis:")
    trends = analyzer.analyze_emotional_trends()
    for ptype, emotions in trends.items():
        print(f"\n{ptype.title()} Type:")
        for emotion, stats in emotions.items():
            print(f"  {emotion}: mean={stats['mean']:.2f}, std={stats['std']:.2f}")

    print("\nGenerating Personality Space Visualization...")
    analyzer.visualize_personality_space()
    print("Visualization saved as 'personality_space.png'")


if __name__ == "__main__":
    main()
