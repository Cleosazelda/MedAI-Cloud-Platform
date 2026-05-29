import psycopg2
import os
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.host = os.environ.get('DB_HOST', 'localhost')
        self.dbname = os.environ.get('DB_NAME', 'med_sdg_db')
        self.user = os.environ.get('DB_USER', 'postgres')
        self.password = os.environ.get('DB_PASSWORD', 'postgres')
        self.port = os.environ.get('DB_PORT', '5432')

    def get_connection(self):
        try:
            conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            return conn
        except psycopg2.Error as e:
            logger.error(f"Error connecting to PostgreSQL database: {e}")
            raise Exception("Database connection failed")

    def save_diagnosis(self, patient_name, symptoms, ai_analysis, report_url):
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            insert_query = """
                INSERT INTO health_diagnoses (patient_name, symptoms, ai_analysis, report_url)
                VALUES (%s, %s, %s, %s) RETURNING id, created_at;
            """
            
            cur.execute(insert_query, (patient_name, symptoms, ai_analysis, report_url))
            result = cur.fetchone()
            conn.commit()
            
            return {
                "id": result[0],
                "created_at": result[1].isoformat()
            }
        except Exception as e:
            logger.error(f"Error saving diagnosis: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                cur.close()
                conn.close()

    def get_all_history(self):
        conn = None
        try:
            conn = self.get_connection()
            cur = conn.cursor()
            
            select_query = """
                SELECT id, patient_name, symptoms, ai_analysis, report_url, created_at
                FROM health_diagnoses
                ORDER BY created_at DESC;
            """
            
            cur.execute(select_query)
            rows = cur.fetchall()
            
            history = []
            for row in rows:
                history.append({
                    "id": row[0],
                    "patient_name": row[1],
                    "symptoms": row[2],
                    "ai_analysis": row[3],
                    "report_url": row[4],
                    "created_at": row[5].isoformat()
                })
                
            return history
        except Exception as e:
            logger.error(f"Error fetching history: {e}")
            raise
        finally:
            if conn:
                cur.close()
                conn.close()
