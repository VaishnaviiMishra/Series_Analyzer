import gradio as gr
import os
import sys
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Suppress known deprecation warnings from transformers library
warnings.filterwarnings("ignore", category=FutureWarning, module="transformers")

# Auto-download spaCy model if not present (needed for Character Network)
# COMMENTED OUT: Only needed if processing new subtitle files from scratch
# Since we're using pre-computed stub files (ner_output.csv), this is not required
# Uncomment below if you want to process new subtitles:

# try:
#     import spacy
#     try:
#         nlp = spacy.load("en_core_web_trf")
#         print("✅ spaCy model 'en_core_web_trf' loaded successfully!")
#     except OSError:
#         print("📥 Downloading spaCy model 'en_core_web_trf'... (this may take a few minutes on first run)")
#         os.system("python -m spacy download en_core_web_trf")
#         print("✅ spaCy model downloaded successfully!")
# except Exception as e:
#     print(f"⚠️ Warning: Could not load spaCy model: {e}")
#     print("Character Network feature may not work properly.")

print("ℹ️ Using pre-computed data from stubs/ folder (spaCy model not required)")

# Now import modules that depend on spaCy
from theme_classifier import ThemeClassifier
from character_network import NamedEntityRecognizer, CharacterNetworkGenerator
from text_classification import JutsuClassifier
from character_chatbot import GeminiChatBot
from components import create_navbar, create_hero_section, create_footer, create_about_section

load_dotenv()

# Get project root directory (works on any OS - Windows, Linux, Mac)
PROJECT_ROOT = Path(__file__).parent.absolute()
STUBS_DIR = PROJECT_ROOT / "stubs"
THEME_OUTPUT_PATH = STUBS_DIR / "theme_classifier_output.csv"
NER_OUTPUT_PATH = STUBS_DIR / "ner_output.csv"

# Initialize the Gemini chatbot
try:
    character_chatbot = GeminiChatBot()
    chatbot_available = character_chatbot.available
    if chatbot_available:
        print("✅ Gemini chatbot initialized successfully!")
    else:
        print("❌ Gemini chatbot failed to initialize")
except Exception as e:
    print(f"❌ Error initializing chatbot: {e}")
    chatbot_available = False
    character_chatbot = None

def get_themes(theme_list_str, subtitles_path, save_path):
    # Handle save path - if it's just a filename, use stubs directory
    if save_path and not ('/' in save_path or '\\' in save_path):
        save_path = str(STUBS_DIR / save_path)
    
    theme_list = theme_list_str.split(',')
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_themes(subtitles_path, save_path)
    theme_list = [theme for theme in theme_list if theme != 'dialogue']
    output_df = output_df[theme_list]
    output_df = output_df[theme_list].sum().reset_index()
    output_df.columns = ['Theme','Score']
    output_chart = gr.BarPlot(
        output_df,
        x="Theme",
        y="Score",
        title="Series Themes",
        tooltip=["Theme","Score"],
        vertical=False,
        width=500,
        height=260
    )
    return output_chart

def get_character_network(subtitles_path, ner_path):
    # Handle NER path - if it's just a filename, use stubs directory
    if ner_path and not ('/' in ner_path or '\\' in ner_path):
        ner_path = str(STUBS_DIR / ner_path)
    
    ner = NamedEntityRecognizer()
    ner_df = ner.get_ners(subtitles_path, ner_path)
    character_network_generator = CharacterNetworkGenerator()
    relationship_df = character_network_generator.generate_character_network(ner_df)
    html = character_network_generator.draw_network_graph(relationship_df)
    return html

def classify_text(text_classifcation_model, text_classifcation_data_path, text_to_classify):
    jutsu_classifier = JutsuClassifier(
        model_path=text_classifcation_model,
        data_path=text_classifcation_data_path,
        huggingface_token=os.getenv('huggingface_token')
    )
    output = jutsu_classifier.classify_jutsu(text_to_classify)
    return output[0]

