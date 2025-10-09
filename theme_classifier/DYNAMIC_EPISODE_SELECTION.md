# Dynamic Episode Selection for Theme Classification

## Overview

Enhance the Theme Classifier to support dynamic episode selection, allowing users to analyze:
- **Single episodes** (e.g., Episode 5)
- **Episode ranges** (e.g., Episodes 10-20)
- **Seasons** (e.g., All episodes from Season 2)
- **Complete series** (existing functionality)

---

## Current vs Enhanced

| Feature | Current | Enhanced |
|---------|---------|----------|
| **Scope** | Entire series only | Single episode, ranges, seasons, or full series |
| **Granularity** | All episodes combined | Per-episode or custom grouping |
| **Flexibility** | Fixed | Dynamic selection by user |
| **Visualization** | Single bar chart | Bar chart + line chart (theme evolution) |

---

## Implementation

### 1. Enhanced Data Loader

Add to `utils/data_loader.py`:

```python
def load_subtitles_by_episodes(dataset_path, episode_numbers=None, 
                               episode_range=None, season=None):
    """
    Load subtitles with flexible episode selection.
    
    Args:
        dataset_path (str): Path to subtitles folder
        episode_numbers (list): Specific episode numbers [1, 5, 10]
        episode_range (tuple): Episode range (start, end) e.g., (10, 20)
        season (int): Load all episodes from this season
    """
    from glob import glob
    import pandas as pd
    import re
    
    all_files = glob(dataset_path + '/*.ass') + glob(dataset_path + '/*.srt')
    
    # Get all episodes with metadata
    episodes = []
    for path in all_files:
        match = re.search(r'Season (\d+) - (\d+)', path)
        if match:
            ep_season = int(match.group(1))
            ep_num = int(match.group(2))
            episodes.append({'episode': ep_num, 'season': ep_season, 'path': path})
    
    # Filter based on selection
    if episode_numbers:
        episodes = [e for e in episodes if e['episode'] in episode_numbers]
    elif episode_range:
        start, end = episode_range
        episodes = [e for e in episodes if start <= e['episode'] <= end]
    elif season:
        episodes = [e for e in episodes if e['season'] == season]
    
    # Load filtered episodes
    scripts = []
    for ep in sorted(episodes, key=lambda x: x['episode']):
        with open(ep['path'], 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if ep['path'].endswith('.ass'):
                lines = lines[27:]
                lines = [",".join(line.split(',')[9:]) for line in lines]
            lines = [line.replace('\\N', ' ') for line in lines]
            script = " ".join(lines)
        
        scripts.append({
            'episode': ep['episode'],
            'season': ep['season'],
            'script': script
        })
    
    return pd.DataFrame(scripts)
```

### 2. Episode Selector

Create `theme_classifier/episode_selector.py`:

```python
class EpisodeSelector:
    """Handles episode selection with various input formats."""
    
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.available_episodes = self._get_available_episodes()
    
    def _get_available_episodes(self):
        """Get list of available episodes."""
        from glob import glob
        import re
        
        files = glob(self.dataset_path + '/*.ass') + glob(self.dataset_path + '/*.srt')
        episodes = []
        
        for f in files:
            match = re.search(r'Season (\d+) - (\d+)', f)
            if match:
                episodes.append({
                    'season': int(match.group(1)),
                    'episode': int(match.group(2))
                })
        
        return sorted(episodes, key=lambda x: x['episode'])
    
    def parse_selection(self, selection_string):
        """
        Parse user selection string into list of episode numbers.
        
        Examples:
            "5" -> [5]
            "1-5" -> [1, 2, 3, 4, 5]
            "1,5,10" -> [1, 5, 10]
            "Season 2" -> [27, 28, ..., 52]
        """
        import re
        
        selection = selection_string.strip().lower()
        
        # Handle "all"
        if selection in ['all', '*']:
            return [e['episode'] for e in self.available_episodes]
        
        # Handle season
        if 'season' in selection:
            season_num = int(re.search(r'\d+', selection).group())
            return [e['episode'] for e in self.available_episodes 
                   if e['season'] == season_num]
        
        # Handle ranges and lists
        episodes = set()
        parts = selection.split(',')
        
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                episodes.update(range(start, end + 1))
            else:
                episodes.add(int(part.strip()))
        
        return sorted(episodes)
```

### 3. Enhanced Theme Classifier

Add to `theme_classifier/theme_classifier.py`:

