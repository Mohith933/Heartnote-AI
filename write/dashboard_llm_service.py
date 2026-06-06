import requests
from datetime import datetime
import os
import random


GEMINI_MODEL = "gemini-2.5-flash"




# -----------------------------------------------------
# TONE DEPTH MAP
# -----------------------------------------------------
DEPTH_TONE = {
    "light": """Write gently and simply.
Use easy words and a soft tone.
Keep it natural, like a passing thought.""",

    "medium": """Write naturally and honestly.
Keep it clear but not too polished.
Let it feel like everyday thinking.""",

    "deep": """Write like a quiet, personal thought.
Use short and slightly uneven sentences.
Include one real detail.
Let one sentence feel slightly incomplete.
Avoid polished or poetic language."""
}

SUPPORTED_LANGUAGES = {
    "en": "English",
    "english": "English",
    "hi": "Hindi",
    "hindi": "Hindi"
}


# -----------------------------------------------------
# SIMPLE EMOTIONAL TEMPLATES FOR 8 MODES
# -----------------------------------------------------

DASHBOARD_REFLECTION = """
Write a short emotional reflection in {language}.

Topic: {name}
Feeling: {desc}
Style: {tone}

Write like a real person thinking quietly.

Guidelines:
- 40–60 words
- 3–5 sentences
- Include one small, specific real-world detail
- Let the tone be slightly uneven
- Let one sentence feel a bit imperfect or unfinished
- Avoid advice or life lessons
- Avoid polished or poetic phrasing

Return only the reflection.
"""


DASHBOARD_LETTER = """
Write a short emotional letter in {language}.

Recipient: {name}
Feeling: {desc}
Style: {tone}

Write like someone expressing something they didn’t fully say before.

Guidelines:
- 50–60 words
- 3–4 sentences
- Keep tone honest and slightly vulnerable
- Include one small, real detail (memory, object, or moment)
- Let one sentence feel slightly incomplete or soft
- Avoid advice or moral tone
- Avoid perfect phrasing

Start with:
Dear You,

Return only the letter.
"""


DASHBOARD_JOURNAL = """
Write a calm personal journal entry in {language}.

Topic: {name}
Feeling: {desc}
Style: {tone}

Write like a quiet end-of-day thought.

Guidelines:
- 50–70 words
- 4–6 sentences
- Include one small, real detail from the day (object, place, or moment)
- Let thoughts flow naturally, not perfectly structured
- Allow slight repetition or pause-like phrasing
- Keep tone reflective, not philosophical
- Avoid advice or conclusions

Start with:
Date: {date}

Return only the journal.
"""


DASHBOARD_MESSAGES = """
Write a short emotional message in {language}.

For:
{name}

Feeling:
{desc}

Style: {tone}

Write like a real message someone would send and then pause before hitting send.

Guidelines:
- 25–45 words
- Simple, natural, and honest
- Include one small specific detail if it fits
- Let the tone feel slightly unfinished or open
- Avoid advice or dramatic tone
- Avoid overly polished language

Return only the message.
"""



