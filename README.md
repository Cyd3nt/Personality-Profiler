# Generative Agent Simulation with Emotional Modeling

## Overview

This project implements an advanced framework for simulating artificial agents with dynamic personalities, memories, and
emotional responses. It features a comprehensive personality assessment system with adaptive questioning and a web-based
interface for emotional interaction simulation.

## Key Features

- Comprehensive Personality Assessment (500+ questions)
- Adaptive Follow-up Questioning System
- Advanced Emotional Modeling
- Interactive Web Interface
- Real-time Emotional Response Simulation
- Personality Trait Analysis
- Memory Integration

## Assessment System

### Initial Assessment

- 500 carefully crafted questions across multiple dimensions:
    - Traditional Personality Traits (openness, conscientiousness, etc.)
    - Emotional Traits (emotional resilience, empathy, etc.)
    - Moral Dimensions (fairness, care, loyalty, etc.)

### Adaptive Assessment

- Dynamic generation of 50 personalized follow-up questions
- Questions adapt based on:
    - Initial assessment responses
    - High-scoring traits (≥0.7)
    - Low-scoring traits (≤0.3)
    - Interesting trait interactions
    - Moral dilemmas and scenarios

### Moral Compass Dimensions

1. **Fairness**: Justice, equality, and fair treatment
2. **Care**: Compassion and concern for others
3. **Loyalty**: Group values and relationships
4. **Authority**: Respect for leadership and structure
5. **Sanctity**: Sacred values and traditions
6. **Responsibility**: Personal accountability
7. **Honesty**: Truth and transparency
8. **Courage**: Standing up for beliefs
9. **Wisdom**: Ethical reasoning
10. **Temperance**: Self-control and moderation

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Safari, or Edge)

### Setup Instructions

1. Clone the repository:

```bash
git clone <repository-url>
cd personality
```

2. Create a virtual environment (recommended):

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run streamlit_app.py
```

## Using the Application

### Initial Personality Assessment

1. Navigate to the "Initial Assessment" tab
2. Complete the comprehensive questionnaire (500 questions)
3. Submit your responses to generate your personality profile
4. View your trait analysis and proceed to adaptive assessment

### Adaptive Assessment

1. Go to the "Adaptive Assessment" tab
2. Answer personalized follow-up questions
3. Provide detailed responses to scenario-based questions
4. Get deeper insights into your personality traits

### Emotional Chat Interface

1. Access the "Emotional Chat" tab
2. Interact with the emotional model through chat
3. Observe real-time emotional state changes
4. View emotional state visualizations

## Data Storage

### Output Directory Structure

```
output/
├── personality_results/     # Initial assessment results
├── adaptive_questions/      # Generated adaptive questions
├── adaptive_responses/      # Responses to adaptive questions
├── chat_history/           # Chat interaction logs
└── emotional_states/       # Emotional state snapshots
```

## Personality Framework with Advanced Emotional Model

A sophisticated personality framework featuring:

- Multi-dimensional emotion tracking
- Emotional memory integration
- Valence-Arousal-Dominance (VAD) model
- Configurable emotional intensity
- Complex phrase recognition

### Core Components

1. **Emotional Model**
    - Joy, sadness, anger, fear, trust, surprise
    - Emotional state transitions
    - Context maintenance

2. **Adaptive Question Generator**
    - Dynamic template system
    - Scenario-based questions
    - Trait interaction analysis

3. **Data Analysis**
    - Personality trait scoring
    - Moral compass evaluation
    - Emotional pattern recognition

## Quick Start

```python
from emotional_model import EmotionalModel
from adaptive_questions import AdaptiveQuestionGenerator

# Initialize models
emotional_model = EmotionalModel(DEFAULT_PERSONALITY)
question_generator = AdaptiveQuestionGenerator()

# Generate adaptive questions
adaptive_questions = question_generator.generate_adaptive_questions(
    personality_scores,
    previous_responses
)
```

## Contributing

Contributions are welcome! Please read our contributing guidelines and code of conduct before submitting pull requests.
