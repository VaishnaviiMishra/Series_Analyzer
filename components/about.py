import gradio as gr

def create_about_section():
    with gr.Row(elem_id="about-section", elem_classes="section"):
        with gr.Column():
            gr.HTML("""
            <div style="
                padding: 40px; 
                background: rgba(30, 30, 30, 0.9); 
                border-radius: 15px;
                border: 1px solid #444;
                color: #f0f0f0;
            ">
                <h2 style="
                    color: #FF8C00; 
                    text-align: center; 
                    margin-bottom: 30px;
                    font-size: 2.2em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                ">About Naruto Series</h2>
                
                <div style="
                    margin-bottom: 40px;
                    background: rgba(40, 40, 40, 0.7);
                    padding: 25px;
                    border-radius: 12px;
                    border-left: 4px solid #FF8C00;
                ">
                    <h3 style="color: #FFD700; margin-top: 0;">Story Overview</h3>
                    <p style="line-height: 1.6;">Naruto follows the journey of Naruto Uzumaki, a young ninja who seeks recognition from his peers and dreams of becoming the Hokage, the leader of his village. The story explores his growth from a lonely orphan to a hero who saves the shinobi world through three main parts: Original Series, Shippuden, and Boruto: Naruto Next Generations.</p>
                </div>

                <div style="
                    display: grid; 
                    grid-template-columns: 1fr 1fr; 
                    gap: 30px; 
                    margin-bottom: 40px;
                ">
                    <div style="
                        background: rgba(40, 40, 40, 0.7);
                        padding: 25px;
                        border-radius: 12px;
                        border-left: 4px solid #1a2a6c;
                    ">
                        <h3 style="color: #FFD700;">Main Themes</h3>
                        <p style="line-height: 1.6;">The series explores profound themes including friendship, perseverance, redemption, and the struggle between destiny and free will. It emphasizes the importance of never giving up and the power of bonds between people, while addressing complex topics like discrimination, war, and the cycle of hatred that plagues the shinobi world.</p>
                    </div>
                    <div style="
                        background: rgba(40, 40, 40, 0.7);
                        padding: 25px;
                        border-radius: 12px;
                        border-left: 4px solid #b21f1f;
                    ">
                        <h3 style="color: #FFD700;">Cultural Impact</h3>
                        <p style="line-height: 1.6;">Naruto has become one of the most influential manga and anime series worldwide, inspiring countless fans and creators. Its characters, techniques, and themes have left a lasting impact on popular culture and the shonen genre, with iconic elements like Rasengan, Shadow Clone Jutsu, and the Sharingan becoming globally recognized symbols.</p>
                    </div>
                </div>

                <div style="
                    background: rgba(40, 40, 40, 0.7);
                    padding: 25px;
                    border-radius: 12px;
                    border-left: 4px solid #6a0dad;
                    margin-bottom: 40px;
                ">
                    <h3 style="color: #FFD700; text-align: center; margin-bottom: 20px;">Series Timeline</h3>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
                        <div>
                            <h4 style="color: #FF8C00; border-bottom: 2px solid #FF8C00; padding-bottom: 5px;">Original Series</h4>
                            <p style="margin: 10px 0 0 0; font-size: 0.9em;">2002-2007<br>Episodes 1-220<br>Focuses on Naruto's early years and Chunin Exams</p>
                        </div>
                        <div>
                            <h4 style="color: #1a2a6c; border-bottom: 2px solid #1a2a6c; padding-bottom: 5px;">Shippuden</h4>
                            <p style="margin: 10px 0 0 0; font-size: 0.9em;">2007-2017<br>Episodes 1-500<br>Continues with time skip and Akatsuki storyline</p>
                        </div>
                        <div>
                            <h4 style="color: #e75480; border-bottom: 2px solid #e75480; padding-bottom: 5px;">Boruto: Next Generations</h4>
                            <p style="margin: 10px 0 0 0; font-size: 0.9em;">2017-Present<br>Ongoing<br>Focuses on Naruto's son and new generation</p>
                        </div>
                    </div>
                </div>

                <div style="
                    background: rgba(40, 40, 40, 0.7);
                    padding: 25px;
                    border-radius: 12px;
                    border-left: 4px solid #008080;
                    margin-bottom: 30px;
                ">
                    <h3 style="color: #FFD700; text-align: center; margin-bottom: 20px;">Main Characters</h3>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
                        <div>
                            <h4 style="color: #FF8C00; border-bottom: 2px solid #FF8C00; padding-bottom: 5px;">Naruto Uzumaki</h4>
                            <p style="margin: 10px 0 0 0; font-size: 0.9em;">The protagonist and jinchuriki of the Nine-Tails who dreams of becoming Hokage. Known for his determination, resilience, and belief in never giving up.</p>
                        </div>
                        <div>
                            <h4 style="color: #1a2a6c; border-bottom: 2px solid #1a2a6c; padding-bottom: 5px;">Sasuke Uchiha</h4>
                            <p style="margin: 10px 0 0 0; font-size: 0.9em;">The last surviving member of the Uchiha clan, driven by revenge but ultimately seeking redemption. Possesses the powerful Sharingan and Rinnegan.</p>
                        </div>
                        <div>
                            <h4 style="color: #e75480; border-bottom: 2px solid #e75480; padding-bottom: 5px;">Sakura Haruno</h4>
                            <p style="margin: 10px 0 0 0; font-size: 0.9em;">A skilled medical ninja trained by Tsunade, possessing incredible strength and chakra control. Represents the growth from infatuation to maturity.</p>
                        </div>
                    </div>
                </div>

                <div style="
                    margin-top: 30px; 
                    text-align: center;
                    background: rgba(40, 40, 40, 0.7);
                    padding: 20px;
                    border-radius: 10px;
                    border-top: 2px solid #FF8C00;
                ">
                    <p style="margin: 0; color: #FFD700;">
                        <strong>Series Duration:</strong> 2002-2017 | 
                        <strong>Total Episodes:</strong> 720+ | 
                        <strong>Manga Chapters:</strong> 700 | 
                        <strong>Creator:</strong> Masashi Kishimoto
                    </p>
                    <p style="margin: 10px 0 0 0; color: #FFD700; font-size: 0.9em;">
                        The series has spawned numerous movies, video games, novels, and a lasting legacy in anime culture worldwide.
                    </p>
                </div>
            </div>
            """)