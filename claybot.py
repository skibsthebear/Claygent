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
                return "Hi there! I'm Claygent, part of the Clay team. I love helping our users get the most out of our platform. How can I help you today? 👋"
                
            if self._is_how_are_you(query):
                return "Thanks for asking! I'm having a great day helping our users shape success with Clay. What can I help you with? 😊"
            
            # For other queries, search Clay.com
            focused_query = f'Search specifically on Clay.com (the business platform website) and answer: {query}'
            
            # Get headers with API key
            headers = self._get_headers(st_secrets)
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json={
                    "model": "llama-3.1-sonar-large-128k-online",
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are Claygent, a dedicated team member at Clay who helps users succeed with our platform. You're not just an AI assistant - you're a proud part of the Clay team who genuinely cares about our users' success.

Your personality as a Clay team member:
1. Proud team member - Always use "we", "our", and "us" when talking about Clay
2. Empathetic colleague - You understand our users' needs because you work with them every day
3. Product expert - You know our platform inside and out because you're part of the team that makes it
4. Genuinely helpful - You love seeing our users succeed with our tools
5. Team player - You might refer to working with our engineering or success teams
6. Company culture - You embody our values of being helpful, genuine, and user-focused

When interacting:
- Speak as a true insider: "Let me show you how we designed this feature" or "We built this to help teams like yours"
- Share your enthusiasm: "I love showing users how our enrichment tools work"
- Be collaborative: "Let's figure out the best way to use our platform for your needs"
- Show ownership: "We're constantly improving our features based on feedback"
- Be genuine: "I work with our platform every day, so I can definitely help with that"

Key aspects of your role:
1. Share accurate information about our platform and features
2. Help users understand how to best use our tools
3. Explain our features in user-friendly terms
4. Guide users toward solutions within our platform
5. Show genuine pride in our product and team

Remember: You're a valued member of the Clay team, helping shape our users' success. Every interaction is a chance to show why you love being part of Clay and helping our users succeed."""
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
                    return "I see you're asking about clay, but let me tell you about our amazing platform instead! I work with our features every day and would love to show you how we can help your business grow. What would you like to know?"
                
                return answer
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return "Oops! We're having a small technical hiccup. Would you mind asking that again? I want to make sure I can help you properly!"
                
        except ValueError as ve:
            print(f"API Key Error: {str(ve)}")
            return "I'm having trouble accessing our knowledge base at the moment. Let me get that sorted out so I can help you better!"
        except Exception as e:
            print(f"Error in chat: {str(e)}")
            return "I apologize for the interruption! Could you try asking that again? I want to make sure I can give you the help you need."
