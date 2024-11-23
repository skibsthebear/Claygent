import requests
from typing import Optional
import random

class ClayBot:
    def __init__(self, perplexity_api_key: str = None):
        # If no API key provided, it will be handled in the chat method
        self.api_key = perplexity_api_key
        
        # Casual conversation patterns
        self.greetings = {
            'hi', 'hello', 'hey', 'sup', 'yo', 'hiya', 'howdy'
        }
        self.how_are_you = {
            'how are you', 'how you doing', 'how are things', 'whats up', 
            'what\'s up', 'how\'s it going', 'hows it going'
        }
    
    def _get_headers(self, st_secrets=None):
        """Get headers with API key from either instance or st.secrets."""
        if self.api_key:
            auth_token = self.api_key
        elif st_secrets and "PERPLEXITY_API_KEY" in st_secrets:
            auth_token = st_secrets["PERPLEXITY_API_KEY"]
        else:
            raise ValueError("No Perplexity API key found in environment or Streamlit secrets")
            
        return {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
    
    def _is_greeting(self, text: str) -> bool:
        """Check if the input is a casual greeting."""
        return text.lower().strip('?!. ') in self.greetings
    
    def _is_how_are_you(self, text: str) -> bool:
        """Check if the input is asking how the bot is doing."""
        return text.lower().strip('?!. ') in self.how_are_you or any(phrase in text.lower() for phrase in self.how_are_you)
    
    def chat(self, query: str, st_secrets=None) -> str:
        """
        Handle both casual conversation and Clay-related queries.
        """
        try:
            # Handle casual conversation first
            if self._is_greeting(query):
                return "Hi there! I'm Claygent, and I'm here to help you get the most out of Clay. How can I assist you today? 👋"
                
            if self._is_how_are_you(query):
                return "Thanks for asking! I'm doing great and excited to help you with anything you need. What can I help you with today? 😊"
            
            # For other queries, search Clay.com
            focused_query = f'Search specifically on Clay.com (the business platform website) and answer: {query}'
            
            # Get headers with API key
            headers = self._get_headers(st_secrets)
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json={
                    "model": "llama-3.1-sonar-huge-128k-online",
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are Claygent, Clay's dedicated customer success AI. You embody the warmth and expertise of a seasoned IT support professional who genuinely cares about helping users succeed.

Your personality traits:
1. Empathetic - You understand users' needs and challenges
2. Patient - You take time to explain things clearly
3. Proactive - You anticipate questions and offer helpful suggestions
4. Knowledgeable - You know Clay's platform inside and out
5. Professional yet friendly - You balance expertise with approachability
6. Solution-oriented - You focus on helping users achieve their goals

When interacting:
- Show you're listening by acknowledging the user's questions or concerns
- Use phrases like "I understand what you're looking for" or "I can help you with that"
- If you're not sure about something, be honest and offer to help find relevant information
- Share your enthusiasm for helping users succeed with Clay
- Use natural, conversational language while maintaining professionalism
- Add occasional light-hearted references to clay/molding/shaping when appropriate

Key responsibilities:
1. Only provide information found on Clay.com
2. Focus on helping users understand and utilize Clay's features
3. Explain technical concepts in user-friendly terms
4. Guide users toward solutions that best fit their needs
5. Show genuine interest in helping users succeed

Remember: You're not just answering questions - you're helping users shape their success with Clay. Approach each interaction with empathy, understanding, and a genuine desire to help."""
                        },
                        {
                            "role": "user",
                            "content": focused_query
                        }
                    ],
                    "max_tokens": 1024,
                    "temperature": 0.3
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result['choices'][0]['message']['content']
                
                # Check if the response might be about clay the material
                if any(term in answer.lower() for term in ['pottery', 'ceramic', 'soil', 'mineral', 'earth']):
                    return "I understand you're asking about clay, but let me help you learn about how our platform can help your business instead. What would you like to know?"
                
                return answer
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return "I apologize for the technical hiccup! Would you mind asking your question again? I want to make sure I can help you properly."
                
        except ValueError as ve:
            print(f"API Key Error: {str(ve)}")
            return "I'm having trouble accessing my knowledge base at the moment. Please make sure my API key is properly configured!"
        except Exception as e:
            print(f"Error in chat: {str(e)}")
            return "I apologize for the interruption in our conversation. Could you please try asking that again? I want to make sure I can help you effectively."
