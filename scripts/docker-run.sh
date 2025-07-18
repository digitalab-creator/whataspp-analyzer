#!/bin/bash

# 🏴‍☠️ Docker Run Script for Communication Analyzer
# By the grace of the Flying Spaghetti Monster! 🍝

set -e

echo "🏴‍☠️ Setting up Communication Analyzer Docker container..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
mkdir -p google-drive
mkdir -p credentials

echo "📁 Created directories:"
echo "  - google-drive/ (for Google Drive files)"
echo "  - credentials/ (for API credentials)"

echo ""
echo "📋 Please ensure you have the following files in place:"
echo "  - google-drive/My Drive/AI lawsuit project/legal-cases-9230f33b39a5-service-account.json"
echo "  - google-drive/My Drive/WhatsApp Chat with מיכל ט.txt"
echo "  - google-drive/My Drive/AI lawsuit project/token.pickle"
echo "  - google-drive/My Drive/AI lawsuit project/auth-client-secret.json"

echo ""
echo "🐳 Building Docker image..."
docker-compose build

echo ""
echo "🚀 Starting container..."
echo "Note: The container will run in interactive mode to handle Gmail authentication prompts"
echo "Press Ctrl+C to stop the container when done"
docker-compose up

echo ""
echo "✅ Container stopped. Check the output above for analysis results!" 