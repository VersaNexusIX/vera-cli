# utils/__init__.py
import os
import time

def get_next_filename(ext):
    timestamp = int(time.time())
    return f"vera_{timestamp}.{ext}"

def trigger_media_scan(filepath):
    os.system(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{os.path.abspath(filepath)}")