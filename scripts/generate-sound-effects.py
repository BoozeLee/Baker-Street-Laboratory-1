#!/home/kilisan/baker-street-audio-venv/bin/python3
"""
Baker Street Laboratory - Sound Effects Generation
Generates sound effects and speech using Bark
"""

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import argparse
from pathlib import Path
import numpy as np

class BakerStreetSoundGenerator:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.models_loaded = False
    
    def load_models(self):
        """Load Bark models"""
        if not self.models_loaded:
            print("🔊 Loading Bark models...")
            preload_models()
            self.models_loaded = True
            print("✅ Bark models loaded")
    
    def generate_speech(self, text, voice_preset="v2/en_speaker_6", output_path=None):
        """Generate speech from text"""
        
        self.load_models()
        
        print(f"🗣️  Generating speech: {text[:50]}...")
        
        # Generate audio
        audio_array = generate_audio(text, history_prompt=voice_preset)
        
        # Save audio file
        if output_path is None:
            output_path = f"$SCRIPT_DIR/../output/audio/speech_{hash(text) % 10000}.wav"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Normalize and save
        audio_array = audio_array / np.max(np.abs(audio_array))
        write_wav(str(output_path), self.sample_rate, audio_array)
        
        print(f"✅ Speech saved: {output_path}")
        return str(output_path)
    
    def generate_sound_effect(self, description, output_path=None):
        """Generate sound effect from description"""
        
        # Use special sound effect prompts
        sound_prompt = f"[sound effect: {description}]"
        
        return self.generate_speech(sound_prompt, voice_preset="v2/en_speaker_9", output_path=output_path)

def main():
    parser = argparse.ArgumentParser(description="Generate Baker Street Laboratory sound effects")
    parser.add_argument("text", help="Text to convert to speech or sound effect description")
    parser.add_argument("--type", choices=["speech", "sound"], default="speech", help="Type of audio to generate")
    parser.add_argument("--voice", default="v2/en_speaker_6", help="Voice preset for speech")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    generator = BakerStreetSoundGenerator()
    
    if args.type == "speech":
        result = generator.generate_speech(args.text, args.voice, args.output)
    else:
        result = generator.generate_sound_effect(args.text, args.output)
    
    if result:
        print(f"🔊 Generated audio: {result}")
    else:
        print("❌ Failed to generate audio")

if __name__ == "__main__":
    main()
