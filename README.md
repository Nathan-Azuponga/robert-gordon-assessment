# Dialogue Analysis App

## Overview

The **Dialogue Analysis App** is a Streamlit-based web application that processes, classifies, and visualizes dialogue from uploaded text files. It uses spaCy to classify utterances (e.g., Proposal, Query, Challenge), generates a flow diagram with Graphviz, and produces a concise narrative summary via the OpenAI API.

## Features

- **Upload Dialogue**: Upload a `.txt` file containing dialogue (format: "Speaker: Utterance").
- **Classify Utterances**: Labels each line as Proposal, Query, Challenge, Justification, Deferral, Commitment, or Other, with confidence scores.
- **Visualize Flow**: Displays a dialogue flow diagram using Graphviz.
- **Summarize Conversation**: Generates a concise narrative summary using OpenAI's `gpt-4o-mini` model.
- **Interactive UI**: Toggle confidence scores and diagram visibility, view results in a table.

## Requirements

- **Python**: 3.8 or higher
- **Dependencies**: Listed in `requirements.txt`:
  - streamlit==1.38.0
  - spacy==3.7.6
  - pandas==2.2.2
  - graphviz==0.20.3
  - openai==1.45.0
  - python-dotenv==1.0.1
  - torch==2.4.1

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Nathan-Azuponga/robert-gordon-assessment.git
   cd robert-gordon-assessment
   ```
2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate   # Windows
   ```
3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Download spaCy Model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```
5. **Set Up OpenAI API Key**:
   - Create a `.env` file in the project root.
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your-api-key-here
     ```
   - Get your key from [platform.openai.com](https://platform.openai.com).

## Usage

1. **Run the App**:
   ```bash
   streamlit run dialogue_app_enhanced.py
   ```
2. **Interact with the App**:
   - Open your browser (usually at `http://localhost:8501`).
   - Upload a `.txt` file with dialogue.
   - Click "Classify" to process and label utterances.
   - Toggle "Show/Hide Confidence Score" to view confidence values.
   - Click "Show Dialogue Flow" to see a visual diagram.
   - Click "Summarize" for a concise narrative summary.
