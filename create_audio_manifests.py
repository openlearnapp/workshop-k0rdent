#!/usr/bin/env python3
"""
Create audio/manifest.yaml files for all k0rdent lessons in all languages.
Based on the milas-abenteuer pattern where each lesson has:
  audio/manifest.yaml  → lists all expected MP3 files
  audio/title.mp3       → lesson title narration
  audio/0-title.mp3     → section 0 title narration
  audio/0-0-q.mp3       → section 0, example 0, question
  audio/0-0-a.mp3       → section 0, example 0, answer (if has 'a' field)
"""

import os
import yaml

BASE = '/Users/reza/Github/openlearnapp/workshop-k0rdent/'
LANGUAGES = ['english', 'deutsch', 'farsi', 'arabic']
WORKSHOP = 'k0rdent-workshop'


def generate_manifest_files(content_yaml):
    """Generate list of expected audio files from content.yaml structure."""
    files = ['title.mp3']  # lesson title

    sections = content_yaml.get('sections', [])
    for sec_idx, section in enumerate(sections):
        files.append(f'{sec_idx}-title.mp3')  # section title

        examples = section.get('examples', [])
        for ex_idx, example in enumerate(examples):
            # Only generate audio for non-interactive, narrative examples
            ex_type = example.get('type', '')
            if ex_type in ('input', 'select', 'multiple-choice'):
                continue  # Skip quiz items — no audio needed

            q = example.get('q', '')
            a = example.get('a', '')
            voice = example.get('voice', '')

            # Generate audio for:
            # - Items with voice field (story/narrator style)
            # - Short Q&A items (concept explanations)
            # - Not for code commands (starts with $, kubectl, docker, etc.)
            is_code = any(q.strip().startswith(cmd) for cmd in [
                '$', 'kubectl', 'docker', 'helm', 'k0s', 'ssh',
                'cat ', 'echo ', 'export ', 'curl ', 'apt ', 'pip ',
                'cd ', 'ls ', 'mkdir ', 'git '
            ])

            if voice or (not is_code and len(q) > 20):
                files.append(f'{sec_idx}-{ex_idx}-q.mp3')
                if a and len(a) > 10 and not is_code:
                    files.append(f'{sec_idx}-{ex_idx}-a.mp3')

    return files


def create_manifests():
    total = 0
    errors = 0

    for lang in LANGUAGES:
        lessons_path = os.path.join(BASE, lang, WORKSHOP)
        if not os.path.exists(lessons_path):
            print(f'  ⚠ {lang}: {lessons_path} not found')
            continue

        for lesson_dir in sorted(os.listdir(lessons_path)):
            lesson_path = os.path.join(lessons_path, lesson_dir)
            content_path = os.path.join(lesson_path, 'content.yaml')

            if not os.path.isdir(lesson_path) or not os.path.exists(content_path):
                continue

            try:
                with open(content_path, 'r', encoding='utf-8') as f:
                    content = yaml.safe_load(f)

                if not content:
                    continue

                audio_files = generate_manifest_files(content)

                # Create audio/ directory
                audio_dir = os.path.join(lesson_path, 'audio')
                os.makedirs(audio_dir, exist_ok=True)

                # Write manifest.yaml
                manifest_path = os.path.join(audio_dir, 'manifest.yaml')
                manifest_content = 'files:\n'
                for f in audio_files:
                    manifest_content += f'  - {f}\n'

                with open(manifest_path, 'w', encoding='utf-8') as mf:
                    mf.write(manifest_content)

                total += 1
                print(f'  ✓ {lang}/{lesson_dir}: {len(audio_files)} audio files planned')

            except Exception as e:
                errors += 1
                print(f'  ✗ {lang}/{lesson_dir}: {e}')

    print(f'\n✅ Created: {total} manifests | Errors: {errors}')


if __name__ == '__main__':
    print('Creating audio manifest files for all k0rdent lessons...\n')
    create_manifests()
