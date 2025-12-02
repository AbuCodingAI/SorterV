#!/bin/bash

# Sorter - Git Setup & Push Script
# Usage: bash setup.sh <github-repo-url>

echo "=========================================="
echo "Sorter - Git Setup & Push"
echo "=========================================="
echo ""

# Check if repo URL provided
if [ -z "$1" ]; then
    echo "Usage: bash setup.sh <github-repo-url>"
    echo "Example: bash setup.sh https://github.com/your-username/Sorter.git"
    exit 1
fi

REPO_URL=$1

echo "Setting up Git repository..."
echo ""

# Configure git
git config user.name "Sorter Developer"
git config user.email "dev@sorter.local"

# Add all files
echo "Adding files..."
git add .

# Create initial commit
echo "Creating initial commit..."
git commit -m "Initial commit: Sorter v1.0.0

- Keyword Sorter: Search files by keyword
- TimeSort: Find files not accessed in X days
- SmartSort: Intelligent file organization
- Modern glossy UI with PyQt6
- Python API and PowerShell CLI
- Web download page for Vercel/Netlify/Surge"

# Add remote
echo "Adding remote repository..."
git remote add origin "$REPO_URL"

# Push to main branch
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "✓ Successfully pushed to GitHub!"
echo "Repository: $REPO_URL"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create a GitHub Release"
echo "2. Upload split files to release"
echo "3. Deploy web page to Vercel/Netlify"
echo ""
