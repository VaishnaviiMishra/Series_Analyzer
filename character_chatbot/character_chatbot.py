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
                
                # List available models for debugging
                try:
                    available_models = genai.list_models()
                    print("\n📋 Available Gemini models with generateContent support:")
                    for model in available_models:
                        if 'generateContent' in model.supported_generation_methods:
                            print(f"   ✓ {model.name}")
                    print()  # Empty line for readability
                except Exception as list_error:
                    print(f"⚠️ Could not list models: {list_error}")
                
                # Try multiple model names in order of preference
                # Updated with latest stable model names (2024)
                model_names = [
                    'gemini-2.0-flash-exp',      # Newest experimental
                    'gemini-1.5-flash',          # Latest stable Flash model
                    'gemini-1.5-pro',            # Latest stable Pro model
                    'gemini-pro',                # Fallback to older stable
                ]
                
                model_loaded = False
                print("🔍 Trying to load Gemini model...")
                for model_name in model_names:
                    try:
                        print(f"   Attempting: {model_name}...", end=" ")
                        self.model = genai.GenerativeModel(model_name)
                        # Test if model is accessible
                        self.available = True
                        print(f"✅ SUCCESS!")
                        print(f"\n🎉 Chatbot ready with model: {model_name}\n")
                        model_loaded = True
                        break
                    except Exception as model_error:
                        print(f"❌ Failed")
                        # Only print full error for debugging if needed
                        if "404" in str(model_error):
                            print(f"      (Model not found)")
                        else:
                            print(f"      ({str(model_error)[:80]})")
                        continue
                
                if not model_loaded:
                    print("\n" + "="*60)
                    print("❌ ERROR: Could not load any Gemini model!")
                    print("="*60)
                    print("📝 Solutions:")
                    print("   1. Check if your API key is valid")
                    print("   2. Look at the 'Available Gemini models' list above")
                    print("   3. Update model_names in character_chatbot.py to match")
                    print("   4. Run: pip install --upgrade google-generativeai")
                    print("="*60 + "\n")
                    self.available = False
                    
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