"""
Resume Auto-Fetcher Module - CLEAN CODE
Fetches resumes from cloud storage links
"""

import os
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Directories
FETCHED_RESUMES_DIR = "fetched_resumes"
os.makedirs(FETCHED_RESUMES_DIR, exist_ok=True)

# HTTP Headers
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


class ResumeFetcher:
    """Fetches resumes from various URL sources"""
    
    @staticmethod
    def get_file_extension(url, content_type=None):
        """Extract file extension from URL or content-type"""
        path = urlparse(url).path.lower()
        
        if path.endswith('.pdf'):
            return '.pdf'
        elif path.endswith('.docx'):
            return '.docx'
        elif path.endswith('.doc'):
            return '.doc'
        elif path.endswith('.txt'):
            return '.txt'
        
        if content_type:
            if 'pdf' in content_type:
                return '.pdf'
            elif 'word' in content_type or 'docx' in content_type:
                return '.docx'
            elif 'text' in content_type:
                return '.txt'
        
        return '.pdf'
    
    @staticmethod
    def fetch_from_google_drive(url):
        """Fetch from Google Drive"""
        try:
            if 'drive.google.com' not in url:
                return {'status': 'error', 'message': 'Invalid Google Drive URL'}
            
            file_id = None
            if '/d/' in url:
                file_id = url.split('/d/')[1].split('/')[0]
            elif 'id=' in url:
                file_id = parse_qs(urlparse(url).query).get('id', [None])[0]
            
            if not file_id:
                return {'status': 'error', 'message': 'Cannot extract file ID'}
            
            download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
            response = requests.get(download_url, headers=HEADERS, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            extension = ResumeFetcher.get_file_extension(url, response.headers.get('content-type'))
            
            return {
                'status': 'success',
                'content': response.content,
                'filename': f'resume_{datetime.now().strftime("%Y%m%d_%H%M%S")}{extension}',
                'size': len(response.content)
            }
        except Exception as e:
            return {'status': 'error', 'message': f'Google Drive error: {str(e)}'}
    
    @staticmethod
    def fetch_from_dropbox(url):
        """Fetch from Dropbox"""
        try:
            if 'dropbox.com' not in url:
                return {'status': 'error', 'message': 'Invalid Dropbox URL'}
            
            if '?dl=0' in url:
                download_url = url.replace('?dl=0', '?dl=1')
            elif '?dl=1' not in url:
                download_url = url + '?dl=1'
            else:
                download_url = url
            
            response = requests.get(download_url, headers=HEADERS, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            extension = ResumeFetcher.get_file_extension(url, response.headers.get('content-type'))
            
            return {
                'status': 'success',
                'content': response.content,
                'filename': f'resume_{datetime.now().strftime("%Y%m%d_%H%M%S")}{extension}',
                'size': len(response.content)
            }
        except Exception as e:
            return {'status': 'error', 'message': f'Dropbox error: {str(e)}'}
    
    @staticmethod
    def fetch_from_onedrive(url):
        """Fetch from OneDrive"""
        try:
            if 'onedrive.live.com' not in url and 'sharepoint.com' not in url:
                return {'status': 'error', 'message': 'Invalid OneDrive URL'}
            
            if '?e=' in url:
                download_url = url.split('?e=')[0] + '?download=1'
            else:
                download_url = url + '?download=1'
            
            response = requests.get(download_url, headers=HEADERS, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            extension = ResumeFetcher.get_file_extension(url, response.headers.get('content-type'))
            
            return {
                'status': 'success',
                'content': response.content,
                'filename': f'resume_{datetime.now().strftime("%Y%m%d_%H%M%S")}{extension}',
                'size': len(response.content)
            }
        except Exception as e:
            return {'status': 'error', 'message': f'OneDrive error: {str(e)}'}
    
    @staticmethod
    def fetch_from_direct_link(url):
        """Fetch from direct download link"""
        try:
            response = requests.get(url, headers=HEADERS, timeout=30, allow_redirects=True)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type', '')
            extension = ResumeFetcher.get_file_extension(url, content_type)
            
            return {
                'status': 'success',
                'content': response.content,
                'filename': f'resume_{datetime.now().strftime("%Y%m%d_%H%M%S")}{extension}',
                'size': len(response.content)
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
    
    @staticmethod
    def fetch_from_url(url):
        """Auto-detect source and fetch"""
        url = url.strip()
        
        if not url:
            return {'status': 'error', 'message': 'Empty URL'}
        
        if not url.startswith(('http://', 'https://')):
            return {'status': 'error', 'message': 'URL must start with http:// or https://'}
        
        if 'drive.google.com' in url:
            return ResumeFetcher.fetch_from_google_drive(url)
        elif 'dropbox.com' in url:
            return ResumeFetcher.fetch_from_dropbox(url)
        elif 'onedrive.live.com' in url or 'sharepoint.com' in url:
            return ResumeFetcher.fetch_from_onedrive(url)
        else:
            return ResumeFetcher.fetch_from_direct_link(url)
    
    @staticmethod
    def validate_content(content):
        """Validate if content is a valid document"""
        if len(content) < 100:
            return False, "File too small"
        
        if content.startswith(b'%PDF'):
            return True, "Valid PDF"
        
        if content.startswith(b'PK'):
            return True, "Valid DOCX"
        
        try:
            content.decode('utf-8')
            if len(content) > 200:
                return True, "Valid text"
        except:
            pass
        
        return False, "Invalid format"
    
    @staticmethod
    def save_resume(content, filename):
        """Save resume to disk"""
        try:
            filepath = os.path.join(FETCHED_RESUMES_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(content)
            return {'status': 'success', 'filepath': filepath}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}