# Vercel API entry point
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

# This is the entry point for Vercel
