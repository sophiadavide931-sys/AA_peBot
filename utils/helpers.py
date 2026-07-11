import re
import json
from typing import Dict, Any, Optional
from datetime import datetime

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def format_result(data: Any) -> str:
    """Format any data into readable output"""
    if isinstance(data, dict):
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif isinstance(data, list):
        return "\n".join([str(item) for item in data])
    return str(data)

def truncate_text(text: str, max_length: int = 4000) -> str:
    """Truncate text to Telegram's message limit"""
    if not text:
        return ""
    if len(text) > max_length:
        return text[:max_length - 100] + "\n\n... (Output truncated)"
    return text

def format_timestamp(timestamp: Optional[int] = None) -> str:
    """Format timestamp to readable date"""
    if timestamp:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def extract_domain(url: str) -> str:
    """Extract domain from URL"""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc or parsed.path
    except:
        return url
