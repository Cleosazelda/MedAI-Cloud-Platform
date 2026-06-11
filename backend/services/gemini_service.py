import os
import requests
import logging

logger = logging.getLogger(__name__)

def generate_diagnosis(patient_name, patient_age, symptoms):
    try:
        # Mengambil API Key dari .env yang sudah kamu isi dengan key fresh dari temanmu
        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            logger.error("API Key Gemini tidak ditemukan di environment .env!")
            raise Exception("API Key Gemini is missing")

        # MENGGUNAKAN JALUR GEMINI 1.5 PRO (ASLI & LEBIH STABIL UNTUK IP EC2)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        prompt = f"""
        You are a highly skilled AI medical assistant. Please analyze the following patient symptoms.
        DISCLAIMER: State clearly that this is an AI analysis and not a substitute for professional medical advice.

        Patient Profile:
        - Name: {patient_name}
        - Age: {patient_age}

        Symptoms Reported:
        {symptoms}

        Please provide potential conditions, suggested next steps, and relevant medical specialties.
        Format your response clearly with headings using Markdown.
        """

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }

        logger.info("=" * 50)
        logger.info(f"Patient Name: {patient_name}")
        logger.info(f"Patient Age: {patient_age}")
        logger.info(f"Symptoms Length: {len(str(symptoms))}")
        logger.info(f"Symptoms: {str(symptoms)[:1000]}")
        logger.info(f"Prompt Length: {len(prompt)}")
        logger.info("=" * 50)
        # Nembak langsung ke Google asli
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code != 200:
            logger.error(f"Google API Error ({response.status_code}): {response.text}")
            raise Exception(f"Gemini API returned status code {response.status_code}")

        res_json = response.json()
        
        # Ambil teks asli dari respon Google
        text_output = res_json['candidates'][0]['content']['parts'][0]['text']
        return text_output

    except Exception as e:
        logger.error(f"Error fatal pada sistem internal Gemini: {e}")
        raise e
