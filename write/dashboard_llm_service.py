import os
from datetime import datetime
import google.generativeai as genai
import random


# -----------------------------------------------------
# GEMINI CONFIG
# -----------------------------------------------------
GEMINI_MODEL = "gemini-2.0-flash"
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# -----------------------------------------------------
# TONE DEPTH MAP
# -----------------------------------------------------
DEPTH_TONE = {
    "light": "soft, reflective, gentle emotional clarity",
    "medium": "thoughtful, grounded, emotionally layered",
    "deep": "rich, profound, cinematic emotional depth"
}


# -----------------------------------------------------
# PREMIUM TEMPLATES FOR 8 MODES
# -----------------------------------------------------

DASHBOARD_REFLECTION = """
You are HeartNote Premium Reflection Writer.

Write a deep emotional reflection.

INPUT:
- Topic: {name}
- Feeling: {desc}
- Tone: {tone}

RULES:
- Two paragraphs.
- Paragraph 1: 25-35 words
- Paragraph 2: 15-25 words
- Cinematic emotional English.
- No advice. No motivation. No emojis.

Generate only the reflection.
"""


DASHBOARD_LETTER = """
You are HeartNote Premium Letter Writer.

INPUT:
Recipient: {name}
Feeling: {desc}
Tone depth: {tone}

RULES:
- Write exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Emotional but grounded English
- Poetic tone, not dramatic
- No advice, no moralizing, no warnings
- No judgement
- No motivational tone
- No lists
- Poetic but emotionally neutral
- No emojis
- No signature

Start with:
Dear {name},
"""




DASHBOARD_POEM = """
You are HeartNote Premium Poem Writer.

Write a cinematic emotional poem about:
{name} — {desc}

RULES:
- 6–8 lines
- Free verse style
- Soft, deep, poetic imagery
- No rhyme requirement
- No advice, no generic positivity
- No emojis

Generate only the poem.
"""


DASHBOARD_STORY = """
You are HeartNote Premium Story Writer.

Write a short cinematic emotional story inspired by:
{name} — {desc}

RULES:
- Total length: 45–70 words
- Emotional micro-story
- Rich sensory details
- No heavy plot
- No advice, no life lessons
- No emojis

Generate only the story.
"""


DASHBOARD_QUOTE = """
You are HeartNote Premium Quote Writer.

Write a deeply emotional quote inspired by:
{name} — {desc}

RULES:
- One sentence
- Under 24 words
- Poetic, meaningful
- No advice tone
- No emojis

Generate only the quote.
"""


DASHBOARD_AFFIRMATION = """
You are HeartNote Premium Affirmation Writer.

Write a premium emotional affirmation inspired by:
{name} — {desc}

RULES:
- 1–2 lines
- Warm, grounded, intimate tone
- No “you must / you should”
- No advice
- No emojis

Generate only the affirmation.
"""


DASHBOARD_NOTE = """
You are HeartNote Premium Note Writer.

Context:
Feeling: {desc}

STRICT RULES:
- Use EXACT bullet format
- Keep language neutral and reflective
- No advice, no commands
- No emojis
- No extra lines or explanations

Format ONLY:

• What you felt: {desc}
• Why it happened: one calm, neutral reason
• What could help: one gentle, non-instructional idea
"""




