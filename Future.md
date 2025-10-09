# Future Roadmap: Adapting TVanalyser for Other Series

## 🎯 Overview

This document provides a **non-technical roadmap** for adapting the TVanalyser project from Naruto to any other TV series, anime, or show. By following this guide, you can replace the Naruto-specific data with content from your favorite series and have a fully functional analysis platform.

---

## 📋 Table of Contents

1. [Understanding the Project Structure](#understanding-the-project-structure)
2. [Data Requirements by Phase](#data-requirements-by-phase)
3. [Step-by-Step Adaptation Guide](#step-by-step-adaptation-guide)
4. [Series-Specific Considerations](#series-specific-considerations)
5. [Quality Assurance Checklist](#quality-assurance-checklist)

---

## 🏗️ Understanding the Project Structure

The project has **4 main phases**, each requiring specific data:

### Phase 1: Theme Classifier
- **Purpose**: Analyzes themes across episodes (e.g., friendship, betrayal, sacrifice)
- **Data Needed**: Episode subtitles or scripts
- **Series-Agnostic**: Themes can be customized for any show

### Phase 2: Character Network
- **Purpose**: Maps character relationships and interactions
- **Data Needed**: Subtitles/scripts with character names and dialogue
- **Series-Specific**: Requires accurate character identification

### Phase 3: Text Classification (Domain-Specific Classifier)
- **Purpose**: Classifies series-specific concepts (e.g., Jutsu types in Naruto)
- **Data Needed**: Domain-specific terminology and descriptions
- **Highly Series-Specific**: Requires complete reimagining for new series

### Phase 4: Character Chatbot
- **Purpose**: Interactive conversations with main characters
- **Data Needed**: Character dialogue and personality profiles
- **Series-Specific**: Requires character-specific prompt engineering

---

## 📊 Data Requirements by Phase

### 1. **Subtitle/Script Data** (Phases 1, 2, 4)

#### Current Format (Naruto):
- Location: `data/Subtitles/`
- Format: `.ass` and `.srt` subtitle files
- Content: Character names + dialogue lines
- Episodes: 220+ files

#### What You Need for Your Series:
- **Source**: Download subtitles from streaming services or subtitle databases
- **Format Options**: 
  - Subtitle files (`.srt`, `.ass`, `.vtt`)
  - Fan transcripts
  - Official scripts (if available)
  - Web-scraped episode transcripts
- **Quality Requirements**:
  - Must include character names for each line of dialogue
  - Should cover all or most episodes/seasons
  - Consistent formatting across files
  - Clear separation between character names and dialogue

#### Format Example Structure:
```
Character Name, Dialogue Line
Character Name, Dialogue Line
```

#### How to Obtain:
1. **Legal Sources**: Official subtitle downloads, DVD/Blu-ray rips (personal use)
2. **Fan Communities**: Fan-made transcripts from series-specific wikis
3. **Subtitle Databases**: OpenSubtitles, Subscene, etc.
4. **Web Scraping**: Episode transcript websites (respect terms of service)

---

### 2. **Character Dialogue CSV** (Phases 2, 4)

#### Current Format (Naruto):
- Location: `data/naruto.csv`
- Columns: `name` (character), `line` (dialogue)
- Purpose: Structured dialogue for NER and chatbot training

#### What You Need for Your Series:
- **Format**: CSV file with character names and their dialogue
- **Content**: 
  - Every line of dialogue from your series
  - Character names normalized (e.g., always "Tony Stark" not "Iron Man" or "Tony")
  - Chronological order helps but not required
- **Size**: More data = better results (aim for hundreds to thousands of lines)

#### Creation Process:
1. **From Subtitles**: Extract character names and dialogue into CSV
2. **From Transcripts**: Parse transcript files into structured format
3. **Manual Curation**: Clean up character name variations and errors
4. **Validation**: Check for duplicate entries and formatting issues

---

### 3. **Domain-Specific Classification Data** (Phase 3)

#### Current Format (Naruto):
- Location: `data/jutsus.jsonl`
- Format: JSONL (JSON Lines)
- Fields:
  - `jutsu_name`: Name of the technique
  - `jutsu_type`: Category (Ninjutsu, Genjutsu, Taijutsu)
  - `jutsu_description`: Detailed explanation

#### What You Need for Your Series:
This is the **most series-specific** component. You need to identify a classifiable domain concept in your series:

**Examples by Series Type**:
- **Harry Potter**: Spell classification (Charm, Transfiguration, Curse, etc.)
- **Star Trek**: Technology classification (Propulsion, Weapons, Medical, etc.)
- **Game of Thrones**: House allegiance classification
- **Marvel/DC**: Superpower classification (Strength, Speed, Telepathy, etc.)
- **Attack on Titan**: Titan type classification
- **My Hero Academia**: Quirk type classification
- **Pokemon**: Move type classification

#### Data Structure:
- **Item Name**: The specific instance (spell name, power name, etc.)
- **Category/Type**: The classification label
- **Description**: Detailed text explaining the item (used for training)

#### Collection Methods:
1. **Fan Wikis**: Most series have comprehensive wikis with categorized information
2. **Official Guides**: Published reference materials
3. **Web Scraping**: Automated collection from wiki pages (adapt the crawler)
4. **Community Databases**: Fan-maintained databases
5. **Manual Curation**: Create your own dataset from watching the series

#### Minimum Dataset Size:
- **Small Dataset**: 100-200 items (may work but limited)
- **Good Dataset**: 500-1000 items (recommended)
- **Excellent Dataset**: 1000+ items (best results)

---

### 4. **Character Personality Profiles** (Phase 4)

#### Current Implementation (Naruto):
- Location: Hardcoded in `character_chatbot/character_chatbot.py`
- Format: Character-specific system prompts
- Content: Personality traits, speech patterns, abilities, relationships

#### What You Need for Your Series:
For each character you want users to chat with:

**Essential Information**:
1. **Core Personality**: Key traits (brave, cynical, optimistic, etc.)
2. **Speech Patterns**: How they talk (formal, casual, uses catchphrases, etc.)
3. **Background**: Major life events, motivations, goals
4. **Abilities/Skills**: What makes them special in the series
5. **Relationships**: Family, friends, rivals
6. **Iconic Phrases**: Catchphrases or memorable quotes

**Example Template**:
- **Character**: [Name]
- **Personality**: [3-5 key traits]
- **Speaking Style**: [How they communicate]
- **Abilities**: [Powers, skills, or expertise]
- **Relationships**: [Key connections]
- **Background**: [Major story points]
- **Catchphrases**: [Signature expressions]

#### Character Selection:
- Start with 3-5 main characters
- Choose characters with distinct personalities
- Include fan favorites
- Cover different personality types (hero, anti-hero, comic relief, etc.)

---

## 🚀 Step-by-Step Adaptation Guide

### **STEP 1: Choose Your Series**

**Considerations**:
- **Episode Count**: More episodes = more data (ideal: 20+ episodes)
- **Character Count**: Not too many main characters (ideal: 5-15 major characters)
- **Domain Concept**: Does it have a classifiable system? (powers, magic, technology)
- **Data Availability**: Can you access subtitles/transcripts?
- **Language**: English content is easiest; other languages require translation

**Good Candidates**:
- Long-running anime (One Piece, Bleach, Attack on Titan)
- TV dramas with multiple seasons (Breaking Bad, Friends, The Office)
- Fantasy series with magic systems (Harry Potter, LOTR)
- Sci-fi with technology systems (Star Trek, Doctor Who)
- Superhero series (Marvel shows, The Boys)

---

### **STEP 2: Gather Subtitle/Script Data**

**Action Items**:
1. **Locate Sources**:
   - Check OpenSubtitles, Subscene, or series-specific subtitle sites
   - Look for fan transcript projects
   - Consider series-specific wikis with episode transcripts

2. **Download Files**:
   - Get subtitles for all available episodes
   - Maintain consistent naming (e.g., `SeriesName_S01E01.srt`)

3. **Verify Format**:
   - Check if character names are included
   - Verify dialogue is readable
   - Ensure files are in a processable format

4. **Organize**:
   - Create folder: `data/Subtitles/`
   - Place all subtitle files there
   - Keep backup copies

---

### **STEP 3: Create Character Dialogue CSV**

**Action Items**:
1. **Extract Dialogue**:
   - Parse subtitle files to extract character names and lines
   - Use scripting or manual extraction depending on file format
   - Tools: Python scripts, text editors with regex, or CSV editors

2. **Normalize Character Names**:
   - Pick one canonical name per character
   - Replace all variations (nicknames, titles) with canonical name
   - Examples: "Mr. White" → "Walter White", "The Doctor" → "The Doctor" (keep consistent)

3. **Create CSV**:
   - Columns: `name`, `line`
   - Format: One row per dialogue line
   - Save as: `data/[your_series_name].csv`

4. **Quality Check**:
   - Remove duplicates
   - Fix encoding issues
   - Verify character names are correct

---

### **STEP 4: Build Domain Classification Dataset**

**Action Items**:
1. **Identify Domain Concept**:
   - What unique system exists in your series?
   - What categories/types are there?
   - Is there enough variety for classification?

2. **Gather Data**:
   - **Option A: Web Scraping**
     - Adapt the `crawler/jutsu_crawler.py` script
     - Target: Series-specific wiki (e.g., fandom.com)
     - Extract: Item names, types, descriptions
   
   - **Option B: Manual Collection**
     - Create spreadsheet with columns: Name, Type, Description
     - Fill from official guides or wiki pages
     - Export as JSONL or CSV

3. **Format Data**:
   - JSONL format (one JSON object per line)
   - Fields: `item_name`, `item_type`, `item_description`
   - Example naming: `data/[domain_items].jsonl`

4. **Validate**:
   - Check all entries have descriptions
   - Verify types are consistent
   - Aim for balanced distribution across types

---

### **STEP 5: Define Character Personalities**

**Action Items**:
1. **Select Characters**:
   - Choose 3-5 main characters
   - Pick characters with distinct, recognizable personalities
   - Include fan favorites

2. **Research Each Character**:
   - **Read**: Character wiki pages, character analyses
   - **Watch**: Key episodes featuring the character
   - **Note**: Speech patterns, catchphrases, mannerisms
   - **List**: Abilities, relationships, motivations

3. **Write Personality Prompts**:
   - Create a detailed description for each character
   - Include: personality traits, speaking style, background, abilities
   - Format: One prompt per character (150-300 words each)
   - Store in a document for later implementation

4. **Test Prompts Mentally**:
   - Would a fan recognize this character from the description?
   - Are the unique traits captured?
   - Is the speaking style clear?

---

### **STEP 6: Update Configuration Files**

**Action Items**:
1. **Main Application** (`gradio_app.py`):
   - Update title from "Naruto TV Analyzer" to "[Your Series] Analyzer"
   - Change hero section text and images
   - Update example themes in theme classification
   - Modify text classification section from "Jutsu Classification" to your domain

2. **Theme Classifier** (`theme_classifier/`):
   - Update default themes to match your series
   - Examples for different series:
     - **Breaking Bad**: moral-decline, family, crime, consequences, power, survival
     - **Harry Potter**: friendship, courage, good-vs-evil, sacrifice, love, destiny
     - **The Office**: workplace-humor, romance, awkwardness, ambition, team-dynamics

3. **Character Network** (`character_network/`):
   - No changes needed initially (works automatically with NER)
   - May need character name list for filtering/focusing on main characters

4. **Text Classifier** (`text_classification/`):
   - Update labels from jutsu types to your domain types
   - Update model name if you fine-tune a new model
   - Update examples in UI

5. **Character Chatbot** (`character_chatbot/`):
   - Replace character prompts with your character personality profiles
   - Update character names in dropdown/tabs
   - Update example questions for each character

---

### **STEP 7: Update File Paths and References**

**Action Items**:
1. **Data Paths**:
   - Change all references to `data/naruto.csv` → `data/[your_series].csv`
   - Update subtitle directory paths if different
   - Update classification data paths

2. **Output Paths**:
   - Update stub file paths if needed
   - Ensure output directories exist

3. **Model Paths**:
   - Phase 1 & 2: No changes (use same pre-trained models)
   - Phase 3: Update to your fine-tuned model path
   - Phase 4: No changes (Gemini API works universally)

---

### **STEP 8: Visual and Branding Updates**

**Action Items**:
1. **UI Elements**:
   - Replace Naruto-themed colors (currently orange)
   - Update hero section images
   - Change emojis to match series theme
   - Update section titles

2. **Documentation**:
   - Update README.md with your series name
   - Change screenshots to your project
   - Update project description

3. **Component Files** (`components/`):
   - Update navbar text
   - Update hero section with series-specific information
   - Update about section
   - Update footer

---

## 🎨 Series-Specific Considerations

### **Anime/Manga Series**
- **Advantages**: Usually have comprehensive wikis, fan translations
- **Data Sources**: Fan subtitle groups, Crunchyroll, Funimation
- **Domain Concepts**: Powers, techniques, transformations
- **Examples**: One Piece, Bleach, Attack on Titan, My Hero Academia

---

### **Western TV Dramas**
- **Advantages**: Professional subtitles, detailed transcripts
- **Data Sources**: OpenSubtitles, official streaming services
- **Domain Concepts**: May need creative classification (character relationships, plot devices)
- **Examples**: Breaking Bad, Game of Thrones, The Wire, Lost

---

### **Sitcoms**
- **Advantages**: Clear character personalities, lots of dialogue
- **Data Sources**: Fan transcript sites, subtitle databases
- **Domain Concepts**: Joke types, recurring gags, episode themes
- **Challenges**: Domain classification may be less natural
- **Examples**: Friends, The Office, Parks and Recreation, Brooklyn Nine-Nine

---

### **Fantasy Series**
- **Advantages**: Rich lore, magic systems, creature classifications
- **Data Sources**: Fan wikis, official guides, subtitle databases
- **Domain Concepts**: Spells, creatures, artifacts, prophecies
- **Examples**: Harry Potter, Lord of the Rings, The Witcher, Avatar: TLA

---

### **Sci-Fi Series**
- **Advantages**: Technology systems, alien species, equipment
- **Data Sources**: Detailed fan wikis, technical manuals
- **Domain Concepts**: Technology types, species, ship classes
- **Examples**: Star Trek, Doctor Who, The Expanse, Battlestar Galactica

---

### **Superhero Series**
- **Advantages**: Power classification, character abilities
- **Data Sources**: Comic databases, wiki pages, subtitles
- **Domain Concepts**: Powers, abilities, equipment, fighting styles
- **Examples**: Marvel shows, The Boys, Invincible, Arrow-verse

---

## ✅ Quality Assurance Checklist

### **Phase 1: Theme Classifier**
- [ ] Subtitles/scripts are in accessible location
- [ ] Files are in compatible format (.srt, .ass, or .vtt)
- [ ] Themes are defined and relevant to your series
- [ ] Test with a single file before processing all episodes
- [ ] Output CSV generates correctly with theme scores

---

### **Phase 2: Character Network**
- [ ] Character dialogue CSV exists with correct format
- [ ] Main character names are normalized (no duplicates)
- [ ] NER model correctly identifies character names
- [ ] Network graph generates with readable character nodes
- [ ] Relationships make sense based on actual show dynamics

---

### **Phase 3: Text Classification**
- [ ] Domain items dataset has at least 100+ entries
- [ ] Each item has a type/category and description
- [ ] Data is formatted correctly (JSONL or CSV)
- [ ] Model training data is balanced across categories
- [ ] Fine-tuned model is uploaded (if using Hugging Face)
- [ ] Test classifications are accurate for common items

---

### **Phase 4: Character Chatbot**
- [ ] Gemini API key is configured
- [ ] 3-5 character personality prompts are written
- [ ] Each prompt captures character's voice and traits
- [ ] Example questions are relevant to each character
- [ ] Chatbot responses feel authentic to character
- [ ] Multiple test conversations confirm quality

---

### **General Application**
- [ ] All file paths are updated to new series
- [ ] UI text references new series (not Naruto)
- [ ] Visual theme matches new series aesthetic
- [ ] All 4 phases work independently
- [ ] Example inputs are provided for each feature
- [ ] README is updated with new series information
- [ ] No broken links or missing files

---

## 🔄 Iterative Improvement Strategy

### **Start Small, Scale Up**
1. **Prototype Phase**:
   - Start with one season or 10-20 episodes
   - Test each phase with limited data
   - Validate approach before scaling

2. **Expand Data**:
   - Add more episodes gradually
   - Grow domain classification dataset
   - Add more characters to chatbot

3. **Refine Quality**:
   - Improve character name normalization
   - Enhance domain classification accuracy
   - Polish chatbot personality prompts
   - Fine-tune theme selections

---

### **Community Contribution**
- **Open Data Collection**: Invite fans to contribute transcripts
- **Crowd-Sourced Classification**: Create forms for fans to submit domain items
- **Character Prompt Refinement**: Test with fans to improve chatbot accuracy
- **Multi-Language Support**: Add subtitle support for other languages

---

## 🌟 Advanced Extensions

### **Multi-Series Support**
- Adapt the project to support multiple series in one application
- Add series selector dropdown in UI
- Maintain separate data folders per series
- Switch between series contexts dynamically

---

### **Cross-Series Analysis**
- Compare themes across different series
- Identify similar character archetypes
- Analyze narrative patterns across genres

---

### **Real-Time Updates**
- Automatically update when new episodes release
- Integrate with subtitle APIs for auto-download
- Continuous model fine-tuning with new data

---

### **Enhanced Character Chatbot**
- Fine-tune models on character-specific dialogue
- Implement retrieval-augmented generation for episode references
- Add multi-character conversations
- Enable episode-specific context (e.g., "talk as Naruto from Season 5")

---

## 📚 Resources and Tools

### **Data Collection**
- **Subtitle Sources**: OpenSubtitles, Subscene, Podnapisi
- **Transcripts**: Fan wikis, Springfield! Springfield!, Scraps from the Loft
- **Web Scraping**: Beautiful Soup (Python), Scrapy
- **Wikis**: Fandom.com, series-specific wikis

---

### **Data Processing**
- **CSV/JSON Tools**: pandas (Python), Excel, Google Sheets
- **Text Processing**: regex, NLTK, spaCy
- **File Conversion**: pysubs2 (subtitle format conversion)

---

### **Model Training**
- **Pre-trained Models**: Hugging Face Model Hub
- **Fine-Tuning**: Hugging Face Trainer, Google Colab
- **Evaluation**: scikit-learn, evaluate library

---

### **Character Research**
- **Character Wikis**: Detailed personality, backstory, relationships
- **Fan Communities**: Reddit, Discord, dedicated forums
- **YouTube**: Character analysis videos, compilation videos

---

## 🎯 Success Criteria

You'll know your adaptation is successful when:

1. **Theme Classifier**: Produces meaningful theme distributions that match your viewing experience
2. **Character Network**: Shows expected relationships (allies, rivals, family)
3. **Text Classifier**: Accurately categorizes domain items with 70%+ accuracy
4. **Character Chatbot**: Responses feel authentic and fans recognize the character's voice
5. **Overall**: Fans of the series find the tool useful and enjoyable

---

## 💡 Final Tips

1. **Start Simple**: Don't try to perfect everything at once
2. **Test Early**: Validate each phase before moving to the next
3. **Community Input**: Get feedback from fans of your series
4. **Document Changes**: Keep notes on what you modified for future reference
5. **Iterate**: First version won't be perfect—improve based on testing
6. **Have Fun**: This project is a celebration of the series you love!

---

## 📞 Need Help?

If you run into issues:
1. Check the original Naruto implementation for reference
2. Review error messages carefully (often point to file paths or data format issues)
3. Test with small datasets first (1-2 episodes, 10 domain items)
4. Validate data format matches expected structure
5. Ensure all dependencies are installed (`requirements.txt`)

---

## 🚀 You're Ready!

With this guide, you have everything you need to adapt TVanalyser to any series you love. The key is gathering quality data and updating references systematically. Take it one phase at a time, test frequently, and enjoy building your own series analysis platform!

**Happy Analyzing! 🎬📊✨**

