import os
from core.config import GROQ_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY

def get_portfolio_insight(portfolio_text: str) -> str:
    """
    Analyzes the portfolio text and returns a 1-2 sentence insight.
    It automatically detects which API key is provided and uses the corresponding AI provider.
    Priority: OpenAI -> Gemini -> Groq
    """
    prompt = (
        "Aşağıdaki portföy özetine bakarak, profesyonel ve kısa bir finansal yorum yap. "
        "Sadece 1-2 cümle olsun. Fazla riskli duran bir şey varsa uyar, kâr iyiyse tebrik et. "
        "Markdown formatı kullanma. Sadece doğrudan metni ver.\n\n"
        f"Portföy Özeti:\n{portfolio_text}"
    )
    system_prompt = "Sen çok tecrübeli ve profesyonel bir portföy yöneticisisin. Cevapların kısa, net ve yapay zeka olduğunu belli etmeyen doğal bir üslupta olmalı."
    
    insight = ""

    try:
        # 1. OpenAI (ChatGPT)
        if OPENAI_API_KEY and OPENAI_API_KEY != "YOUR_OPENAI_API_KEY":
            from openai import OpenAI
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=150
            )
            insight = response.choices[0].message.content.strip()
            return f"\n\n🤖 *AI Analizi (ChatGPT):* {insight}"

        # 2. Anthropic (Claude)
        elif ANTHROPIC_API_KEY and ANTHROPIC_API_KEY != "YOUR_ANTHROPIC_API_KEY":
            from anthropic import Anthropic
            client = Anthropic(api_key=ANTHROPIC_API_KEY)
            response = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=150,
                temperature=0.5,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            insight = response.content[0].text.strip()
            return f"\n\n🤖 *AI Analizi (Claude):* {insight}"

        # 3. Google Gemini
        elif GEMINI_API_KEY and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY":
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(
                'gemini-1.5-flash',
                system_instruction=system_prompt
            )
            response = model.generate_content(prompt)
            insight = response.text.strip()
            return f"\n\n🤖 *AI Analizi (Gemini):* {insight}"

        # 4. Groq (Llama)
        elif GROQ_API_KEY and GROQ_API_KEY != "YOUR_GROQ_API_KEY":
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=150
            )
            insight = chat_completion.choices[0].message.content.strip()
            return f"\n\n🤖 *AI Analizi (Groq):* {insight}"
            
    except Exception as e:
        import logging
        logging.error(f"AI API Error: {e}")
        
    return ""
