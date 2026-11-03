import streamlit as st
import pandas as pd
from modules.gemini_analyzer import analyze_with_gemini, GeminiConfigurationError
from modules.scam_classifier import analyze_message
from modules.url_checker import analyze_url
from utils.dataset_loader import load_dataset, evaluate_dataset
from utils.history import add_history, get_history, clear_history

st.set_page_config(page_title="ScamGuard AI", page_icon="🛡️", layout="wide")
st.markdown("""
<style>
.stApp{background:#0b1220;color:#e8eef8}
[data-testid="stSidebar"]{background:#111c2e}
.hero{padding:1.5rem 1.7rem;border:1px solid #263750;border-radius:18px;background:linear-gradient(120deg,#14243b,#101a2b);margin-bottom:1rem}
.hero h1{margin:0;color:#f4f8ff;font-size:2.15rem}
.hero p{color:#aebed3;margin:.45rem 0 0}
div[data-testid="stMetric"]{background:#142238;border:1px solid #293d59;padding:14px;border-radius:13px}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🛡️ ScamGuard AI")
    st.caption("Context-aware scam detection and explanation")
    page = st.radio("NAVIGATION", ["Message Scanner", "URL Checker", "Dataset Evaluation", "Detection History", "About"])
    st.divider()
    use_gemini = st.toggle("Use Gemini AI", value=bool(__import__("os").getenv("GEMINI_API_KEY")))
    prompt_mode = st.selectbox("Prompt strategy", ["zero_shot", "few_shot", "dynamic_few_shot", "react"])
    st.caption("Gemini is optional. The local baseline works without an API key.")

if page == "Message Scanner":
    st.markdown('<div class="hero"><h1>🛡️ ScamGuard AI</h1><p>Context-aware scam detection · Intent analysis · Explainable risk scoring</p></div>', unsafe_allow_html=True)
    st.subheader("Analyze a message")
    sample_choice = st.selectbox("Try an example", ["Choose a sample", "OTP phishing", "Fake reward", "Loan scam", "Account suspension", "Legitimate message"])
    samples = {
        "OTP phishing": "URGENT: Your bank account will be blocked today. Verify your account immediately and share your OTP at http://secure-bank-login.example",
        "Fake reward": "Congratulations! You have won a phone. Pay a processing fee to claim your prize.",
        "Loan scam": "Pre-approved instant loan guaranteed. Pay an upfront release fee now. No credit checks.",
        "Account suspension": "Your account will be suspended in 2 hours. Click here to restore access and enter your password.",
        "Legitimate message": "Hi, are we still meeting at the library at 4 pm? I will bring the notes."
    }
    message = st.text_area("Message / email / SMS", value=samples.get(sample_choice, ""), height=170, placeholder="Paste the message here...")
    lang = st.selectbox("Message language", ["Auto / English", "Hindi", "Other / multilingual"])
    c1, c2 = st.columns([1, 1])
    run = c1.button("Analyze message", type="primary", use_container_width=True)
    if run:
        if not message.strip():
            st.warning("Enter a message first.")
        else:
            baseline = analyze_message(message)
            result = baseline
            if use_gemini:
                try:
                    result = analyze_with_gemini(message, prompt_mode=prompt_mode, language=lang, baseline=baseline)
                    result["engine"] = "Gemini AI + local indicators"
                except GeminiConfigurationError as e:
                    st.error(str(e))
                    result["engine"] = "Local fallback"
                except Exception as e:
                    st.error(f"Gemini request failed; showing local analysis instead. Details: {e}")
                    result["engine"] = "Local fallback"
            else:
                result["engine"] = "Local explainable baseline"
            add_history("message", message, result)
            st.divider()
            st.subheader("Analysis report")
            a,b,c = st.columns(3)
            a.metric("Risk score", f"{result['risk_score']}/100")
            b.metric("Classification", result["classification"])
            c.metric("Scam category", result.get("scam_type", "Unknown"))
            st.progress(result["risk_score"]/100)
            st.markdown(f"### {result.get('verdict', '')}")
            st.caption(f"Analysis engine: {result['engine']} · Prompt: {prompt_mode}")
            left,right = st.columns(2)
            with left:
                st.markdown("#### Detected indicators")
                for item in result.get("signals", []):
                    st.markdown(f"- **{item.get('label','Indicator')}** — {item.get('detail','')}")
                for item in result.get("evidence", []):
                    st.markdown(f"- **AI evidence:** {item}")
            with right:
                st.markdown("#### Manipulative intent")
                st.write(result.get("intent", "No AI intent summary available."))
                st.markdown("#### Recommended actions")
                for tip in result.get("recommendations", []):
                    st.markdown(f"- {tip}")
            with st.expander("Structured analysis output"):
                st.json(result)

elif page == "URL Checker":
    st.markdown('<div class="hero"><h1>🔗 URL Safety Checker</h1><p>Heuristic link inspection without visiting the submitted URL.</p></div>', unsafe_allow_html=True)
    url = st.text_input("URL", placeholder="https://example.com")
    if st.button("Check URL", type="primary"):
        if not url.strip():
            st.warning("Enter a URL.")
        else:
            result = analyze_url(url)
            add_history("url", url, result)
            x,y = st.columns(2)
            x.metric("Risk score", f"{result['risk_score']}/100")
            y.metric("Classification", result["classification"])
            st.progress(result["risk_score"]/100)
            for signal in result["signals"]:
                st.markdown(f"- **{signal['label']}** — {signal['detail']}")
            st.warning("This is a heuristic check, not a reputation lookup. Do not enter credentials on unfamiliar sites.")

elif page == "Dataset Evaluation":
    st.markdown('<div class="hero"><h1>📊 Dataset Evaluation</h1><p>Evaluate the local baseline against a CSV with text and label columns.</p></div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload scam dataset CSV", type=["csv"])
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
            st.write("Dataset preview", df.head(10))
            if st.button("Evaluate local classifier", type="primary"):
                report = evaluate_dataset(df)
                st.metric("Accuracy", f"{report['accuracy']:.1%}")
                st.metric("Rows evaluated", report["rows"])
                st.json(report["classification_report"])
                st.caption("This evaluates the rule-based baseline, not Gemini. Dataset quality and label balance affect results.")
        except Exception as e:
            st.error(f"Could not read/evaluate CSV: {e}")
    else:
        st.info("Expected columns: `text` and `label`. Upload your assignment dataset to evaluate it.")

elif page == "Detection History":
    st.markdown('<div class="hero"><h1>🧾 Detection History</h1><p>Recent analyses stored in this Streamlit session.</p></div>', unsafe_allow_html=True)
    rows = get_history()
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        if st.button("Clear history"):
            clear_history()
            st.rerun()
    else:
        st.info("No scans yet.")

else:
    st.markdown('<div class="hero"><h1>About ScamGuard AI</h1><p>A modular, explainable prototype for detecting digital communication scams.</p></div>', unsafe_allow_html=True)
    st.markdown("""
### Capabilities
- OTP fraud, phishing, account suspension, fake rewards, fear tactics, fake authority, loan scams and urgency indicators.
- Context-aware LLM analysis through the optional Gemini API.
- Zero-shot, few-shot, dynamic few-shot and ReAct-style tool workflow prompt strategies.
- Pydantic validation for Gemini structured output.
- Local URL heuristics and CSV evaluation.

### Important limitations
Gemini analysis requires your own API key. The app does not claim that chain-of-thought is exposed: it requests concise, user-facing rationale and evidence instead. The included local detector is a heuristic baseline, not a trained ML model. URL checks do not contact threat-intelligence databases or visit URLs. Multi-language analysis depends on the connected Gemini model and your API configuration.
""")
