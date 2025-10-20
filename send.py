import json, os, random, pathlib, sys
if not uniq:
raise RuntimeError("No quotes found in quotes.json")
return uniq




def load_state(total):
if STATE_PATH.exists():
with open(STATE_PATH, "r", encoding="utf-8") as f:
state = json.load(f)
# Defensive: if quotes were added/removed, rebuild order when needed
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
# cycle completed — reshuffle a new permutation
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
body = f"\U0001F9D8 Stoic Minute ({datetime.now().strftime('%Y-%m-%d')}):\n“{quote['text']}” — {quote['author']}"
sid = send_whatsapp(body)
save_state(state)
print("Sent:", sid)




if __name__ == "__main__":
try:
main()
except Exception as e:
print("ERROR:", e)
sys.exit(1)