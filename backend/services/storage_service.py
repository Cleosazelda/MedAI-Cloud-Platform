import os
import uuid
import logging
# pyrefly: ignore [missing-import]
from google.cloud import storage

logger = logging.getLogger(__name__)

def upload_diagnosis_report(patient_name, patient_age, symptoms, ai_analysis):
    """
    Generates a report file and uploads it to Google Cloud Storage.
    Returns the public URL of the uploaded report.
    """
    try:
        bucket_name = os.getenv("GCS_BUCKET_NAME")
        
        if not bucket_name:
            logger.warning("GCS_BUCKET_NAME is not set. Skipping object storage upload. Returning mock URL.")
            # Return a mock URL for development if bucket is not configured
            safe_name = patient_name.replace(' ', '-').lower()
            return f"https://storage.googleapis.com/mock-bucket/report-{safe_name}.txt"
            
        # Create a report content
        report_content = f"Medical Diagnosis Report\n"
        report_content += f"========================\n"
        report_content += f"Patient Name: {patient_name}\n"
        report_content += f"Patient Age: {patient_age}\n\n"
        report_content += f"Symptoms:\n{symptoms}\n\n"
        report_content += f"AI Analysis:\n{ai_analysis}\n"
        
        # Initialize GCS client
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        
        # Generate a unique filename
        filename = f"reports/report-{uuid.uuid4().hex}.txt"
        blob = bucket.blob(filename)
        
        # Upload from string
        blob.upload_from_string(report_content, content_type="text/plain")
        
        # Make the blob publicly viewable (optional, depends on your bucket settings)
        # blob.make_public()
        
        # Return the public URL
        return blob.public_url
        
    except Exception as e:
        logger.error(f"Error uploading report to GCS: {e}")
        # Even if upload fails, we don't want to crash the whole request, so return a placeholder
        return "Upload failed"
