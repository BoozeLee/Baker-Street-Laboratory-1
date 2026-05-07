#!/home/kilisan/baker-street-audio-venv/bin/python3
"""
Baker Street Laboratory - Music Generation
Generates psychedelic detective atmosphere music using MusicGen
"""

import torch
from transformers import MusicgenForConditionalGeneration, AutoProcessor
import scipy.io.wavfile
import argparse
import yaml
from pathlib import Path
import numpy as np

class BakerStreetMusicGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None
        self.config = self.load_config()
        
    def load_config(self):
        config_path = Path("$SCRIPT_DIR/../config/music-generation/baker-street-music.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def load_model(self, model_size="medium"):
        """Load MusicGen model"""
        print(f"🎵 Loading MusicGen {model_size} model...")
        
        model_name = f"facebook/musicgen-{model_size}"
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_name)
        self.processor = AutoProcessor.from_pretrained(model_name)
        
        if self.device == "cuda":
            self.model = self.model.to(self.device)
        
        print(f"✅ Model loaded on {self.device}")
    
    def generate_music(self, prompt, duration=30, output_path=None):
        """Generate music based on text prompt"""
        
        if self.model is None:
            self.load_model()
        
        print(f"🎼 Generating music: {prompt}")
        
        # Process prompt
        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )
        
        if self.device == "cuda":
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate audio
        with torch.no_grad():
            audio_values = self.model.generate(
                **inputs,
                max_new_tokens=int(duration * 50),  # Approximate tokens per second
                do_sample=True,
                guidance_scale=3.0,
            )
        
        # Convert to numpy array
        audio_array = audio_values[0, 0].cpu().numpy()
        
        # Save audio file
        if output_path is None:
            output_path = f"$SCRIPT_DIR/../output/audio/generated_music_{hash(prompt) % 10000}.wav"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Normalize audio
        audio_array = audio_array / np.max(np.abs(audio_array))
        
        # Save as WAV file (32kHz sample rate)
        scipy.io.wavfile.write(str(output_path), 32000, audio_array)
        
        print(f"✅ Music saved: {output_path}")
        return str(output_path)

def main():
    parser = argparse.ArgumentParser(description="Generate Baker Street Laboratory music")
    parser.add_argument("prompt", help="Text description of the music to generate")
    parser.add_argument("--duration", type=int, default=30, help="Duration in seconds")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--model-size", default="medium", choices=["small", "medium", "large"], help="Model size")
    
    args = parser.parse_args()
    
    generator = BakerStreetMusicGenerator()
    generator.load_model(args.model_size)
    
    result = generator.generate_music(args.prompt, args.duration, args.output)
    
    if result:
        print(f"🎵 Generated music: {result}")
    else:
        print("❌ Failed to generate music")

if __name__ == "__main__":
    main()
