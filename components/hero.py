import gradio as gr

def create_hero_section():
    with gr.Row(elem_classes="hero-section"):
        with gr.Column():
            # Main container with improved layout
            with gr.Row():
                # Text content column
                with gr.Column(scale=3, min_width=500):
                    gr.HTML("""
                    <div style="text-align: left; padding: 20px;">
                        <h1 style="
                            font-size: 3em; 
                            margin-bottom: 15px; 
                            background: linear-gradient(45deg, #FF8C00, #FFD700, #FF4500);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            font-weight: 800;
                            letter-spacing: 0.5px;
                            line-height: 1.1;
                        ">Naruto Universe Analyzer</h1>
                        
                        <p style="
                            font-size: 1.2em; 
                            color: #FFD700;
                            font-weight: 300;
                            line-height: 1.4;
                            margin-bottom: 25px;
                        ">Unlock the hidden depths of the Naruto series through advanced AI-powered analysis</p>
                        
                        <div style="
                            background: rgba(255, 140, 0, 0.2); 
                            padding: 15px; 
                            border-radius: 8px;
                            border-left: 3px solid #FF8C00;
                            margin-bottom: 15px;
                        ">
                            <p style="
                                margin: 0; 
                                font-style: italic; 
                                color: #FFD700;
                                font-size: 0.95em;
                            ">
                                "Those who break the rules are scum, but those who abandon their friends are worse than scum."
                            </p>
                            <p style="
                                margin: 5px 0 0 0; 
                                color: #FFFFFF;
                                font-size: 0.9em;
                                text-align: right;
                            ">- Kakashi Hatake</p>
                        </div>
                        <div style="
                            background: rgba(34, 139, 34, 0.2); 
                            padding: 15px; 
                            border-radius: 8px;
                            border-left: 3px solid #FF8C00;
                        ">
                            <p style="
                                margin: 0; 
                                font-style: italic; 
                                color: #FFD700;
                                font-size: 0.95em;
                            ">
                                "A place where someone still thinks about you is a place you can call home."
                            </p>
                            <p style="
                                margin: 5px 0 0 0; 
                                color: #FFFFFF;
                                font-size: 0.9em;
                                text-align: right;
                            ">- Jiraiya</p>
                        </div>    
                    </div>
                    """)
                
                # Image column
                with gr.Column(scale=2, min_width=300):
                    # Use Gradio's Image component with square aspect ratio
                    gr.Image("components/assets/naruto.jpg", 
                            show_label=False, 
                            height=350, 
                            width=600,
                            elem_classes="hero-main-image")
            
            # Feature cards in a single row
            with gr.Row():
                gr.HTML("""
                <div style="
                    display: grid; 
                    grid-template-columns: repeat(4, 1fr); 
                    gap: 15px; 
                    width: 100%;
                    margin-top: 10px;
                ">
                    <div style="
                        background: linear-gradient(135deg, rgba(26, 42, 108, 0.9), rgba(26, 42, 108, 0.7)); 
                        padding: 15px; 
                        border-radius: 10px; 
                        border: 1px solid rgba(255, 140, 0, 0.3);
                        transition: all 0.3s ease;
                        text-align: center;
                    " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 5px 15px rgba(255, 140, 0, 0.2)'" 
                    onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
                        <h3 style="color: #FFD700; margin: 0 0 10px 0; font-size: 1.1em;">🎭 Theme Analysis</h3>
                        <p style="margin: 0; color: #FFFFFF; font-size: 0.9em;">Discover underlying themes</p>
                    </div>
                    <div style="
                        background: linear-gradient(135deg, rgba(178, 31, 31, 0.9), rgba(178, 31, 31, 0.7)); 
                        padding: 15px; 
                        border-radius: 10px; 
                        border: 1px solid rgba(255, 140, 0, 0.3);
                        transition: all 0.3s ease;
                        text-align: center;
                    " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 5px 15px rgba(255, 140, 0, 0.2)'" 
                    onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
                        <h3 style="color: #FFD700; margin: 0 0 10px 0; font-size: 1.1em;">👥 Network</h3>
                        <p style="margin: 0; color: #FFFFFF; font-size: 0.9em;">Character relationships</p>
                    </div>
                    <div style="
                        background: linear-gradient(135deg, rgba(253, 187, 45, 0.9), rgba(253, 187, 45, 0.7)); 
                        padding: 15px; 
                        border-radius: 10px; 
                        border: 1px solid rgba(255, 140, 0, 0.3);
                        transition: all 0.3s ease;
                        text-align: center;
                    " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 5px 15px rgba(255, 140, 0, 0.2)'" 
                    onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
                        <h3 style="color: #1a2a6c; margin: 0 0 10px 0; font-size: 1.1em;">🌀 Jutsu AI</h3>
                        <p style="margin: 0; color: #1a2a6c; font-size: 0.9em;">Classify techniques</p>
                    </div>
                    <div style="
                        background: linear-gradient(135deg, rgba(231, 84, 128, 0.9), rgba(231, 84, 128, 0.7)); 
                        padding: 15px; 
                        border-radius: 10px; 
                        border: 1px solid rgba(255, 140, 0, 0.3);
                        transition: all 0.3s ease;
                        text-align: center;
                    " onmouseover="this.style.transform='translateY(-3px)'; this.style.boxShadow='0 5px 15px rgba(255, 140, 0, 0.2)'" 
                    onmouseout="this.style.transform='none'; this.style.boxShadow='none'">
                        <h3 style="color: #FFFFFF; margin: 0 0 10px 0; font-size: 1.1em;">🗣️ AI Chat</h3>
                        <p style="margin: 0; color: #FFFFFF; font-size: 0.9em;">Talk with characters</p>
                    </div>
                </div>
                """)