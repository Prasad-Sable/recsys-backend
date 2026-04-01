import os
import json
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv
from database import lessons_collection

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_api_key,
)

async def generate_lesson_via_llm(topic: str, difficulty: str, duration: int) -> dict:
    """
    Calls OpenRouter (e.g., using a gemini model) to generate a customized micro-lesson.
    Parses the JSON output and returns a Lesson dictionary ready to insert into MongoDB.
    """
    prompt = f"""
    You are an expert micro-learning content creator. 
    Create a highly engaging, informative, and knowledgeable brief {duration}-minute lesson about "{topic}" at a {difficulty} level.
    
    IMPORTANT: Provide deep insights and useful information. Do not be overly basic. 
    Even if the level is Beginner, include interesting facts or specialized knowledge that makes the article truly informative.
    
    The lesson content should be formatted in Markdown (using ## for main headers, ### for subheaders, and bullet points).
    Include an interactive 3-question Multiple Choice Quiz (MCQ) based exactly on the content.

    Return the result strictly as a raw JSON object with the following schema (DO NOT wrap in ```json ... ``` tags, just raw JSON):
    {{
        "title": "A catchy and professional title for the lesson",
        "topic": "{topic}",
        "difficulty": "{difficulty}",
        "duration": {duration},
        "content": "The markdown formatted text here...",
        "quiz": [
            {{
                "question": "Question text here?",
                "options": [{{"text": "Option A"}}, {{"text": "Option B"}}, {{"text": "Option C"}}, {{"text": "Option D"}}],
                "answer_index": 0,
                "explanation": "Why this is correct."
            }},
            // exactly 3 questions
        ]
    }}
    Ensure all string escaping is perfectly valid JSON. Do not include any text before or after the JSON braces.
    """
    
    try:
        response = await client.chat.completions.create(
            # Using Gemini 2.0 Flash for superior intelligence and speed
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": "You are a professional educational content generator. You output strict raw JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2500
        )
        
        content = response.choices[0].message.content.strip()
        
        # Clean up any potential markdown formatting in the output
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        lesson_data = json.loads(content)
        return lesson_data
        
    except Exception as e:
        print("LLM Generation Error:", e)
        return None

async def evaluate_quiz_via_llm(lesson: dict, user_answers: list) -> dict:
    """
    Passes the lesson context, quiz questions, and the user's selected answers to OpenRouter.
    The LLM scores the quiz and provides highly tailored, encouraging feedback.
    """
    prompt = f"""
    You are an expert, highly encouraging tutor evaluating a student's quiz submission.
    Here is the original lesson context:
    Title: {lesson['title']}
    Topic: {lesson['topic']}

    Here is the Quiz they took, alongside what options they selected:
    """
    
    for i, q in enumerate(lesson.get("quiz", [])):
        # find user's answer
        user_opt_idx = next((a["selected_option"] for a in user_answers if a["question_index"] == i), -1)
        user_opt_text = q["options"][user_opt_idx]["text"] if 0 <= user_opt_idx < len(q["options"]) else "No Answer"
        correct_opt_text = q["options"][q["answer_index"]]["text"]
        
        prompt += f"\nQ{i+1}: {q['question']}\nUser Answered: {user_opt_text}\nCorrect Answer: {correct_opt_text}\n"

    prompt += """
    Evaluate their performance.
    Return EXACTLY a raw JSON object with the following schema:
    {
        "score_percentage": number (0 to 100),
        "total_correct": number,
        "total_questions": number,
        "feedback": "A very encouraging, personalized 1-2 sentence feedback string explaining what they did well and what they need to review based exactly on the questions they got wrong."
    }
    """
    
    try:
        response = await client.chat.completions.create(
            model="google/gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You output strict raw JSON according to user specifications."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        content = response.choices[0].message.content.strip()
        if content.startswith("```json"): content = content[7:]
        if content.startswith("```"): content = content[3:]
        if content.endswith("```"): content = content[:-3]
            
        evaluation = json.loads(content)
        return evaluation
        
    except Exception as e:
        print("LLM Evaluation Error:", e)
        return None

async def create_and_store_lesson(topic: str, difficulty: str, duration: int):
    lesson_data = await generate_lesson_via_llm(topic, difficulty, duration)
    if lesson_data:
        # validate required fields
        if "title" in lesson_data and "content" in lesson_data and "quiz" in lesson_data:
            result = await lessons_collection.insert_one(lesson_data)
            lesson_data["_id"] = str(result.inserted_id)
            return lesson_data
    return None
