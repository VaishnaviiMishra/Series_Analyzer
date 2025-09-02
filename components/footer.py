import gradio as gr

def create_footer():
    with gr.Row(elem_classes="footer"):
        with gr.Column():
            gr.HTML("""
            <div style="text-align: center; padding: 20px; background: #2c3e50; color: white; border-radius: 10px; margin-top: 30px;">
                <div style="margin-bottom: 15px;">
                    <span style="margin: 0 15px;">🍥</span>
                    <span style="margin: 0 15px;">👁️</span>
                    <span style="margin: 0 15px;">💕</span>
                </div>
                <p style="margin: 10px 0;">© 2024 Naruto TV Analyzer | Built by Vaishnavi Mishra</p>
                <p style="margin: 10px 0;">Models Used : facebook/bart-large-mnli | spacy en_core_web_trf | distilbert/distilbert-base-uncased | google/gemma-2b </p>    
                <p style="margin: 5px 0; font-size: 0.9em;">Naruto and all related characters are trademarks of Masashi Kishimoto/Shueisha</p>
                <p style="margin: 5px 0; font-size: 0.9em;">This is a fan-made analytical tool for educational purposes</p>
            </div>
            """)