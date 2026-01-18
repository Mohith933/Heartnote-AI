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
from datetime import datetime
import random

FALLBACK_CONTENT = {

  // -----------------------------
  // REFLECTION (25–45 words)
  // -----------------------------
  reflection: {
    light: [
      "Some feelings rise quietly and settle without resistance, allowing a soft awareness to form naturally. Nothing needs fixing right now, only gentle presence.",
      "A calm emotional state appears without effort, creating space to breathe and simply exist within the moment.",
      "The mind slows slightly, letting thoughts pass without attachment or urgency.",
      "There is ease here, light and open, with no demand to understand more."
    ],
    medium: [
      "There is a balanced emotional tone here, steady and grounded, allowing reflection without pressure or confusion.",
      "Emotions stay centered and thoughtful, offering clarity that forms slowly and without force.",
      "Awareness remains calm while meaning settles naturally over time.",
      "This moment holds balance, neither heavy nor distant."
    ],
    deep: [
      "This feeling carries quiet depth, resting beneath the surface without resolution, yet remaining meaningful.",
      "There is something layered here, unresolved but steady, holding space without needing answers.",
      "The emotion stays present without explanation, calm and reflective.",
      "Depth exists gently, without pulling or pushing."
    ]
  },

  // -----------------------------
  // JOURNAL (25–45 words)
  // -----------------------------
  journal: {
    light: [
      "Date: {date}\n\nToday moved gently, with a calm emotional rhythm carrying the day from morning to night.",
      "Date: {date}\n\nThe day felt light and unforced, allowing emotions to pass softly without attention.",
      "Date: {date}\n\nSmall moments blended smoothly, creating a peaceful flow.",
      "Date: {date}\n\nNothing stood out strongly, and that felt okay."
    ],
    medium: [
      "Date: {date}\n\nEmotions felt balanced today, supporting reflection and steady awareness throughout the day.",
      "Date: {date}\n\nThere was a grounded emotional presence, holding balance during pauses.",
      "Date: {date}\n\nThoughts and feelings stayed aligned without tension.",
      "Date: {date}\n\nThe day remained calm, thoughtful, and clear."
    ],
    deep: [
      "Date: {date}\n\nEmotions felt layered today, quiet and meaningful, staying close without explanation.",
      "Date: {date}\n\nSome unresolved feelings remained calmly present.",
      "Date: {date}\n\nDepth followed the day without becoming heavy.",
      "Date: {date}\n\nThe feeling stayed even after moments passed."
    ]
  },

  // -----------------------------
  // POEMS (3–4 lines)
  // -----------------------------
  poems: {
    light: [
      "A soft feeling rests\nwithout needing words\njust breathing space.",
      "Quiet moments pass\nnothing held tightly\nnothing lost.",
      "Still air moves gently\nand so do thoughts.",
      "Light stays\nwithout asking why."
    ],
    medium: [
      "A steady emotion stays\nbetween thought and breath\nquiet, aware.",
      "Balance forms slowly\nwithout effort.",
      "The moment holds\nwithout pulling.",
      "Clarity appears\nthen rests."
    ],
    deep: [
      "Something unresolved remains\nsilent\nand meaningful.",
      "Depth waits\nwithout sound.",
      "The feeling stays\nlonger than words.",
      "Meaning settles\nwithout shape."
    ]
  },

  // -----------------------------
  // LETTERS (25–45 words)
  // -----------------------------
  letters: {
    light: [
      "Dear,\n\nThis feeling feels gentle and sincere, carrying warmth without needing many words.\n\nWarmth By,\n💗 HeartNote AI",
      "Dear,\n\nA quiet sense of ease is present, calm and open.\n\nWarmth By,\n💗 HeartNote AI",
      "Dear,\n\nNothing urgent lives here, only softness.\n\nWarmth By,\n💗 HeartNote AI",
      "Dear,\n\nThis moment feels kind and simple.\n\nWarmth By,\n💗 HeartNote AI"
    ],
    medium: [
      "Dear,\n\nThis feeling holds balance and honesty, steady and thoughtful.\n\nWarmth By,\n💗 HeartNote AI",
      "Dear,\n\nCalm reflection stays present.\n\nWarmth By,\n💗 HeartNote AI",
      "Dear,\n\nThere is quiet clarity here.\n\nWarmth By,\n💗 HeartNote AI",
      "Dear,\n\nThe emotion feels centered and real.\n\nWarmth By,\n💗 HeartNote AI"
    ],
    deep: [
      "Dear,\n\nThis feeling carries quiet depth, present without urgency or resolution.\n\nWarmth By,\n💗 HeartNote AI",
      "Dear,\n\nSomething meaningful stays unspoken.\n\nWarmth By,\n💗 HeartNote AI",
      "Dear,\n\nDepth rests without explanation.\n\nWarmth By,\n💗 HeartNote AI",
      "Dear,\n\nThe feeling remains, even in silence.\n\nWarmth By,\n💗 HeartNote AI"
    ]
  },

  // -----------------------------
  // STORY (25–45 words, max 2 sentences)
  // -----------------------------
  story: {
    light: [
      "The moment unfolded quietly, without urgency or expectation. Calm settled naturally.",
      "Nothing dramatic occurred, yet peace stayed.",
      "Time moved gently, leaving softness behind.",
      "The feeling passed without resistance."
    ],
    medium: [
      "The experience moved slowly, allowing emotions to settle with balance. Meaning stayed present.",
      "The moment felt steady and thoughtful.",
      "Clarity formed without effort.",
      "The pause mattered."
    ],
    deep: [
      "The moment ended, but the feeling did not. It remained quietly.",
      "Something stayed unresolved, yet calm.",
      "Depth lingered without demand.",
      "Silence carried meaning."
    ]
  },

  // -----------------------------
  // QUOTES
  // -----------------------------
  quotes: {
    light: [
      "Gentle moments still matter.",
      "Calm has its own strength.",
      "Softness is not weakness.",
      "Stillness can be enough."
    ],
    medium: [
      "Balance often speaks softly.",
      "Presence does not rush.",
      "Clarity grows in quiet.",
      "Steadiness lasts."
    ],
    deep: [
      "Some feelings do not seek answers.",
      "Silence can hold depth.",
      "Meaning exists without words.",
      "Depth does not explain itself."
    ]
  },

  // -----------------------------
  // AFFIRMATION
  // -----------------------------
  affirmation: {
    light: [
      "This feeling is allowed.",
      "Gentleness is enough right now.",
      "I can rest here.",
      "Calm is safe."
    ],
    medium: [
      "I trust the steadiness of this moment.",
      "Balance can remain.",
      "I do not need to rush.",
      "Clarity will come."
    ],
    deep: [
      "Depth does not need answers.",
      "Stillness is safe.",
      "I can hold unresolved feelings.",
      "Meaning exists quietly."
    ]
  },

  // -----------------------------
  // NOTES (STRICT BULLETS)
  // -----------------------------
  notes: {
    light: [
      "• What you felt: gentle calm\n• Why it happened: awareness\n• What remained: space",
      "• What you felt: light ease\n• Why it happened: slow pace\n• What remained: stillness",
      "• What you felt: quiet comfort\n• Why it happened: presence\n• What remained: openness",
      "• What you felt: ease\n• Why it happened: acceptance\n• What remained: calm"
    ],
    medium: [
      "• What you felt: balance\n• Why it happened: grounding\n• What remained: steadiness",
      "• What you felt: clarity\n• Why it happened: reflection\n• What remained: focus",
      "• What you felt: stability\n• Why it happened: calm thought\n• What remained: alignment",
      "• What you felt: awareness\n• Why it happened: pause\n• What remained: control"
    ],
    deep: [
      "• What you felt: unresolved depth\n• Why it happened: complexity\n• What remained: silence",
      "• What you felt: weight\n• Why it happened: reflection\n• What remained: meaning",
      "• What you felt: depth\n• Why it happened: inner stillness\n• What remained: presence",
      "• What you felt: quiet intensity\n• Why it happened: awareness\n• What remained: calm depth"
    ]
  }
};

