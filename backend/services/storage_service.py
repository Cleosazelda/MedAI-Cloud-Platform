import os
import boto3
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def upload_diagnosis_report(patient_name, patient_age, symptoms, ai_analysis):
    try:
        # Ambil kredensial Cloudflare R2 dari file .env
        access_key = os.getenv('AWS_ACCESS_KEY_ID')
        secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        endpoint = os.getenv('AWS_ENDPOINT_URL')
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME', 'medai-reports')
        region = os.getenv('AWS_REGION', 'auto')

        if not access_key or not secret_key or not endpoint:
            logger.warning("Kredensial Cloudflare R2 tidak lengkap di .env! Menggunakan fallback local.")
            return f"/mock-url/{patient_name}_report.md"

        # LOGIKA PEMBUATAN NAMA FILE OTOMATIS DI DALAM SERVICE
        # Mengubah spasi jadi underscore dan menambah timestamp biar nama file unik
        safe_patient_name = patient_name.replace(' ', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"{safe_patient_name}_{timestamp}_report.md"

        # Inisialisasi client Boto3 untuk Cloudflare R2
        s3_client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint,
            region_name=region
        )

        # Konten file yang akan diupload adalah hasil analisis dari Gemini (ai_analysis)
        file_content = ai_analysis
        if isinstance(file_content, str):
            file_content = file_content.encode('utf-8')

        # Upload langsung ke Cloudflare R2 Bucket
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_content,
            ContentType='text/markdown'
        )

        logger.info(f"Berhasil mengunggah laporan {file_name} ke Cloudflare R2!")
        
        # Mengembalikan string URL lokasi file di bucket R2
        return f"{endpoint}/{bucket_name}/{file_name}"

    except Exception as e:
        logger.error(f"Gagal mengunggah file ke Cloudflare R2: {e}")
        # Fallback aman agar demo tidak crash jika koneksi R2 bermasalah
        return f"/mock-url-fallback/{patient_name}_report.md"
