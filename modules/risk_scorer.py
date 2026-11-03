def score_signals(signals):
    score=min(100, sum(s["weight"] for s in signals))
    label="Likely scam" if score>=65 else ("Suspicious" if score>=35 else "Likely safe")
    verdict={
        "Likely scam":"High-risk indicators found. Do not respond or share information.",
        "Suspicious":"Warning signs found. Verify independently before taking action.",
        "Likely safe":"Few common warning signs found. This is not proof that the message is safe."
    }[label]
    return {"risk_score":score,"classification":label,"verdict":verdict,"signals":signals}
