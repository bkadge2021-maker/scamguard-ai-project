# 🛡️ ScamGuard AI — Context-Aware Scam Detection

A modular Streamlit project for identifying suspicious digital messages and URLs. It combines an explainable local heuristic baseline with optional Google Gemini analysis, prompt strategies, Pydantic output validation, and CSV-based evaluation.

> **Honest implementation note:** Gemini features require your own API key. The default local detector is a rule-based baseline, not a trained machine-learning model. The assignment dataset was not supplied, so no dataset benchmark or accuracy claim is included. URL checks are local heuristics and do not query external threat databases.

## Features mapped to the problem statement

- **Scam categories:** OTP fraud, phishing cues, account suspension, fake rewards, fear tactics, fake authority, loan scams, urgency, payment requests.
- **Context-aware analysis:** Optional Gemini analysis of intent and manipulative context.
- **Prompt engineering:** Zero-shot, few-shot, dynamic few-shot, and ReAct-style tool workflow prompt modes.
- **Explainability:** Risk score, category, observable evidence, intent summary, and safety recommendations.
- **Structured validation:** Pydantic validates the Gemini JSON response.
- **Real-time UI:** Streamlit scanner, URL checker, history, and dataset evaluation.
- **Dataset evaluation:** Upload a CSV with `text` and `label` columns to evaluate the local baseline.
- **Modular design:** Separate prompt, Gemini, classifier, risk scoring, URL, schema, and dataset modules.

## Tech stack

Python 3.12+, Google Gemini API (`google-genai`), Streamlit, Pandas, python-dotenv, Pydantic, scikit-learn, Pytest.

## Project structure

```text
scamguard-ai/
├── app.py
├── config.py
├── modules/
│   ├── gemini_analyzer.py
│   ├── prompt_engineering.py
│   ├── scam_classifier.py
│   ├── risk_scorer.py
│   ├── schemas.py
│   └── url_checker.py
├── utils/
│   ├── dataset_loader.py
│   └── history.py
├── dataset/
│   └── README.md
├── tests/
│   └── test_detection.py
├── assets/
├── .env.example
├── .gitignore
└── requirements.txt
```

## Run locally

### 1. Create environment

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:
```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Gemini (optional)

Copy `.env.example` to `.env`, then add your own Gemini API key:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Never commit `.env` or publish API keys. The app works in local-baseline mode without a key.

### 4. Launch

```bash
streamlit run app.py
```

### 5. Run tests

```bash
pytest -q
```

## Dataset evaluation

Open **Dataset Evaluation** in the app and upload the assignment CSV. It must have:
- `text`: actual message
- `label`: scam or not_scam (similar label names are normalized)

The displayed metrics evaluate the local heuristic baseline. For a credible academic evaluation, use a representative labeled dataset, check class balance, create a held-out test set, and report precision, recall, F1-score, and confusion matrix. Do not tune and evaluate on the same rows.

## Prompt strategies

- **Zero-shot:** schema and task instructions without examples.
- **Few-shot:** fixed labeled examples guide classification.
- **Dynamic few-shot:** selects a small set of examples using simple text-token overlap. This is a starter retrieval method, not an embedding-based retriever.
- **ReAct-style:** asks the model to follow an inspect/evidence/assess workflow. This project does not expose private chain-of-thought or pretend to call unavailable external tools.

## Security, privacy, and limitations

- The app does not store scans in a database; history is session-local.
- Messages sent to Gemini are processed by Google's API under the user's account and applicable provider terms. Avoid submitting sensitive personal information.
- The URL checker does not visit URLs or use a threat-intelligence feed.
- Multi-language interpretation depends on the Gemini model; language selector is contextual guidance, not a translation guarantee.
- Risk scores are heuristic/model assessments, not calibrated probabilities or proof of fraud.
- Add threat-feed integrations, robust URL parsing, privacy review, rate limits, and human review before production deployment.

## Suggested GitHub demo screenshots

Capture your running Streamlit app and save:
- `assets/message-scan.png`
- `assets/url-check.png`
- `assets/dataset-evaluation.png`

## Author

Your Name · `https://github.com/YOUR-USERNAME`