```python
def get_themes_by_episodes(self, dataset_path, episode_numbers=None, 
                          episode_range=None, season=None):
    """
    Get themes with episode selection support.
    
    Args:
        dataset_path: Path to subtitles
        episode_numbers: Specific episodes to analyze
        episode_range: (start, end) episode range
        season: Season number to analyze
    """
    from utils.data_loader import load_subtitles_by_episodes
    
    # Load selected episodes
    df = load_subtitles_by_episodes(
        dataset_path,
        episode_numbers=episode_numbers,
        episode_range=episode_range,
        season=season
    )
    
    # Run inference
    df['themes'] = df['script'].apply(self.get_themes_inference)
    
    return df

def get_theme_evolution(self, dataset_path, episode_numbers=None,
                       episode_range=None, season=None):
    """Get theme evolution across episodes (for line charts)."""
    return self.get_themes_by_episodes(
        dataset_path,
        episode_numbers=episode_numbers,
        episode_range=episode_range,
        season=season
    )
```

### 4. Updated Gradio Interface

Replace theme classification section in `gradio_app.py`:

```python
def get_themes_dynamic(theme_list_str, subtitles_path, episode_selection):
    """Enhanced theme classification with episode selection."""
    from theme_classifier.episode_selector import EpisodeSelector
    
    theme_list = [t.strip() for t in theme_list_str.split(',')]
    selector = EpisodeSelector(subtitles_path)
    episodes = selector.parse_selection(episode_selection)
    
    classifier = ThemeClassifier(theme_list)
    df = classifier.get_themes_by_episodes(subtitles_path, episode_numbers=episodes)
    
    # Create visualization
    theme_cols = [t for t in theme_list if t != 'dialogue']
    theme_scores = df[theme_cols].mean().reset_index()
    theme_scores.columns = ['Theme', 'Score']
    
    chart = gr.BarPlot(
        theme_scores,
        x="Theme",
        y="Score",
        title=f"Theme Analysis: {len(episodes)} episodes"
    )
    
    return chart

# In Gradio UI:
with gr.Row():
    theme_list = gr.Textbox(label="Themes", value="friendship,hope,sacrifice,battle")
    episode_selection = gr.Textbox(
        label="Episodes",
        value="all",
        placeholder="Examples: '5', '1-10', 'Season 2', 'all'"
    )
    subtitles_path = gr.Textbox(label="Subtitles Path", value="data/Subtitles")
    
    analyze_btn = gr.Button("Analyze")
    output = gr.Plot()
    
    analyze_btn.click(
        get_themes_dynamic,
        inputs=[theme_list, subtitles_path, episode_selection],
        outputs=[output]
    )
```

---

## Usage Examples

```python
from theme_classifier import ThemeClassifier
from theme_classifier.episode_selector import EpisodeSelector

classifier = ThemeClassifier(['friendship', 'battle', 'sacrifice'])
selector = EpisodeSelector('data/Subtitles')

# Single episode
episodes = selector.parse_selection("5")
df = classifier.get_themes_by_episodes('data/Subtitles', episode_numbers=episodes)

# Episode range
episodes = selector.parse_selection("20-67")  # Chunin Exam Arc
df = classifier.get_theme_evolution('data/Subtitles', episode_numbers=episodes)

# Season
episodes = selector.parse_selection("Season 2")
df = classifier.get_themes_by_episodes('data/Subtitles', episode_numbers=episodes)
```

---

---

## Visualization Types

### 1. Bar Chart (Aggregated)
- Shows average theme scores for selected episodes
- Best for: Comparing themes within a selection
- Use case: "What are the dominant themes in Season 2?"

### 2. Line Chart (Evolution)
- Shows theme scores across episodes over time
- Best for: Tracking theme trends
- Use case: "How does 'sacrifice' theme evolve through Chunin Exam Arc?"

### 3. Heatmap
- Shows all themes across all episodes in a grid
- Best for: Identifying patterns and clusters
- Use case: "Which episodes have similar theme profiles?"

### 4. Comparison Chart
- Compare multiple selections side-by-side
- Best for: Arc vs Arc, Season vs Season
- Use case: "How do themes differ between Season 1 and Season 5?"

---

## Story Arc Presets

Pre-define popular story arcs for quick selection:

**Naruto Arcs:**
- Land of Waves Arc: Episodes 6-19
- Chunin Exam Arc: Episodes 20-67
- Konoha Crush Arc: Episodes 68-80
- Search for Tsunade Arc: Episodes 81-100
- Sasuke Recovery Arc: Episodes 107-135

