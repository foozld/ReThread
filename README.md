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
- ✅ 12 pre-loaded clothing materials
- ✅ Sustainability ratings
- ✅ Environmental impact descriptions
- ✅ Water usage statistics
- ✅ Biodegradability info
- ✅ Alternative suggestions

## 🚢 Deployment (After Hackathon)

### Quick Deployment to Heroku
1. Install Heroku CLI
2. `heroku create rethread-yourname`
3. Add `gunicorn` to `requirements.txt`
4. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
5. `git push heroku main`

### Using Services
- **Frontend**: Vercel, Netlify (after separating frontend)
- **Backend**: Heroku, Railway, Render
- **Database**: PostgreSQL (if you add one later)

## 🎨 Possible Extensions

- **Admin Panel**: CRUD interface for materials
- **User Accounts**: Save favorite materials
- **Advanced Search**: Filter by sustainability rating
- **Material Recommendations**: Quiz-based fabric suggestions
- **Community Reviews**: User feedback on materials
- **Carbon Calculator**: Estimate carbon footprint of clothing
- **Price Comparison**: Show sustainable alternatives with costs
- **Mobile App**: React Native or Flutter wrapper
- **Database**: Migrate from JSON to PostgreSQL
- **Analytics**: Track popular searches

## 📝 Code Quality

All code includes:
- Meaningful variable names
- Detailed docstrings for functions
- Inline comments for complex logic
- Clear error messages
- Consistent formatting
- No hardcoded values (use `materials.json` and `.env`)

## 🤝 Contributing to This Project

1. Create descriptive commit messages
2. Follow the existing code style
3. Add comments for new features
4. Update `materials.json` for new fabrics
5. Test before pushing

## 📄 License

This starter project is provided AS-IS for educational and hackathon purposes.

## ❓ Questions?

- Check the comments in each file - they're very thorough!
- Run `python ai_helper.py` to see example outputs
- Check browser console for debugging (F12)
- Read the docstrings: they explain what each function does

---

## 🎯 Final Checklist Before Submission

- [ ] App runs without errors
- [ ] All 12 materials can be analyzed
- [ ] Frontend displays results correctly
- [ ] JavaScript works (can click alternatives)
- [ ] `.env` file is in `.gitignore`
- [ ] No API keys in git
- [ ] README is clear and helpful
- [ ] Code is commented
- [ ] Responsive design works on mobile
- [ ] Error handling works (try analyzing "invalid")

---

## 🌍 Mission

ReThread exists to make sustainable fashion more accessible. By providing clear, science-based information about fabric sustainability, we empower consumers to make environmentally conscious choices.

**Every sustainable choice matters. 🌱**

---

Made with 💚 for sustainable fashion
