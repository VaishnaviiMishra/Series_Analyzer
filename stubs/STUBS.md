# Stubs Data Strategy Guide

A simple guide to pre-compute all analysis data once, store it in `stubs/` folder, and provide instant access to users.

---

## The Problem

**Current State:**
- Users must provide file paths to subtitles (confusing and error-prone)
- Each user waits 30-60 minutes for models to process 220 episodes
- Models run repeatedly for every user (waste of resources)
- Poor user experience with technical requirements

**Solution:**
- You (developer) run models ONCE using Google Colab
- Save all results to `stubs/` folder
- Users select from dropdowns → instant results
- No paths, no processing, no waiting

---

## Overall Strategy

### Phase 1: Data Generation (Developer - One Time)
1. Upload subtitles to Google Colab
2. Run 3 analysis notebooks
3. Download generated files
4. Organize in `stubs/` folder
5. Commit to GitHub

### Phase 2: User Access (End Users - Forever Fast)
1. User opens Gradio app
2. User selects from dropdown (e.g., "Season 1")
3. App loads pre-computed data from `stubs/`
4. Results display instantly (< 1 second)

---

## Step-by-Step Process

### Step 1: Prepare Google Colab Environment

**What to do:**
- Create a Google Drive folder structure
- Upload all 220 subtitle files (.ass/.srt) to Google Drive
- Create empty output folder for generated data

**What you'll need:**
- Google account (free)
- Subtitle files (~150 MB)
- ~4 hours of processing time (one-time)

**Why Google Colab:**
- Free GPU access (faster processing)
- No local resource usage
- Can run in background
- Easy to share notebooks

---

### Step 2: Run Theme Classification Analysis

**What this does:**
- Loads all 220 episodes
- Runs BART-large-MNLI model for theme detection
- Analyzes themes like: friendship, hope, sacrifice, battle, etc.
- Generates theme scores for each episode

**What gets generated:**
1. **Per-episode themes** - Theme scores for each of 220 episodes
2. **Per-season themes** - Aggregated themes for each of 9 seasons
3. **Full series themes** - Overall theme distribution
4. **Per-arc themes** - Themes for story arcs (Chunin Exam, etc.)

**Time required:** ~2-3 hours (with GPU)

**Output files:**
- `theme_per_episode.csv` (~220 rows)
- `theme_per_season.csv` (~9 rows)
- `theme_all_episodes.csv` (~1 row)
- `theme_per_arc.csv` (~5-10 rows)

---

### Step 3: Run Character Network Analysis

**What this does:**
- Extracts all character names using spaCy NER
- Builds relationship graph based on co-occurrence
- Creates interactive visualizations
- Generates networks for full series and per-season

**What gets generated:**
1. **Entity data** - All extracted character names with metadata
2. **Network edges** - Character relationship strengths
3. **HTML visualizations** - Interactive network graphs

**Time required:** ~1-2 hours (with GPU)

**Output files:**
- `ner_output.csv` (all entities)
- `network_edges_all.csv` (relationship data)
- `network_viz_full.html` (interactive graph)
- `network_viz_season_1.html` through `season_9.html` (9 files)
- `network_edges_season_1.csv` through `season_9.csv` (9 files)

---

### Step 4: Generate Metadata

**What this does:**
- Scans all subtitle files
- Creates episode index with season/episode numbers
- Generates dropdown options for UI
- Defines story arcs and selections

**What gets generated:**
1. **Episode metadata** - Complete episode listing
2. **Selection options** - Dropdown choices for users
3. **Arc definitions** - Story arc boundaries

**Time required:** ~5 minutes

**Output files:**
- `episode_metadata.json`
- `selection_options.json`
- `arc_metadata.json` (optional)

---

### Step 5: Download and Organize Data

**What to do:**
- Download entire output folder from Google Drive
- Organize locally into proper folder structure
- Verify all files are present
- Check file sizes are reasonable

**Where files go:**
```
stubs/
├── theme_per_episode.csv
├── theme_per_season.csv
├── theme_all_episodes.csv
├── theme_per_arc.csv
├── ner_output.csv
├── network_edges_all.csv
├── network_viz_full.html
├── network_viz_season_1.html
├── network_viz_season_2.html
├── ... (more season files)
├── network_edges_season_1.csv
├── ... (more edge files)
├── episode_metadata.json
└── selection_options.json
```

**Total size:** ~40-50 MB (easy to commit to GitHub)

---

## Stubs Folder Structure

### Purpose of Each File

**Theme Classification Files:**
- `theme_per_episode.csv` → For episode-level analysis and line charts
- `theme_per_season.csv` → For season comparison bar charts
- `theme_all_episodes.csv` → For full series overview
- `theme_per_arc.csv` → For story arc analysis

**Character Network Files:**
- `ner_output.csv` → Raw entity data (backup/reference)
- `network_edges_all.csv` → Can regenerate graphs if needed
- `network_viz_full.html` → Ready-to-display full series network
- `network_viz_season_X.html` → Pre-rendered season networks
- `network_edges_season_X.csv` → Season-specific relationship data

**Metadata Files:**
- `episode_metadata.json` → Episode listing and info
- `selection_options.json` → Dropdown menu choices
- `arc_metadata.json` → Story arc definitions (optional)

### Organization Principles

**Flat Structure (Recommended for simplicity):**
- All files in root `stubs/` folder
- Easy to reference: `stubs/theme_per_episode.csv`
- Simple path management
- Quick to load

