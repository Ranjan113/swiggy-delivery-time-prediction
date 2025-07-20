# Vercel API entry point for hybrid app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app_hybrid import app

# This is the entry point for Vercel