def main():
    # Custom CSS with background image and dark theme
    custom_css = """
        .gradio-container {
            background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7));
            background-size: cover !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
            background-position: center !important;
        }
        .navbar { 
            margin-bottom: 20px; 
            background: rgba(30, 30, 30, 0.9) !important;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #444;
        }
        .hero-section { 
            margin: 20px 0; 
            background: rgba(30, 30, 30, 0.9) !important;
            border-radius: 15px;
            padding: 25px;
            border: 1px solid #444;
        }
        .footer { 
            margin-top: 30px; 
            background: rgba(30, 30, 30, 0.9) !important;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #444;
        }
        .section { 
            background: rgba(30, 30, 30, 0.9) !important; 
            padding: 25px; 
            border-radius: 15px; 
            margin: 20px 0; 
            border: 1px solid #444;
        }
        /* Hero image styling - Square and modern */
        .hero-main-image img {
            border-radius: 10px !important;
            border: 3px solid #FF8C00 !important;
            box-shadow: 0 8px 25px rgba(255, 140, 0, 0.3) !important;
            object-fit: cover !important;
            width: 100% !important;
            height: 350px !important;
        }
        /* Improved text styling */
        h1, h2, h3, h4, h5, h6 {
            color: #f0f0f0 !important;
            font-family: 'Arial', sans-serif !important;
        }
        p, label {
            color: #e0e0e0 !important;
            font-family: 'Arial', sans-serif !important;
        }
        .input-text, .textarea, .input-number {
            background: rgba(50, 50, 50, 0.8) !important;
            color: #ffffff !important;
            border: 1px solid #555 !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
        .button-primary {
            background: linear-gradient(45deg, #1a2a6c, #b21f1f, #fdbb2d) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
        }
        .button-secondary {
            background: rgba(60, 60, 60, 0.9) !important;
            color: #f0f0f0 !important;
            border: 1px solid #555 !important;
            border-radius: 8px !important;
        }
        .tab-button {
            background: rgba(50, 50, 50, 0.8) !important;
            color: #f0f0f0 !important;
            border: 1px solid #555 !important;
            border-radius: 8px 8px 0 0 !important;
        }
        .tab-button.selected {
            background: rgba(80, 80, 80, 0.9) !important;
            border-bottom: 3px solid #FF8C00 !important;
        }
        
        /* CHATBOT SPECIFIC STYLING FIXES */
        /* Main chatbot container - increased height */
        .gr-chatbot {
            min-height: 500px !important;
            height: 500px !important;
            max-height: 500px !important;
            background: rgba(40, 40, 40, 0.9) !important;
            border: 1px solid #555 !important;
            border-radius: 10px !important;
            padding: 10px !important;
        }
        
        /* Message container - increased height and better spacing */
        .gr-chat-message {
            overflow-y: auto !important;
            padding: 10px !important;
            margin-bottom: 1px !important;
        }
        
        /* Individual messages - better spacing and wrapping */
        .message {
            margin: 8px 0 !important;
            padding: 12px !important;
            border-radius: 12px !important;
            max-width: 85% !important;
            word-wrap: break-word !important;
            white-space: pre-wrap !important;
        }
        
        .message.user {
            background: rgba(60, 90, 120, 0.9) !important;
            margin-left: auto !important;
            margin-right: 0 !important;
        }
        
        .message.bot {
            background: rgba(90, 60, 90, 0.9) !important;
            margin-left: 0 !important;
            margin-right: auto !important;
        }
        
        /* Input area - better spacing */
        .gr-chat-input {
            min-height: 80px !important;
            margin-top: 10px !important;
        }
        
        /* Examples row - better spacing */
        .gr-examples {
            margin-top: 15px !important;
            margin-bottom: 5px !important;
        }
        
        /* General form styling */
        .gr-box {
            background: rgba(50, 50, 50, 0.8) !important;
            color: #ffffff !important;
            border: 1px solid #555 !important;
        }
        .gr-form {
            background: rgba(30, 30, 30, 0.7) !important;
        }
        .panel {
            background: rgba(30, 30, 30, 0.9) !important;
            border: 1px solid #444 !important;
        }
        
        /* Reduce spacing around the chatbot section */
        #chat-section {
            padding: 15px !important;
            margin: 10px 0 !important;
        }
        
        /* Tab styling for character selection */
        .tab {
            padding: 5px !important;
        }
    """
    with gr.Blocks(title="Naruto TV Analyzer", css=custom_css) as iface:
        
        # Navigation Bar
        create_navbar()
        
        # Hero Section
        create_hero_section()

        # About Section
        create_about_section()
        
        # Theme Classification Section
        with gr.Row(elem_id="theme-section", elem_classes="section"):
            with gr.Column():
                gr.HTML("<h2 style='color: #FF8C00 !important;'>🎭 Theme Classification</h2>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot()
                    with gr.Column():
                        theme_list = gr.Textbox(
                            label="Themes (comma-separated)", 
                            value="friendship,hope,sacrifice,battle,self development,betrayal,love,dialogue"
                        )
                        # Commented out for deployment - using pre-computed data
                        # Uncomment below if you want users to provide their own subtitle files
                        # subtitles_path = gr.Textbox(
                        #     label="Subtitles or Script Path", 
                        #     value="  "
                        # )
                        save_path = gr.Textbox(
                            label="Save Path", 
                            value="theme_classifier_output.csv",
                            placeholder="Filename (saved in stubs/)"
                        )
                        get_themes_button = gr.Button("Analyze Themes", variant="primary")
                        # Using empty string for subtitles_path since we're using pre-computed data
                        get_themes_button.click(get_themes, inputs=[theme_list, gr.Textbox(value="", visible=False), save_path], outputs=[plot])

        # Character Network Section
        with gr.Row(elem_id="network-section", elem_classes="section"):
            with gr.Column():
                gr.HTML("<h2 style='color: #FF8C00 !important;'>👥 Character Network</h2>")
                with gr.Row():
                    with gr.Column():
                        network_html = gr.HTML()
                    with gr.Column():
                        # Commented out for deployment - using pre-computed data
                        # Uncomment below if you want users to provide their own subtitle files
                        # subtitles_path_ner = gr.Textbox(
                        #     label="Subtitles or Script Path", 
                        #     value=" "
                        # )
                        ner_path = gr.Textbox(
                            label="NERs Save Path", 
                            value="ner_output.csv",
                            placeholder="Filename (saved in stubs/)"
                        )
                        get_network_graph_button = gr.Button("Generate Network", variant="primary")
                        # Using empty string for subtitles_path_ner since we're using pre-computed data
                        get_network_graph_button.click(get_character_network, inputs=[gr.Textbox(value="", visible=False), ner_path], outputs=[network_html])

        # Text Classification with LLMs
        with gr.Row(elem_id="jutsu-section", elem_classes="section"):
            with gr.Column():
                gr.HTML("<h2 style='color: #FF8C00 !important;'>🌀 Jutsu Classification</h2>")
                with gr.Row():
                    with gr.Column():
                        text_classification_output = gr.Textbox(label="Classification Result", lines=3)
                    with gr.Column():
                        text_classifcation_model = gr.Textbox(
                            label='Model Path', 
                            value="vaishnaviiii34/jutsu_classifier"
                        )
                        # Commented out for deployment - model handles data internally
                        # Uncomment below if you want users to provide custom data path
                        # text_classifcation_data_path = gr.Textbox(
                        #     label='Data Path', 
                        #     value="  "
                        # )
                        text_to_classify = gr.Textbox(
                            label='Jutsu Description', 
                            value="The Rasengan is a powerful, spherical ball of rapidly spinning chakra created and held in the user's palm, developed by Minato Namikaze and described as the pinnacle of shape transformation in Naruto. It's a high-level, A-rank technique that focuses on compressing and rotating chakra to achieve incredible density and rotational power",
                            lines=3
                        )
                        classify_text_button = gr.Button("Classify Jutsu", variant="primary")
                        # Using empty string for data path since model is pre-trained
                        classify_text_button.click(classify_text, inputs=[text_classifcation_model, gr.Textbox(value="", visible=False), text_to_classify], outputs=[text_classification_output])

       # Character Chatbot Section
        with gr.Row(elem_id="chat-section", elem_classes="section"):
            with gr.Column():
                gr.HTML("<h2 style='color: #FF8C00 !important;'>🗣️ Chat with Naruto Characters</h2>")
                if not chatbot_available:
                    gr.Warning("⚠️ Please add GEMINI_API_KEY=your_key_here to your .env file")
                else:
                    gr.Info("✅ Chat with Naruto, Sasuke, or Sakura!")
                
                # Separate chat interfaces for each character
                with gr.Tab("🍥 Naruto"):
                    def chat_naruto(message, history):
                        return character_chatbot.chat(message, history, "naruto")
                    
                    gr.ChatInterface(
                        chat_naruto,
                        examples=[
                            "What's your dream?",
                            "Tell me about your abilities",
                            "Who is your sensei?",
                            "What's your strongest technique?"
                        ],
                        title="Chat with Naruto"
                    )
                
                with gr.Tab("👁️ Sasuke"):
                    def chat_sasuke(message, history):
                        return character_chatbot.chat(message, history, "sasuke")
                    
                    gr.ChatInterface(
                        chat_sasuke,
                        examples=[
                            "What is your goal?",
                            "Tell me about the Uchiha clan",
                            "Why do you seek power?",
                            "What is the Sharingan?"
                        ],
                        title="Chat with Sasuke"
                    )
                
                with gr.Tab("💕 Sakura"):
                    def chat_sakura(message, history):
                        return character_chatbot.chat(message, history, "sakura")
                    
                    gr.ChatInterface(
                        chat_sakura,
                        examples=[
                            "What medical jutsu do you know?",
                            "How did you train with Tsunade?",
                            "What is chakra control?",
                            "Tell me about your strength"
                        ],
                        title="Chat with Sakura"
                    )


        create_footer() 

        iface.launch(share=True, server_name="0.0.0.0")

if __name__ == '__main__':
    main()