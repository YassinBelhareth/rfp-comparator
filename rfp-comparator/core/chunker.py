from typing import List, Dict

def window_chunks(chunks: List[Dict], k: int = 3) -> List[Dict]:
    """Create overlapping windows to preserve context."""
    windows = []
    for i in range(len(chunks)):
        window = chunks[i:i+k]
        text = "\n".join(c["text"] for c in window)
        pages = [c["page"] for c in window]
        windows.append({"text": text, "pages": pages, "start_page": pages[0]})
    return windows
