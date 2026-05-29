CREATE TABLE IF NOT EXISTS consultation_history (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    patient_age INT NOT NULL,
    symptoms TEXT NOT NULL,
    ai_analysis TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster retrieval ordered by creation time
CREATE INDEX IF NOT EXISTS idx_consultation_history_created_at 
ON consultation_history(created_at DESC);
