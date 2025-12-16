import google.generativeai as genai
from django.conf import settings
from openai import OpenAI
import environ



genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")  

