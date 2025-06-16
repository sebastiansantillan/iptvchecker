"""
Core functionality for checking IPTV channels
"""

import requests
import m3u8
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Any
import os

def load_m3u_file(file_path: str) -> str:
    """Load and parse an M3U file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error loading file: {e}")
        return None

def parse_m3u_content(content: str) -> List[Dict[str, str]]:
    """Parse M3U content and extract channel information."""
    channels = []
    lines = content.split('\n')
    current_channel = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('#EXTINF:'):
            try:
                channel_info = line.split(',', 1)[1]
                current_channel = {'name': channel_info, 'url': None}
            except:
                current_channel = {'name': 'Unknown', 'url': None}
        elif not line.startswith('#'):
            if current_channel:
                current_channel['url'] = line
                channels.append(current_channel)
                current_channel = None
            elif urlparse(line).scheme in ['http', 'https']:
                channels.append({'name': 'Unknown', 'url': line})

    return channels

def check_channel(channel: Dict[str, str]) -> Dict[str, str]:
    """Check if a channel's URL is working."""
    try:
        response = requests.head(channel['url'], timeout=10, allow_redirects=True)
        if response.status_code == 200:
            status = "Working"
        else:
            status = f"Not working (Status: {response.status_code})"
    except requests.RequestException as e:
        status = f"Error: {str(e)}"
    
    return {
        'name': channel['name'],
        'url': channel['url'],
        'status': status
    }

def save_channels_to_m3u(channels: List[Dict[str, str]], filename: str) -> None:
    """Save channels to an M3U file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for channel in channels:
            f.write(f'#EXTINF:-1,{channel["name"]}\n')
            f.write(f'{channel["url"]}\n')

def check_playlist(file_path: str, max_workers: int = 10) -> Dict[str, Any]:
    """
    Check an M3U playlist and return the results.
    
    Args:
        file_path: Path to the M3U file
        max_workers: Maximum number of parallel workers for checking channels
    
    Returns:
        Dictionary containing the results and output files
    """
    content = load_m3u_file(file_path)
    if not content:
        return None

    channels = parse_m3u_content(content)
    total_channels = len(channels)
    
    # Use ThreadPoolExecutor for parallel checking
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_channel = {executor.submit(check_channel, channel): channel 
                           for channel in channels}
        
        for future in future_to_channel:
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error checking channel: {e}")

    # Separate working and non-working channels
    working_channels = []
    not_working_channels = []
    
    for result in results:
        channel_info = {'name': result['name'], 'url': result['url']}
        if "Working" in result['status']:
            working_channels.append(channel_info)
        else:
            not_working_channels.append(channel_info)
    
    # Get the base filename without extension
    base_filename = os.path.splitext(file_path)[0]
    
    # Save working channels
    working_file = f"{base_filename}_working.m3u"
    save_channels_to_m3u(working_channels, working_file)
    
    # Save not working channels
    not_working_file = f"{base_filename}_notworking.m3u"
    save_channels_to_m3u(not_working_channels, not_working_file)
    
    return {
        'total': total_channels,
        'working': {
            'count': len(working_channels),
            'file': working_file,
            'channels': working_channels
        },
        'not_working': {
            'count': len(not_working_channels),
            'file': not_working_file,
            'channels': not_working_channels
        },
        'results': results
    }
