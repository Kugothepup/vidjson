#!/usr/bin/env python3
"""
Simple Veo3 Prompt Builder
A command-line tool for building structured JSON prompts for Veo3
"""

import json
import sys
from dataclasses import dataclass, asdict
from typing import Dict, Any

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
        self.components = PromptComponents()
        self.scene = SceneConfig()
        self.current_prompt = {
            "prompt": "",
            "caption": "",
            "file_name": "video.mp4",
            "input_image_urls": [],
            "input_ids": []
        }

    def display_welcome(self):
        print("=" * 60)
        print("🎬 VEO3 INTERACTIVE PROMPT BUILDER")
        print("=" * 60)
        print("Build professional JSON prompts for Veo3 AI video generation")
        print("Using the 8-component framework with scene visualization")
        print()

    def display_scene_info(self):
        print(f"\n📊 CURRENT SCENE CONFIGURATION:")
        print(f"   Camera: {self.scene.shot_type} shot, {self.scene.camera_fov}° FOV")
        print(f"   Angle: {self.scene.camera_angle}")
        print(f"   Position: Height {self.scene.camera_height}m, Distance {self.scene.camera_distance}m")
        print(f"   Lighting: {self.scene.lighting_type}, {self.scene.time_of_day}")
        print(f"   Weather: {self.scene.weather}")
        print()

    def display_lens_guide(self, fov: float):
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
        
        print(f"📷 Lens Guide: {lens_type}")
        print(f"   Effect: {effect}")

    def configure_scene(self):
        print("\n🎛️  SCENE CONFIGURATION")
        print("-" * 30)
        
        while True:
            self.display_scene_info()
            
            print("Configuration Options:")
            print("1. Camera FOV (Field of View)")
            print("2. Shot Type")
            print("3. Camera Angle") 
            print("4. Camera Position")
            print("5. Lighting Style")
            print("6. Time of Day")
            print("7. Weather")
            print("8. Continue to Prompt Building")
            
            choice = input("\nSelect option (1-8): ").strip()
            
            if choice == "1":
                print(f"\nCurrent FOV: {self.scene.camera_fov}°")
                self.display_lens_guide(self.scene.camera_fov)
                try:
                    fov = float(input("Enter FOV (20-120°): "))
                    if 20 <= fov <= 120:
                        self.scene.camera_fov = fov
                        self.display_lens_guide(fov)
                    else:
                        print("FOV must be between 20° and 120°")
                except ValueError:
                    print("Please enter a valid number")
            
            elif choice == "2":
                print("\nShot Types:")
                print("1. Wide Shot")
                print("2. Medium Shot") 
                print("3. Close-up")
                print("4. Extreme Close-up")
                shot_choice = input("Select shot type (1-4): ").strip()
                shots = {"1": "wide", "2": "medium", "3": "close-up", "4": "extreme close-up"}
                if shot_choice in shots:
                    self.scene.shot_type = shots[shot_choice]
            
            elif choice == "3":
                print("\nCamera Angles:")
                print("1. Eye Level")
                print("2. Low Angle")
                print("3. High Angle")
                print("4. Bird's Eye")
                print("5. Dutch Angle")
                angle_choice = input("Select angle (1-5): ").strip()
                angles = {"1": "eye-level", "2": "low angle", "3": "high angle", 
                         "4": "bird's eye", "5": "dutch angle"}
                if angle_choice in angles:
                    self.scene.camera_angle = angles[angle_choice]
            
            elif choice == "4":
                try:
                    height = float(input(f"Camera height (current: {self.scene.camera_height}m): "))
                    distance = float(input(f"Camera distance (current: {self.scene.camera_distance}m): "))
                    if height >= 0 and distance > 0:
                        self.scene.camera_height = height
                        self.scene.camera_distance = distance
                except ValueError:
                    print("Please enter valid numbers")
            
            elif choice == "5":
                print("\nLighting Styles:")
                print("1. Natural")
                print("2. Dramatic")
                print("3. Soft")
                print("4. Backlit")
                light_choice = input("Select lighting (1-4): ").strip()
                lights = {"1": "natural", "2": "dramatic", "3": "soft", "4": "backlit"}
                if light_choice in lights:
                    self.scene.lighting_type = lights[light_choice]
            
            elif choice == "6":
                print("\nTime of Day:")
                print("1. Dawn")
                print("2. Day")
                print("3. Dusk")
                print("4. Night")
                time_choice = input("Select time (1-4): ").strip()
                times = {"1": "dawn", "2": "day", "3": "dusk", "4": "night"}
                if time_choice in times:
                    self.scene.time_of_day = times[time_choice]
            
            elif choice == "7":
                print("\nWeather:")
                print("1. Clear")
                print("2. Cloudy")
                print("3. Rainy")
                print("4. Foggy")
                print("5. Snowy")
                weather_choice = input("Select weather (1-5): ").strip()
                weathers = {"1": "clear", "2": "cloudy", "3": "rainy", "4": "foggy", "5": "snowy"}
                if weather_choice in weathers:
                    self.scene.weather = weathers[weather_choice]
            
            elif choice == "8":
                break
            else:
                print("Invalid choice. Please select 1-8.")

    def build_prompt_components(self):
        print("\n📝 8-COMPONENT PROMPT BUILDING")
        print("-" * 40)
        
        components_info = {
            "subject": "Detailed character/object description (age, appearance, wardrobe, emotional state)",
            "action": "What they're doing - single clear beat of action with vivid verbs",
            "scene": "Environment: location, time of day, weather, key props",
            "camera": "Camera movement: dolly, pan, tracking, static, handheld",
            "composition": "Framing: wide shot, medium shot, close-up, extreme close-up",
            "ambiance": "Lighting and color tone: soft north-light, Rembrandt lighting, sunset orange",
            "audio": "All sound elements: dialogue, ambient noise, sound effects, music",
            "style": "Visual aesthetic: film genres, artistic movements, technical qualities"
        }
        
        for component, description in components_info.items():
            print(f"\n{component.upper()}:")
            print(f"   {description}")
            current_value = getattr(self.components, component)
            if current_value:
                print(f"   Current: {current_value}")
            
            new_value = input(f"   Enter {component}: ").strip()
            if new_value:
                setattr(self.components, component, new_value)
        
        # Auto-suggest based on scene config
        self.suggest_from_scene()

    def suggest_from_scene(self):
        print("\n🤖 AI SUGGESTIONS BASED ON SCENE:")
        print("-" * 35)
        
        # Camera suggestions
        if not self.components.camera:
            camera_suggestions = {
                "wide": "Static wide shot establishing the environment",
                "medium": "Slow dolly forward for character focus",
                "close-up": "Handheld close-up for intimacy",
                "extreme close-up": "Macro lens extreme close-up revealing details"
            }
            suggestion = camera_suggestions.get(self.scene.shot_type, "Static shot")
            print(f"📷 Camera suggestion: {suggestion}")
            if input("   Use this suggestion? (y/n): ").lower() == 'y':
                self.components.camera = suggestion
        
        # Ambiance suggestions
        if not self.components.ambiance:
            ambiance_map = {
                ("natural", "day"): "Bright natural sunlight with soft shadows",
                ("natural", "dawn"): "Golden hour lighting with warm orange tones",
                ("natural", "dusk"): "Blue hour with deep purple and orange sky",
                ("natural", "night"): "Moonlight with cool blue tones and deep shadows",
                ("dramatic", "day"): "High contrast lighting with sharp shadows",
                ("dramatic", "night"): "Chiaroscuro lighting with stark black and white contrast",
                ("soft", "day"): "Diffused overcast light with gentle shadows",
                ("backlit", "day"): "Strong backlighting creating silhouettes and rim light"
            }
            
            key = (self.scene.lighting_type, self.scene.time_of_day)
            suggestion = ambiance_map.get(key, f"{self.scene.lighting_type} {self.scene.time_of_day} lighting")
            print(f"💡 Ambiance suggestion: {suggestion}")
            if input("   Use this suggestion? (y/n): ").lower() == 'y':
                self.components.ambiance = suggestion

    def build_final_prompt(self):
        components = [
            f"Subject: {self.components.subject}" if self.components.subject else "",
            f"Action: {self.components.action}" if self.components.action else "",
            f"Scene: {self.components.scene}" if self.components.scene else "",
            f"Camera: {self.components.camera}" if self.components.camera else "",
            f"Composition: {self.scene.shot_type} shot, {self.scene.camera_angle}" if self.scene.shot_type else "",
            f"Ambiance: {self.components.ambiance}" if self.components.ambiance else "",
            f"Audio: {self.components.audio}" if self.components.audio else "",
            f"Style: {self.components.style}" if self.components.style else ""
        ]
        
        # Filter out empty components
        components = [c for c in components if c]
        
        self.current_prompt["prompt"] = ". ".join(components)
        
        # Auto-generate caption
        if self.components.subject and self.components.action:
            words = f"{self.components.subject} {self.components.action}".split()[:8]
            self.current_prompt["caption"] = " ".join(words)
        
        # Auto-generate filename
        scene_type = self.scene.shot_type.replace("-", "").replace(" ", "")
        time_suffix = self.scene.time_of_day
        self.current_prompt["file_name"] = f"{scene_type}-{time_suffix}.mp4"

    def display_final_output(self):
        print("\n📋 GENERATED VEO3 JSON PROMPT")
        print("=" * 50)
        
        json_output = json.dumps(self.current_prompt, indent=2)
        print(json_output)
        
        print("\n💡 AUDIO GENERATION TIPS:")
        print("   ✓ Dialogue syntax: Character says: \"dialogue\" (colon prevents subtitles)")
        print("   ✓ Layer sounds: ambient + effects + music")
        print("   ✓ Be explicit about audio to prevent hallucinations")
        
        print("\n🎬 CAMERA & LIGHTING ANALYSIS:")
        self.display_lens_guide(self.scene.camera_fov)
        print(f"   Scene mood: {self.scene.lighting_type} {self.scene.time_of_day} lighting")
        print(f"   Weather atmosphere: {self.scene.weather}")
        
        # Save to file
        with open("veo3_prompt.json", "w") as f:
            json.dump(self.current_prompt, f, indent=2)
        print(f"\n💾 JSON saved to: veo3_prompt.json")

    def run(self):
        self.display_welcome()
        
        try:
            # Scene configuration
            self.configure_scene()
            
            # Prompt building
            self.build_prompt_components()
            
            # Generate final prompt
            self.build_final_prompt()
            
            # Display output
            self.display_final_output()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Your progress has been saved.")
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    app = Veo3PromptBuilder()
    app.run()