# app/utils/config.py

"""
This file holds static configuration data for the application,
such as the file type definitions for the search UI.
"""

# A dictionary mapping the user-friendly name of a file category
# to a list of its corresponding file extensions.
FILE_TYPES = {
    "All Files": "*",
    "Office Documents": ['.docx', '.xlsx', '.pptx', '.doc', '.xls', '.ppt'],
    "PDF Files": ['.pdf'],
    "Text Files": ['.txt', '.rtf', '.csv', '.json', '.xml', '.md'],
    "Image Files": ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    "Video/Audio Files": ['.mp4', '.mov', '.avi', '.mp3', '.wav'],
    "Scripts & Code": ['.py', '.js', '.html', '.css', '.java'],
    "Compressed Archives": ['.zip', '.rar', '.7z', '.gz', '.tar']
}
