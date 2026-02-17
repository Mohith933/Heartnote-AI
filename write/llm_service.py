import os
from datetime import datetime
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

# ------------------------------------------
# TONE STYLES
# ------------------------------------------
DETAIL_MAP = {
    "soft": "concise and brief",
    "balanced": "clear and structured",
    "deep": "detailed and comprehensive"
}


SUMMARY_TEMPLATE = """
You are a professional meeting assistant.

Convert the following raw notes into a structured summary.

STRICT RULES:
- Clear headings
- Bullet points where necessary
- No emojis
- Professional tone
- Detail level: {detail}

Input:
{text}

Output format:

Meeting Summary
Key Points:
- ...

Decisions:
- ...

Action Items:
- ...
"""

KEYPOINTS_TEMPLATE = """
Extract only the key discussion points.

STRICT RULES:
- Bullet format
- No explanations
- No emojis
- Detail level: {detail}

Input:
{text}
"""

ACTION_TEMPLATE = """
Identify actionable tasks from the discussion.

STRICT RULES:
- Bullet format
- Each bullet must include responsible person if mentioned
- No emojis
- Detail level: {detail}

Input:
{text}
"""

MINUTES_TEMPLATE = """
Create formal meeting minutes.

STRICT RULES:
- Include Date (today)
- Structured sections
- Professional tone
- Detail level: {detail}

Input:
{text}
"""

BRAINSTORM_TEMPLATE = """
Organize brainstorming ideas clearly.

STRICT RULES:
- Group similar ideas
- Bullet format
- No emojis
- Detail level: {detail}

Input:
{text}
"""


# ------------------------------------------
# LLM SERVICE (LOCAL OLLAMA + SAFE FALLBACK)
# ------------------------------------------
# ------------------------------------------
# LLM SERVICE (GEMINI CLOUD)
# ------------------------------------------
class LLM_Service:

    def __init__(self):
        self.model = model  # using global Gemini model

    # -------------------------
    # Fallback
    # -------------------------
    def get_fallback(self):
        return "⚠️ AI service temporarily unavailable. Please try again shortly."

    # -------------------------
    # Main generator
    # -------------------------
    def generate(self, mode, text, tone="balanced"):
        mode = mode.lower().strip()
        detail_style = DETAIL_MAP.get(tone, DETAIL_MAP["balanced"])

        # Safety check
        safe, safe_response = self.safety_filter(text)
        if not safe:
            return safe_response

        prompt = self.build_prompt(mode, text, detail_style)
        if not prompt:
            return "⚠️ Unknown mode."

        try:
            response = self.model.generate_content(prompt)
            if not response or not response.text:
                return self.get_fallback()
            return response.text.strip()
        except Exception as e:
            print("Gemini error:", e)
            return self.get_fallback()

    # -------------------------
    # Prompt builder
    # -------------------------
    def build_prompt(self, mode, text, detail):

        if mode == "summary":
            return SUMMARY_TEMPLATE.format(text=text, detail=detail)

        if mode == "keypoints":
            return KEYPOINTS_TEMPLATE.format(text=text, detail=detail)

        if mode == "action":
            return ACTION_TEMPLATE.format(text=text, detail=detail)

        if mode == "minutes":
            return MINUTES_TEMPLATE.format(text=text, detail=detail)

        if mode == "brainstorm":
            return BRAINSTORM_TEMPLATE.format(text=text, detail=detail)

        return None

    # -------------------------
    # Safety filter
    # -------------------------
    def safety_filter(self, text):
        t = text.lower().strip()

        bad_words = [
            "fuck", "bitch", "shit", "asshole",
            "bastard", "slut", "dick", "pussy",
            "kill you", "hurt you"
        ]
        for w in bad_words:
            if w in t:
                return False, "⚠️ Please rewrite your text using respectful language."

        selfharm_patterns = [
            "kill myself", "kill me", "i want to die",
            "end my life", "i want to disappear",
            "self harm", "i can't live", "no reason to live"
        ]
        for p in selfharm_patterns:
            if p in t:
                return False, (
                    "⚠️ This system cannot process this request.\n\n"
                    "If you're struggling, please consider reaching out to someone you trust."
                )

        return True, text
