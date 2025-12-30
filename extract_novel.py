#!/usr/bin/env python3
"""
Extract and analyze text from all .docx files in the robindynamo directory.
"""

import os
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from collections import defaultdict

def extract_text_from_docx(docx_path):
    """
    Extract text from a .docx file using zipfile and xml.etree.
    """
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            # Read the document.xml file which contains the main text
            xml_content = zip_ref.read('word/document.xml')

            # Parse the XML
            root = ET.fromstring(xml_content)

            # Define the namespace
            namespace = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

            # Extract all text elements
            text_elements = root.findall('.//w:t', namespace)

            # Combine all text
            text = ' '.join([elem.text for elem in text_elements if elem.text])

            return text
    except Exception as e:
        print(f"Error reading {docx_path}: {e}")
        return ""

def get_all_docx_files(base_dir):
    """
    Get all .docx files from the directory, organized by draft.
    """
    files_by_draft = defaultdict(list)

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.docx') and not file.startswith('~$'):  # Skip temp files
                full_path = os.path.join(root, file)
                # Extract draft number from path
                draft_match = re.search(r'Draft (\d+)', root)
                if draft_match:
                    draft_num = int(draft_match.group(1))
                    files_by_draft[draft_num].append((file, full_path))

    return files_by_draft

def analyze_novel():
    """
    Main analysis function.
    """
    base_dir = '/home/user/robindynamo'

    print("=" * 80)
    print("NOVEL ANALYSIS: Robin Dynamo Project")
    print("=" * 80)
    print()

    # Get all files organized by draft
    files_by_draft = get_all_docx_files(base_dir)

    print(f"Found {len(files_by_draft)} drafts")
    for draft_num in sorted(files_by_draft.keys()):
        print(f"  Draft {draft_num}: {len(files_by_draft[draft_num])} files")
    print()

    # Focus on Draft 25 (most recent)
    print("=" * 80)
    print("DRAFT 25 ANALYSIS (CURRENT VERSION)")
    print("=" * 80)
    print()

    draft_25_files = sorted(files_by_draft[25], key=lambda x: x[0])

    all_text_draft_25 = []
    chapters = {}

    print("Draft 25 Files:")
    for filename, filepath in draft_25_files:
        print(f"  - {filename}")
        text = extract_text_from_docx(filepath)

        # Try to identify chapter number
        chapter_match = re.match(r'(\d+)', filename)
        if chapter_match:
            chapter_num = int(chapter_match.group(1))
            chapters[chapter_num] = {
                'filename': filename,
                'text': text,
                'word_count': len(text.split())
            }

        all_text_draft_25.append({
            'filename': filename,
            'text': text,
            'word_count': len(text.split())
        })

    print()
    print("=" * 80)
    print("CHAPTER STRUCTURE (Draft 25)")
    print("=" * 80)
    print()

    for chapter_num in sorted(chapters.keys()):
        ch = chapters[chapter_num]
        print(f"Chapter {chapter_num}: {ch['filename']}")
        print(f"  Word count: {ch['word_count']}")
        # Print first 200 characters
        preview = ch['text'][:300].replace('\n', ' ').strip()
        print(f"  Preview: {preview}...")
        print()

    # Combine all text for analysis
    full_text_draft_25 = ' '.join([item['text'] for item in all_text_draft_25])

    print("=" * 80)
    print("CHARACTER ANALYSIS")
    print("=" * 80)
    print()

    # Look for character names (capitalized words that appear frequently)
    # Common character name patterns
    character_names = [
        'Gavin', 'Raven', 'Grandpa', 'Kermit', 'Siggy', 'Mom', 'Dad',
        'Brimley', 'Hudson', 'Aanya', 'Callie', 'Marvin', 'Evie',
        'Captain Laser', 'Norwood', 'Marindale'
    ]

    print("Character appearances in Draft 25:")
    for name in character_names:
        count = full_text_draft_25.count(name)
        if count > 0:
            print(f"  {name}: {count} mentions")

    print()
    print("=" * 80)
    print("LOCATION/SETTING ANALYSIS")
    print("=" * 80)
    print()

    locations = [
        'Albuquerque', 'Mesa View', 'Galaxy Pizza', 'Grindle Park',
        'Atlas', 'Brimley Forge', 'casita', 'workshop', 'library',
        'Spangenberg', 'museum', 'Rainier Park', 'fortress'
    ]

    print("Location mentions in Draft 25:")
    for location in locations:
        count = full_text_draft_25.lower().count(location.lower())
        if count > 0:
            print(f"  {location}: {count} mentions")

    print()
    print("=" * 80)
    print("TECHNICAL/THEMATIC ELEMENTS")
    print("=" * 80)
    print()

    themes = [
        'Arduino', 'Raspberry Pi', 'robot', 'circuit', 'programming',
        'Pythagorean theorem', 'math', 'inventor', 'riddle', 'clue',
        'mystery', 'puzzle', 'wheel', 'azimuth', 'compass', 'golden ratio',
        'pi', 'sigma', 'Greek', 'electronics', 'STEM'
    ]

    print("Thematic elements in Draft 25:")
    for theme in themes:
        count = full_text_draft_25.lower().count(theme.lower())
        if count > 0:
            print(f"  {theme}: {count} mentions")

    print()
    print("=" * 80)
    print("DETAILED CHAPTER CONTENT (Draft 25)")
    print("=" * 80)
    print()

    for chapter_num in sorted(chapters.keys()):
        ch = chapters[chapter_num]
        print(f"\n{'=' * 80}")
        print(f"CHAPTER {chapter_num}: {ch['filename']}")
        print(f"{'=' * 80}")
        print(f"Word count: {ch['word_count']}")
        print()

        # Print first 1500 characters of each chapter
        text_preview = ch['text'][:1500]
        print(text_preview)
        if len(ch['text']) > 1500:
            print("\n[... content continues ...]")
        print()

    # Sample earlier drafts for evolution
    print("\n" + "=" * 80)
    print("EVOLUTION ACROSS DRAFTS (Sampling)")
    print("=" * 80)
    print()

    sample_drafts = [1, 5, 10, 15, 20, 25]
    for draft_num in sample_drafts:
        if draft_num in files_by_draft:
            print(f"\nDraft {draft_num}:")
            print(f"  Number of files: {len(files_by_draft[draft_num])}")

            # Get some sample filenames
            sample_files = sorted([f[0] for f in files_by_draft[draft_num]])[:10]
            print(f"  Sample files: {', '.join(sample_files[:5])}")

            # Count total words
            total_words = 0
            for filename, filepath in files_by_draft[draft_num]:
                text = extract_text_from_docx(filepath)
                total_words += len(text.split())
            print(f"  Approximate total words: {total_words:,}")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    analyze_novel()
