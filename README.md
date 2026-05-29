# Cloud Computing SDGs Health AI (MedAI Cloud Platform)

MedAI Cloud Platform is a cloud-native healthcare application that utilizes AI (Google Gemini) to analyze patient symptoms and provide a preliminary diagnosis, suggested next steps, and recommended medical specialties. The platform is designed with a modern architecture, utilizing a React-like responsive UI (Vanilla JS + CSS), a Python/Flask API, and PostgreSQL for persistent data storage.

This project was built to align with the Sustainable Development Goals (SDGs) for Good Health and Well-being.

## Architecture & Tech Stack

- **Frontend:** HTML5, CSS3 (Modern, Responsive, Glassmorphism), Vanilla JavaScript, Nginx (for serving static files and proxying API).
- **Backend:** Python, Flask, Gunicorn, Google Generative AI (Gemini SDK).
- **Database:** PostgreSQL 15.
- **Containerization:** Docker & Docker Compose.
- **CI/CD:** GitHub Actions.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose installed on your local machine.
- A valid [Google Gemini API Key](https://aistudio.google.com/app/apikey).

## Local Setup & Deployment Tutorial

1. **Clone the repository (if applicable)**
   ```bash
   git clone <repository_url>
   cd UTS3
   ```

2. **Configure Environment Variables**
   - Create a `.env` file in the root of the project (where `docker-compose.yml` is located). You can copy the template from `backend/.env.example`:
   ```bash
   cp backend/.env.example .env
   ```
   - Open `.env` and fill in your Gemini API key:
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password
   POSTGRES_DB=medai_db
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Build and Run with Docker Compose**
   From the root directory, run the following command to build the images and start the containers in detached mode:
   ```bash
   docker-compose up --build -d
   ```

4. **Verify Deployment**
   - Wait a few seconds for the database to initialize.
   - Access the Frontend: Open your browser and go to `http://localhost`.
   - Access the Backend API: `http://localhost:5000/api/health`

5. **Usage**
   - Enter patient details and symptoms in the "New Diagnosis" section.
   - Click "Analyze Symptoms". The backend will contact the Gemini API and save the results to the database.
   - Go to "Consultation History" to view past records.

6. **Stopping the Application**
   ```bash
   docker-compose down
   ```

## Folder Structure

```
├── .github/
│   └── workflows/
│       └── deploy.yml        # CI/CD Pipeline Configuration
├── backend/
│   ├── routes/
│   │   └── api.py            # API Endpoints (diagnose, history, health)
│   ├── services/
│   │   ├── db_service.py     # PostgreSQL database logic
│   │   └── gemini_service.py # Gemini AI integration logic
│   ├── .env.example          # Template for backend env vars
│   ├── app.py                # Main Flask application
│   ├── Dockerfile            # Backend container instructions
│   └── requirements.txt      # Python dependencies
├── database/
│   └── init.sql              # Database schema and initial setup
├── frontend/
│   ├── app.js                # Frontend logic and API integration
│   ├── Dockerfile            # Frontend container instructions
│   ├── index.html            # Main UI layout
│   ├── nginx.conf            # Nginx reverse proxy configuration
│   └── styles.css            # Custom styling
├── docker-compose.yml        # Orchestration for the entire stack
└── README.md                 # Project documentation
```

## API Documentation

### 1. Health Check
- **Endpoint:** `GET /api/health`
- **Description:** Returns the status of the API.
- **Response:** `200 OK`
```json
{
  "status": "healthy",
  "service": "MedAI Backend API"
}
```

### 2. Generate Diagnosis
- **Endpoint:** `POST /api/diagnose`
- **Description:** Sends symptoms to AI and returns analysis.
- **Body:**
```json
{
  "patient_name": "John Doe",
  "patient_age": 30,
  "symptoms": "Headache and fever for 2 days"
}
```
- **Response:** `200 OK` with JSON object containing `data` with `ai_analysis`.

### 3. Consultation History
- **Endpoint:** `GET /api/history`
- **Description:** Retrieves past consultations.
- **Query Params:** `?limit=50` (optional)
- **Response:** `200 OK` with list of records.
