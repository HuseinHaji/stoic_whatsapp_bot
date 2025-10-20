import json, os, random, pathlib, sys
from datetime import datetime
from twilio.rest import Client

# --- ENV VARS ---
ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN  = os.environ["TWILIO_AUTH_TOKEN"]
FROM_WHATS  = os.environ.get("TWILIO_FROM", "whatsapp:+14155238886")  # Twilio Sandbox default
TO_WHATS    = os.environ["TO_WHATSAPP"]  # e.g., "whatsapp:+49XXXXXXXXXX"

ROOT = pathlib.Path(__file__).parent
QUOTES_PATH = ROOT / "quotes.json"
STATE_PATH  = ROOT / "state.json"

def load_quotes():
    with open(QUOTES_PATH, "r", encoding="utf-8") as f:
        quotes = json.load(f)
    # Normalize & dedupe
    seen, uniq = set(), []
    for q in quotes:
        text = q["text"].strip()
        author = q.get("author", "").strip()
        key = (text, author)
        if key not in seen:
            seen.add(key)
            uniq.append({"text": text, "author": author})
    if not uniq:
        raise RuntimeError("No quotes found in quotes.json")
    return uniq

def load_state(total):
    if STATE_PATH.exists():
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
        N = total
        order = state.get("order", [])
        idx = state.get("idx", 0)
        if len(order) != N:
            order = list(range(N))
            random.shuffle(order)
            idx = 0
            state = {"order": order, "idx": idx}
    else:
        order = list(range(total))
        random.shuffle(order)
        state = {"order": order, "idx": 0}
    return state

def save_state(state):
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def pick_next(quotes, state):
    order, idx = state["order"], state["idx"]
    if idx >= len(order):
        order = list(range(len(quotes)))
        random.shuffle(order)
        idx = 0
    qidx = order[idx]
    state["order"], state["idx"] = order, idx + 1
    return quotes[qidx], state

def send_whatsapp(body):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    msg = client.messages.create(from_=FROM_WHATS, to=TO_WHATS, body=body)
    return msg.sid

def main():
    quotes = load_quotes()
    state = load_state(len(quotes))
    quote, state = pick_next(quotes, state)
    body = f"🧘 Stoic Minute ({datetime.now().strftime('%Y-%m-%d')}):\n“{quote['text']}” — {quote['author']}"
    sid = send_whatsapp(body)
    save_state(state)
    print("Sent:", sid)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)