# -----------------------------------------------------
# LLM SERVICE
# -----------------------------------------------------
class Dashboard_LLM_Service:

    def __init__(self, model=GEMINI_MODEL):
        self.model = model
    
    
    def generate_fallback(self, mode, name, desc, language, depth="medium"):
        # We keep name and desc in the arguments so we don't break existing calls,
        # but we ignore them to prevent mixed-language issues in the fallback.
        
        lang = language.lower()
        depth = depth.lower()
        date_str = datetime.now().strftime("%d/%m/%Y")
        variations = []

        if lang in ["en", "english"]:
            if mode == "reflection":
                if depth == "light":
                    variations = [
                        "just a passing thought that made me smile lightly",
                        "a quiet moment of clarity today",
                        "thinking about things and feeling a gentle shift"
                    ]
                elif depth == "medium":
                    variations = [
                        "my mind keeps going back to the same thought today",
                        "honestly just reflecting on where things are right now",
                        "it feels completely natural to just sit with these thoughts"
                    ]
                elif depth == "deep":
                    variations = [
                        "staring at the shadow on the wall. the weight of it feels heavy today",
                        "the room is quiet but the feeling remains. hard to shake off",
                        "holding a cold cup of tea. letting the thought sit in my chest"
                    ]

            elif mode == "messages":
                if depth == "light":
                    variations = [
                        "hey just thinking about you today",
                        "thought of this and wanted to share",
                        "a simple text to say you are on my mind"
                    ]
                elif depth == "medium":
                    variations = [
                        "i wanted to be honest about how i am feeling right now",
                        "just being clear about where my head is at today",
                        "everyday thoughts but i wanted to reach out"
                    ]
                elif depth == "deep":
                    variations = [
                        "i typed this twice. sending it anyway",
                        "phone feels heavy in my hand. maybe i shouldn't send this",
                        "staring at the screen. leaving it at that"
                    ]

            elif mode == "journal":
                if depth == "light":
                    variations = [
                        f"Date: {date_str}\n\ntoday was simple. thoughts came and went easily",
                        f"Date: {date_str}\n\na light day. just watching things as they pass",
                        f"Date: {date_str}\n\npassing thoughts. nothing more to add"
                    ]
                elif depth == "medium":
                    variations = [
                        f"Date: {date_str}\n\njust an everyday kind of day. checking in with myself",
                        f"Date: {date_str}\n\nhonest check in. trying to stay grounded today",
                        f"Date: {date_str}\n\nclear thoughts tonight. writing it down helps"
                    ]
                elif depth == "deep":
                    variations = [
                        f"Date: {date_str}\n\nthe pen feels heavy. the thought came back again. almost unfinished",
                        f"Date: {date_str}\n\nrain on the window. stuck in my head. letting it sit here",
                        f"Date: {date_str}\n\npage is half empty. the reality of it all. tired now"
                    ]

            elif mode == "letters":
                if depth == "light":
                    variations = [
                        "Dear You,\n\nthinking of things today. just wanted to send a gentle note",
                        "Dear You,\n\na simple letter. hope you are well",
                        "Dear You,\n\nquiet thoughts came up. wanted to share"
                    ]
                elif depth == "medium":
                    variations = [
                        "Dear You,\n\n i wanted to be honest with you. it feels clear now",
                        "Dear You,\n\n writing this just to get my thoughts out",
                        "Dear You,\n\n everyday life happens but this stays"
                    ]
                elif depth == "deep":
                    variations = [
                        "Dear You,\n\n the paper is slightly creased. keeps coming back. i should have said it sooner",
                        "Dear You,\n\n ink is smudging on the page. didn't know how to tell you",
                        "Dear You,\n\n quiet room. loud in my head. maybe you already know"
                    ]

        elif lang in ["hi", "hindi"]:
            if mode == "reflection":
                if depth == "light":
                    variations = [
                        "एक बहुत हल्का और सहज सा विचार आया",
                        "सोच रहा था और बस अच्छा लगा",
                        "एक शांत पल। जैसे हवा का झोंका"
                    ]
                elif depth == "medium":
                    variations = [
                        "सच कहूँ तो यह विचार दिमाग में है। एक आम ख्याल की तरह",
                        "आज का दिन सामान्य है पर वही बातें याद आ रही हैं",
                        "बिल्कुल स्पष्ट तौर पर सब कुछ समझ आ रहा है"
                    ]
                elif depth == "deep":
                    variations = [
                        "दीवार पर पड़ती धूप देख रहा हूँ। अजीब सा अधूरापन है",
                        "कमरा खामोश है। यह सच्चाई थोड़ी भारी लग रही है",
                        "हाथ में ठंडी चाय का कप है। एक बात सीने में अटकी है"
                    ]

            elif mode == "messages":
                if depth == "light":
                    variations = [
                        "सुनो बस ख्याल आया और सोचा बता दूँ",
                        "आज तुम्हारी याद आई तो सोचा संदेश भेज दूँ",
                        "एक छोटा सा संदेश बस ऐसे ही"
                    ]
                elif depth == "medium":
                    variations = [
                        "मुझे साफ तौर पर अपनी बात कहनी थी",
                        "ईमानदारी से कहूँ तो कुछ बताना चाहता था",
                        "रोजमर्रा की बातें हैं पर तुमसे कहनी थीं"
                    ]
                elif depth == "deep":
                    variations = [
                        "फोन हाथ में लेकर बस सोच रहा हूँ। खैर जाने दो",
                        "इसे दो बार टाइप किया। शायद इसे नहीं भेजना चाहिए",
                        "स्क्रीन को घूर रहा हूँ। बस इतना ही"
                    ]

            elif mode == "journal":
                if depth == "light":
                    variations = [
                        f"दिनांक: {date_str}\n\nदिन बहुत सहज था। बस याद आया",
                        f"दिनांक: {date_str}\n\nएक हल्का दिन। कुछ विचार आए और चले गए",
                        f"दिनांक: {date_str}\n\nगुजरते हुए विचार। बस इतना ही"
                    ]
                elif depth == "medium":
                    variations = [
                        f"दिनांक: {date_str}\n\nआज का दिन आम था। वही बातें दिमाग में घूमती रहीं",
                        f"दिनांक: {date_str}\n\nईमानदारी से लिख रहा हूँ। आज का सच यही है",
                        f"दिनांक: {date_str}\n\nआज विचार स्पष्ट हैं। लिखना सही लग रहा है"
                    ]
                elif depth == "deep":
                    variations = [
                        f"दिनांक: {date_str}\n\nकमरे में शांति है। नींद नहीं आ रही",
                        f"दिनांक: {date_str}\n\nकलम थोड़ी भारी लग रही है। पन्ना अधूरा छोड़ रहा हूँ",
                        f"दिनांक: {date_str}\n\nखिड़की पर बारिश की बूंदें। अब थक गया हूँ"
                    ]

            elif mode == "letters":
                if depth == "light":
                    variations = [
                        "प्रिय तुम,\n\nबस ख्याल आया। और कुछ नहीं",
                        "प्रिय तुम,\n\nएक छोटा सा खत। उम्मीद है तुम ठीक हो",
                        "प्रिय तुम,\n\nसहज विचार आए तो लिख दिया"
                    ]
                elif depth == "medium":
                    variations = [
                        "प्रिय तुम,\n\nमुझे सच कहना था जो मैंने पहले नहीं कहा",
                        "प्रिय तुम,\n\nयह खत सिर्फ यह बताने के लिए है कि कुछ बातें याद हैं",
                        "प्रिय तुम,\n\nज़िंदगी अपनी रफ्तार से चल रही है पर विचार वहीं हैं"
                    ]
                elif depth == "deep":
                    variations = [
                        "प्रिय तुम,\n\nस्याही थोड़ी फैल गई है। शायद यह खत कभी न भेज सकूं",
                        "प्रिय तुम,\n\nकागज़ के किनारे मुड़ गए हैं। मुझे पहले कहना चाहिए था",
                        "प्रिय तुम,\n\nशांत कमरा। दिमाग में बहुत शोर है। शायद तुम समझते होगे"
                    ]

        # Failsafe if anything slips through
        if not variations:
            variations = ["something feels quiet right now. words will come soon"]

        return random.choice(variations)
    # -------------------------------------------------
    # MAIN GENERATE
    # -------------------------------------------------
    def generate(self, mode, name, desc, depth, language):
        mode = (mode or "").lower().strip()
        depth = (depth or "light").lower().strip()
        raw_lang = (language or "en").lower().strip()
        language = SUPPORTED_LANGUAGES.get(raw_lang, "English")
        tone = DEPTH_TONE.get(depth, DEPTH_TONE["light"])
        safe, safe_message = self.safety_filter(desc)
        if not safe:
            return {
            "response": safe_message,
            "blocked": True,
            "is_fallback": False}
        template = self.get_template(mode)
        if not template:
            return {
            "response": "This writing mode is not available right now.",
            "blocked": False,
            "is_fallback": True}
        date = datetime.now().strftime("%d/%m/%Y")
        try:
            prompt = template.format(
            name=name,
            desc=desc,
            tone=tone,
            depth=depth,
            language=language,
            date=date)
        except Exception:
            prompt = template.format(
            name=name,
            desc=desc,
            tone=tone,
            language=language)
        
        full_prompt = f"[LANG={language}]\n{prompt}"
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            print("API KEY EXISTS:", bool(api_key))
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
            res = requests.post(url, headers=headers, json=payload, timeout=30)
            print("STATUS:", res.status_code)
            print("BODY:", res.text)
            res.raise_for_status()
            data = res.json()
            try:
                raw = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                raw = None
            if raw and isinstance(raw, str) and raw.strip():
                return {
            "response": raw.strip(),
            "blocked": False,
            "is_fallback": False
                }
            fallback = self.generate_fallback(mode, name, desc, language)
            return {
        "response": fallback,
        "blocked": False,
        "is_fallback": True
            }
        except Exception as e:
            print("GEMINI ERROR:", str(e))
            fallback = self.generate_fallback(mode,name,desc,language,depth)
            return {
        "response": fallback,
        "blocked": False,
        "is_fallback": True}




    # -------------------------------------------------
    # TEMPLATE ROUTER
    # -------------------------------------------------
    def get_template(self, mode):
        return {
            "reflection": DASHBOARD_REFLECTION,
            "letters": DASHBOARD_LETTER,
            "journal": DASHBOARD_JOURNAL,
            "messages": DASHBOARD_MESSAGES
        }.get(mode)

    # -------------------------------------------------
    # SAFETY FILTER (MINIMAL)
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
