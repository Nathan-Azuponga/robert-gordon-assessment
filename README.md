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
   git clone <repository-url>
   cd dialogue-analysis-app
   ```
2. **Set Up a Virtual Environment** (recommended):
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
   streamlit run your_script_name.py
   ```
2. **Interact with the App**:
   - Open your browser (usually at `http://localhost:8501`).
   - Upload a `.txt` file with dialogue (e.g., "Sam: I think we should integrate the chatbot.").
   - Click "Classify" to process and label utterances.
   - Toggle "Show/Hide Confidence Score" to view confidence values.
   - Click "Show Dialogue Flow" to see a visual diagram.
   - Click "Summarize" for a concise narrative summary.

## Example Input File

Create a `.txt` file (e.g., `dialogue.txt`):

```
Sam: I think we should integrate the chatbot into the main website.
Jamie: I’m not convinced - we’ve had issues with reliability.
Sam: True, but the latest version uses a more stable backend.
Jamie: Have we tested it under real user conditions?
Sam: Not yet. That’s on the roadmap for next month.
Jamie: Then maybe we hold off integration until those results are in.
Sam: Fair enough. I’ll prepare a status update for the next team meeting.
```

## Output

- **Classified Utterances**: Table with Speaker, Utterance, Label, and optional Confidence.
- **Dialogue Flow**: Visual diagram showing conversation progression.
- **Summary**: Narrative, e.g., "A proposal was made to integrate a chatbot. Concerns about reliability were raised..."
