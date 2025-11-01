---
title: Naruto TVanalyser
emoji: 🍥
colorFrom: orange
colorTo: red
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# TVanalyser - Naruto Character Analysis & Chatbot Platform

A comprehensive AI-powered platform for analyzing Naruto anime content, featuring theme classification, character network analysis, jutsu classification, and interactive character chatbots.

<img width="1918" height="927" alt="Screenshot 2025-09-02 102344" src="https://github.com/user-attachments/assets/af489f4f-e16d-45a7-bab7-0dcff15060a9" />

## 🎯 Project Overview

TVanalyser is a multi-phase machine learning project that leverages various NLP techniques to analyze and interact with Naruto anime content. The platform combines theme classification, character relationship mapping, jutsu categorization, and conversational AI to create an immersive fan experience.

## 🛠️ Tech Stack & Architecture

### Core Technologies
- **Python 3.12+**
- **Gradio** - Interactive UI framework
- **Hugging Face Transformers** - Pre-trained models and fine-tuning
- **spaCy** - Advanced NLP processing
- **NetworkX** - Graph analysis and visualization
- **PyVis** - Interactive network visualization

### Data Processing
- **pandas** - Data manipulation and analysis
- **numpy** - Numerical computing
- **nltk** - Natural language processing
- **pathlib** - File system operations

## 📊 Project Phases

### Phase 1 – Theme Classifier
**Objective**: Classify themes and their importance across 300+ Naruto episodes

**Technologies**:
- `transformers` - Hugging Face model integration
- `nltk` - Text preprocessing and analysis
- `pandas` - Data handling
- `numpy` - Numerical operations
- `pathlib` - File management

**Model**: `facebook/bart-large-mnli`
- Zero-shot classification for theme detection
- Importance scoring for narrative elements
- Episode-level theme analysis

<img width="1919" height="537" alt="Screenshot 2025-09-02 102415" src="https://github.com/user-attachments/assets/1f336963-7489-48fd-be10-ac45dccff751" />
  
### Phase 2 – Character Neural Network
**Objective**: Build an interactive web of character connections and relationships

**Technologies**:
- `nltk` - Text processing
- `pandas` - Data manipulation
- `networkx` - Graph theory and network analysis
- `pyvis` - Interactive network visualization
- `pathlib` - File operations

**Model**: `spacy en_core_web_trf`
- Named Entity Recognition (NER) for character identification
- Relationship extraction from dialogue and narrative
- Dynamic network visualization with character interactions

<img width="1864" height="828" alt="Screenshot 2025-09-02 102505" src="https://github.com/user-attachments/assets/8877ce96-88b6-425b-8e64-1407f254e9c5" />

### Phase 3 – Text Classification (Jutsu Classification)
**Objective**: Classify queries into ninja techniques (Ninjutsu, Genjutsu, Taijutsu)

**Technologies**:
- `numpy` - Numerical computing
- `pandas` - Data analysis
- `evaluate` - Model evaluation metrics
- `huggingface_hub` - Model management
- `sklearn` - Machine learning utilities
- `datasets` - Data handling

**Model**: Fine-tuned `distilbert/distilbert-base-uncased`
- Custom training on Naruto-specific terminology
- Multi-class classification for jutsu types
- High accuracy classification system

🔗 **Hugging Face Model**: https://lnkd.in/gCN-atFY

<img width="1798" height="607" alt="Screenshot 2025-09-02 103109" src="https://github.com/user-attachments/assets/f7d70269-3874-4f1e-8668-a62aec44f89d" />

### Phase 4 – Character Chatbot
**Objective**: Enable conversations with favorite characters (Naruto, Sasuke, Sakura)

**Evolution & Learning**:
- **Initial Approach**: `meta-llama/Meta-Llama-3-8B`
  - Experienced challenges with Colab Pro GPU requirements
  - Gained hands-on experience with model deployment trade-offs
  - Learned about scaling challenges and inference pipeline optimization
  - **Experiment Link**: https://lnkd.in/gpBD445n

- **Current Solution**: Gemini API with fine-tuning
  - Focused on conversation design and retrieval augmentation
  - Implemented multi-agent conversation flows
  - Optimized for resource efficiency and deployment scalability

<img width="1839" height="670" alt="Screenshot 2025-09-02 105824" src="https://github.com/user-attachments/assets/e25c7f27-1dee-4e59-8c3c-d68566f3f4d2" />

## 🎨 User Interface

**Gradio Integration**
- Seamless integration with Hugging Face ecosystem
- Interactive and responsive web interface
- Real-time model inference and visualization
- User-friendly design for complex AI operations

## 📁 Project Structure

```
TVanalyser/
├── character_chatbot/          # Phase 4 - Character chatbot implementation
├── character_network/          # Phase 2 - Character relationship analysis
├── components/                 # UI components and assets
├── crawler/                   # Data collection utilities
├── data/                      # Datasets and processed data
├── text_classification/       # Phase 3 - Jutsu classification
├── theme_classifier/          # Phase 1 - Theme analysis
├── utils/                     # Shared utilities and data loaders
├── vaishnaviiii34/           # Model checkpoints and training artifacts
└── gradio_app.py             # Main application entry point
```

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Virtual environment (recommended)

### Installation
1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
```bash
python gradio_app.py
```

## 📈 Key Features

- **Multi-Modal Analysis**: Combines text classification, NER, and conversational AI
- **Interactive Visualizations**: Dynamic character networks and theme analysis
- **Scalable Architecture**: Modular design supporting multiple ML models
- **Real-time Inference**: Fast model predictions through optimized pipelines
- **User-Friendly Interface**: Intuitive Gradio-based web application

## 🎓 Learning Outcomes

This project demonstrates expertise in:
- **Model Fine-tuning**: Custom training on domain-specific data
- **Deployment Trade-offs**: Understanding resource constraints vs. model performance
- **Multi-Agent Systems**: Complex conversation flows and retrieval augmentation
- **End-to-End ML Pipelines**: From data collection to user interface
- **Production Considerations**: Scaling, optimization, and maintenance

## 📊 Data Sources

- **300+ Naruto Episodes**: Comprehensive anime content analysis
- **Subtitles**: Multi-language subtitle processing
- **Character Data**: Extensive character relationship mapping
- **Jutsu Database**: Curated ninja technique classifications

## 🤝 Contributing

This project showcases advanced NLP techniques and ML deployment strategies. Feel free to explore the codebase and adapt the methodologies for your own projects.

## 📄 License

This project is for educational and demonstration purposes.
---
🔗 **LinkedIn Post**: https://www.linkedin.com/posts/vaishnavi-mishra-b17ba6256_adding-another-skill-that-nowadays-is-a-must-activity-7368537981785153538-WKyB?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD8uPMMBqRpwGF1E1y23LaGw3BRKzCllt0Q 
---

*Built with ❤️ using Python, Hugging Face, and Gradio*
