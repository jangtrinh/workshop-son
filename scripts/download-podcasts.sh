#!/bin/bash
# Download NotebookLM podcast audio for each workshop level
# Run this script after audio generation completes (~5-30 minutes)

set -e

AUDIO_DIR="/Users/jang/Desktop/Jang/tai-lieu/workshop-son/audio"
mkdir -p "$AUDIO_DIR"

echo "📥 Downloading Workshop Audio..."
echo ""

# Level 1 — Understand
echo "🎧 Level 1: Understand..."
notebooklm use df3320a7-70dd-48fe-b3d7-41a70efe3baa
notebooklm download audio "$AUDIO_DIR/podcast-level-1-understand.mp3" && echo "  ✅ Downloaded" || echo "  ⏳ Not ready yet — try again later"
echo ""

# Level 2 — Customize
echo "🎧 Level 2: Customize..."
notebooklm use 2d4aca28-21ff-44ed-b351-2658abd4e15b
notebooklm download audio "$AUDIO_DIR/podcast-level-2-customize.mp3" && echo "  ✅ Downloaded" || echo "  ⏳ Not ready yet — try again later"
echo ""

# Level 3 — Build
echo "🎧 Level 3: Build..."
notebooklm use 956f7237-91e4-49b8-8387-c397d2141ab7
notebooklm download audio "$AUDIO_DIR/podcast-level-3-build.mp3" && echo "  ✅ Downloaded" || echo "  ⏳ Not ready yet — try again later"
echo ""

echo "📂 Output: $AUDIO_DIR"
ls -lah "$AUDIO_DIR"/*.mp3 2>/dev/null || echo "No MP3 files found yet."
