# VidJSON - Veo3 AI Prompt Builder

Professional JSON prompt generation tool for Google's Veo3 AI video synthesis model, featuring interactive scene controls and AI-powered prompt assistance.

## 🚀 Live Demo

**[🎬 Try the AI-Powered Builder](ai_veo3_builder.html)** - Open in any browser, no installation required!

## Features

### 🤖 AI-Powered Prompt Building
- **Interactive Chat Assistant** - Describe your video in plain English
- **Smart Component Population** - AI automatically fills the 8-component framework
- **Scene-Aware Responses** - AI considers your current camera/lighting settings
- **Conversation Memory** - Builds on previous context for better suggestions

### 🎬 Professional Video Controls
- **Interactive Scene Configuration** - Camera FOV, angles, lighting, weather
- **Real-time Lens Analysis** - Shows focal length effects (telephoto to ultra-wide)
- **Scene Presets** - Film Noir, Nature Documentary, Portrait styles
- **8-Component Framework** - Subject, Action, Scene, Camera, Composition, Ambiance, Audio, Style

### 📋 Veo3 API Ready
- **Official JSON Format** - Compliant with Veo3 API requirements
- **Proper Audio Syntax** - Prevents subtitle generation issues
- **Copy/Download** - Ready to use with Vertex AI, Gemini API, or third-party services

## 🎯 Quick Start

### Option 1: Web Interface (Recommended)
1. Open `ai_veo3_builder.html` in any browser
2. Get your Mistral API key from [console.mistral.ai](https://console.mistral.ai/)
3. Enter the key and describe your video idea
4. Watch the AI build a structured prompt
5. Copy the JSON for use with Veo3

### Option 2: Python Version
```bash
pip install streamlit plotly aiohttp numpy
streamlit run veo3_prompt_builder.py
```

### Option 3: Demo/Learning
```bash
python3 demo_veo3_builder.py
```

## 📁 File Structure

```
├── ai_veo3_builder.html          # 🎯 Main AI-powered web interface
├── web_veo3_builder.html         # 🌐 Static web version (no AI)
├── veo3_prompt_builder.py        # 🐍 Full Streamlit application
├── demo_veo3_builder.py          # 📚 Python demo (no dependencies)
├── simple_veo3_builder.py        # 💻 CLI interactive version
├── requirements.txt              # 📦 Python dependencies
└── README.md                     # 📖 Documentation
```

## 🎨 Example Usage

### Sample Input
```
"A chef cooking pasta in a busy restaurant kitchen"
```

### AI Response
```
Great! I see you have a medium shot with natural lighting. Let me help build this out:

1. What type of pasta are they making?
2. What's the kitchen atmosphere - chaotic or organized?
3. Any specific cooking techniques to highlight?

COMPONENT SUGGESTIONS:
Subject: Professional chef in white coat, focused expression, experienced hands
Action: tossing fresh linguine in a large sauté pan with practiced movements
Scene: Busy restaurant kitchen with stainless steel surfaces, hanging utensils
Audio: sizzling oil, pasta water boiling, kitchen chatter in background
```

### Generated JSON
```json
{
  "prompt": "Subject: Professional chef in white coat, focused expression, experienced hands. Action: tossing fresh linguine in a large sauté pan with practiced movements. Scene: Busy restaurant kitchen with stainless steel surfaces, hanging utensils. Camera: medium shot, eye-level, 50° FOV. Composition: Rule of thirds with chef on right side. Ambiance: natural lighting, warm kitchen atmosphere. Audio: sizzling oil, pasta water boiling, kitchen chatter in background. Style: cinematic, documentary-style realism",
  "caption": "Professional chef expertly prepares fresh pasta in busy restaurant kitchen",
  "file_name": "chef-pasta-kitchen.mp4",
  "input_image_urls": [],
  "input_ids": []
}
```

## 🎥 8-Component Framework

1. **Subject** - Detailed character/object description
2. **Action** - What they're doing (single clear beat)
3. **Scene** - Location, time, weather, props
4. **Style** - Visual aesthetic (film noir, documentary, etc.)
5. **Camera** - Movement (dolly, pan, tracking, static)
6. **Composition** - Framing (wide shot, close-up, etc.)
7. **Ambiance** - Lighting and color tone
8. **Audio** - Dialogue, ambient sounds, music

## 🎤 Audio Best Practices

### Dialogue Syntax
```
✅ Correct: The chef says: "Order up!"
❌ Wrong:   The chef says "Order up!" (causes subtitles)
```

### Sound Layering
- **Ambient**: Kitchen noise, traffic, nature sounds
- **Effects**: Footsteps, cooking sounds, door closes
- **Music**: Background score, diegetic music
- **Dialogue**: Character speech with proper syntax

## 🔧 Technical Details

### Camera Controls
- **FOV Range**: 20° (telephoto) to 120° (ultra-wide)
- **Shot Types**: Wide, Medium, Close-up, Extreme Close-up
- **Angles**: Eye-level, Low, High, Bird's Eye, Dutch
- **Real-time Analysis**: Lens type and perspective effects

### Lighting Options
- **Natural**: Soft, even illumination
- **Dramatic**: High contrast, deep shadows
- **Soft**: Diffused, flattering light
- **Backlit**: Rim lighting, silhouette effects

### Time & Weather
- **Time of Day**: Dawn, Day, Dusk, Night
- **Weather**: Clear, Cloudy, Rainy, Foggy, Snowy
- **Atmosphere**: Auto-generated mood descriptions

## 🌐 Deployment Options

### Local Development
```bash
# Clone the repository
git clone https://github.com/Kugothepup/vidjson.git
cd vidjson

# Option 1: Open HTML file directly
open ai_veo3_builder.html

# Option 2: Python development
pip install -r requirements.txt
streamlit run veo3_prompt_builder.py
```

### Web Hosting
- **GitHub Pages** - Static hosting for HTML versions
- **Streamlit Cloud** - Full Python app deployment
- **Vercel/Netlify** - Fast static site deployment

## 🔑 API Keys

### Mistral AI
1. Visit [console.mistral.ai](https://console.mistral.ai/)
2. Sign up for free account
3. Generate API key
4. Enter in the application

### Veo3 Access
- **Google Vertex AI** - Enterprise-grade API
- **Gemini API** - Developer-friendly SDK
- **Third-party**: Leonardo.ai, fal.ai, Pollo.ai

## 🛠️ Development

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

### Testing
```bash
# Test Python version
python3 demo_veo3_builder.py

# Test web version
open ai_veo3_builder.html in browser
```

## 📜 License

MIT License - see LICENSE file for details.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/Kugothepup/vidjson/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Kugothepup/vidjson/discussions)
- **Documentation**: [Wiki](https://github.com/Kugothepup/vidjson/wiki)

## 📈 Roadmap

- [ ] Advanced scene presets library
- [ ] Video preview generation
- [ ] Batch prompt processing
- [ ] Template system for common scenarios
- [ ] Integration with more AI video models
- [ ] Community prompt sharing

---

**Built with ❤️ for the AI video generation community**