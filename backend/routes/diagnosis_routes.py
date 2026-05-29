from flask import Blueprint, request, jsonify
from services.database_service import DatabaseService
from services.gemini_service import GeminiService
import logging

logger = logging.getLogger(__name__)
diagnosis_bp = Blueprint('diagnosis', __name__)

db_service = DatabaseService()
gemini_service = GeminiService()

@diagnosis_bp.route('/diagnose', methods=['POST'])
def diagnose():
    try:
        data = request.get_json()
        
        # Input Validation
        if not data:
            return jsonify({"error": "Invalid JSON payload."}), 400
            
        patient_name = data.get('patient_name')
        symptoms = data.get('symptoms')
        
        if not patient_name or not patient_name.strip():
            return jsonify({"error": "Patient name is required."}), 400
            
        if not symptoms or not symptoms.strip():
            return jsonify({"error": "Symptoms are required."}), 400

        # AI Processing
        logger.info(f"Processing diagnosis for {patient_name}")
        ai_analysis = gemini_service.analyze_symptoms(patient_name, symptoms)
        
        # Simulated Object Storage (GCS)
        report_url = f"https://storage.googleapis.com/medical-report/example-report-{patient_name.replace(' ', '-').lower()}.pdf"
        
        # Database Storage
        db_result = db_service.save_diagnosis(patient_name, symptoms, ai_analysis, report_url)
        
        return jsonify({
            "success": True,
            "message": "Diagnosis completed successfully.",
            "data": {
                "id": db_result['id'],
                "patient_name": patient_name,
                "symptoms": symptoms,
                "ai_analysis": ai_analysis,
                "report_url": report_url,
                "created_at": db_result['created_at']
            }
        }), 201

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Server Error during diagnosis: {e}")
        return jsonify({"error": "An internal server error occurred while processing the diagnosis."}), 500


@diagnosis_bp.route('/history', methods=['GET'])
def history():
    try:
        history_data = db_service.get_all_history()
        return jsonify({
            "success": True,
            "count": len(history_data),
            "data": history_data
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        return jsonify({"error": "Failed to retrieve diagnosis history."}), 500
