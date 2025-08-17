#!/usr/bin/env python3
"""
Demo Veo3 Prompt Builder
Shows the complete workflow for building structured JSON prompts for Veo3
"""

import json
from dataclasses import dataclass

@dataclass
class SceneConfig:
    camera_fov: float = 85.0
    shot_type: str = "medium"
    camera_angle: str = "low angle"
    lighting_type: str = "dramatic"
    time_of_day: str = "dusk"
    weather: str = "rainy"

@dataclass
class PromptComponents:
    subject: str = "A woman in her late 20s, wearing an elegant, floor-length scarlet red dress, confident expression"
    action: str = "walking slowly down a rain-slicked city street, looking over her shoulder mysteriously"
    scene: str = "Downtown district at midnight, neon signs reflecting in wet pavement, narrow alleyway"
    camera: str = "Smooth tracking shot following behind, 85mm lens with shallow depth of field"
    composition: str = "Medium shot transitioning to close-up, rule of thirds composition"
    ambiance: str = "Film noir aesthetic, high contrast lighting, deep blues and purples with crimson dress accent"
    audio: str = "Audio: steady rain on pavement, distant jazz saxophone from a bar, her heels clicking on wet stone"
    style: str = "cinematic, film noir, moody atmospheric lighting"

def display_welcome():
    print("=" * 70)
    print("🎬 VEO3 INTERACTIVE PROMPT BUILDER - DEMO")
    print("=" * 70)
    print("Demonstrating professional JSON prompt generation for Veo3")
    print("Using the 8-component framework with scene visualization")
    print()

def analyze_scene_setup(scene: SceneConfig):
    print("🎛️  SCENE CONFIGURATION ANALYSIS")
    print("-" * 40)
    
    # Lens analysis
    fov = scene.camera_fov
    if fov < 25:
        lens_type = "Super Telephoto (200mm+)"
        effect = "Strong compression, isolated subjects"
    elif fov < 35:
        lens_type = "Telephoto (85-135mm)"
        effect = "Portrait lens, natural compression"
    elif fov < 55:
        lens_type = "Standard (35-50mm)"
        effect = "Natural perspective, human-like vision"
    elif fov < 75:
        lens_type = "Wide Angle (24-35mm)"
        effect = "Expanded view, some distortion"
    else:
        lens_type = "Ultra Wide (14-24mm)"
        effect = "Dramatic perspective, high distortion"
    
    print(f"📷 Camera Setup:")
    print(f"   FOV: {scene.camera_fov}° ({lens_type})")
    print(f"   Effect: {effect}")
    print(f"   Shot: {scene.shot_type}")
    print(f"   Angle: {scene.camera_angle}")
    
    print(f"\n💡 Lighting Analysis:")
    print(f"   Style: {scene.lighting_type}")
    print(f"   Time: {scene.time_of_day}")
    print(f"   Weather: {scene.weather}")
    
    # Mood analysis
    mood_combinations = {
        ("dramatic", "dusk", "rainy"): "Intense, moody atmosphere with high contrast shadows and reflective surfaces",
        ("natural", "day", "clear"): "Bright, clean aesthetic with even lighting",
        ("soft", "dawn", "foggy"): "Ethereal, dreamlike quality with diffused light"
    }
    
    key = (scene.lighting_type, scene.time_of_day, scene.weather)
    mood = mood_combinations.get(key, f"{scene.lighting_type} {scene.time_of_day} mood")
    print(f"   Atmosphere: {mood}")
    print()

def display_8_component_framework(components: PromptComponents):
    print("📝 8-COMPONENT FRAMEWORK BREAKDOWN")
    print("-" * 45)
    
    framework = [
        ("1. SUBJECT", components.subject, "Character/object details: appearance, wardrobe, emotion"),
        ("2. ACTION", components.action, "What they're doing - single clear beat"),
        ("3. SCENE", components.scene, "Environment: location, time, props"),
        ("4. CAMERA", components.camera, "Movement: dolly, pan, tracking, static"),
        ("5. COMPOSITION", components.composition, "Framing: wide, medium, close-up"),
        ("6. AMBIANCE", components.ambiance, "Lighting and color tone"),
        ("7. AUDIO", components.audio, "Dialogue, ambient, effects, music"),
        ("8. STYLE", components.style, "Visual aesthetic and genre")
    ]
    
    for title, content, description in framework:
        print(f"\n{title}")
        print(f"   Purpose: {description}")
        print(f"   Content: {content}")

