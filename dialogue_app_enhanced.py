import streamlit as st
import spacy
import os
from typing import List, Dict, Tuple
import pandas as pd
from graphviz import Digraph
from openai import OpenAI
import torch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

torch.classes.__path__ = []

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# --- Dialogue Classification Function ---
def classify_utterance(utterance: str) -> Tuple[str, float]:
    """
        Classify a single utterance into a dialogue act category based on rule-based approach.

        Confidence is calculated and capped at a maximum of 1.0.

        Parameters:
            utterance (str): A single line of dialogue in the format "Speaker: Utterance".

        Returns:
            Tuple[str, float]: A tuple containing the predicted label and a confidence score 
            between 0.0 and 1.0. Returns ("Other", 0.0) if no meaningful category is matched.
    """

    doc = nlp(utterance.lower())
    text = utterance.lower()
    max_confidence = 5.0

    scores = {}
    
    # Set words for rule base approach
    proposal_keywords = ["should", "let's", "i think we", "propose", "recommend", "suggest", "put forward", "offer", 
                         "could", "ought to", "How about", "What if", ]
    query_keywords = ["what", "how", "have we", "are we", "why", "which", "when", "where"]
    challenge_keywords = ["not", "don't", "i'm not", "disagree", "on the contrary", "but", "however", "unlikely", 
                         "doesn’t", "contradicts", "whereas", "challenge", "object"]
    justification_keywords = ["because", "since", "uses", "due to", "owing to", "thus", "hence", "for example", "for instance",
                              "this is because", "given that", "justify","prove", "true", "but"]
    deferral_keywords = ["not yet", "later", "on the roadmap", "eventually", "postpone", "sometime later", "next", "maybe", 
                         "postpone", "push back", "defer", "in the next phase", "in the future", "in due course", "not now"]
    commitment_keywords = ["i'll", "fair", "enough", "agree", "will", "sounds good", "going to", "commit"]

    # Calculte the confidence score 
    scores["Proposal"] = min(
        sum(1 for word in proposal_keywords if word in text) + sum(1 for token in doc if token.tag_ == "MD"),
        max_confidence) / max_confidence
 
    query_score = 1 if text.endswith("?") else 0
    query_score += sum(1 for q in query_keywords if text.startswith(q))

    scores["Query"] = min(query_score, max_confidence) / max_confidence
    scores["Challenge"] = min(sum(1 for word in challenge_keywords if word in text), max_confidence) / max_confidence
    scores["Justification"] = min(sum(1 for word in justification_keywords if word in text), max_confidence) / max_confidence
    scores["Deferral"] = min(sum(1 for word in deferral_keywords if word in text), max_confidence) / max_confidence
    scores["Commitment"] = min(sum(1 for word in commitment_keywords if word in text), max_confidence) / max_confidence

    # Determine the label with the highest confidence score
    best_label = max(scores, key=scores.get)
    confidence = scores[best_label]

    return ("Other", 0.0) if confidence == 0.0 else (best_label, confidence)

# --- Process Dialogue ---
def process_dialogue(file_content: str) -> List[Dict]:
    """
        Process a dialogue transcript and classify each utterance by dialogue act.

        Parameters:
            file_content (str): Each line representing one utterance.

        Returns:
            List[Dict]: A list of dictionaries, each containing:
                - 'Speaker' (str)
                - 'Utterance' (str)
                - 'Label' (str)
                - 'Confidence' (float)
    """

    results = []
    lines = file_content.strip().split("\n")
    for line in lines:
        if not line or ": " not in line:
            continue
        try:
            speaker, utterance = line.split(": ", 1)
            label, confidence = classify_utterance(utterance)
            results.append({"Speaker": speaker, "Utterance": utterance, "Label": label, "Confidence": confidence})
        except ValueError:
            st.warning(f"Skipping malformed line: {line}")
    return results

