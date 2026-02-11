import os
import aiohttp

# PASTE YOUR KEY HERE IF ENV VARS FAIL
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "groq_api_key" 

class InterviewManager:
    def __init__(self, resume_text, difficulty="intermediate"):
        self.api_key = GROQ_API_KEY
        self.difficulty = difficulty.lower()
        
        # Difficulty-specific instructions
        difficulty_prompts = {
            "beginner": "Ask foundational and easy questions about basic concepts. Focus on understanding the candidate's basic knowledge.",
            "intermediate": "Ask moderately challenging questions that test practical knowledge and problem-solving skills.",
            "advanced": "Ask very challenging questions that test deep expertise, system design, edge cases, and advanced problem-solving abilities."
        }
        
        difficulty_instruction = difficulty_prompts.get(self.difficulty, difficulty_prompts["intermediate"])
        
        self.history = [
            {
                "role": "system", 
                "content": f"""
                You are an expert technical interviewer. 
                You have the candidate's resume below. 
                
                DIFFICULTY LEVEL: {self.difficulty.upper()}
                {difficulty_instruction}
                
                RESUME CONTEXT:
                {resume_text}
                
                YOUR GOAL:
                1. Ask relevant questions based on the resume and the candidate's previous answers.
                2. Adjust question complexity based on the difficulty level specified above.
                3. Do NOT provide feedback yet. Just ask the next question.
                4. Keep questions concise (1-2 sentences).
                5. If the user says "Please repeat the question", then ask the question again.
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
        
        difficulty_feedback_prompts = {
            "beginner": "Provide constructive feedback on their understanding of basic concepts. Mention what they did well and areas for improvement in foundational knowledge.",
            "intermediate": "Provide detailed feedback on their technical knowledge, problem-solving approach, and communication skills. Mention strengths and areas for improvement.",
            "advanced": "Provide expert-level feedback on their deep technical expertise, architectural thinking, edge case handling, and advanced problem-solving abilities. Mention standout performances and areas to strengthen."
        }
        
        feedback_instruction = difficulty_feedback_prompts.get(self.difficulty, difficulty_feedback_prompts["intermediate"])
        
        feedback_prompt.append({
            "role": "system", 
            "content": f"The interview ({self.difficulty.upper()} level) is over. {feedback_instruction}"
        })
        
        feedback = await self._call_groq(feedback_prompt, max_tokens=600)
        return feedback
