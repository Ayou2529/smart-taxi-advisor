# api/index.py - Vercel Serverless Entry Point
# This file redirects all requests to the main Flask app

import os
import sys

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects 'app' or 'application' to be the WSGI handler
application = app
