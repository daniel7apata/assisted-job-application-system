# Assisted Job Application System

## Overview

The **Assisted Job Application System** is a voice-controlled application designed to assist users in Peru with the job search and application processes. It features a Streamlit frontend for a voice-guided user experience, a FastAPI backend for data management, and leverages AI/LLMs for Natural Language Understanding (NLU), CV refinement, and job summary generation.

## Key Features

### Voice-Assisted Interface (Frontend)

  * **Full Voice Control:** Navigates the entire application using speech-to-text (Google Cloud Speech) and provides audio feedback via text-to-speech (gTTS).
  * **Audio Pre-processing:** Includes noise reduction (`noisereduce`) to improve speech recognition accuracy.
  * **LLM Integration (NLU/AI):** Uses OpenAI's models for:
      * Classifying user intent (e.g., login, create CV, apply for a job).
      * Refining raw voice transcription into formal, structured CV content (Education, Skills, Experience).
      * Summarizing long job descriptions for quick voice review.

### Job Application Flow

  * **Targeted Job Search:** Scrapes job offers from **Computrabajo (Peru)** filtered by role, modality (Virtual/Presential/Hybrid), and region (for non-remote jobs).
  * **CV Management:** Users can create a new CV or modify an existing one. The system generates a formatted Harvard-style CV in a `.docx` document.
  * **Guided Application:** Saves the user's application details and provides a direct, transformed link to the job posting page for final submission.
  * **Application Review:** Users can review a summary of their past job applications.

### Backend API (FastAPI)

  * **Technology Stack:** Built with Python, FastAPI, and SQLAlchemy.
  * **Database:** Uses MySQL (configured for AWS RDS) for persistent storage.
  * **Models (Pydantic/SQLAlchemy):** Manages data for `Usuario` (User), `Vacante` (Job Posting), `Postulacion` (Application), and `HojaDeVida` (CV).
  * **CRUD Operations:** Complete set of CRUD operations are implemented for all core models.

## Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend Framework** | FastAPI | High-performance Python web framework for the API. |
| **Database/ORM** | SQLAlchemy, PyMySQL | ORM for interacting with the MySQL/AWS RDS database. |
| **API Deployment** | Mangum, Docker | Used to deploy the FastAPI application as an AWS Lambda function. |
| **Frontend UI** | Streamlit | Web application framework for the user interface. |
| **Speech-to-Text** | Google Cloud Speech | Converts user voice commands into text. |
| **Text-to-Speech** | gTTS | Provides voice responses to the user. |
| **Job Scraping** | Requests, BeautifulSoup4 | Used to fetch and parse job data from Computrabajo. |
| **AI/NLU** | OpenAI (GPT-4.1-nano) | Handles intent classification and intelligent text refinement. |
| **Document Generation** | python-docx | Generates the professional CV document. |


### Prerequisites

  * Python 3.11
  * An active **AWS RDS** MySQL instance (or local MySQL setup).
  * **Google Cloud Project** with Speech-to-Text API enabled.
  * **OpenAI API Key**.

## Usage

1.  Access the Streamlit application in your browser.
2.  The application will prompt you with the message: "¿Tiene cuenta creada?" (Do you have an account created?).
3.  Follow the voice prompts to either **Login** or **Register**.
4.  From the main menu, you can choose to:
      * **Create/Modify CV:** The system will gather information via voice and generate a formatted `.docx` file.
      * **Apply for a job:** Specify role, modality, and region (if applicable). The system will present summarized job postings for selection.
      * **Review Applications:** View a summary of your past applications.