def build_veo3_json(scene: SceneConfig, components: PromptComponents):
    print("\n🔧 BUILDING VEO3 JSON STRUCTURE")
    print("-" * 40)
    
    # Build the main prompt from components
    prompt_parts = [
        f"Subject: {components.subject}",
        f"Action: {components.action}",
        f"Scene: {components.scene}",
        f"Camera: {components.camera}",
        f"Composition: {components.composition}",
        f"Ambiance: {components.ambiance}",
        f"Audio: {components.audio}",
        f"Style: {components.style}"
    ]
    
    full_prompt = ". ".join(prompt_parts)
    
    # Generate caption (first 30 words)
    words = full_prompt.replace("Subject: ", "").replace("Action: ", "").split()[:8]
    caption = " ".join(words) + "..."
    
    # Generate filename
    scene_descriptor = f"{scene.shot_type.replace(' ', '')}-{scene.time_of_day}"
    filename = f"{scene_descriptor}.mp4"
    
    # Build final JSON
    veo3_json = {
        "prompt": full_prompt,
        "caption": caption,
        "file_name": filename,
        "input_image_urls": [],
        "input_ids": []
    }
    
    return veo3_json

def display_audio_best_practices():
    print("\n🎤 AUDIO GENERATION BEST PRACTICES")
    print("-" * 45)
    print("✓ DIALOGUE SYNTAX:")
    print("   Correct: The woman says: \"Let's go.\" (colon prevents subtitles)")
    print("   Wrong:   The woman says \"Let's go.\" (causes subtitles)")
    print("\n✓ SOUND LAYERING:")
    print("   • Ambient: rain on pavement, city traffic")
    print("   • Effects: heels clicking, door closing")
    print("   • Music: jazz saxophone, string quartet")
    print("\n✓ PREVENT HALLUCINATIONS:")
    print("   • Be explicit about expected audio")
    print("   • Specify 'no dialogue' if silent scene")
    print("   • Define background audio even if minimal")

def display_camera_techniques():
    print("\n🎬 ADVANCED CAMERA TECHNIQUES")
    print("-" * 40)
    print("📷 MOVEMENT OPTIONS:")
    print("   • Static: No movement, focus on performance")
    print("   • Dolly: Physical camera movement toward/away")
    print("   • Tracking: Following subject movement")
    print("   • Pan/Tilt: Rotating to reveal or follow")
    print("   • Crane: Sweeping vertical movements")
    print("   • Handheld: Intimate, documentary feel")
    print("\n🎯 COMPOSITION RULES:")
    print("   • Rule of thirds: Subject on intersection points")
    print("   • Leading lines: Guide viewer's eye")
    print("   • Depth of field: Isolate subject with blur")
    print("   • Symmetry: Create balance and harmony")

def main():
    display_welcome()
    
    # Demo scene configuration
    scene = SceneConfig()
    components = PromptComponents()
    
    # Analyze the scene setup
    analyze_scene_setup(scene)
    
    # Show 8-component framework
    display_8_component_framework(components)
    
    # Build the JSON
    veo3_json = build_veo3_json(scene, components)
    
    # Display final output
    print("\n📋 FINAL VEO3 JSON PROMPT")
    print("=" * 50)
    print(json.dumps(veo3_json, indent=2))
    
    # Best practices
    display_audio_best_practices()
    display_camera_techniques()
    
    # Save to file
    with open("demo_veo3_prompt.json", "w") as f:
        json.dump(veo3_json, f, indent=2)
    
    print(f"\n💾 Demo JSON saved to: demo_veo3_prompt.json")
    print("\n🎯 NEXT STEPS:")
    print("   1. Copy this JSON structure")
    print("   2. Modify components for your specific video")
    print("   3. Use with Veo3 API (Vertex AI, Gemini API, or third-party)")
    print("   4. Experiment with different camera angles and lighting")
    print("\n🚀 For full interactive version, install Streamlit:")
    print("   pip install streamlit plotly aiohttp")
    print("   streamlit run veo3_prompt_builder.py")

if __name__ == "__main__":
    main()