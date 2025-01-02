import json
from datetime import datetime
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from adaptive_questions import AdaptiveQuestionGenerator
from emotional_model import EmotionalModel

# Create output directories if they don't exist
OUTPUT_DIR = Path("output")
PERSONALITY_DIR = OUTPUT_DIR / "personality_results"
CHAT_DIR = OUTPUT_DIR / "chat_history"
EMOTIONAL_DIR = OUTPUT_DIR / "emotional_states"

for directory in [OUTPUT_DIR, PERSONALITY_DIR, CHAT_DIR, EMOTIONAL_DIR]:
    directory.mkdir(exist_ok=True)

# Default personality traits
DEFAULT_PERSONALITY = {
    "optimism": 0.5,
    "energy_level": 0.5,
    "confidence": 0.5,
    "emotional_stability": 0.5,
    "openness": 0.5,
    "conscientiousness": 0.5,
    "extraversion": 0.5,
    "agreeableness": 0.5,
    "neuroticism": 0.5
}

# Initialize session state
if 'emotional_model' not in st.session_state:
    st.session_state.emotional_model = EmotionalModel(DEFAULT_PERSONALITY)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'personality_scores' not in st.session_state:
    st.session_state.personality_scores = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
if 'adaptive_generator' not in st.session_state:
    st.session_state.adaptive_generator = AdaptiveQuestionGenerator()
if 'adaptive_questions' not in st.session_state:
    st.session_state.adaptive_questions = None
if 'previous_responses' not in st.session_state:
    st.session_state.previous_responses = {}


def save_personality_results(personality_scores):
    """Save personality assessment results"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = PERSONALITY_DIR / f"personality_assessment_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(personality_scores, f, indent=4)
    return filename


def save_chat_history(chat_history):
    """Save chat history"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = CHAT_DIR / f"chat_history_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(chat_history, f, indent=4)
    return filename


