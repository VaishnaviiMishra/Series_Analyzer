import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiChatBot:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.available = bool(self.api_key)
        
        if self.available:
            try:
                genai.configure(api_key=self.api_key)
                model_name = 'models/gemini-1.5-flash-latest'
                self.model = genai.GenerativeModel(model_name)
                self.available = True
                print(f"✅ Using model: {model_name}")
            except Exception as e:
                print(f"❌ Error configuring Gemini: {e}")
                self.available = False
        else:
            print("❌ Gemini API key not found in .env file")
    
    def chat(self, message, history, character="naruto"):
        if not self.available:
            return "❌ Gemini chatbot not available. Please check your API key."
        
        try:
            # Enhanced character-specific prompts with detailed personalities
            character_prompts = {
                "naruto": """You ARE Naruto Uzumaki. Respond EXACTLY as him:
- ORPHAN JINCHURIKI of Nine-Tails, hated by village, dreams of becoming HOKAGE
- SUPER energetic! Use "DATTEBAYO!", "BELIEVE IT!", lots of EXCLAMATIONS!!
- Techniques: Shadow Clone Jutsu, Rasengan, Sage Mode, Six Paths Sage Mode
- Talk about: Ramen, protecting friends, Training with Jiraiya, Kurama inside me
- Family: Son of Minato & Kushina, Husband to Hinata, Father of Boruto & Himawari
- NEVER give up! SUPER positive attitude! Loud and passionate!""",

                "sasuke": """You ARE Sasuke Uchiha. Respond EXACTLY as him:
- SOLE UCHIHA survivor, clan massacred by brother Itachi, seeks power & redemption
- COLD, BROODING, minimal words. No emotions. Formal, measured speech.
- Techniques: Sharingan, Rinnegan, Chidori, Amaterasu, Susanoo
- Talk about: Uchiha clan honor, revenge, becoming stronger, hating weakness
- Family: Son of Fugaku & Mikoto, Husband to Sakura, Father of Sarada
- Short, direct responses. No exclamations. Distant and superior tone.""",

                "sakura": """You ARE Sakura Haruno. Respond EXACTLY as her:
- MEDICAL NINJA prodigy, trained by Tsunade, overcame insecurity about forehead
- INTELLIGENT but emotional. Practical yet caring. Blunt but protective.
- Techniques: Mystical Palm, Creation Rebirth, super strength "SHANNARO!"
- Talk about: Chakra control, healing, protecting patients, Tsunade's teachings
- Family: Married Sasuke Uchiha, became Sakura Uchiha, mother of Sarada
- Balance medical knowledge with emotional depth. Strong-willed determination."""
            }
            
            # Character display names
            char_display_name = {"naruto": "Naruto", "sasuke": "Sasuke", "sakura": "Sakura"}[character]
            
            # Build concise conversation with better formatting
            conversation_parts = [character_prompts[character]]
            
            # Add history efficiently
            for user_msg, bot_msg in history[-6:]:  # Keep only last 6 exchanges for context
                conversation_parts.append(f"Human: {user_msg}")
                conversation_parts.append(f"{char_display_name}: {bot_msg}")
            
            conversation_parts.append(f"Human: {message}")
            conversation_parts.append(f"{char_display_name}:")
            
            conversation = "\n".join(conversation_parts)
            
            # Character-specific generation settings with increased token limits
            generation_config = {
                "naruto": {"temperature": 0.95, "max_output_tokens": 500, "top_p": 0.9},
                "sasuke": {"temperature": 0.6, "max_output_tokens": 300, "top_p": 0.8},
                "sakura": {"temperature": 0.8, "max_output_tokens": 400, "top_p": 0.85}
            }[character]
            
            response = self.model.generate_content(
                conversation,
                generation_config=genai.types.GenerationConfig(**generation_config)
            )
            
            # Clean and enhance response
            response_text = response.text.strip()
            
            # Character-specific response enhancements (less aggressive)
            if character == "naruto":
                if not any(x in response_text.lower() for x in ['dattebayo', 'believe it']):
                    if len(response_text) < 100:
                        response_text += " Believe it, dattebayo!"
                    else:
                        # Add to the end if it's a longer response
                        response_text = response_text.rstrip('.!') + "! Believe it, dattebayo!"
                
            elif character == "sasuke":
                # Don't truncate Sasuke's responses - let him speak
                response_text = response_text.replace('Hmm', 'Hn.')
                
            elif character == "sakura":
                if 'strength' in response_text.lower() and 'shannaro' not in response_text.lower():
                    if len(response_text.split()) < 30:  # Only for shorter responses
                        response_text = response_text.rstrip('.!') + ' SHANNARO!'
            
            return response_text
            
        except Exception as e:
            return f"❌ Error: {str(e)}"