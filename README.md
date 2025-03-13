# Latin2Sonnet API

A simple API for transforming text with customizable options.

## API Endpoints

### POST /api/process-text

Transform input text with specified options.

**Request Body:**
```json
{
    "text": "Your input text here",
    "options": {
        "addErrors": false,    // Add human-like typing errors
        "keepProfessional": true    // Maintain professional tone
    }
}
```

**Response:**
```json
{
    "success": true,
    "modifiedText": "Transformed text result"
}
```

**Error Response:**
```json
{
    "success": false,
    "error": "Error message"
}
```

## Running Locally

1. Install dependencies:
```bash
pip install flask flask-cors nltk
```

2. Start the server:
```bash
cd backend
python app.py
```

The server will run on http://localhost:5000
