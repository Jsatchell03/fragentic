# Fragentic: AI-Powered Fragrance Recommendation Engine

## 📋 Overview

Fragentic is a full-stack AI-powered recommendation system that helps users discover fragrances tailored to their preferences. Using OpenAI's embeddings and MongoDB vector search, the platform analyzes natural language descriptions of fragrance notes and returns the most relevant fragrances from a curated dataset of 23,000+ products.

---

## 🎯 Problem & Solution

### The Challenge
Fragrance discovery is inherently subjective. Users often struggle to describe what they're looking for, and traditional keyword-based search fails to capture the nuances of scent profiles.

### Our Solution
By leveraging **semantic embeddings** and **vector search**, Fragentic understands the meaning behind user descriptions rather than just keyword matching. A user can say "warm vanilla with citrus top notes" and get accurate results, even if those exact words aren't in a fragrance's metadata.

---

## 🏗️ Architecture

### System Design
```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                     │
│  DescriptorSearch → Filters → Results Display           │
├─────────────────────────────────────────────────────────┤
│                    REST API (Flask)                     │
│  /search, /filters, /accords, /brands, /notes           │
├─────────────────────────────────────────────────────────┤
│            OpenAI API (text-embedding-3-small)          │
│         Semantic embeddings                             │
├─────────────────────────────────────────────────────────┤
│            MongoDB Atlas Vector Search                  │
│   - Fragrances collection with embedded vectors         │
│   - Aggregation pipeline for post-filtering             │
└─────────────────────────────────────────────────────────┘
```


## 💡 Technical Highlights

### Frontend (React 19 + Vite)
- **Advanced State Management**: Complex nested state using `useState` hooks with careful dependency management
- **Responsive Design**: Mobile-first approach with custom Tailwind breakpoints for optimal UX across devices
- **Real-time Filtering**: Cascading filters (gender, brand, country, rating, popularity, notes)
- **Performance**: Client-side fuzzy matching using Levenshtein distance algorithm for instant autocomplete feedback
- **Loading States**: Full-screen spinner during initial data load, inline spinner for search results
- **Component Architecture**: Modular, reusable components (FilterSearch, FilterRating, FilterRange) reducing code duplication

**Key Files**:
- `UserInput.jsx` (158 LOC): Main orchestrator managing API calls and state synchronization
- `SearchBar.jsx` (174 LOC): Custom autocomplete with fuzzy matching
- `Results.jsx`: Sorting (relevance, rating, popularity) and result limiting (5-100)

### Backend (Flask 3 + REST API)
- **API Design**: 6 RESTful endpoints with consistent response formatting
- **MongoDB Aggregation**: Complex aggregation pipelines with vector search, filtering, and sorting in single database round-trip
- **Error Handling Strategy**: Retry logic with exponential backoff for resilience
- **Cost Optimization**: Averages multiple embeddings into single vector to reduce OpenAI API calls

### Data Pipeline (Python Scripts)
- **Embedding Generation** (`embed_frags.py`): Batch processing of 23K fragrances, generating and storing OpenAI embeddings
- **Analytics** (`add_popularity.py`): Calculates popularity quintiles using statistical analysis
- **LRU Cache** (`LRU_cache.py`): Custom in-memory cache implementation reducing duplicate API calls during data processing

### Database (MongoDB Atlas)
- **Vector Index**: `fragranceVectorSearch` on 384-dimensional `fragranceVector` field for O(1) similarity queries
- **Document Structure**: ~23K fragrances with metadata (brand, country, rating, popularity quintile, notes, accords, gender)
- **Scalability**: Vector indices enable sub-second search even with growing dataset

---

## 🚀 Skills Demonstrated

### Full-Stack Development
✅ React (hooks, state management, responsive design)
✅ Flask REST API (routing, serialization, error handling)
✅ MongoDB (aggregation pipelines, indexing, vector search)
✅ Python data processing (batch operations, ETL pipelines)

### AI & Machine Learning
✅ Semantic embeddings (OpenAI API integration)
✅ Vector similarity search and retrieval
✅ Embedding averaging and dimension handling
✅ Real-world LLM application design

### System Design
✅ Client-server architecture
✅ RESTful API design principles
✅ Scalable data pipeline
✅ Caching strategies (LRU, database indices)



---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React | 19 |
| Frontend Framework | Vite | 7 |
| Styling | Tailwind CSS | 4 |
| Backend | Flask | 3 |
| Database | MongoDB Atlas | - |
| Vector Search | MongoDB Vector Search | - |
| AI/Embeddings | OpenAI API | text-embedding-3-small |
| Package Manager (Frontend) | npm | - |
| Package Manager (Backend) | pip | - |

---


## 🔄 Key Features

✨ **Semantic Search**: Understand fragrance preferences in natural language
🎯 **Advanced Filtering**: Gender, brand, country, rating, popularity, notes/accords
⚡ **Real-time Autocomplete**: Client-side fuzzy matching for instant feedback
📱 **Responsive Design**: Optimized for mobile, tablet, and desktop
🔄 **Sorting Options**: By relevance, rating, or popularity
🎨 **Modern UI**: Clean, intuitive interface with loading states

---

## 📈 Future Enhancements

### Performance Optimization
- Implement query result caching (Redis) to reduce OpenAI API calls
- Pre-compute embeddings for common descriptor combinations
- Add pagination to reduce initial payload size

### Feature Expansion
- User accounts and search history
- Save favorite fragrances
- Collaborative filtering for personalized recommendations
- Reviews and ratings from users
- "Similar Fragrances" suggestions



## 📄 License

Personal portfolio project - for demonstration purposes.
