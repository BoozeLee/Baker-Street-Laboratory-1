#!/bin/bash

# Baker Street Laboratory - Audio Generation Examples
# Demonstrates various audio generation capabilities

echo "🎵 Baker Street Laboratory - Audio Examples"
echo "=========================================="

# Generate background music for different scenarios
echo "🎼 Generating background music..."

# Research session music
python3 scripts/generate-music.py \
    "ambient psychedelic music for focused research, dreamy synthesizers, laboratory atmosphere" \
    --duration 60 \
    --output "$SCRIPT_DIR/../output/audio/research_session.wav"

# Investigation music
python3 scripts/generate-music.py \
    "detective noir investigation music, mysterious jazz, urban night atmosphere" \
    --duration 45 \
    --output "$SCRIPT_DIR/../output/audio/investigation_theme.wav"

# Data analysis music
python3 scripts/generate-music.py \
    "rhythmic data analysis music, digital patterns, computational beats" \
    --duration 90 \
    --output "$SCRIPT_DIR/../output/audio/data_analysis.wav"

# Generate sound effects
echo "🔊 Generating sound effects..."

# Laboratory sounds
python3 scripts/generate-sound-effects.py \
    "laboratory equipment humming, scientific atmosphere" \
    --type sound \
    --output "$SCRIPT_DIR/../output/audio/lab_ambient.wav"

# Discovery sound
python3 scripts/generate-sound-effects.py \
    "eureka moment, breakthrough discovery chime" \
    --type sound \
    --output "$SCRIPT_DIR/../output/audio/discovery.wav"

# Generate speech examples
echo "🗣️  Generating speech examples..."

# Detective narration
python3 scripts/generate-sound-effects.py \
    "The investigation reveals fascinating patterns in the data, leading us deeper into the mystery." \
    --type speech \
    --voice "v2/en_speaker_6" \
    --output "$SCRIPT_DIR/../output/audio/detective_narration.wav"

# Research summary
python3 scripts/generate-sound-effects.py \
    "Analysis complete. The results show significant correlations in the psychedelic research data." \
    --type speech \
    --voice "v2/en_speaker_3" \
    --output "$SCRIPT_DIR/../output/audio/research_summary.wav"

echo "✅ Audio examples generated in output/audio/"
echo "🎧 Play the files to test the Baker Street Laboratory audio system!"
