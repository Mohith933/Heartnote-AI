import os
from datetime import datetime
import google.generativeai as genai


# -----------------------------------------------------
# GEMINI CONFIG (optional)
# -----------------------------------------------------
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-2.0-flash"


def call_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini API key not configured")

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)
    return response.text.strip()


# -----------------------------------------------------
# TONE DEPTH MAP
# -----------------------------------------------------
DEPTH_TONE = {
    "light": "soft, reflective, gentle emotional clarity",
    "medium": "thoughtful, grounded, emotionally layered",
    "deep": "rich, profound, cinematic emotional depth",
}


# -----------------------------------------------------
# DASHBOARD TEMPLATES
# -----------------------------------------------------
DASHBOARD_REFLECTION = """
You are HeartNote Premium Reflection Writer.

Topic: {name}
Feeling: {desc}
Tone: {tone}

Rules:
- Two paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Emotional, cinematic English
- No advice, no motivation, no emojis
"""

DASHBOARD_LETTER = """
You are HeartNote Premium Letter Writer.

Recipient: {name}
Feeling: {desc}
Tone: {tone}

Rules:
- Exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Poetic, grounded
- No advice, no judgement, no emojis
"""

DASHBOARD_JOURNAL = """
You are HeartNote Premium Journal Writer.

Topic: {name}
Feeling: {desc}
Tone: {tone}

Rules:
- 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Reflective, cinematic
- No advice, no emojis

Date: {date}
"""

DASHBOARD_POEM = """
You are HeartNote Premium Poem Writer.

Theme: {name} — {desc}

Rules:
- 6–8 free-verse lines
- Soft emotional imagery
- No advice, no emojis
"""

DASHBOARD_STORY = """
You are HeartNote Premium Story Writer.

Theme: {name} — {desc}

Rules:
- 45–70 words
- Emotional micro-story
- No advice, no emojis
"""

DASHBOARD_QUOTE = """
You are HeartNote Premium Quote Writer.

Theme: {name} — {desc}

Rules:
- One sentence
- Under 24 words
- Poetic, reflective
- No emojis
"""

DASHBOARD_AFFIRMATION = """
You are HeartNote Premium Affirmation Writer.

Theme: {name} — {desc}

Rules:
- 1–2 lines
- Gentle, grounded
- No advice, no emojis
"""

DASHBOARD_NOTE = """
You are HeartNote Premium Note Writer.

Format ONLY:

• What you felt: {desc}
• Why it happened: one calm, neutral reason
• What could help: one gentle, non-instructional idea
"""


# -----------------------------------------------------
# LLM SERVICE
# -----------------------------------------------------
class Dashboard_LLM_Service:

    def generate(self, mode, name, desc, depth, language):
    depth = (depth or "light").lower()
    tone = DEPTH_TONE.get(depth, DEPTH_TONE["light"])
    mode = (mode or "").lower()
    language = (language or "en").lower()

    templates = {
        "reflection": DASHBOARD_REFLECTION,
        "letters": DASHBOARD_LETTER,
        "journal": DASHBOARD_JOURNAL,
        "poems": DASHBOARD_POEM,
        "story": DASHBOARD_STORY,
        "quotes": DASHBOARD_QUOTE,
        "affirmation": DASHBOARD_AFFIRMATION,
        "notes": DASHBOARD_NOTE,
    }

    template = templates.get(mode)
    if not template:
        return {"response": "This writing mode is not available yet."}

    date = datetime.now().strftime("%d/%m/%Y")

    prompt = template.format(
        name=name,
        desc=desc,
        tone=tone,
        date=date
    )

    prompt = f"[LANG={language}]\n{prompt}"

    try:
        text = call_gemini(prompt)
        if not text:
            raise ValueError("Empty LLM response")
    except Exception:
        text = (
            "✨ HeartNote is taking a short pause.\n\n"
            "Please try again in a moment."
        )

    return {"response": text}

