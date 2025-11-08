"""
Vercel serverless function entry point for FastAPI application.
"""
import sys
import os

# Add parent directory to path to import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mangum import Mangum
from main import app

# Wrap FastAPI app with Mangum to make it compatible with AWS Lambda/Vercel
handler = Mangum(app, lifespan="off")

