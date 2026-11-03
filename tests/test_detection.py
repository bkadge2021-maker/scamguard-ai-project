import pandas as pd
from modules.scam_classifier import analyze_message
from modules.url_checker import analyze_url
from utils.dataset_loader import evaluate_dataset

def test_otp_and_urgency_flagged():
    r=analyze_message("URGENT: share your OTP immediately or account will be blocked")
    assert r["risk_score"] >= 65
    assert r["classification"] == "Likely scam"

def test_safe_text_low_score():
    r=analyze_message("Are we meeting at the library at 4 pm?")
    assert r["risk_score"] < 35

def test_loan_scam_rule():
    r=analyze_message("Pre-approved loan guaranteed. Pay an upfront release fee.")
    assert r["risk_score"] >= 35

def test_url_output():
    r=analyze_url("http://login-secure-bank.example")
    assert 0 <= r["risk_score"] <= 100

def test_dataset_eval():
    df=pd.DataFrame({"text":["share your OTP urgently","hello see you soon"],"label":["scam","not_scam"]})
    report=evaluate_dataset(df)
    assert report["rows"] == 2
