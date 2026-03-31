import os
import json
import urllib.parse
from datetime import datetime

h_dirs = [
    r"C:\Users\SHIVANI\AppData\Roaming\Code\User\History", 
    r"C:\Users\SHIVANI\AppData\Roaming\Cursor\User\History"
]

target_dir = r"d:\hospital"
restored_count = 0

for h_dir in h_dirs:
    if os.path.exists(h_dir):
        for folder in os.listdir(h_dir):
            entries_path = os.path.join(h_dir, folder, 'entries.json')
            if os.path.exists(entries_path):
                try:
                    with open(entries_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    resource_uri = data.get('resource', '')
                    # Need to parse this because it's encoded like file:///d%3A/hospital/...
                    if resource_uri.startswith('file://'):
                        # convert file:///d%3A/hospital/xxx to d:\hospital\xxx
                        resource_path = urllib.parse.unquote(resource_uri[7:]) # remove file://
                        
                        # Fix drive letter mapping (d%3A -> d:)
                        if resource_path.startswith('/'):
                            resource_path = resource_path[1:] # remove leading slash in windows
                        
                        # normalize path
                        resource_path = os.path.normpath(resource_path)
                        
                        # Check if it belongs to our target directory
                        if resource_path.lower().startswith(target_dir.lower()):
                            # It belongs! Check if it's missing or empty
                            if not os.path.exists(resource_path) or os.path.getsize(resource_path) == 0:
                                entries = data.get('entries', [])
                                if entries:
                                    # Get the most recent entry
                                    latest_entry = max(entries, key=lambda e: e.get('timestamp', 0))
                                    entry_id = latest_entry.get('id')
                                    entry_file_path = os.path.join(h_dir, folder, entry_id)
                                    
                                    if os.path.exists(entry_file_path):
                                        source_size = os.path.getsize(entry_file_path)
                                        if source_size > 5:
                                            # We have a valid backup! Let's restore it
                                            # Create directories if they don't exist
                                            os.makedirs(os.path.dirname(resource_path), exist_ok=True)
                                            with open(entry_file_path, 'r', encoding='utf-8') as src, \
                                                 open(resource_path, 'w', encoding='utf-8') as dst:
                                                dst.write(src.read())
                                            print(f"Restored: {resource_path}")
                                            restored_count += 1
                except Exception as e:
                    # ignore errors processing individual histories
                    pass

print(f"Total files restored: {restored_count}")
