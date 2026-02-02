import os
import aiohttp

# PASTE YOUR KEY HERE IF ENV VARS FAIL
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "groq_api_key" 

class InterviewManager:
    def __init__(self, resume_text):
        self.api_key = GROQ_API_KEY
        self.history = [
            {
                "role": "system", 
                "content": f"""
                You are an expert technical interviewer. 
                You have the candidate's resume below. 
                
                RESUME CONTEXT:
                {resume_text}
                
                YOUR GOAL:
                1. Ask relevant, challenging questions based on the resume and the candidate's previous answers.
                2. Do NOT provide feedback yet. Just ask the next question.
                3. Keep questions concise (1-2 sentences).
                4. If the user says "Please repeat the question", then ask the question again.
                """
            }
        ]

    async def _call_groq(self, messages, max_tokens=150):
        if not self.api_key or "YOUR_ACTUAL" in self.api_key:
            return "Error: API Key missing in groq_llm.py"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "max_tokens": max_tokens
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            ) as response:
                if response.status != 200:
                    return f"Error: {await response.text()}"
                result = await response.json()
                return result["choices"][0]["message"]["content"]

    async def get_next_question(self, user_answer):
        # 1. Add user answer to history
        self.history.append({"role": "user", "content": user_answer})
        
        # 2. Get AI response (The Question)
        question = await self._call_groq(self.history, max_tokens=100)
        
        # 3. Add AI question to history so it remembers for next time
        self.history.append({"role": "assistant", "content": question})
        
        return question

    async def get_final_feedback(self):
        # Create a temporary prompt for feedback without messing up the main history too much
        feedback_prompt = list(self.history)
        feedback_prompt.append({
            "role": "system", 
            "content": "The interview is over. Provide detailed feedback on the candidate's performance. Mention strengths, weaknesses, and clarity of speech. Be constructive."
        })
        
        feedback = await self._call_groq(feedback_prompt, max_tokens=600)
        return feedback