**Alternative: Nested Structure** (if you have many files):
```
stubs/
├── themes/
│   ├── per_episode.csv
│   ├── per_season.csv
│   └── full_series.csv
├── networks/
│   ├── visualizations/
│   │   ├── full.html
│   │   └── season_*.html
│   └── edges/
│       └── *.csv
└── metadata/
    └── *.json
```

---

## Gradio App Changes

### Current Approach (Bad UX)
**User sees:**
- Text input: "Enter subtitles path: ___________"
- Text input: "Enter save path: ___________"
- Button: "Process and Analyze" (takes 30+ minutes)

**Problems:**
- Users don't know what paths to enter
- Paths are different on each system
- Processing takes forever
- High chance of errors

### New Approach (Good UX)
**User sees:**
- Dropdown: "Select: [Full Series ▼ | Season 1 | Season 2 | ...]"
- Button: "View Analysis" (instant results)

**Benefits:**
- No paths needed
- Clear options
- Instant results
- No errors possible

---

## Gradio Modifications Needed

### 1. Remove Path Inputs

**What to remove:**
- All `gr.Textbox()` components asking for file paths
- Processing status indicators
- Loading spinners for long processes

**Why:**
- No more file path confusion
- No more waiting indicators needed
- Simpler, cleaner interface

### 2. Add Dropdown Selectors

**What to add:**
- Dropdown menu with pre-defined options
- Load options from `selection_options.json`
- Options like: "Full Series", "Season 1", "Season 2", etc.

**Why:**
- Users can't make mistakes
- Clear, limited choices
- Professional appearance

### 3. Load from Stubs Instead of Processing

**Theme Classification:**
- **Before:** Load subtitles → Run BART model → Display results
- **After:** User selects option → Load matching CSV → Display results

**Character Network:**
- **Before:** Load subtitles → Run spaCy → Build graph → Render HTML
- **After:** User selects option → Load matching HTML file → Display

**Text Classification (Jutsu):**
- **No change needed** - Already fast (user provides text input)

**Character Chatbot:**
- **No change needed** - Real-time API calls

### 4. Mapping Logic

**How it works:**
- User selects "Season 1" from dropdown
- App checks `selection_options.json` to map to data
- App loads `theme_per_season.csv`, filters for season 1
- App loads `network_viz_season_1.html`
- Display results instantly

**Selection types:**
- "Full Series" → Load `*_all.*` files
- "Season X" → Load `*_season_X.*` files or filter CSV
- "Arc Name" → Load `*_arc.*` file or filter by episode range

### 5. Response Time Improvement

**Before:** 30-60 minutes per user
**After:** < 1 second per user

**How:**
- No model loading
- No inference running
- Just file loading (CSV/HTML)
- Pure data retrieval

---

## Benefits Summary

### For Users
✅ No technical knowledge required
✅ No file paths to figure out
✅ Instant results (< 1 second)
✅ Clear, simple dropdown choices
✅ Professional user experience
✅ Works the same for everyone

### For You (Developer)
✅ One-time processing (4 hours)
✅ Free Google Colab GPU
✅ Easy to update (re-run notebooks)
✅ Small file size (~40 MB)
✅ Free to host (static files)
✅ Scales infinitely (no per-user processing)

### For Deployment
✅ No GPU needed for serving
✅ Low resource usage
✅ Fast response times
✅ Can use free hosting (Hugging Face Spaces)
✅ Works on any device
✅ No database needed

---

## Maintenance

### When to Re-Run Notebooks

**Scenario 1: New Episodes Released**
- Upload new subtitle files to Google Drive
- Re-run all 3 notebooks
- Download updated files
- Replace files in `stubs/`
- Commit to GitHub

**Scenario 2: Change Themes**
- Modify theme list in notebook 1
- Re-run notebook 1 only
- Download updated theme files
- Replace in `stubs/`

**Scenario 3: Improve Models**
- Update model in appropriate notebook
- Re-run that notebook
- Download new results
- Test locally before committing

### Version Control

**What to commit:**
- All CSV files in `stubs/`
- All JSON files in `stubs/`
- HTML files (if not too large)
- Updated `gradio_app.py`

**What NOT to commit:**
- Original subtitle files (too large)
- Temporary processing files
- Model cache files

---

## Performance Comparison

### Old Way (On-Demand Processing)
- User waits: 30-60 minutes
- CPU usage: 100%
- GPU needed: Yes
- Memory usage: 4-8 GB
- Per-user cost: $0.10-0.50
- Error rate: High (path issues)

### New Way (Pre-Computed)
- User waits: < 1 second
- CPU usage: < 5%
- GPU needed: No
- Memory usage: < 500 MB
- Per-user cost: $0
- Error rate: Near zero

### Cost Analysis
- One-time processing: 4 hours (free on Colab)
- Monthly hosting: $0 (static files)
- Per-user serving: $0 (just file loading)
- Total savings: $100-500/month for 1000 users

---

## Success Checklist

After implementing this strategy, you should have:

- ✅ All data files in `stubs/` folder (~40 MB total)
- ✅ Gradio app with dropdown selections (no path inputs)
- ✅ Instant results for all selections (< 1 second)
- ✅ Professional, user-friendly interface
- ✅ No processing or waiting indicators
- ✅ Works consistently for all users
- ✅ Easy to deploy and host
- ✅ Simple update process (re-run notebooks)

---

## Summary

**The Big Idea:**
Process heavy → Process once → Store results → Serve instantly

**The Trade-Off:**
Your 4 hours (one time) = Every user's 30-60 minutes (forever)

**The Result:**
Professional app with instant results and zero user confusion.