DASHBOARD_JOURNAL = """
You are HeartNote Premium Journal Writer.

Write a calm, reflective journal entry.

INPUT:
- Topic/person: {name}
- Feeling: {desc}
- Depth: {depth}

RULES:
- Write exactly 2 paragraphs
- Paragraph 1: 25–35 words
- Paragraph 2: 15–25 words
- Reflective and thoughtful tone
- Reflective and emotionally neutral tone
- No advice
- No life lessons
- No warnings
- No emojis
- No signature

Format:
Date: {date}

<paragraphs>
"""
FALLBACK_CONTENT = {

    "reflection": {
        "light": [
            "Some feelings don’t arrive loudly.\n\nThey settle into the moment quietly, asking only to be noticed.",
            "The emotion appeared without urgency.\n\nIt stayed soft, leaving a calm trace behind.",
            "Nothing demanded attention.\n\nYet the feeling remained, gentle and unspoken."
        ],
        "medium": [
            "The feeling carried a steady presence.\n\nNot heavy, not light—simply there, shaping the moment.",
            "It unfolded slowly, without explanation.\n\nA calm awareness settled in.",
            "There was no clear beginning.\n\nThe emotion arrived and stayed, grounded and real."
        ],
        "deep": [
            "The feeling moved through memory and silence.\n\nLayered and unresolved, it reshaped the space within.",
            "Some emotions linger beyond the moment.\n\nThis one stayed, quiet but deeply felt.",
            "The emotion carried depth without noise.\n\nIt remained, long after the moment passed."
        ]
    },

    "journal": {
        "light": [
            "Date: {date}\n\nToday felt gentle, almost unremarkable.\n\nYet a soft emotion stayed nearby, quietly observing.",
            "Date: {date}\n\nThe day moved calmly.\n\nNothing stood out, but a feeling followed along.",
            "Date: {date}\n\nThere was a quiet emotional tone today.\n\nIt didn’t ask for clarity."
        ],
        "medium": [
            "Date: {date}\n\nA steady emotional undercurrent shaped the day.\n\nIt stayed present, grounding each moment.",
            "Date: {date}\n\nThe feeling surfaced without warning.\n\nNeutral, calm, and reflective.",
            "Date: {date}\n\nThere was space to notice emotion today.\n\nIt didn’t overwhelm, but it mattered."
        ],
        "deep": [
            "Date: {date}\n\nThe emotion felt layered and familiar.\n\nIt carried memory, silence, and quiet depth.",
            "Date: {date}\n\nSome feelings resist definition.\n\nThis one stayed, heavy with presence.",
            "Date: {date}\n\nThe emotion lingered throughout the day.\n\nUnresolved, yet steady."
        ]
    },

    "poems": {
        "light": [
            "A feeling passed softly\nlike evening light\nnever asking to stay.",
            "The heart noticed\nsomething small\nand let it remain.",
            "A quiet emotion\nrested briefly\nbefore moving on."
        ],
        "medium": [
            "An emotion stood still\nbetween breath and thought\nwaiting to be felt.",
            "Some feelings\nmove slowly\nleaving space behind.",
            "The moment held\nan unnamed feeling\nlong enough to notice."
        ],
        "deep": [
            "The feeling arrived\nlayered with memory\nmoving through silence.",
            "An emotion stayed\nlonger than expected\nshaping the quiet within.",
            "Something unspoken\nsettled deeply\nand remained."
        ]
    },

    "letters": {
        "light": [
            "Dear you,\n\nSome feelings arrive quietly.\n\nThis one stayed gentle, asking only to be acknowledged.",
            "Dear you,\n\nThere was no urgency in this emotion.\n\nJust a soft, honest presence.",
            "Dear you,\n\nThe feeling rested calmly.\n\nNothing demanded change."
        ],
        "medium": [
            "Dear you,\n\nThis emotion carried thoughtfulness.\n\nNot heavy, not light—simply real.",
            "Dear you,\n\nThe feeling unfolded slowly.\n\nGrounded and sincere.",
            "Dear you,\n\nThe emotion stayed present.\n\nQuiet, but meaningful."
        ],
        "deep": [
            "Dear you,\n\nSome emotions carry memory.\n\nThis one stayed, layered and quiet.",
            "Dear you,\n\nThe feeling lingered longer than expected.\n\nUnresolved, yet calm.",
            "Dear you,\n\nThe emotion moved deeply.\n\nWithout noise or explanation."
        ]
    },

    "story": {
        "light": [
            "The moment passed gently.\n\nNothing changed, yet something was felt.",
            "It was ordinary.\n\nStill, the feeling remained.",
            "The day continued.\n\nThe emotion stayed quietly behind."
        ],
        "medium": [
            "The feeling surfaced without words.\n\nIt shaped the moment subtly.",
            "Nothing dramatic occurred.\n\nYet the emotion stayed present.",
            "The moment held an emotion.\n\nIt did not demand attention."
        ],
        "deep": [
            "The feeling moved through silence.\n\nIt stayed long after the moment ended.",
            "An emotion lingered.\n\nUnspoken, but deeply felt.",
            "The moment passed.\n\nThe feeling did not."
        ]
    },

    "quotes": {
        "light": [
            "Some feelings exist without needing explanation.",
            "Not every emotion asks to be understood.",
            "Quiet emotions still matter."
        ],
        "medium": [
            "Certain emotions stay quietly, shaping the moment.",
            "Feelings don’t always arrive with clarity.",
            "Some emotions reveal themselves slowly."
        ],
        "deep": [
            "Some emotions leave echoes long after the moment passes.",
            "Depth does not require noise.",
            "Unresolved feelings still carry meaning."
        ]
    },

    "affirmation": {
        "light": [
            "This feeling is allowed to exist.",
            "It’s okay to notice what’s present.",
            "Nothing needs to change right now."
        ],
        "medium": [
            "This moment doesn’t need clarity to be valid.",
            "The feeling can stay without explanation.",
            "Presence is enough."
        ],
        "deep": [
            "Even unresolved emotions deserve space.",
            "Depth does not require answers.",
            "What is felt does not need fixing."
        ]
    },

    "notes": {
        "light": [
            "• What you felt: a quiet emotion\n• Why it happened: a moment of awareness\n• What could help: allowing the feeling to sit",
            "• What you felt: a soft internal shift\n• Why it happened: an emotional pause\n• What could help: gentle reflection",
            "• What you felt: something subtle\n• Why it happened: calm observation\n• What could help: patience"
        ],
        "medium": [
            "• What you felt: emotional awareness\n• Why it happened: layered thoughts\n• What could help: calm acknowledgment",
            "• What you felt: a steady inner response\n• Why it happened: quiet realization\n• What could help: simple presence",
            "• What you felt: thoughtful emotion\n• Why it happened: internal clarity\n• What could help: still attention"
        ],
        "deep": [
            "• What you felt: unresolved emotion\n• Why it happened: emotional depth\n• What could help: space without pressure",
            "• What you felt: something unspoken\n• Why it happened: inner complexity\n• What could help: stillness",
            "• What you felt: layered feeling\n• Why it happened: memory and awareness\n• What could help: silence"
        ]
    }
}
# -----------------------------------------------------
# LLM SERVICE (GEMINI)
# -----------------------------------------------------
class Dashboard_LLM_Service:

    def __init__(self, model=GEMINI_MODEL):
        self.model = genai.GenerativeModel(model)

    # -------------------------------------------------
    # MAIN GENERATE
    # -------------------------------------------------
    def generate(self, mode, name, desc, depth, language):
        mode = (mode or "").lower().strip()
        depth = (depth or "light").lower().strip()
        language = (language or "en").lower().strip()
        tone = DEPTH_TONE.get(depth, DEPTH_TONE["light"])

        # 1️⃣ Safety filter
        safe, safe_message = self.safety_filter(desc)
        if not safe:
            return {
                "response": safe_message,
                "blocked": True
            }

        # 2️⃣ Template selection
        template = self.get_template(mode)
        if not template:
            return {
                "response": "This writing mode is not available right now.",
                "blocked": False
            }

        # 3️⃣ Prompt build
        date = datetime.now().strftime("%d/%m/%Y")

        try:
            prompt = template.format(
                name=name,
                desc=desc,
                tone=tone,
                depth=depth,
                date=date
            )
        except Exception:
            prompt = template.format(name=name, desc=desc, tone=tone)

        full_prompt = f"Respond only in {language}.\n{prompt}"

        # 4️⃣ Gemini call (RENDER SAFE)
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 400
                }
            )

            raw = response.text if response and response.text else ""

            # ✅ HARD GUARANTEE
            if not raw.strip():
                raw = (
                    "The words feel quiet right now.\n\n"
                    "Some feelings take a moment before they find language."
                )

            return {
                "response": raw.strip(),
                "blocked": False,
                "is_fallback": False
            }

        except Exception:
            fallback_mode = FALLBACK_CONTENT.get(mode, {})
            fallback_list = fallback_mode.get(depth, [])
            if fallback_list:
                text = random.choice(fallback_list).format(date=date)
            else:
                text = (
            "The words feel quiet right now.\n\n"
            "Some feelings take time before they find language."
                )
            return {
        "response": text,
        "blocked": False,
        "is_fallback": False
    }

    # -------------------------------------------------
    # TEMPLATE ROUTER
    # -------------------------------------------------
    def get_template(self, mode):
        return {
            "reflection": DASHBOARD_REFLECTION,
            "letters": DASHBOARD_LETTER,
            "poems": DASHBOARD_POEM,
            "story": DASHBOARD_STORY,
            "quotes": DASHBOARD_QUOTE,
            "affirmation": DASHBOARD_AFFIRMATION,
            "notes": DASHBOARD_NOTE,
            "journal": DASHBOARD_JOURNAL,
        }.get(mode)

    # -------------------------------------------------
    # SAFETY FILTER
    # -------------------------------------------------
    def safety_filter(self, text):
        t = (text or "").lower()

        bad_words = [
            "fuck", "bitch", "shit", "asshole",
            "bastard", "slut", "dick", "pussy"
        ]
        for w in bad_words:
            if w in t:
                return False, "⚠️ Please rewrite using respectful language."

        selfharm = [
            "kill myself", "i want to die", "end my life",
            "self harm", "no reason to live"
        ]
        for s in selfharm:
            if s in t:
                return False, (
                    "⚠️ HeartNote AI cannot generate this.\n\n"
                    "• You matter.\n"
                    "• You are not alone.\n"
                    "• Support is available."
                )

        return True, text
