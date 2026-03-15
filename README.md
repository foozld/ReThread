# 🌿 ReThread - Sustainable Fashion Analyzer

Welcome to ReThread! This is a full-stack web application that analyzes clothing materials and provides information about their environmental sustainability.

## 📋 Project Overview

ReThread allows users to:
- Enter a clothing material name or composition of materials (e.g., hemp, linen, 50% polyester 50% cotton)
- Get detailed sustainability information including:
  - Environmental impact description
  - Water usage statistics
  - Biodegradability timeline
  - Sustainable alternative suggestions
  - AI-generated explanations

This project includes:
- ✅ Clean, beginner-friendly code with extensive comments
- ✅ Complete project structure ready to extend
- ✅ Pre-loaded sustainability database with 28 materials
- ✅ Responsive UI with sustainability-focused green design
- ✅ Graceful fallbacks for API outages
- ✅ All necessary configuration files

## 🏗️ Project Structure

```
ReThread/
├── app.py                 # Flask backend application
├── ai_helper.py           # LLM integration module
├── materials.json         # Clothing materials database
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (secrets)
├── .gitignore             # Git ignore file
├── README.md              # This file
│
├── templates/
│   └── index.html         # Frontend homepage
│
└── static/
    ├── style.css          # Stylesheet (green sustainability theme)
    └── script.js          # Frontend JavaScript logic
```

## 📚 Project Features

### Backend (Python + Flask)
- ✅ REST API for material analysis
- ✅ JSON-based material database
- ✅ LLM integration placeholder (ready for OpenAI or similar)
- ✅ Error handling and validation
- ✅ Graceful fallbacks
- ✅ Detailed comments for learning

### Frontend (HTML + CSS + JavaScript)
- ✅ Responsive design (works on mobile/tablet/desktop)
- ✅ Green sustainability color theme
- ✅ Dynamic result rendering
- ✅ Loading states and error messages
- ✅ Click alternatives to analyze them
- ✅ Smooth animations and transitions
- ✅ Accessibility features

### Data (JSON)
- ✅ 28 pre-loaded clothing materials
- ✅ Sustainability ratings
- ✅ Environmental impact descriptions
- ✅ Water usage statistics
- ✅ Biodegradability info
- ✅ Alternative suggestions

### Using Services
- **Frontend**: Vercel, Netlify (after separating frontend)
- **Backend**: Heroku, Railway, Render
- **Database**: PostgreSQL (if you add one later)

## 📄 License

This starter project is provided AS-IS for educational and hackathon purposes.

---

## 🌍 Mission

ReThread exists to make sustainable fashion more accessible. By providing clear, science-based information about fabric sustainability, we empower consumers to make environmentally conscious choices.

**Every sustainable choice matters. 🌱**

---

Made with 💚 for sustainable fashion
