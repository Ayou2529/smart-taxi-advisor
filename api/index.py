# api/index.py - Vercel Serverless Entry Point
# This file redirects all requests to the main Flask app

import os
import sys

# Add parent directory to path so we can import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

print(f"DEBUG: Root dir contents: {os.listdir(parent_dir)}", file=sys.stderr)
print(f"DEBUG: Current dir contents: {os.listdir(os.path.dirname(os.path.abspath(__file__)))}", file=sys.stderr)

from app import app

# Fix for Vercel: Explicitly set template folder to root
app.template_folder = parent_dir
app.static_folder = os.path.join(parent_dir, 'static')

# Vercel expects 'app' or 'application' to be the WSGI handler
application = app
