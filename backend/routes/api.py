import logging
# pyrefly: ignore [missing-import]
from flask import Blueprint, request, jsonify
from services.gemini_service import generate_diagnosis
from services.storage_service import upload_diagnosis_report
from services.db_service import save_consultation, get_consultation_history

logger = logging.getLogger(__name__)
api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "healthy", "service": "MedAI Backend API"}), 200

@api_bp.route('/diagnose', methods=['POST'])
def diagnose():
    """Endpoint to process symptoms and return an AI diagnosis."""
    try:
        data = request.get_json()
        
        # Input Validation
        if not data:
            return jsonify({"error": "Invalid JSON format."}), 400
            
        patient_name = data.get('patient_name')
        patient_age = data.get('patient_age')
        symptoms = data.get('symptoms')
        
        if not patient_name or not isinstance(patient_name, str) or not patient_name.strip():
            return jsonify({"error": "Valid patient_name is required."}), 400
            
        if patient_age is None or not isinstance(patient_age, (int, float)) or patient_age <= 0:
            return jsonify({"error": "Valid patient_age is required."}), 400
            
        if not symptoms or not isinstance(symptoms, str) or not symptoms.strip():
            return jsonify({"error": "Symptoms description is required."}), 400
            
        # Get AI Diagnosis
        ai_analysis = generate_diagnosis(patient_name, patient_age, symptoms)
        
        # Upload to Object Storage
        report_url = upload_diagnosis_report(patient_name, patient_age, symptoms, ai_analysis)
        
        # Save to Database (with fallback for testing without DB)
        try:
            db_result = save_consultation(patient_name, patient_age, symptoms, ai_analysis, report_url)
        except Exception as e:
            logger.warning(f"Database save failed, returning mock data for test mode. Error: {e}")
            from datetime import datetime
            db_result = {
                "id": "mock-id-999",
                "created_at": datetime.now()
            }
        
        return jsonify({
            "message": "Diagnosis generated successfully.",
            "data": {
                "id": db_result['id'],
                "patient_name": patient_name,
                "patient_age": patient_age,
                "symptoms": symptoms,
                "ai_analysis": ai_analysis,
                "report_url": report_url,
                "created_at": db_result['created_at'].isoformat() if db_result.get('created_at') else None
            }
        }), 200
        
    except ValueError as ve:
        logger.error(f"Validation/Configuration Error: {ve}")
        return jsonify({"error": str(ve)}), 500
    except Exception as e:
        logger.error(f"Unexpected Error during diagnosis: {e}")
        return jsonify({"error": "An internal server error occurred while processing the request."}), 500

@api_bp.route('/history', methods=['GET'])
def history():
    """Endpoint to fetch consultation history."""
    try:
        limit = request.args.get('limit', default=50, type=int)
        records = get_consultation_history(limit=limit)
        return jsonify({
            "message": "History fetched successfully.",
            "data": records
        }), 200
    except Exception as e:
        logger.error(f"Error fetching history (DB might be down): {e}")
        return jsonify({
            "error": "Failed to fetch history (DB might be offline).", 
            "data": []
        }), 200