const FALLBACK_CONTENT_HI = {

  // --------------------------------
  // REFLECTION (25–45 words)
  // --------------------------------
  reflection: {
    light: [
      "कुछ भावनाएँ धीरे-धीरे उभरती हैं और बिना किसी विरोध के शांत हो जाती हैं। इस क्षण में कुछ सुधारने की ज़रूरत नहीं है, बस हल्की-सी उपस्थिति ही पर्याप्त है।",
      "एक सहज और शांत भाव अपने आप बनता है, जहाँ साँस लेने और बस मौजूद रहने के लिए जगह मिलती है।",
      "मन थोड़ी देर के लिए धीमा हो जाता है, विचार बिना पकड़े जाने के गुजरते हैं।",
      "यहाँ सब कुछ हल्का है, समझने का कोई दबाव नहीं।"
    ],
    medium: [
      "यहाँ भावनाएँ संतुलित और स्थिर हैं, जो बिना दबाव के आत्म-चिंतन की अनुमति देती हैं।",
      "भावनाएँ केंद्रित और विचारशील बनी रहती हैं, जहाँ स्पष्टता धीरे-धीरे बनती है।",
      "जागरूकता शांत रहती है और अर्थ समय के साथ उभरता है।",
      "यह क्षण न तो भारी है, न ही दूर।"
    ],
    deep: [
      "यह भावना शांत गहराई लिए हुए है, बिना समाधान के भी अर्थपूर्ण बनी रहती है।",
      "यहाँ कुछ परतें हैं—अधूरी लेकिन स्थिर—जो बिना उत्तर माँगे स्थान बनाए रखती हैं।",
      "भावना बिना स्पष्टीकरण के मौजूद रहती है, शांत और गंभीर।",
      "गहराई यहाँ है, लेकिन खींचती नहीं।"
    ]
  },

  // --------------------------------
  // JOURNAL (25–45 words)
  // --------------------------------
  journal: {
    light: [
      "दिनांक: {date}\n\nआज का दिन धीरे-धीरे बीता, सुबह से रात तक एक शांत भावनात्मक लय साथ रही।",
      "दिनांक: {date}\n\nदिन हल्का और सहज रहा, भावनाएँ बिना ध्यान माँगे आती-जाती रहीं।",
      "दिनांक: {date}\n\nछोटे-छोटे क्षण मिलकर एक शांत दिन बनाते रहे।",
      "दिनांक: {date}\n\nआज कुछ भी बहुत तीव्र नहीं था, और वह ठीक लगा।"
    ],
    medium: [
      "दिनांक: {date}\n\nआज भावनाएँ संतुलित रहीं, पूरे दिन स्थिर जागरूकता बनी रही।",
      "दिनांक: {date}\n\nएक स्थिर भावनात्मक उपस्थिति बनी रही।",
      "दिनांक: {date}\n\nसोच और भावना में तालमेल रहा।",
      "दिनांक: {date}\n\nदिन शांत, स्पष्ट और संतुलित रहा।"
    ],
    deep: [
      "दिनांक: {date}\n\nआज भावनाएँ परतदार और शांत रहीं, बिना स्पष्टीकरण के पास बनी रहीं।",
      "दिनांक: {date}\n\nकुछ अधूरी भावनाएँ शांति से मौजूद रहीं।",
      "दिनांक: {date}\n\nगहराई दिन भर साथ रही, बिना भारी हुए।",
      "दिनांक: {date}\n\nक्षण बीत गए, भावना बनी रही।"
    ]
  },

  // --------------------------------
  // POEMS (3–4 lines)
  // --------------------------------
  poems: {
    light: [
      "एक कोमल-सा भाव ठहरता है\nबिना शब्दों की ज़रूरत के\nबस साँसों के बीच",
      "शांत क्षण गुजरते हैं\nकुछ पकड़ा नहीं जाता",
      "हल्की हवा-सा मन\nऔर खुले विचार",
      "कोमलता रहती है\nबिना कारण"
    ],
    medium: [
      "एक स्थिर भावना रहती है\nसोच और साँस के बीच\nशांत, जागरूक",
      "संतुलन धीरे बनता है\nबिना प्रयास",
      "क्षण थामे रहते हैं\nबिना खींचे",
      "स्पष्टता आती है\nऔर ठहर जाती है"
    ],
    deep: [
      "कुछ अधूरा-सा ठहर जाता है\nमौन में\nऔर अर्थपूर्ण",
      "गहराई प्रतीक्षा करती है\nबिना आवाज़",
      "भावना शब्दों से आगे\nठहरती है",
      "अर्थ चुपचाप\nबस रहता है"
    ]
  },

  // --------------------------------
  // LETTERS (25–45 words)
  // --------------------------------
  letters: {
    light: [
      "प्रिय,\n\nयह भावना कोमल और सच्ची लगती है, बिना अधिक शब्दों के भी अपनी गर्माहट बनाए रखती है।\n\nस्नेह सहित,\n💗 HeartNote AI",
      "प्रिय,\n\nयह क्षण शांत और सरल है।\n\nस्नेह सहित,\n💗 HeartNote AI",
      "प्रिय,\n\nयहाँ कोई जल्दी नहीं है।\n\nस्नेह सहित,\n💗 HeartNote AI",
      "प्रिय,\n\nयह भाव सहज और हल्का है।\n\nस्नेह सहित,\n💗 HeartNote AI"
    ],
    medium: [
      "प्रिय,\n\nयह भावना संतुलन और ईमानदारी लिए हुए है।\n\nस्नेह सहित,\n💗 HeartNote AI",
      "प्रिय,\n\nशांत स्पष्टता बनी रहती है।\n\nस्नेह सहित,\n💗 HeartNote AI",
      "प्रिय,\n\nभावना स्थिर और वास्तविक है।\n\nस्नेह सहित,\n💗 HeartNote AI",
      "प्रिय,\n\nयह क्षण संतुलित है।\n\nस्नेह सहित,\n💗 HeartNote AI"
    ],
    deep: [
      "प्रिय,\n\nयह भावना शांत गहराई लिए हुए है, बिना किसी जल्दबाज़ी के।\n\nस्नेह सहित,\n💗 HeartNote AI",
      "प्रिय,\n\nकुछ अर्थ मौन में रहते हैं।\n\nस्नेह सहित,\n💗 HeartNote AI",
      "प्रिय,\n\nगहराई बिना उत्तर के भी पूरी है।\n\nस्नेह सहित,\n💗 HeartNote AI",
      "प्रिय,\n\nभावना मौन में बनी रहती है।\n\nस्नेह सहित,\n💗 HeartNote AI"
    ]
  },

  // --------------------------------
  // STORY (25–45 words)
  // --------------------------------
  story: {
    light: [
      "वह क्षण बिना किसी जल्दबाज़ी के शांतिपूर्वक खुला। एक कोमल शांति ठहर गई।",
      "कुछ खास नहीं हुआ, फिर भी मन शांत रहा।",
      "समय धीरे चला और हल्कापन छोड़ गया।",
      "भावना बिना विरोध के बीत गई।"
    ],
    medium: [
      "अनुभव धीरे आगे बढ़ा, भावनाओं को संतुलन में ठहरने दिया।",
      "क्षण स्थिर और विचारशील रहा।",
      "स्पष्टता अपने आप बनी।",
      "ठहराव मायने रखता था।"
    ],
    deep: [
      "क्षण समाप्त हुआ, पर भावना नहीं गई।",
      "कुछ अधूरा शांति से बना रहा।",
      "गहराई बिना दबाव के रही।",
      "मौन में अर्थ ठहरा।"
    ]
  },

  // --------------------------------
  // QUOTES
  // --------------------------------
  quotes: {
    light: [
      "कोमल क्षण भी मायने रखते हैं।",
      "शांति की अपनी शक्ति होती है।",
      "हल्कापन भी पर्याप्त है।",
      "स्थिरता आराम देती है।"
    ],
    medium: [
      "संतुलन धीरे बोलता है।",
      "उपस्थिति को जल्दी नहीं होती।",
      "स्पष्टता शांति में आती है।",
      "स्थिरता टिकती है।"
    ],
    deep: [
      "कुछ भावनाएँ उत्तर नहीं माँगतीं।",
      "मौन भी अर्थ रखता है।",
      "गहराई शब्दों से आगे है।",
      "अर्थ को समझाने की ज़रूरत नहीं।"
    ]
  },

  // --------------------------------
  // AFFIRMATION
  // --------------------------------
  affirmation: {
    light: [
      "यह भावना स्वीकार्य है।",
      "अभी कोमलता पर्याप्त है।",
      "मैं यहाँ ठहर सकता हूँ।",
      "शांति सुरक्षित है।"
    ],
    medium: [
      "मैं इस क्षण की स्थिरता पर भरोसा करता हूँ।",
      "संतुलन बना रह सकता है।",
      "मुझे जल्दी नहीं करनी है।",
      "स्पष्टता आएगी।"
    ],
    deep: [
      "गहराई को उत्तरों की आवश्यकता नहीं।",
      "स्थिरता सुरक्षित है।",
      "मैं अधूरी भावनाएँ संभाल सकता हूँ।",
      "अर्थ शांत रूप से मौजूद है।"
    ]
  },

  // --------------------------------
  // NOTES (STRICT BULLETS)
  // --------------------------------
  notes: {
    light: [
      "• आपने क्या महसूस किया: कोमल शांति\n• यह क्यों हुआ: जागरूकता\n• क्या शेष रहा: खाली स्थान",
      "• आपने क्या महसूस किया: सहजता\n• यह क्यों हुआ: धीमी गति\n• क्या शेष रहा: स्थिरता",
      "• आपने क्या महसूस किया: आराम\n• यह क्यों हुआ: स्वीकृति\n• क्या शेष रहा: खुलापन",
      "• आपने क्या महसूस किया: हल्कापन\n• यह क्यों हुआ: शांत उपस्थिति\n• क्या शेष रहा: संतोष"
    ],
    medium: [
      "• आपने क्या महसूस किया: संतुलन\n• यह क्यों हुआ: आंतरिक स्थिरता\n• क्या शेष रहा: स्पष्टता",
      "• आपने क्या महसूस किया: जागरूकता\n• यह क्यों हुआ: ठहराव\n• क्या शेष रहा: नियंत्रण",
      "• आपने क्या महसूस किया: स्थिरता\n• यह क्यों हुआ: विचारशीलता\n• क्या शेष रहा: तालमेल",
      "• आपने क्या महसूस किया: संतुलित भाव\n• यह क्यों हुआ: शांति\n• क्या शेष रहा: फोकस"
    ],
    deep: [
      "• आपने क्या महसूस किया: अधूरी गहराई\n• यह क्यों हुआ: आंतरिक जटिलता\n• क्या शेष रहा: मौन",
      "• आपने क्या महसूस किया: भावनात्मक भार\n• यह क्यों हुआ: आत्म-चिंतन\n• क्या शेष रहा: अर्थ",
      "• आपने क्या महसूस किया: गहराई\n• यह क्यों हुआ: स्थिर मौन\n• क्या शेष रहा: उपस्थिति",
      "• आपने क्या महसूस किया: शांत तीव्रता\n• यह क्यों हुआ: जागरूकता\n• क्या शेष रहा: गहन शांति"
    ]
  }
};

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
        language = "en" if language not in ["en", "hi"] else language
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
           if language == "hi":
              fallback = FALLBACK_CONTENT_HI
           else:
             fallback = FALLBACK_CONTENT

           fallback_mode = fallback.get(mode, {})
           fallback_list = fallback_mode.get(depth, [])

           if fallback_list:
              text = random.choice(fallback_list).format(
            date=date,
            name=name
        )
           else:
               text = ("The words feel  quiet right now.\n\n"
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
