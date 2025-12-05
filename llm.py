# llm.py
import os
import json
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# If you have openai installed and a key, this will call the model.
# Keep calls concise to avoid large token usage.


def parse_receipt_with_fallback(text):
    """Parse receipt text into structured JSON using simple heuristics (fallback)."""
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    data = {
        "store": None,
        "date": None,
        "total": None,
        "items": [],
        "category": None,
        "summary": None
    }
    # Heuristics: last line with word 'total' or 'amount' -> total
    for l in reversed(lines[-10:]):
        low = l.lower()
        if 'total' in low or 'amount' in low:
            # extract numbers
            import re
            m = re.search(r"([0-9]+(?:[.,][0-9]{1,2})?)", l)
            if m:
                data['total'] = m.group(1)
                break
    # store => first line
    if lines:
        data['store'] = lines[0]
    # items: lines that look like "name number"
    import re
    for l in lines:
        m = re.match(r"^(.+)\s+([0-9]+(?:[.,][0-9]{1,2})?)$", l)
        if m:
            name = m.group(1).strip()
            price = m.group(2)
            data['items'].append({"name": name, "price": price})
    data['summary'] = f"Detected {len(data['items'])} items, total {data['total']}"
    # naive category
    data['category'] = 'Groceries' if any(i for i in data['items']) else 'Other'
    return data


# Optional: OpenAI usage
try:
    import openai
except Exception:
    openai = None




def parse_receipt_via_openai(text):
    if not OPENAI_API_KEY or openai is None: # type: ignore
        return parse_receipt_with_fallback(text)
    openai.api_key = OPENAI_API_KEY
    prompt = f"Extract the following fields from this receipt text and return JSON only: store, date, total, items(list of {{name, price}}), category, summary. Receipt text:\n\n{text}"
    try:
        resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=400,
        temperature=0
        )
        content = resp['choices'][0]['message']['content']
        # try to parse JSON directly
        import re
        m = re.search(r"\{.*\}", content, re.S)
        if m:
            return json.loads(m.group(0))
        else:
            # fallback
            return parse_receipt_with_fallback(text)
    except Exception as e:
        print('OpenAI call failed', e)
        return parse_receipt_with_fallback(text)




def parse_receipt(text):
    # wrapper
    if OPENAI_API_KEY:
        return parse_receipt_via_openai(text)
    else:
        return parse_receipt_with_fallback(text)