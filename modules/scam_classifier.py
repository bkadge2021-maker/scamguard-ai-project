import re
from modules.risk_scorer import score_signals

RULES = [
    ("OTP / credential theft", 30, ["otp", "one-time password", "password", "pin", "login details", "verify your account", "bank details"]),
    ("Urgency / pressure", 18, ["urgent", "immediately", "act now", "within 24 hours", "today", "final warning", "in 2 hours"]),
    ("Account suspension threat", 22, ["account will be blocked", "account will be suspended", "account suspended", "sim deactivation", "service will be closed"]),
    ("Money / advance fee", 24, ["processing fee", "upfront fee", "release fee", "pay a fee", "transfer money", "send money", "gift card"]),
    ("Reward manipulation", 18, ["you have won", "congratulations", "claim your prize", "lottery winner", "free iphone", "prize"]),
    ("Fear / legal threat", 22, ["arrest warrant", "legal action", "police case", "account closure", "fine will be imposed"]),
    ("Fake authority / impersonation", 20, ["rbi", "police", "government", "tax department", "customs officer", "bank officer"]),
    ("Loan scam", 24, ["pre-approved loan", "guaranteed loan", "no credit checks", "loan release fee", "instant loan"]),
    ("Phishing link language", 12, ["click here", "verify here", "update your details", "restore access", "open this link"]),
]
def analyze_message(text):
    normalized = re.sub(r"\s+", " ", text.lower())
    signals=[]
    for label, weight, phrases in RULES:
        matches=[p for p in phrases if p in normalized]
        if matches:
            signals.append({"label":label,"weight":weight,"detail":"Matched: "+", ".join(matches[:4])})
    urls=re.findall(r"https?://[^\s<>()]+|www\.[^\s<>()]+", text, re.I)
    if urls:
        signals.append({"label":"Link present","weight":12,"detail":f"Found {len(urls)} URL(s); inspect before opening."})
    result=score_signals(signals)
    result.update({
        "scam_type": signals[0]["label"] if signals else "No clear scam category",
        "intent": "Local baseline detected observable scam-related phrases." if signals else "No common scam indicators matched; unexpected requests still need verification.",
        "evidence": [s["detail"] for s in signals],
        "recommendations": _tips(signals)
    })
    return result

def _tips(signals):
    labels=" ".join(s["label"] for s in signals).lower()
    tips=[]
    if "credential" in labels or "otp" in labels: tips.append("Never share OTPs, PINs, passwords, or recovery codes.")
    if "link" in labels or "phishing" in labels: tips.append("Do not use the message link; navigate to the official site or app yourself.")
    if "money" in labels or "loan" in labels or "reward" in labels: tips.append("Do not pay upfront fees to receive a loan, prize, or refund.")
    if "authority" in labels or "fear" in labels or "suspension" in labels: tips.append("Contact the organization through a verified official channel.")
    if not tips: tips.append("Verify unexpected requests using a separate trusted channel.")
    return tips + ["Do not forward or act on the message until verified."]
