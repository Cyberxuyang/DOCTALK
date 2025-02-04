import re
import logging

logger = logging.getLogger(__name__)

def clean_answer(text: str) -> str:
    """
    Clean and format the model's response text
    """
    try:
        # Remove any special tokens
        text = text.replace("</s>", "").replace("<s>", "")
        
        # Remove "Answer:" prefix if present
        text = text.replace("Answer:", "").strip()
        
        # Remove everything after </think> tag
        if "</think>" in text:
            text = text.split("</think>")[0].strip()
            
        # Remove <think> tag if present
        text = text.replace("<think>", "").strip()
        
        # Remove multiple newlines and spaces
        text = " ".join(text.split())
        
        # Extract complete sentences
        pattern = r'([^.!?]*[.!?])'
        matches = re.findall(pattern, text)
        if matches:
            text = ' '.join(matches).strip()
        
        return text
    except Exception as e:
        logger.error(f"Error in clean_answer: {str(e)}")
        return text  # Return original text if cleaning fails