# --- Create Flow Diagram ---
def create_flow_diagram(results: List[Dict]) -> Digraph:
    """
        Generate a directed flow diagram representing the sequence of dialogue utterances.

        Parameters:
            results (List[Dict])
                - Speaker (str)
                - Utterance (str)
                - Label (str)

        Returns:
            Digraph: A Graphviz Digraph object representing the dialogue flow.
    """

    dot = Digraph(comment="Dialogue Flow")

    dot.attr(rankdir='HR', size='20,10', nodesep='1.0', ranksep='0.6') 

    for i, r in enumerate(results):
        label = f"{r['Speaker']}: {r['Label']}\\n\\\"{r['Utterance']}\\\""
        dot.node(str(i), label, shape='box', style='rounded,filled', fillcolor='lightblue')
        if i > 0:
            dot.edge(str(i - 1), str(i))

    return dot

# --- Generate summary of dialogue ---
def generate_llm_summary(dialogue_results: List[Dict]) -> str:
    """
        Generate a concise narrative summary of a dialogue using the OpenAI API.

        Parameters:
            dialogue_results (List[Dict])
                - 'Speaker' (str)
                - 'Utterance' (str)
                - 'Label' (str)

        Returns:
            str: A narrative summary of the dialogue structure.
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Define the summarization prompt
    prompt = (
        "Given the following dialogue where each utterance is labeled with its discourse act, "
        "write a concise narrative summary describing how the conversation progressed structurally. It should be as short and concise as possible. \n\n"
    )
    for turn in dialogue_results:
        prompt += f"{turn['Speaker']}: {turn['Utterance']} [{turn['Label']}]\n"

    prompt += "\nSummary (e.g., 'Sam proposes ..., Alex challenges...'):\n"

    # Call OpenAI API to generate summary
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant skilled at summarizing conversations concisely."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
        top_p=0.9
    )
    summary = response.choices[0].message.content

    return summary

# --- Streamlit UI ---
def main():
    st.set_page_config(page_title="Dialogue Analysis App", layout="wide")
    st.title("Dialogue Analysis App")
    st.write("Upload a dialogue file to classify utterances, visualize the flow, and summarize the conversation.")

    uploaded_file = st.file_uploader("Upload a dialogue .txt file", type="txt")

    # Initialize session state keys
    for key in ["results", "show_confidence", "summary", "toggle_confidence_clicked"]:
        if key not in st.session_state:
            st.session_state[key] = [] if key == "results" else False if key in ["show_confidence", "toggle_confidence_clicked"] else ""

    if uploaded_file is not None:
        try:
            file_content = uploaded_file.read().decode("utf-8")
            st.subheader("Original Dialogue")
            st.text(file_content)

            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

            with col1:
                classify_clicked = st.button("Classify")

            # Run classification
            if classify_clicked:
                st.session_state.results = process_dialogue(file_content)

            if st.session_state.results:
                # Handle toggle button manually
                with col3:
                    if st.button("Show/Hide Confidence Score"):
                        st.session_state.show_confidence = not st.session_state.show_confidence
                        st.session_state.toggle_confidence_clicked = True
                    else:
                        st.session_state.toggle_confidence_clicked = False

                with col4:
                    summarize_clicked = st.button("Summarize")

                # Show classified utterances
                st.subheader("Classified Utterances")
                df = pd.DataFrame(st.session_state.results)
                if not st.session_state.show_confidence:
                    df = df.drop(columns=["Confidence"], errors="ignore")
                st.dataframe(df, use_container_width=True)

                # Initialize toggle state if not already set
                if "show_dialogue" not in st.session_state:
                    st.session_state.show_dialogue = False

                # Define a toggle function to flip the state
                def toggle_dialogue_flow():
                    st.session_state.show_dialogue = not st.session_state.show_dialogue

                # Button label changes based on current state
                toggle_dialogue_label = "Hide Dialogue Flow" if st.session_state.show_dialogue else "Show Dialogue Flow"

                with col2:
                    st.button(toggle_dialogue_label, on_click=toggle_dialogue_flow)

                # Show the diagram only if toggled on
                if st.session_state.show_dialogue and st.session_state.results:
                    st.subheader("Dialogue Flow Diagram")
                    diagram = create_flow_diagram(st.session_state.results)
                    st.graphviz_chart(diagram.source)

                # Show summary if requested
                if summarize_clicked:
                    # Generate summary
                    with st.spinner("Generating summary..."):
                        summary = generate_llm_summary(st.session_state.results)
                    st.subheader("Dialogue Summary")
                    st.write(summary)

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    else:
        st.info("Please upload a dialogue file to begin.")

if __name__ == "__main__":
    main()
