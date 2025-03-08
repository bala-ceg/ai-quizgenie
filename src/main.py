import asyncio
import os
import sys
from apify import Actor
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
from langchain_core.output_parsers.json import JsonOutputParser

from src.models import QuizGenieState
from src.tools import scrape_webpage, extract_pdf_from_url

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

def generate_quiz(text, num_questions=5, difficulty="Medium",model='gpt-4o'):
    """Generate quiz questions using LangChain-OpenAI with an AI Quizzer system prompt."""
    system_message = SystemMessage(content=(
        "You are AI Quizzer, an expert in creating high-quality multiple-choice questions (MCQs) from educational texts. "
        "Your goal is to generate engaging and insightful quizzes based on the provided content, ensuring accuracy and variety.\n\n"
        "- Use clear and concise language.\n"
        "- Ensure only one correct answer per question.\n"
        "- Provide explanations for each answer.\n"
        "- Follow the structured format strictly."
    ))

    prompt = ChatPromptTemplate.from_messages([
        system_message,  # ✅ No `MessagesPlaceholder`
        ("user", """Generate {num_questions} multiple-choice questions at a {difficulty} level based on the text.

        **Text:**
        {text}

        **Output Format (JSON Array)**
        [
            {{
                "question": "What is AI?",
                "options": ["Artificial Intelligence", "Machine Learning", "Data Science", "Neural Networks"],
                "answer": "Artificial Intelligence",
                "explanation": "AI refers to machine-based intelligence."
            }},
            ...
        ]
        """)
    ])

    llm = ChatOpenAI(
        model_name=model,
        temperature=0.7,
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_API_BASE
    )

    output_parser = JsonOutputParser()
    chain = prompt | llm | output_parser

    response = chain.invoke({
        "text": text[:5000],
        "num_questions": num_questions,
        "difficulty": difficulty
    })
    return response

graph = StateGraph(QuizGenieState)

def detect_content_type(state: QuizGenieState):
    """Detect whether the URL is a webpage or a PDF and extract text."""
    url = state.url.lower()

    # Detect PDF URLs accurately (ArXiv, ResearchGate, etc.)
    if url.endswith(".pdf") or "/pdf/" in url:
        state.extracted_text = extract_pdf_from_url(state.url)
    else:
        state.extracted_text = scrape_webpage(state.url)

    return state

graph.add_node("detect_content_type", detect_content_type)

def generate_questions(state: QuizGenieState):
    """Generate quiz questions based on extracted content."""
    state.questions = generate_quiz(state.extracted_text, state.num_questions, state.difficulty,state.model)
    Actor.log.info(state.questions)
    return state

graph.add_node("generate_questions", generate_questions)

graph.add_edge("detect_content_type", "generate_questions")
graph.set_entry_point("detect_content_type")
graph.add_edge("generate_questions", END)

quizgenie_workflow = graph.compile()

async def main():
    """Main Apify Actor function."""
    async with Actor:
        actor_input = await Actor.get_input() or {}

        # Validate input using Pydantic
        try:
            quiz_state = QuizGenieState(**actor_input)
        except ValueError as e:
            Actor.log.warning(f"Invalid input: {e}")
            await Actor.push_data({"error": str(e)})
            return

        # Execute the workflow
        final_state = quizgenie_workflow.invoke(quiz_state)
        
        # Charge for task completion
        await Actor.charge("generate-quiz")
        
        # Properly extract questions from `AddableValuesDict`
        await Actor.push_data({"questions": final_state.get('questions', [])})
        Actor.log.info("Quiz generated successfully!")
