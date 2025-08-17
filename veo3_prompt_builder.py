import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import json
import asyncio
import aiohttp
from typing import Dict, Any
import numpy as np
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Veo3 Interactive Prompt Builder",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class PromptComponents:
    subject: str = ""
    action: str = ""
    scene: str = ""
    style: str = "cinematic, photorealistic"
    camera: str = ""
    composition: str = ""
    ambiance: str = ""
    audio: str = ""

@dataclass
class SceneConfig:
    camera_fov: float = 50.0
    camera_height: float = 5.0
    camera_distance: float = 10.0
    camera_angle: str = "eye-level"
    shot_type: str = "medium"
    lighting_intensity: float = 1.0
    lighting_type: str = "natural"
    time_of_day: str = "day"
    weather: str = "clear"

class Veo3PromptBuilder:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Hi! I'm your Veo3 prompt assistant. Use the controls to set up your scene, then describe your video idea. I'll help you build a structured JSON prompt using the 8-component framework and current scene settings."
                }
            ]
        
        if 'prompt_components' not in st.session_state:
            st.session_state.prompt_components = PromptComponents()
        
        if 'scene_config' not in st.session_state:
            st.session_state.scene_config = SceneConfig()
        
        if 'current_prompt' not in st.session_state:
            st.session_state.current_prompt = {
                "prompt": "",
                "caption": "",
                "file_name": "video.mp4",
                "input_image_urls": [],
                "input_ids": []
            }

    def create_3d_scene_visualization(self, config: SceneConfig) -> go.Figure:
        """Create interactive 3D scene visualization using Plotly."""
        
        # Calculate camera position based on config
        camera_x = config.camera_distance * np.cos(np.radians(0))
        camera_y = config.camera_height
        camera_z = config.camera_distance * np.sin(np.radians(0))
        
        # Create figure
        fig = go.Figure()
        
        # Ground plane
        ground_size = 15
        ground_x, ground_z = np.meshgrid(
            np.linspace(-ground_size/2, ground_size/2, 10),
            np.linspace(-ground_size/2, ground_size/2, 10)
        )
        ground_y = np.zeros_like(ground_x)
        
        fig.add_trace(go.Surface(
            x=ground_x, y=ground_y, z=ground_z,
            colorscale=[[0, 'gray'], [1, 'gray']],
            showscale=False,
            name="Ground"
        ))
        
        # Subject (represented as a box)
        subject_points = [
            [0, 0, 0], [1, 0, 0], [1, 2, 0], [0, 2, 0],  # Front face
            [0, 0, 1], [1, 0, 1], [1, 2, 1], [0, 2, 1]   # Back face
        ]
        
        # Add subject as scatter points
        fig.add_trace(go.Scatter3d(
            x=[p[0] for p in subject_points],
            y=[p[1] for p in subject_points],
            z=[p[2] for p in subject_points],
            mode='markers',
            marker=dict(size=8, color='blue'),
            name="Subject"
        ))
        
        # Camera position indicator
        fig.add_trace(go.Scatter3d(
            x=[camera_x], y=[camera_y], z=[camera_z],
            mode='markers+text',
            marker=dict(size=12, color='red', symbol='diamond'),
            text=['Camera'],
            textposition='top center',
            name="Camera"
        ))
        
        # Camera to subject line
        fig.add_trace(go.Scatter3d(
            x=[camera_x, 0.5], y=[camera_y, 1], z=[camera_z, 0.5],
            mode='lines',
            line=dict(color='red', width=3, dash='dash'),
            name="Camera View"
        ))
        
        # Lighting direction indicator
        light_positions = {
            'natural': (3, 8, 3),
            'dramatic': (-2, 10, 2),
            'soft': (5, 6, 5),
            'backlit': (-3, 4, -3)
        }
        
        light_pos = light_positions.get(config.lighting_type, (3, 8, 3))
        fig.add_trace(go.Scatter3d(
            x=[light_pos[0]], y=[light_pos[1]], z=[light_pos[2]],
            mode='markers+text',
            marker=dict(size=10, color='yellow', symbol='star'),
            text=['Light'],
            textposition='top center',
            name="Key Light"
        ))
        
        # Set layout
        fig.update_layout(
            title=f"Scene Preview: {config.shot_type.title()} Shot, {config.camera_angle.title()} Angle",
            scene=dict(
                xaxis_title="X",
                yaxis_title="Y (Height)",
                zaxis_title="Z",
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                ),
                aspectmode='cube'
            ),
            height=400,
            showlegend=True
        )
        
        return fig

    def create_fov_visualization(self, fov: float) -> go.Figure:
        """Create field of view visualization."""
        # Calculate FOV cone
        distance = 10
        half_fov = np.radians(fov / 2)
        
        # FOV cone points
        cone_width = distance * np.tan(half_fov)
        
        fig = go.Figure()
        
        # Camera cone
        fig.add_trace(go.Scatter(
            x=[0, -cone_width, cone_width, 0],
            y=[0, distance, distance, 0],
            fill='toself',
            fillcolor='rgba(255, 0, 0, 0.3)',
            line=dict(color='red'),
            name=f'FOV: {fov}°'
        ))
        
        # Subject area
        fig.add_shape(
            type="rect",
            x0=-2, y0=8, x1=2, y1=12,
            fillcolor="rgba(0, 100, 255, 0.3)",
            line=dict(color="blue")
        )
        
        fig.update_layout(
            title="Field of View Preview",
            xaxis_title="Width",
            yaxis_title="Distance",
            height=300,
            showlegend=True
        )
        
        return fig

    async def call_mistral_api(self, message: str, api_key: str, scene_context: str) -> str:
        """Call Mistral API with scene context."""
        
        context = f"""You are an expert Veo3 prompt builder. Help create structured JSON prompts using the 8-component framework.

Current 3D scene context: {scene_context}

Veo3 JSON format requirements:
- "prompt": Detailed scene description using 8 components
- "caption": One-sentence summary (max 30 words)  
- "file_name": Descriptive name ending in .mp4 (max 20 chars)
- "input_image_urls": Array of reference URLs (empty if none)
- "input_ids": Array of generated image IDs (empty if none)

8-Component Framework:
1. Subject: Detailed character/object description
2. Action: What they're doing (single clear beat)
3. Scene: Location, time, weather, props
4. Style: Visual aesthetic (film noir, etc.)
5. Camera: Movement (dolly, pan, tracking, static)
6. Composition: Framing (wide shot, close-up, etc.)
7. Ambiance: Lighting and color tone
8. Audio: All sound elements (dialogue: "text", ambient, music)

CRITICAL Audio syntax: Character says: "dialogue" (colon prevents subtitles)

User message: "{message}"

Provide helpful guidance and ask 1-2 targeted questions. When ready, output complete JSON."""

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        payload = {
            'model': 'mistral-large-latest',
            'messages': [
                {'role': 'system', 'content': context},
                {'role': 'user', 'content': message}
            ],
            'temperature': 0.7,
            'max_tokens': 1000
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    'https://api.mistral.ai/v1/chat/completions',
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data['choices'][0]['message']['content']
                    else:
                        return f"API Error: {response.status}"
        except Exception as e:
            return f"Connection error: {str(e)}"

    def build_scene_context(self, config: SceneConfig) -> str:
        """Build scene context string for AI."""
        return f"""Camera: {config.shot_type} shot, {config.camera_fov}° FOV, {config.camera_angle} angle
Lighting: {config.lighting_type} lighting, {config.time_of_day}, intensity {config.lighting_intensity}
Weather: {config.weather}
Position: Camera at height {config.camera_height}m, distance {config.camera_distance}m"""

    def update_prompt_from_components(self):
        """Update main prompt from individual components."""
        components = st.session_state.prompt_components
        
        prompt_parts = []
        if components.subject: prompt_parts.append(f"Subject: {components.subject}")
        if components.action: prompt_parts.append(f"Action: {components.action}")
        if components.scene: prompt_parts.append(f"Scene: {components.scene}")
        if components.camera: prompt_parts.append(f"Camera: {components.camera}")
        if components.composition: prompt_parts.append(f"Composition: {components.composition}")
        if components.ambiance: prompt_parts.append(f"Ambiance: {components.ambiance}")
        if components.audio: prompt_parts.append(f"Audio: {components.audio}")
        if components.style: prompt_parts.append(f"Style: {components.style}")
        
        st.session_state.current_prompt["prompt"] = ". ".join(prompt_parts)

    def run(self):
        """Main Streamlit app."""
        
        # Header
        st.title("🎬 Veo3 Interactive Prompt Builder")
        st.markdown("**Build professional JSON prompts with interactive 3D scene preview**")
        
        # Main layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.subheader("🎛️ Scene Controls")
            
            # API Key
            api_key = st.text_input("Mistral API Key", type="password", help="Get your key at console.mistral.ai")
            
            st.markdown("---")
            
            # Camera controls
            st.markdown("**📷 Camera**")
            config = st.session_state.scene_config
            
            config.camera_fov = st.slider("Field of View", 20, 120, int(config.camera_fov), help="Lens focal length equivalent")
            config.shot_type = st.selectbox("Shot Type", ["wide", "medium", "close-up", "extreme close-up"])
            config.camera_angle = st.selectbox("Camera Angle", ["eye-level", "low angle", "high angle", "bird's eye", "dutch angle"])
            config.camera_height = st.slider("Camera Height", 0.5, 15.0, config.camera_height)
            config.camera_distance = st.slider("Camera Distance", 2.0, 20.0, config.camera_distance)
            
            st.markdown("**💡 Lighting**")
            config.lighting_type = st.selectbox("Lighting Style", ["natural", "dramatic", "soft", "backlit"])
            config.lighting_intensity = st.slider("Intensity", 0.1, 2.0, config.lighting_intensity)
            config.time_of_day = st.selectbox("Time of Day", ["dawn", "day", "dusk", "night"])
            config.weather = st.selectbox("Weather", ["clear", "cloudy", "rainy", "foggy", "snowy"])
            
            # Update session state
            st.session_state.scene_config = config
            
            st.markdown("---")
            
            # 8-Component Framework
            st.subheader("📝 Prompt Components")
            components = st.session_state.prompt_components
            
            components.subject = st.text_area("Subject", components.subject, height=60, help="Detailed character/object description")
            components.action = st.text_area("Action", components.action, height=60, help="What they're doing")
            components.scene = st.text_area("Scene", components.scene, height=60, help="Location, time, props")
            components.camera = st.text_area("Camera", components.camera, height=60, help="Movement: dolly, pan, tracking")
            components.composition = st.text_area("Composition", components.composition, height=60, help="Framing: wide shot, close-up")
            components.ambiance = st.text_area("Ambiance", components.ambiance, height=60, help="Lighting and mood")
            components.audio = st.text_area("Audio", components.audio, height=60, help="Dialogue, sounds, music")
            components.style = st.text_input("Style", components.style, help="Visual aesthetic")
            
            # Update session state
            st.session_state.prompt_components = components
            self.update_prompt_from_components()
        
        with col2:
            st.subheader("🎮 3D Scene Preview")
            
            # 3D Scene
            scene_fig = self.create_3d_scene_visualization(st.session_state.scene_config)
            st.plotly_chart(scene_fig, use_container_width=True)
            
            # FOV Preview
            fov_fig = self.create_fov_visualization(st.session_state.scene_config.camera_fov)
            st.plotly_chart(fov_fig, use_container_width=True)
            
            # Scene info
            with st.expander("📊 Scene Information", expanded=True):
                config = st.session_state.scene_config
                st.write(f"**Camera:** {config.shot_type} shot, {config.camera_fov}° FOV")
                st.write(f"**Angle:** {config.camera_angle}")
                st.write(f"**Lighting:** {config.lighting_type}, {config.time_of_day}")
                st.write(f"**Weather:** {config.weather}")
        
        with col3:
            st.subheader("🤖 AI Assistant")
            
            # Chat messages
            chat_container = st.container()
            with chat_container:
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])
            
            # Chat input
            if prompt := st.chat_input("Describe your video idea..."):
                if not api_key:
                    st.error("Please enter your Mistral API key first!")
                else:
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    
                    # Get AI response
                    scene_context = self.build_scene_context(st.session_state.scene_config)
                    
                    with st.spinner("AI thinking..."):
                        try:
                            response = asyncio.run(self.call_mistral_api(prompt, api_key, scene_context))
                            st.session_state.messages.append({"role": "assistant", "content": response})
                            
                            # Extract JSON if present
                            if "```json" in response:
                                json_start = response.find("```json") + 7
                                json_end = response.find("```", json_start)
                                if json_end > json_start:
                                    try:
                                        json_str = response[json_start:json_end].strip()
                                        new_prompt = json.loads(json_str)
                                        st.session_state.current_prompt.update(new_prompt)
                                        st.success("JSON prompt updated!")
                                    except json.JSONDecodeError:
                                        pass
                            
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
            
            # JSON Output
            st.markdown("---")
            st.subheader("📋 Generated JSON")
            
            # Auto-generate caption and filename
            if st.button("🔄 Auto-Generate Caption & Filename"):
                prompt_text = st.session_state.current_prompt.get("prompt", "")
                if prompt_text:
                    # Simple caption generation
                    words = prompt_text.split()[:8]
                    caption = " ".join(words) + "..."
                    st.session_state.current_prompt["caption"] = caption
                    
                    # Simple filename generation
                    scene_type = st.session_state.scene_config.shot_type
                    time_of_day = st.session_state.scene_config.time_of_day
                    filename = f"{scene_type}-{time_of_day}.mp4"
                    st.session_state.current_prompt["file_name"] = filename
                    st.rerun()
            
            # Display JSON
            json_str = json.dumps(st.session_state.current_prompt, indent=2)
            st.code(json_str, language="json")
            
            # Copy button
            if st.button("📋 Copy JSON"):
                # Note: In real deployment, you'd use a proper clipboard solution
                st.success("JSON copied to display above!")

# Run the app
if __name__ == "__main__":
    app = Veo3PromptBuilder()
    app.run()