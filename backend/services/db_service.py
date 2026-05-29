import os
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    psycopg2 = None
    RealDictCursor = None
import logging

logger = logging.getLogger(__name__)

def get_db_connection():
    if psycopg2 is None:
        raise Exception("psycopg2 is not installed. Running in mock mode.")
    try:
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            database=os.getenv('POSTGRES_DB', 'medai_db'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'password'),
            port=os.getenv('POSTGRES_PORT', '5432')
        )
        return conn
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise e

def save_consultation(patient_name, patient_age, symptoms, ai_analysis, report_url):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            INSERT INTO consultation_history (patient_name, patient_age, symptoms, ai_analysis, report_url)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, created_at;
        """
        cur.execute(query, (patient_name, patient_age, symptoms, ai_analysis, report_url))
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return {"id": result[0], "created_at": result[1]}
    except Exception as e:
        logger.error(f"Error saving consultation: {e}")
        raise e

def get_consultation_history(limit=50):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT id, patient_name, patient_age, symptoms, ai_analysis, report_url, created_at 
            FROM consultation_history 
            ORDER BY created_at DESC 
            LIMIT %s;
        """
        cur.execute(query, (limit,))
        records = cur.fetchall()
        cur.close()
        conn.close()
        
        # Convert datetime objects to ISO strings for JSON serialization
        result = []
        for row in records:
            row_dict = dict(row)
            if row_dict.get('created_at'):
                row_dict['created_at'] = row_dict['created_at'].isoformat()
            result.append(row_dict)
            
        return result
    except Exception as e:
        logger.error(f"Error fetching consultation history: {e}")
        raise e
