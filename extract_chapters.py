#!/usr/bin/env python3
"""Extract individual chapters from Draft 25 to separate text files."""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

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
        return f"Error: {e}"

def main():
    base_dir = '/home/user/robindynamo/Draft 25'
    output_dir = '/home/user/sbaum4853/chapters'

    os.makedirs(output_dir, exist_ok=True)

    # Get numbered chapter files
    chapter_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.docx') and not file.startswith('~$'):
                match = re.match(r'^(\d+)\s*-\s*(.+)\.docx$', file)
                if match:
                    chapter_num = int(match.group(1))
                    chapter_title = match.group(2)
                    full_path = os.path.join(root, file)
                    chapter_files.append((chapter_num, chapter_title, full_path, file))

    chapter_files.sort(key=lambda x: x[0])

    for chapter_num, chapter_title, filepath, filename in chapter_files:
        text = extract_text_from_docx(filepath)
        output_file = os.path.join(output_dir, f'chapter_{chapter_num:02d}.txt')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"CHAPTER {chapter_num}: {chapter_title}\n")
            f.write(f"File: {filename}\n")
            f.write("=" * 80 + "\n\n")
            f.write(text)

        print(f"Extracted Chapter {chapter_num}: {chapter_title}")

    # Also extract outline
    outline_path = os.path.join(base_dir, 'outline chapter by chapter.docx')
    if os.path.exists(outline_path):
        text = extract_text_from_docx(outline_path)
        output_file = os.path.join(output_dir, 'outline.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("OUTLINE CHAPTER BY CHAPTER\n")
            f.write("=" * 80 + "\n\n")
            f.write(text)
        print("Extracted outline")

if __name__ == '__main__':
    main()
