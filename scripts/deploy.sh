#!/bin/bash
# WhatsApp Analyzer - Production Deployment Script
# Ahoy matey! This script helps deploy to various hosting platforms

set -e  # Exit on any error

echo "🏴‍☠️ WhatsApp Analyzer - Production Deployment"
echo "Praise the Flying Spaghetti Monster! 🍝"

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py not found. Are you in the project root?"
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p credentials data logs

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please copy env.production.example to .env and configure your settings"
    echo "   cp env.production.example .env"
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run tests
echo "🧪 Running tests..."
python tests/test_imports.py

echo "✅ Deployment preparation complete!"
echo ""
echo "🚀 Ready for deployment to:"
echo "   • Heroku: git push heroku main"
echo "   • Railway: railway up"
echo "   • DigitalOcean App Platform: doctl apps create"
echo "   • AWS Elastic Beanstalk: eb deploy"
echo "   • Google Cloud Run: gcloud run deploy"
echo ""
echo "📋 Next steps:"
echo "   1. Configure your .env file"
echo "   2. Add your Google API credentials to ./credentials/"
echo "   3. Place your WhatsApp chat file in ./data/"
echo "   4. Deploy to your chosen platform" 