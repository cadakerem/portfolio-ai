import os
from core.config import GROQ_API_KEY
from groq import Groq

def get_portfolio_insight(portfolio_text: str) -> str:
    """
    Analyzes the portfolio text and returns a 1-2 sentence insight using Groq API.
    If no API key is provided, returns an empty string silently.
    """
    if not GROQ_API_KEY or GROQ_API_KEY == "YOUR_GROQ_API_KEY":
        return ""
        
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        prompt = (
            "Aşağıdaki portföy özetine bakarak, profesyonel ve kısa bir finansal yorum yap. "
            "Sadece 1-2 cümle olsun. Fazla riskli duran bir şey varsa uyar, kâr iyiyse tebrik et. "
            "Markdown formatı kullanma. Sadece doğrudan metni ver.\n\n"
            f"Portföy Özeti:\n{portfolio_text}"
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Sen çok tecrübeli ve profesyonel bir portföy yöneticisisin. Cevapların kısa, net ve yapay zeka olduğunu belli etmeyen doğal bir üslupta olmalı."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192",
            temperature=0.5,
            max_tokens=150
        )
        
        insight = chat_completion.choices[0].message.content.strip()
        return f"\n\n🤖 *AI Analizi:* {insight}"
        
    except Exception as e:
        print(f"Groq API Error: {e}")
        return ""
