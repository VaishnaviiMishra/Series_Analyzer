# Converting Character Network to Knowledge Graph

## Table of Contents
1. [Overview](#overview)
2. [Key Differences](#key-differences)
3. [Architecture Changes](#architecture-changes)
4. [Implementation Steps](#implementation-steps)
5. [Complete Code](#complete-code)
6. [Integration Guide](#integration-guide)
7. [Dependencies](#dependencies)

---

## Overview

This document outlines the conversion from a **Character Network** approach to a **Knowledge Graph** approach for analyzing TV show subtitles.

### Current Approach: Character Network
- Extracts only PERSON entities (character names)
- Creates relationships based on co-occurrence within a sliding window
- Simple undirected graph showing character interactions
- Limited to character-to-character relationships

### New Approach: Knowledge Graph
- Extracts multiple entity types (PERSON, LOCATION, ORGANIZATION, EVENT, etc.)
- Creates semantic relationships with labeled edges (e.g., "located_in", "belongs_to", "performs")
- Directed graph with typed relationships
- Rich semantic structure capturing complex relationships between entities

---

## Key Differences

| Feature | Character Network | Knowledge Graph |
|---------|------------------|----------------|
| **Entities** | Only characters (PERSON) | Characters, Locations, Organizations, Events, Concepts |
| **Relationships** | Co-occurrence based | Semantic relationships (typed edges) |
| **Graph Type** | Undirected | Directed with labeled edges |
| **Information** | Who appears with whom | Who does what, where, when, and why |
| **Use Cases** | Character interaction analysis | Question answering, reasoning, semantic search |
| **Visualization** | Simple network | Multi-colored, typed entity graph |

---

## Architecture Changes

### File Structure Changes

**Before:**
```
character_network/
├── __init__.py
├── named_entity_recognizer.py
├── character_network_generator.py
└── naruto.html
```

**After:**
```
knowledge_graph/
├── __init__.py
├── entity_recognizer.py          (Enhanced NER)
├── relation_extractor.py         (NEW - Extracts relationships)
├── knowledge_graph_generator.py  (Replaces character_network_generator.py)
└── naruto_kg.html
```

### Component Changes

1. **Entity Recognizer** (Enhanced from Named Entity Recognizer)
   - Extracts multiple entity types: PERSON, GPE, LOC, ORG, EVENT, WORK_OF_ART, etc.
   - Maintains entity attributes and metadata
   - Uses advanced NLP models for better accuracy

2. **Relation Extractor** (NEW Component)
   - Extracts semantic relationships between entities
   - Uses dependency parsing and pattern matching
   - Identifies relationship types (e.g., "located_in", "member_of", "uses")

3. **Knowledge Graph Generator** (Enhanced from Character Network Generator)
   - Creates knowledge graph triples (subject, predicate, object)
   - Supports directed edges with relationship types
   - Exports to multiple formats (NetworkX, RDF, JSON)
   - Enhanced visualization with entity type colors and relationship labels

---

## Implementation Steps

### Step 1: Install Additional Dependencies
```bash
pip install rdflib spacy-transformers
python -m spacy download en_core_web_trf
```

### Step 2: Rename Folder
Rename `character_network/` to `knowledge_graph/`

### Step 3: Update Files
- Replace `named_entity_recognizer.py` with `entity_recognizer.py`
- Create new `relation_extractor.py`
- Replace `character_network_generator.py` with `knowledge_graph_generator.py`
- Update `__init__.py`

### Step 4: Update Gradio App
Modify `gradio_app.py` to use the new knowledge graph components

### Step 5: Test the Implementation
Run the application and verify the knowledge graph generation

---

## Complete Code

### 1. entity_recognizer.py
```python
"""
Enhanced Entity Recognizer for Knowledge Graph Construction
Extracts multiple entity types from subtitles
"""

import spacy
from nltk.tokenize import sent_tokenize
import pandas as pd
from ast import literal_eval
import os 
import sys
import pathlib
folder_path = pathlib.Path().parent.resolve()
sys.path.append(os.path.join(folder_path, '../'))
from utils import load_subtitles_dataset

class EntityRecognizer:
    """
    Recognizes and extracts multiple entity types from text.
    Supports: PERSON, GPE (Geopolitical Entity), LOC (Location), 
    ORG (Organization), EVENT, WORK_OF_ART, etc.
    """
    
    def __init__(self):
        self.nlp_model = self.load_model()
        # Entity types to extract for knowledge graph
        self.entity_types = {
            'PERSON': 'character',
            'GPE': 'location',
            'LOC': 'location',
            'ORG': 'organization',
            'EVENT': 'event',
            'WORK_OF_ART': 'artifact',
            'FAC': 'facility',
            'NORP': 'group'
        }
    
    def load_model(self):
        """Load spaCy transformer model for better accuracy"""
        nlp = spacy.load("en_core_web_trf")
        return nlp
    
    def get_entities_inference(self, script):
        """
        Extract entities from script with type information.
        
        Args:
            script (str): Input text/script
            
        Returns:
            list: List of dictionaries containing entity information
        """
        script_sentences = sent_tokenize(script)
        entity_output = []
        
        for sentence in script_sentences:
            doc = self.nlp_model(sentence)
            sentence_entities = []
            
            for entity in doc.ents:
                if entity.label_ in self.entity_types:
                    entity_info = {
                        'text': entity.text.strip(),
                        'type': self.entity_types[entity.label_],
                        'label': entity.label_,
                        'sentence': sentence
                    }
                    
                    # Normalize person names to first name
                    if entity.label_ == "PERSON":
                        first_name = entity.text.split(" ")[0].strip()
                        entity_info['text'] = first_name
                    
                    sentence_entities.append(entity_info)
            
            entity_output.append(sentence_entities)
        
        return entity_output
    
    def get_entities(self, dataset_path, save_path=None):
        """
        Extract entities from entire dataset.
        
        Args:
            dataset_path (str): Path to subtitles dataset
            save_path (str, optional): Path to save results
            
        Returns:
            DataFrame: DataFrame with entities extracted
        """
        if save_path is not None and os.path.exists(save_path):
            df = pd.read_csv(save_path)
            df['entities'] = df['entities'].apply(
                lambda x: literal_eval(x) if isinstance(x, str) else x
            )
            return df
        
        # Load dataset 
        df = load_subtitles_dataset(dataset_path)
        
        # Run Inference
        df['entities'] = df['script'].apply(self.get_entities_inference)
        
        if save_path is not None:
            df.to_csv(save_path, index=False)
        
        return df
```

### 2. relation_extractor.py
```python
"""
Relation Extractor for Knowledge Graph
Extracts semantic relationships between entities
"""

import spacy
from itertools import combinations

class RelationExtractor:
    """
    Extracts semantic relationships between entities using
    dependency parsing and pattern matching.
    """
    
    def __init__(self):
        self.nlp_model = spacy.load("en_core_web_trf")
        
        # Define relationship patterns
        self.relation_patterns = {
            'located_in': ['in', 'at', 'from', 'to'],
            'member_of': ['of', 'from', 'belongs'],
            'uses': ['uses', 'wields', 'performs', 'casts'],
            'fights': ['fights', 'battles', 'defeats'],
            'teaches': ['teaches', 'trains'],
        }
        
        # Action verbs for relationship extraction
        self.action_verbs = {
            'fight', 'battle', 'defeat', 'attack',
            'teach', 'train', 'learn',
            'use', 'wield', 'cast', 'perform',
            'create', 'develop',
            'lead', 'command',
        }
    
    def extract_relations_from_sentence(self, sentence, entities):
        """Extract relationships from a single sentence."""
        if len(entities) < 2:
            return []
        
        doc = self.nlp_model(sentence)
        relations = []
        
        # Extract from dependencies
        entity_texts = [e['text'] for e in entities]
        
        for token in doc:
            if token.pos_ == "VERB" and token.lemma_ in self.action_verbs:
                subjects = [c for c in token.children if c.dep_ in ['nsubj', 'nsubjpass']]
                objects = [c for c in token.children if c.dep_ in ['dobj', 'pobj', 'attr']]
                
                for subj in subjects:
                    for obj in objects:
                        if subj.text in entity_texts and obj.text in entity_texts:
                            subj_entity = next(e for e in entities if e['text'] == subj.text)
                            obj_entity = next(e for e in entities if e['text'] == obj.text)
                            
                            relations.append({
                                'subject': subj_entity,
                                'predicate': token.lemma_,
                                'object': obj_entity,
                                'confidence': 0.9
                            })
        
        # Co-occurrence relationships
        for e1, e2 in combinations(entities, 2):
            relation_type = self._infer_relation_type(e1, e2)
            if relation_type:
                relations.append({
                    'subject': e1,
                    'predicate': relation_type,
                    'object': e2,
                    'confidence': 0.5
                })
        
        return relations
    
    def _infer_relation_type(self, entity1, entity2):
        """Infer relationship type based on entity types."""
        type1 = entity1['type']
        type2 = entity2['type']
        
        type_rules = {
            ('character', 'character'): 'interacts_with',
            ('character', 'location'): 'located_in',
            ('character', 'organization'): 'member_of',
            ('character', 'artifact'): 'uses',
        }
        
        return type_rules.get((type1, type2), 'related_to')
    
    def extract_relations(self, df):
        """Extract all relations from entity dataframe."""
        all_relations = []
        
        for entities_list in df['entities']:
            for sentence_entities in entities_list:
                if len(sentence_entities) > 0:
                    sentence = sentence_entities[0]['sentence']
                    relations = self.extract_relations_from_sentence(
                        sentence, sentence_entities
                    )
                    all_relations.extend(relations)
        
        return all_relations
```

### 3. knowledge_graph_generator.py
```python
"""
Knowledge Graph Generator
Creates and visualizes knowledge graphs from extracted entities and relations
"""

import pandas as pd
import networkx as nx
from pyvis.network import Network

class KnowledgeGraphGenerator:
    """
    Generates and visualizes knowledge graphs with typed entities
    and labeled relationships.
    """
    
    def __init__(self):
        self.entity_colors = {
            'character': '#FF6B6B',
            'location': '#4ECDC4',
            'organization': '#95E1D3',
            'event': '#FFE66D',
            'artifact': '#C06C84',
            'facility': '#6C5CE7',
            'group': '#FD79A8'
        }
    
    def generate_knowledge_graph(self, entities_df, relations):
        """Generate knowledge graph from entities and relations."""
        # Extract unique entities
        nodes = {}
        for entities_list in entities_df['entities']:
            for sentence_entities in entities_list:
                for entity in sentence_entities:
                    entity_id = f"{entity['text']}_{entity['type']}"
                    if entity_id not in nodes:
                        nodes[entity_id] = {
                            'id': entity_id,
                            'label': entity['text'],
                            'type': entity['type'],
                            'count': 0
                        }
                    nodes[entity_id]['count'] += 1
        
        nodes_df = pd.DataFrame(list(nodes.values()))
        
        # Process relations into edges
        edges = []
        for relation in relations:
            subj_id = f"{relation['subject']['text']}_{relation['subject']['type']}"
            obj_id = f"{relation['object']['text']}_{relation['object']['type']}"
            
            if subj_id in nodes and obj_id in nodes:
                edges.append({
                    'source': subj_id,
                    'target': obj_id,
                    'relation': relation['predicate'],
                    'confidence': relation.get('confidence', 0.5)
                })
        
        if edges:
            edges_df = pd.DataFrame(edges)
            edges_df = edges_df.groupby(['source', 'target', 'relation']).agg({
                'confidence': 'mean'
            }).reset_index()
        else:
            edges_df = pd.DataFrame(columns=['source', 'target', 'relation', 'confidence'])
        
        return nodes_df, edges_df
    
    def draw_knowledge_graph(self, nodes_df, edges_df, title="Knowledge Graph"):
        """Create interactive visualization of knowledge graph."""
        # Filter top nodes and edges
        nodes_df = nodes_df.nlargest(100, 'count')
        node_ids = set(nodes_df['id'])
        edges_df = edges_df[
            edges_df['source'].isin(node_ids) & 
            edges_df['target'].isin(node_ids)
        ].nlargest(200, 'confidence')
        
        # Create NetworkX graph
        G = nx.DiGraph()
        
        # Add nodes
        for _, node in nodes_df.iterrows():
            G.add_node(
                node['id'],
                label=node['label'],
                title=f"{node['label']} ({node['type']})",
                color=self.entity_colors.get(node['type'], '#95A5A6'),
                size=min(10 + node['count'] * 2, 50)
            )
        
        # Add edges
        for _, edge in edges_df.iterrows():
            if G.has_node(edge['source']) and G.has_node(edge['target']):
                G.add_edge(
                    edge['source'],
                    edge['target'],
                    title=edge['relation'],
                    label=edge['relation']
                )
        
        # Create PyVis network
        net = Network(
            notebook=True,
            width="1000px",
            height="700px",
            bgcolor="#222222",
            font_color="white",
            directed=True
        )
        
        net.from_nx(G)
        html = net.generate_html()
        
        output_html = f"""
        <div style="background-color: #222; padding: 20px;">
            <h3 style="color: #FF8C00;">{title}</h3>
            <iframe srcdoc='{html}' style="width: 100%; height: 600px; border: none;"></iframe>
        </div>
        """
        
        return output_html
```

### 4. __init__.py
```python
from .entity_recognizer import EntityRecognizer
from .relation_extractor import RelationExtractor
from .knowledge_graph_generator import KnowledgeGraphGenerator
```

---

## Integration Guide

### Update gradio_app.py

```python
# Replace the character_network import
from knowledge_graph import EntityRecognizer, RelationExtractor, KnowledgeGraphGenerator

# Replace the get_character_network function
def get_knowledge_graph(subtitles_path, entity_path):
    # Extract entities
    entity_recognizer = EntityRecognizer()
    entities_df = entity_recognizer.get_entities(subtitles_path, entity_path)
    
    # Extract relations
    relation_extractor = RelationExtractor()
    relations = relation_extractor.extract_relations(entities_df)
    
    # Generate knowledge graph
    kg_generator = KnowledgeGraphGenerator()
    nodes_df, edges_df = kg_generator.generate_knowledge_graph(entities_df, relations)
    
    # Create visualization
    html = kg_generator.draw_knowledge_graph(nodes_df, edges_df, "Naruto Knowledge Graph")
    
    return html
```

---

## Dependencies

```txt
spacy>=3.7.0
spacy-transformers>=1.3.0
nltk>=3.8.0
pandas>=2.0.0
networkx>=3.1
pyvis>=0.3.2
rdflib>=7.0.0
```

Install:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_trf
```

---

## Benefits of Knowledge Graph

1. **Richer Information**: Captures not just who appears with whom, but what they do, where, and how
2. **Semantic Queries**: Enable complex queries like "Which characters use artifacts?"
3. **Reasoning**: Support inference about implicit relationships
4. **Integration**: Can be integrated with external knowledge bases
5. **Scalability**: Better structured for large-scale analysis
6. **Visualization**: More informative with typed entities and labeled edges

