# AI Documentation: SDGs Health Analysis

## AI Engine
The MedAI Cloud Platform utilizes the **Google Gemini API** as its core AI Service. Specifically, it employs the `gemini-1.5-pro-latest` model, which provides an excellent balance of speed, cost-effectiveness, and high-quality natural language understanding suitable for processing medical symptoms.

## Alignment with SDGs
**SDG 3: Good Health and Well-being**

This AI integration directly supports SDG 3 by providing accessible, preliminary health assessments. It can act as a telemedicine triage tool, helping patients understand their symptoms quickly, advising them on whether they need immediate emergency care, and suggesting the appropriate medical specialists to consult.

## Implementation Details

### Model Configuration
- **Provider:** Google (Gemini)
- **Model Version:** `gemini-1.5-pro-latest`

### Prompt Engineering
The system uses a highly structured prompt to ensure the AI acts strictly as an assistant and provides safely formatted outputs. 

**System Role:**
```text
You are a highly skilled AI medical assistant.
```

**User Prompt Structure:**
```text
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
```

### Safety & Ethical Considerations
- **Disclaimer:** The prompt strictly instructs the LLM to output a medical disclaimer stating that the analysis is not a substitute for professional medical advice.
- **Privacy:** Patient names and ages are passed to the AI solely for context processing. In a production environment, PII (Personally Identifiable Information) should be anonymized before being sent to third-party APIs.
- **Object Storage Archiving:** Every generated AI report is archived into a Google Cloud Storage Bucket for audit trails and future reference.
