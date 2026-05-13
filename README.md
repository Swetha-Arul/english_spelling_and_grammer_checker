# Compiler Spell Studio

Compiler Spell Studio is a compiler-inspired English text correction system that applies lexical analysis, spelling validation, and grammar checking to improve written English text.
The project demonstrates how compiler design concepts such as tokenization, parsing, and validation can be applied to natural language processing using a simple web-based interface.

---

## Features

- Lexical analysis using custom tokenization
- Dictionary-based spelling validation
- Rule-based grammar checking
- Repeated word detection
- Article agreement correction (`a/an`)
- Capitalization validation
- Missing punctuation detection
- Corrected text generation
- Compiler pipeline visualization
- Token stream preview
- File upload support (`.txt`, `.md`)
- Responsive modern UI

---

## Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- Built-in HTTP Server

---

## Screenshots

### Home Interface

<img width="2182" height="1444" src="https://github.com/user-attachments/assets/cea80d73-bc70-4231-a47f-502c02b3020b" />

---

### Analysis Report

Input loaded using `sample-input.txt`

<img width="2714" height="1508" src="https://github.com/user-attachments/assets/06e891e3-1314-445d-b0d5-9705d2fa6170" />

---

## How It Works

### 1. Lexical Analysis
The lexer breaks input text into:
- Words
- Numbers
- Punctuation
- Whitespace

### 2. Spelling Validation
Words are checked against a dictionary and corrected using edit-distance logic.

### 3. Grammar Checking
The parser identifies:
- Missing punctuation
- Repeated words
- Incorrect articles
- Capitalization issues

### 4. Correction Pipeline
The system generates corrected text after applying all detected fixes.

---

## Project Structure

```text
Compiler-Spell-Studio/
│
├── app.py
├── sample-input.txt
│
├── backend/
│   ├── __init__.py
│   ├── server.py
│   ├── pipeline.py
│   ├── lexer.py
│   ├── parser.py
│   ├── spell_checker.py
│   ├── corrector.py
│   ├── dictionary.py
│   └── utils.py
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
├── LICENSE
│
└── README.md
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/Swetha-Arul/english_spelling_and_grammar_checker.git
cd english_spelling_and_grammar_checker
```

---

## Running the Project

```bash
python app.py
```

or

```bash
py app.py
```

Open the application in your browser:

```text
http://127.0.0.1:3000
```

---

## Sample Input

```text
this is a smple paragraph for the the compiler based checker
i wrote an example report that need punctuation and an book introduction
```

---

## API Endpoint

### Analyze Text

```http
POST /api/analyze
```

### Request Body

```json
{
  "text": "your input text"
}
```

---

## Concepts Demonstrated

- Compiler Design Fundamentals
- Lexical Analysis
- Parsing and Validation
- Token Streams
- Edit Distance Algorithms
- Rule-Based NLP
- Backend/Frontend Integration

---

## License

This project is licensed under the MIT License.
