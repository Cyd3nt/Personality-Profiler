import json

from flask import Flask, render_template, request, jsonify

from emotional_model import EmotionalModel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production

# Initialize the emotional model with default personality traits
default_personality = {
    "openness": 0.7,
    "conscientiousness": 0.8,
    "extraversion": 0.6,
    "agreeableness": 0.7,
    "neuroticism": 0.4,
    "optimism": 0.6,
    "energy_level": 0.7,
    "confidence": 0.6,
    "emotional_stability": 0.7
}

emotional_model = EmotionalModel(default_personality)

# Load personality dataset
with open('personality_dataset.json', 'r') as f:
    personality_dataset = json.load(f)


# Extract unique questions for each trait
def extract_questions():
    questions = {}
    for person in personality_dataset:
        for trait, responses in person['interview_responses'].items():
            if trait not in questions:
                questions[trait] = set()
            questions[trait].update(responses)
    return {trait: list(qs) for trait, qs in questions.items()}


PERSONALITY_QUESTIONS = extract_questions()


@app.route('/')
def index():
    """Render the main interview interface."""
    return render_template('index.html', personality=default_personality)


@app.route('/questionnaire')
def questionnaire():
    """Render the questionnaire interface."""
    return render_template('questionnaire.html', questions=PERSONALITY_QUESTIONS)


@app.route('/process_event', methods=['POST'])
def process_event():
    """Process an emotional event and return the response."""
    try:
        data = request.get_json()
        event = data.get('event')
        context = data.get('context', {})
        intensity = float(data.get('intensity', 0.8))

        # Process the emotional event
        response = emotional_model.process_emotional_event(
            event=event,
            context=context,
            intensity=intensity
        )

        # Get the latest emotional memory
        memory = emotional_model.core.emotional_memory[-1] if emotional_model.core.emotional_memory else None
        memory_data = None
        if memory:
            memory_data = {
                'trigger': memory.trigger,
                'emotion_state': memory.emotion_state,
                'intensity': memory.intensity,
                'context': memory.context
            }

        return jsonify({
            'success': True,
            'response': response,
            'memory': memory_data,
            'current_state': emotional_model.core.current_state
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/get_state')
def get_state():
    """Get the current emotional state."""
    return jsonify({
        'success': True,
        'current_state': emotional_model.core.current_state,
        'personality': default_personality
    })


@app.route('/update_personality', methods=['POST'])
def update_personality():
    """Update the personality traits."""
    try:
        data = request.get_json()
        new_personality = {
            "openness": float(data.get('openness', default_personality['openness'])),
            "conscientiousness": float(data.get('conscientiousness', default_personality['conscientiousness'])),
            "extraversion": float(data.get('extraversion', default_personality['extraversion'])),
            "agreeableness": float(data.get('agreeableness', default_personality['agreeableness'])),
            "neuroticism": float(data.get('neuroticism', default_personality['neuroticism'])),
            "optimism": float(data.get('optimism', default_personality['optimism'])),
            "energy_level": float(data.get('energy_level', default_personality['energy_level'])),
            "confidence": float(data.get('confidence', default_personality['confidence'])),
            "emotional_stability": float(data.get('emotional_stability', default_personality['emotional_stability']))
        }

        # Create a new emotional model with updated personality
        global emotional_model
        emotional_model = EmotionalModel(new_personality)

        return jsonify({
            'success': True,
            'personality': new_personality
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/analyze_responses', methods=['POST'])
def analyze_responses():
    """Analyze questionnaire responses and determine personality traits."""
    try:
        data = request.get_json()
        responses = data.get('responses', {})

        # Calculate personality traits based on responses
        personality_scores = {
            "openness": 0.0,
            "conscientiousness": 0.0,
            "extraversion": 0.0,
            "agreeableness": 0.0,
            "neuroticism": 0.0,
            "optimism": 0.0,
            "energy_level": 0.0,
            "confidence": 0.0,
            "emotional_stability": 0.0
        }

        # Simple scoring: average the response values for each trait
        for trait, answers in responses.items():
            if answers:  # Check if there are any answers for this trait
                personality_scores[trait] = sum(float(score) for score in answers) / len(answers)

        # Update the emotional model with the new personality
        global emotional_model
        emotional_model = EmotionalModel(personality_scores)

        return jsonify({
            'success': True,
            'personality': personality_scores
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
