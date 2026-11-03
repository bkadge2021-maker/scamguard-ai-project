import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
from modules.scam_classifier import analyze_message

def load_dataset(path):
    df=pd.read_csv(path)
    return validate_dataset(df)

def validate_dataset(df):
    required={"text","label"}
    if not required.issubset(df.columns):
        raise ValueError("CSV must contain columns named 'text' and 'label'.")
    clean=df[["text","label"]].dropna().copy()
    clean["text"]=clean["text"].astype(str)
    clean["label"]=clean["label"].astype(str).str.lower().str.strip()
    return clean

def _normal_label(label):
    s=str(label).lower()
    return "scam" if any(x in s for x in ["scam","fraud","phish","spam"]) else "not_scam"

def evaluate_dataset(df):
    clean=validate_dataset(df)
    if clean.empty: raise ValueError("Dataset has no usable rows.")
    y_true=clean["label"].map(_normal_label)
    y_pred=clean["text"].map(lambda t: "scam" if analyze_message(t)["risk_score"]>=35 else "not_scam")
    return {
        "rows":len(clean),
        "accuracy":float(accuracy_score(y_true,y_pred)),
        "classification_report":classification_report(y_true,y_pred,output_dict=True,zero_division=0)
    }