**Benefits:**
- Users don't need to know episode numbers
- One-click access to popular arcs
- Consistent analysis across users

---

## Caching Strategy

### Problem
Running theme classification on 20+ episodes takes time (5-10 minutes)

### Solution: Per-Episode Caching

**How it works:**
1. First time analyzing Episode 5 → Process and cache result
2. Next time Episode 5 is in any selection → Load from cache (instant)
3. Cache stored in `cache/theme_classifier/ep_5_themehash.json`

**Benefits:**
- Analyze 1-10 episodes once → Reuse forever
- Partial selections load instantly
- Overlapping selections share cached episodes
- Example: Cached 1-10, user selects 5-15 → Only process 11-15

**Implementation:**
```python
class CacheManager:
    def get_cached_episode(episode, themes):
        # Load if exists
        
    def cache_episode(episode, themes, scores):
        # Save for future
        
    def get_missing_episodes(episodes, themes):
        # Return which need processing
```

---

## UI Improvements

### Quick Preset Buttons
Instead of typing, add clickable buttons:
- [All Episodes] [Season 1] [Season 2] ... [Season 9]
- [Chunin Exam Arc] [First 10] [Last 10]

### Selection Info Display
Show user what they selected:
```
✓ Selected: 48 episodes
  Range: Episodes 20-67
  Seasons: 1, 2
  Arc: Chunin Exam
```

### Smart Input Validation
- Highlight invalid episode numbers in red
- Suggest corrections: "Did you mean Season 2?"
- Show available ranges: "Episodes 1-220 available"

### Multiple Output Panels
```
┌─────────────────┐  ┌──────────────────┐
│  Visualization  │  │   Statistics     │
│  (Chart/Graph)  │  │  - Dominant themes│
│                 │  │  - Theme rankings│
└─────────────────┘  │  - Episode count │
                     └──────────────────┘
```

---

## Theme Statistics

### Dominant Theme Detection
Automatically identify top themes:
```
🎯 Dominant Themes for Chunin Exam Arc:
1. Battle: 0.847
2. Self Development: 0.723
3. Friendship: 0.691
```

### Theme Trends
```
📊 Theme Trends:
- "Battle" peaks at Episode 45 (0.932)
- "Friendship" most consistent (σ = 0.12)
- "Betrayal" appears in 15/48 episodes
```

### Episode Highlights
```
📺 Notable Episodes:
- Highest "Sacrifice": Episode 133 (0.891)
- Highest "Battle": Episode 78 (0.945)
- Most balanced: Episode 50
```

---

## Advanced Features

### 1. Theme Comparison Mode
Compare same themes across different selections:
```
Friendship Theme:
- Season 1: 0.67
- Season 2: 0.72
- Season 3: 0.58
```

### 2. Export Results
- Download as CSV
- Export charts as PNG/PDF
- Generate summary report

### 3. Custom Theme Lists
Save and reuse theme combinations:
- "Action Themes": battle, sacrifice, betrayal
- "Emotional Themes": friendship, love, hope
- "Growth Themes": self development, training

### 4. Episode Recommendations
"Based on your selection, you might also like:"
- Similar theme profiles
- Same story arc
- Related episodes

---

## Integration with Stubs

### For Pre-Computed Data Approach

When using stubs strategy:
1. Pre-compute themes for ALL episodes in Colab
2. Save `theme_per_episode.csv` with all 220 episodes
3. In Gradio, just filter the CSV based on selection

**Advantages:**
- Zero processing time
- All selections work instantly
- No caching needed
- Simple implementation

**Gradio function:**
```python
def get_themes_from_precomputed(selection):
    # Load pre-computed CSV
    df = pd.read_csv('stubs/theme_per_episode.csv')
    
    # Filter by selection
    episodes = parse_selection(selection)
    filtered = df[df['episode'].isin(episodes)]
    
    # Aggregate and visualize
    return create_chart(filtered)
```

---

## Benefits

✅ **Episode-specific analysis** - Analyze any episode or range
✅ **Story arc tracking** - Follow themes through story arcs  
✅ **Season comparisons** - Compare themes across seasons
✅ **Theme evolution** - Track how themes change over time
✅ **User-friendly interface** - Dropdowns and presets, no manual input
✅ **Fast performance** - Caching or pre-computed data
✅ **Multiple visualizations** - Bar, line, heatmap, comparison
✅ **Rich statistics** - Dominant themes, trends, highlights
✅ **Professional UX** - Info displays, validation, suggestions

