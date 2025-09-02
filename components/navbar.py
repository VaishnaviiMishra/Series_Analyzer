import gradio as gr
import base64

def create_navbar():
    # For now, let's create a navbar without images to avoid the loading issues
    with gr.Row(elem_classes="navbar"):
        with gr.Column(scale=8):
            gr.HTML("""
            <div style="
                display: flex; 
                align-items: center; 
                justify-content: space-between;
                gap: 30px; 
                padding: 15px 25px; 
                background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7));
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
                backdrop-filter: blur(10px);
            ">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        background: linear-gradient(45deg, #FF8C00, #FFD700);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        border: 2px solid #FF8C00;
                        font-size: 20px;
                    ">🍥</div>
                    <h1 style="
                        margin: 0; 
                        color: white; 
                        font-size: 28px;
                        font-weight: 700;
                        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                        background: linear-gradient(45deg, #FFD700, #FF8C00, #FFFFFF);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                    ">Naruto Universe Analyzer</h1>
                </div>
                
                <div style="display: flex; gap: 20px;">
                    <a href="#theme-section" style="
                        color: #FFD700; 
                        text-decoration: none; 
                        font-weight: 600;
                        padding: 8px 16px;
                        border-radius: 6px;
                        transition: all 0.3s ease;
                        background: rgba(0, 0, 0, 0.3);
                    " onmouseover="this.style.background='rgba(255, 140, 0, 0.3)'; this.style.transform='translateY(-2px)'" 
                    onmouseout="this.style.background='rgba(0, 0, 0, 0.3)'; this.style.transform='none'">🎭 Themes</a>
                    
                    <a href="#network-section" style="
                        color: #FFD700; 
                        text-decoration: none; 
                        font-weight: 600;
                        padding: 8px 16px;
                        border-radius: 6px;
                        transition: all 0.3s ease;
                        background: rgba(0, 0, 0, 0.3);
                    " onmouseover="this.style.background='rgba(26, 42, 108, 0.3)'; this.style.transform='translateY(-2px)'" 
                    onmouseout="this.style.background='rgba(0, 0, 0, 0.3)'; this.style.transform='none'">👥 Network</a>
                    
                    <a href="#jutsu-section" style="
                        color: #FFD700; 
                        text-decoration: none; 
                        font-weight: 600;
                        padding: 8px 16px;
                        border-radius: 6px;
                        transition: all 0.3s ease;
                        background: rgba(0, 0, 0, 0.3);
                    " onmouseover="this.style.background='rgba(106, 13, 173, 0.3)'; this.style.transform='translateY(-2px)'" 
                    onmouseout="this.style.background='rgba(0, 0, 0, 0.3)'; this.style.transform='none'">🌀 Jutsu</a>
                    
                    <a href="#chat-section" style="
                        color: #FFD700; 
                        text-decoration: none; 
                        font-weight: 600;
                        padding: 8px 16px;
                        border-radius: 6px;
                        transition: all 0.3s ease;
                        background: rgba(0, 0, 0, 0.3);
                    " onmouseover="this.style.background='rgba(231, 84, 128, 0.3)'; this.style.transform='translateY(-2px)'" 
                    onmouseout="this.style.background='rgba(0, 0, 0, 0.3)'; this.style.transform='none'">🗣️ Chat</a>
                    
                    <a href="#about-section" style="
                        color: #FFD700; 
                        text-decoration: none; 
                        font-weight: 600;
                        padding: 8px 16px;
                        border-radius: 6px;
                        transition: all 0.3s ease;
                        background: rgba(0, 0, 0, 0.3);
                    " onmouseover="this.style.background='rgba(255, 140, 0, 0.3)'; this.style.transform='translateY(-2px)'" 
                    onmouseout="this.style.background='rgba(0, 0, 0, 0.3)'; this.style.transform='none'">📖 About</a>
                </div>
            </div>
            """)
    return gr.Row(visible=True)