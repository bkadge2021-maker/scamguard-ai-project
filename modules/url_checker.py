import re
from urllib.parse import urlparse
from modules.risk_scorer import score_signals

def analyze_url(value):
    candidate=value.strip()
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", candidate):
        candidate="https://"+candidate
    parsed=urlparse(candidate)
    host=(parsed.hostname or "").lower()
    signals=[]
    def add(label,weight,detail): signals.append({"label":label,"weight":weight,"detail":detail})
    if not host or "." not in host: add("Invalid or unusual hostname",35,"Hostname is missing or malformed.")
    if parsed.scheme!="https": add("No HTTPS",18,"URL does not use HTTPS; this alone does not prove fraud.")
    if "@" in parsed.netloc: add("Misleading URL structure",30,"An @ symbol may obscure the actual destination.")
    if len(host)>35: add("Unusually long hostname",12,"Long hostnames can disguise lookalike domains.")
    if host.count("-")>=2: add("Hyphen-heavy hostname",10,"Multiple hyphens can be a warning sign.")
    if re.search(r"\d{5,}",host): add("Long numeric sequence",12,"Hostname contains a long digit sequence.")
    found=[w for w in ["login","verify","secure","wallet","claim","bonus","banking","update"] if w in host]
    if found: add("Sensitive-action wording",12,"Hostname contains: "+", ".join(found))
    result=score_signals(signals)
    result["host"]=host or "Unrecognized"
    return result
