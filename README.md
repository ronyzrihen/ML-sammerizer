# Machine Learning Summarizer API

## Description

This project provides a machine learning-based summarization and translation API designed to meet specific academic deliverables. It takes a text (in Hebrew or English), translates it to English if necessary, summarizes it using Ollama’s Phi-3 model, and then translates the result back to the desired target language. The entire system is built as a FastAPI service that supports real-time streaming responses and is deployed via Docker.

## 🚀 Features

- **Translation Service**: Automatic translation between Hebrew ↔ English using `facebook/nllb-200-distilled-600M`.
- **Summarization Service**: Text summarization powered by `phi-3-mini-4k-instruct` via Ollama.
- **Streaming Responses**: Real-time, low-latency output for a better user experience.
- **Easy Deployment**: A simple Python deployment script for automated setup and healthchecks.
- **Configurable Generation**: API endpoints accept parameters (`temperature`, `top_p`, `max_tokens`) to control model output.
- **Interactive Documentation**: Comes with a full Swagger UI for easy testing.

## 🧠 Requirements

- Python 3.10+
- Docker and Docker Compose
- Internet access for initial model and dependency downloads

## ⚙️ Installation and Deployment

### Step 1: Clone the Repository

```bash
git clone https://github.com/ronyzrihen/ML-summerizer.git
cd ML-summerizer
```

### Step 2: Run the Deployment Script

The provided Python script automates the entire deployment and verification process:

```bash
python3 Deployment.py
```

#### Deployment Script Behavior

The script automatically performs the following actions:

- **Checks for Docker**: Verifies Docker is installed and running.
- **Builds & Starts Containers**: Runs `docker compose up -d` to launch all services.
- **Performs Healthcheck**: Pings the `/healthcheck` endpoint to confirm the API is running.
- **Displays Container Status**: Shows the status of all running project containers.
- **Graceful Error Handling**: Prints a detailed error message and exits if any step fails.

## 🔬 Verification & Testing

### 1. API Healthcheck

Confirm the FastAPI service is online:

```bash
curl http://localhost:8000/healthcheck
```

✅ Expected Response:

```
"Summerizer is up and running"
```

### 2. Test Translation Model

Send a request to `/translate` to verify the NLLB model:

```bash
curl -X POST "http://localhost:8000/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, world!",
    "src_lang": "eng_Latn",
    "tgt_lang": "heb_Hebr"
  }'
```

✅ Expected Response:

```json
{
  "translation": "שלום, עולם!"
}
```

### 3. Test Summarization Model

Send a request to `/summarize` to verify the end-to-end flow:

```bash
curl -N -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "The project uses Docker for deployment. It includes a translation model from Hugging Face and a summarization model from Ollama. The API is built with FastAPI.",
    "src_lang": "eng_Latn",
    "tgt_lang": "eng_Latn"
  }'
```

✅ Expected Response: A streamed, 5-point summary of the text.

## 🧠 Understanding Generation Parameters

The `/summarize` endpoint accepts parameters that influence model output:

| Parameter   | Type  | Default | Description                                                                                                 |
| ----------- | ----- | ------- | ----------------------------------------------------------------------------------------------------------- |
| temperature | float | 0.6     | Controls randomness. Lower values (0.2) produce deterministic output; higher (1.0) produce creative output. |
| top_p       | float | 0.9     | Nucleus sampling; limits vocabulary to the most probable tokens. Lower values lead to more focused output.  |
| max_tokens  | int   | 512     | Maximum number of tokens in the generated summary.                                                          |

### Parameter Effects: Live Examples

#### Input Text

```
אניגמה היא משפחה של מכונות להצפנה ולפענוח של מסרים טקסטואליים, ששימשו את הכוחות הגרמנים והאיטלקים במלחמת העולם השנייה...
```

#### Example 1: Low Temperature (0.2)

```bash
curl -N -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "אניגמה היא משפחה של מכונות להצפנה ולפענוח של מסרים טקסטואליים, ששימשו את הכוחות הגרמנים והאיטלקים במלחמת העולם השנייה...",
    "src_lang": "heb_Hebr",
    "tgt_lang": "heb_Hebr",
    "temperature": 0.2
  }'
```

**Predictable Factual Output:**

1. אניגמה היה מכונת חישוב/החישוב שימשו במלחמת העולם השנייה על ידי כוחות גרמנים ואיטליה.
2. הוא אפשר לתקשורת מוצפנת עבור Kriegsmarine (צי הגרמנים).
3. הצי הצולמי השתמש בטכנולוגיה במהלך הקרב באטלנטיק.
4. הודעות מוצפנות עזרו להגן על בריטניה מפני הפרעות במשאבי הים.
5. אנגמה מילאה תפקיד במניעת אספקה של מזון ומלחמה לאי בריטי על ידי הים.

#### Example 2: High Temperature (1.0)

```bash
curl -N -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "אניגמה היא משפחה של מכונות להצפנה ולפענוח של מסרים טקסטואליים, ששימשו את הכוחות הגרמנים והאיטלקים במלחמת העולם השנייה...",
    "src_lang": "heb_Hebr",
    "tgt_lang": "heb_Hebr",
    "temperature": 1.0
  }'
```

**Creative and Varied Output:**

1. אניגמה שימשה להצפנה/פענוח של הודעות טקסט במלחמת העולם השנייה על ידי כוחות גרמנים ואיטלקים.
2. סייעה לקרייגסמרין (צי הגרמנים).
3. התמקדה בפעילות הצי הצולמי במהלך הקרב באטלנטיק.
4. סיפקה תקשורת מוצפנת כדי להגן על בריטניה דרך דרכים ימיים (1939–1945).
5. מנעה הפרת אספקת מזון ומלחמה באי בריטי דרך הים
