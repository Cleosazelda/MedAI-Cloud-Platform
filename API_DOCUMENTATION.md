# API Documentation

This document provides details on the REST API endpoints available in the MedAI Cloud Platform Backend.

## Base URL
`/api` (e.g., `http://localhost:5000/api`)

---

## 1. Health Check
Endpoint to verify the API is running correctly.

**Endpoint:** `GET /health`

**Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "MedAI Backend API"
}
```

---

## 2. Generate Diagnosis
Analyzes patient symptoms using Google Gemini API and saves the consultation record to PostgreSQL and Google Cloud Storage.

**Endpoint:** `POST /diagnose`

**Headers:**
- `Content-Type: application/json`

**Request Body:**
```json
{
  "patient_name": "John Doe",
  "patient_age": 45,
  "symptoms": "I have been experiencing a mild fever, dry cough, and fatigue for the past 3 days."
}
```

**Response (200 OK):**
```json
{
  "message": "Diagnosis generated successfully.",
  "data": {
    "id": 1,
    "patient_name": "John Doe",
    "patient_age": 45,
    "symptoms": "I have been experiencing a mild fever, dry cough, and fatigue for the past 3 days.",
    "ai_analysis": "### Potential Conditions\n- Common Cold\n- Influenza\n...",
    "report_url": "https://storage.googleapis.com/your-bucket/reports/report-12345.txt",
    "created_at": "2023-10-27T10:00:00.000Z"
  }
}
```

**Error Responses:**
- `400 Bad Request`: Validation errors (e.g., missing patient name or symptoms).
- `500 Internal Server Error`: Server processing errors.

---

## 3. Consultation History
Fetches a list of previous consultations ordered by the most recent.

**Endpoint:** `GET /history`

**Query Parameters:**
- `limit` (optional): Integer representing the maximum number of records to return. Default is 50.

**Response (200 OK):**
```json
{
  "message": "History fetched successfully.",
  "data": [
    {
      "id": 1,
      "patient_name": "John Doe",
      "patient_age": 45,
      "symptoms": "Mild fever, dry cough...",
      "ai_analysis": "### Potential Conditions...",
      "report_url": "https://storage.googleapis.com/your-bucket/reports/report-12345.txt",
      "created_at": "2023-10-27T10:00:00.000Z"
    }
  ]
}
```