def save_emotional_state(emotional_state):
    """Save emotional state snapshot"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = EMOTIONAL_DIR / f"emotional_state_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(emotional_state, f, indent=4)
    return filename


def load_questions():
    """Load personality assessment questions"""
    try:
        with open('questions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Questions file not found. Please make sure questions.json exists in the project directory.")
        return None


def create_emotion_radar_chart(emotional_state):
    emotions = list(emotional_state.keys())
    values = list(emotional_state.values())
    values.append(values[0])
    emotions.append(emotions[0])

    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=emotions,
        fill='toself',
        line=dict(color='rgb(67, 147, 195)'),
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        showlegend=False,
        title="Current Emotional State"
    )
    return fig


def map_questionnaire_to_personality(trait_scores):
    """Map questionnaire scores to emotional model personality traits"""
    # Convert 1-5 scale to 0-1 scale
    normalized_scores = {k: (v - 1) / 4 for k, v in trait_scores.items()}

    return {
        "optimism": 1 - normalized_scores.get("neuroticism", 0.5),  # Inverse of neuroticism
        "energy_level": normalized_scores.get("extraversion", 0.5),
        "confidence": normalized_scores.get("extraversion", 0.5) * 0.7 + normalized_scores.get("neuroticism",
                                                                                               0.5) * -0.3,
        "emotional_stability": 1 - normalized_scores.get("neuroticism", 0.5),
        "openness": normalized_scores.get("openness", 0.5),
        "conscientiousness": normalized_scores.get("conscientiousness", 0.5),
        "extraversion": normalized_scores.get("extraversion", 0.5),
        "agreeableness": normalized_scores.get("agreeableness", 0.5),
        "neuroticism": normalized_scores.get("neuroticism", 0.5)
    }


def main():
    st.set_page_config(page_title="Emotional AI Interface", layout="wide")

    st.title("Personality Assessment and Emotional Chat Interface")

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Initial Assessment", "Adaptive Assessment", "Emotional Chat"])

    with tab1:
        if st.session_state.personality_scores is None:
            st.header("Personality Assessment")
            questions = load_questions()

            with st.form("personality_assessment"):
                responses = {}
                for trait, trait_questions in questions.items():
                    st.subheader(trait.replace('_', ' ').title())
                    for i, question in enumerate(trait_questions):
                        key = f"{trait}_{i}"
                        responses[key] = st.slider(
                            question,
                            min_value=1,
                            max_value=5,
                            value=3,
                            key=key
                        )

                if st.form_submit_button("Submit Assessment"):
                    # Calculate trait scores
                    trait_scores = {}
                    for trait in questions.keys():
                        trait_responses = [responses[f"{trait}_{i}"] for i in range(len(questions[trait]))]
                        trait_scores[trait] = sum(trait_responses) / (len(trait_responses) * 5)  # Normalize to 0-1

                    st.session_state.personality_scores = trait_scores
                    st.session_state.previous_responses = responses

                    # Save results
                    save_personality_results(trait_scores)

                    # Generate adaptive questions
                    st.session_state.adaptive_questions = st.session_state.adaptive_generator.generate_adaptive_questions(
                        trait_scores,
                        st.session_state.previous_responses
                    )

                    st.success("Assessment completed! Please proceed to the Adaptive Assessment tab.")
        else:
            st.success("Initial assessment completed! Please proceed to the Adaptive Assessment tab.")
            if st.button("Retake Initial Assessment"):
                st.session_state.personality_scores = None
                st.session_state.previous_responses = {}
                st.session_state.adaptive_questions = None
                st.rerun()

    with tab2:
        if st.session_state.personality_scores is not None and st.session_state.adaptive_questions is not None:
            st.header("Adaptive Assessment")
            st.write("Based on your initial responses, here are some follow-up questions:")

            with st.form("adaptive_assessment"):
                adaptive_responses = {}
                for i, q in enumerate(st.session_state.adaptive_questions):
                    key = f"adaptive_{i}"
                    st.write(f"**Question {i + 1}:** {q['question']}")
                    st.write(f"*Category: {q['category'].replace('_', ' ').title()}*")
                    adaptive_responses[key] = st.text_area(
                        "Your response:",
                        key=key,
                        height=100
                    )

                if st.form_submit_button("Submit Adaptive Assessment"):
                    # Save adaptive responses
                    output_dir = Path("output/adaptive_responses")
                    output_dir.mkdir(exist_ok=True)

                    results = {
                        "initial_scores": st.session_state.personality_scores,
                        "adaptive_questions": st.session_state.adaptive_questions,
                        "adaptive_responses": adaptive_responses
                    }

                    filename = output_dir / f"adaptive_responses_{st.session_state.session_id}.json"
                    with open(filename, 'w') as f:
                        json.dump(results, f, indent=4)

                    st.success("Adaptive assessment completed! Your responses have been saved.")
                    st.rerun()
        else:
            st.info("Please complete the initial assessment first.")

    with tab3:
        st.header("Emotional Chat")

        # Display current emotional state
        if st.session_state.emotional_model:
            current_state = st.session_state.emotional_model.get_emotional_state()
            fig = create_emotion_radar_chart(current_state)
            st.plotly_chart(fig)

            # Save emotional state periodically
            if len(st.session_state.chat_history) % 5 == 0:  # Save every 5 messages
                save_emotional_state(current_state)

        # Chat interface
        col1, col2 = st.columns([3, 1])

        with col1:
            # Display chat history
            for message in st.session_state.chat_history:
                if message["role"] == "user":
                    st.write("You: " + message["content"])
                else:
                    st.write("AI: " + message["content"])

            # Chat input
            user_input = st.text_input("Type your message:", key="user_input")
            if st.button("Send"):
                if user_input:
                    # Add user message to history
                    st.session_state.chat_history.append({"role": "user", "content": user_input})

                    # Process emotional event
                    response = st.session_state.emotional_model.process_emotional_event(
                        event=user_input,
                        intensity=0.8
                    )

                    # Add AI response to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"Emotional Response: {response}"
                    })

                    # Save chat history
                    save_chat_history(st.session_state.chat_history)

                    # Clear input
                    st.rerun()

        with col2:
            if st.button("Clear Chat"):
                # Save final chat history before clearing
                if st.session_state.chat_history:
                    save_chat_history(st.session_state.chat_history)
                st.session_state.chat_history = []
                st.rerun()


if __name__ == "__main__":
    main()
