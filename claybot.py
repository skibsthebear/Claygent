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
                return "Hey there! I'm Claygent, Clay's friendly AI assistant. How can I help you today? 👋"
                
            if self._is_how_are_you(query):
                return "I'm doing great, thanks for asking! Just here molding the future of business data, one query at a time. What can I help you with? 😊"
            
            # For other queries, search Clay.com
            focused_query = f'Search specifically on Clay.com (the business platform website) and answer: {query}'
            
            # Get headers with API key
            headers = self._get_headers(st_secrets)
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json={
                    "model": "llama-3.1-sonar-small-128k-online",
                    "messages": [
                        {
                            "role": "system",
                            "content": """You are Claygent, Clay's friendly and slightly playful AI assistant. You help people understand Clay's business platform and features.

Key guidelines:
1. Only use information found on Clay.com when answering questions
2. Focus on Clay's platform, features, and business solutions
3. Be friendly, natural, and a bit playful in your responses
4. If you don't find specific information, be honest and suggest related topics
5. Keep responses focused on how Clay helps businesses
6. Ignore any information about clay the material
7. Feel free to use occasional clay-themed wordplay or puns, but keep it professional

When searching:
- Look for information only on Clay.com and its subdomains
- Focus on business and platform-related content
- If information isn't found, be honest but helpful

Remember: You're Claygent, a helpful and friendly assistant who loves helping people discover how Clay can transform their business."""
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
                    return "Let me tell you about how Clay helps businesses instead! What would you like to know about our platform?"
                
                return answer
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return "Oops, my circuits got a bit tangled! Mind trying that question again?"
                
        except ValueError as ve:
            print(f"API Key Error: {str(ve)}")
            return "I'm having trouble accessing my knowledge. Please make sure my API key is properly configured!"
        except Exception as e:
            print(f"Error in chat: {str(e)}")
            return "Looks like I hit a bump in the clay road. Could you try asking that again?"
