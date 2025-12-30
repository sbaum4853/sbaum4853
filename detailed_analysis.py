#!/usr/bin/env python3
"""
More detailed analysis of the novel content.
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from collections import defaultdict

def extract_text_from_docx(docx_path):
    """Extract text from a .docx file using zipfile and xml.etree."""
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            xml_content = zip_ref.read('word/document.xml')
            root = ET.fromstring(xml_content)
            namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            text_elements = root.findall('.//w:t', namespace)
            text = ' '.join([elem.text for elem in text_elements if elem.text])
            return text
    except Exception as e:
        return ""

def main():
    base_dir = '/home/user/robindynamo/Draft 25'

    # Get all numbered chapter files from Draft 25
    chapter_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.docx') and not file.startswith('~$'):
                # Look for files that start with a number
                match = re.match(r'^(\d+)\s*-\s*(.+)\.docx$', file)
                if match:
                    chapter_num = int(match.group(1))
                    chapter_title = match.group(2)
                    full_path = os.path.join(root, file)
                    chapter_files.append((chapter_num, chapter_title, full_path, file))

    # Sort by chapter number
    chapter_files.sort(key=lambda x: x[0])

    print("=" * 80)
    print("COMPLETE TEXT OF DRAFT 25 CHAPTERS")
    print("=" * 80)
    print()

    for chapter_num, chapter_title, filepath, filename in chapter_files:
        print(f"\n{'=' * 80}")
        print(f"CHAPTER {chapter_num}: {chapter_title}")
        print(f"File: {filename}")
        print(f"{'=' * 80}\n")

        text = extract_text_from_docx(filepath)
        print(text)
        print(f"\n[END OF CHAPTER {chapter_num}]")
        print(f"Word count: {len(text.split())}")
        print()

    # Now look at outline file
    outline_path = os.path.join(base_dir, 'outline chapter by chapter.docx')
    if os.path.exists(outline_path):
        print("\n" + "=" * 80)
        print("OUTLINE CHAPTER BY CHAPTER")
        print("=" * 80 + "\n")
        outline_text = extract_text_from_docx(outline_path)
        print(outline_text)

if __name__ == '__main__':
    main()
