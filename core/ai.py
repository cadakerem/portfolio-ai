import os
from core.config import GROQ_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, ANTHROPIC_API_KEY

def get_portfolio_insight(portfolio_text: str) -> str:
    """
    Analyzes the portfolio text and returns a 1-2 sentence insight.
    It automatically detects which API key is provided and uses the corresponding AI provider.
    Priority: OpenAI -> Gemini -> Groq
    """
    prompt = (
        "Based on the following portfolio summary, provide a professional and concise financial insight. "
        "Keep it to 1-2 sentences. Warn if something looks too risky, and congratulate if the profit is good. "
        "Do not use markdown formatting. Just provide the direct text.\n\n"
        f"Portfolio Summary:\n{portfolio_text}"
    )
    system_prompt = "You are a highly experienced and professional portfolio manager. Your responses must be concise, clear, and sound like a natural human rather than an AI."
    
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
            return f"\n\n🤖 *AI Insight (ChatGPT):* {insight}"

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
            return f"\n\n🤖 *AI Insight (Claude):* {insight}"

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
            return f"\n\n🤖 *AI Insight (Gemini):* {insight}"

        # 4. Groq (Llama)
        elif GROQ_API_KEY and GROQ_API_KEY != "YOUR_GROQ_API_KEY":
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model="groq/compound",
                temperature=0.5,
                max_tokens=150
            )
            insight = chat_completion.choices[0].message.content.strip()
            return f"\n\n🤖 *AI Insight (Groq):* {insight}"
            
    except Exception as e:
        import logging
        import traceback
        logging.error(f"AI API Error: {e}")
        return f"\n\n🤖 *AI Error:* `{e}`\n\n`{traceback.format_exc()}`"
        
    return ""
