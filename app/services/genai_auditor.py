import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import Dict

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def audit_ui_ux_with_gemini(metadata: Dict) -> str:
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")

        prompt = f"""
        Conduct a professional UI/UX audit for this website:
        URL: {metadata.get('url')}
        Title: {metadata.get('title')}

        Provide:
        1. Visual design assessment
        2. Usability evaluation
        3. 3 specific improvement recommendations
        4. Mobile-friendliness assessment
        5. Overall score (1-10)
        Be concise but thorough in your analysis.
        """

        with open(metadata["screenshot_path"], "rb") as img_file:
            response = model.generate_content([
                prompt,
                {"mime_type": "image/png", "data": img_file.read()}
            ])

        return response.text
    except Exception as e:
        return f"Audit failed: {str(e)}"
