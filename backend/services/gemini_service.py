import os
# pyrefly: ignore [missing-import]
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in environment variables.")
        raise ValueError("GEMINI_API_KEY is not set.")
    genai.configure(api_key=api_key)

def generate_diagnosis(patient_name, patient_age, symptoms):
    try:
        configure_gemini()
        # Initialize the model, prefer a capable model for health analysis
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        You are a highly skilled AI medical assistant. Please analyze the following patient symptoms.
        DISCLAIMER: State clearly that this is an AI analysis and not a substitute for professional medical advice.

        Patient Profile:
        - Name: {patient_name}
        - Age: {patient_age}

        Symptoms Reported:
        {symptoms}

        Please provide:
        1. Potential conditions or diagnoses based on the symptoms.
        2. Suggested next steps for the patient (e.g., rest, see a doctor, seek immediate emergency care).
        3. Relevant medical specialties the patient might want to consult.
        
        Format your response clearly with headings using Markdown.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error generating diagnosis from Gemini: {e}")
        raise e
