#!/usr/bin/env python3
"""
Baker Street Laboratory - Image Generation API
Generates psychedelic detective art using Stable Diffusion WebUI API
"""

import requests
import json
import base64
import argparse
import yaml
from pathlib import Path

class BakerStreetImageGenerator:
    def __init__(self, webui_url="http://localhost:7860"):
        self.webui_url = webui_url
        self.config = self.load_config()
    
    def load_config(self):
        config_path = Path("$SCRIPT_DIR/../config/image-generation/baker-street-prompts.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def generate_image(self, scene_type, style="amphetamemes", custom_prompt=""):
        """Generate an image based on scene type and style"""
        
        # Get base style
        base_style = self.config.get("base_styles", {}).get(style, {})
        
        # Get scene prompt
        scene_config = self.config.get("scene_types", {}).get(scene_type, {})
        scene_prompt = scene_config.get("prompt", custom_prompt)
        
        # Format prompt with style
        full_prompt = scene_prompt.format(base_style=base_style.get("positive", ""))
        
        # API payload
        payload = {
            "prompt": full_prompt,
            "negative_prompt": base_style.get("negative", ""),
            "steps": self.config.get("settings", {}).get("default_steps", 30),
            "cfg_scale": self.config.get("settings", {}).get("default_cfg_scale", 7.5),
            "width": self.config.get("settings", {}).get("default_width", 768),
            "height": self.config.get("settings", {}).get("default_height", 768),
            "sampler_name": self.config.get("settings", {}).get("default_sampler", "DPM++ 2M Karras"),
        }
        
        try:
            response = requests.post(f"{self.webui_url}/sdapi/v1/txt2img", json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Save image
            if result.get("images"):
                image_data = base64.b64decode(result["images"][0])
                output_path = Path(f"$SCRIPT_DIR/../output/images/{scene_type}_{style}.png")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                print(f"✅ Image generated: {output_path}")
                return str(output_path)
            else:
                print("❌ No image generated")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description="Generate Baker Street Laboratory images")
    parser.add_argument("scene_type", help="Type of scene to generate")
    parser.add_argument("--style", default="amphetamemes", help="Art style to use")
    parser.add_argument("--custom-prompt", help="Custom prompt override")
    
    args = parser.parse_args()
    
    generator = BakerStreetImageGenerator()
    result = generator.generate_image(args.scene_type, args.style, args.custom_prompt)
    
    if result:
        print(f"🎨 Generated image: {result}")
    else:
        print("❌ Failed to generate image")

if __name__ == "__main__":
    main()
