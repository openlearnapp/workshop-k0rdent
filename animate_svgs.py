#!/usr/bin/env python3
"""
Add CSS animations to all SVG files in the k0rdent workshop.
Animations:
- fadeIn: whole SVG fades in on load
- spin: circles with K8s-like spokes (Kubernetes wheel)
- float: container boxes gently float up/down
- pulse: glow effect on key elements
- slideIn: text labels slide in from left
- dashFlow: animated dashes on lines/paths
- typeIn: terminal text typing effect
"""

import os
import re
import sys

ANIMATION_STYLE = '''<style>
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes spinSlow { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
  @keyframes floatUD { 0%,100% { transform: translateY(0px); } 50% { transform: translateY(-6px); } }
  @keyframes floatUD2 { 0%,100% { transform: translateY(0px); } 50% { transform: translateY(-4px); } }
  @keyframes pulseGlow { 0%,100% { opacity:1; filter: drop-shadow(0 0 2px currentColor); } 50% { opacity:0.7; filter: drop-shadow(0 0 8px currentColor); } }
  @keyframes slideInL { from { opacity:0; transform: translateX(-20px); } to { opacity:1; transform: translateX(0); } }
  @keyframes slideInR { from { opacity:0; transform: translateX(20px); } to { opacity:1; transform: translateX(0); } }
  @keyframes slideInU { from { opacity:0; transform: translateY(15px); } to { opacity:1; transform: translateY(0); } }
  @keyframes dashFlow { from { stroke-dashoffset: 100; } to { stroke-dashoffset: 0; } }
  @keyframes blink { 0%,100% { opacity:1; } 50% { opacity:0; } }
  @keyframes scaleIn { from { opacity:0; transform: scale(0.85); } to { opacity:1; transform: scale(1); } }
  @keyframes shimmer { 0%,100% { opacity:0.6; } 50% { opacity:1; } }

  svg { animation: fadeIn 0.8s ease-out both; }

  /* Kubernetes wheel rotation */
  .k8s-wheel, [id*="wheel"], [id*="k8s"] {
    transform-origin: center center;
    animation: spinSlow 12s linear infinite;
  }

  /* Container boxes float */
  .container-box { animation: floatUD 3s ease-in-out infinite; }
  .container-box:nth-child(2) { animation-delay: 0.5s; }
  .container-box:nth-child(3) { animation-delay: 1s; }
  .container-box:nth-child(4) { animation-delay: 1.5s; }

  /* Node circles pulse */
  .node-circle { animation: pulseGlow 2.5s ease-in-out infinite; }

  /* Arrows animate */
  .flow-arrow { stroke-dasharray: 8 4; animation: dashFlow 1.5s linear infinite; }

  /* Section headers slide in */
  .section-title { animation: slideInL 0.6s ease-out 0.3s both; }

  /* Status items appear sequentially */
  .status-item { animation: slideInU 0.5s ease-out both; }
  .status-item:nth-child(1) { animation-delay: 0.1s; }
  .status-item:nth-child(2) { animation-delay: 0.2s; }
  .status-item:nth-child(3) { animation-delay: 0.3s; }
  .status-item:nth-child(4) { animation-delay: 0.4s; }
  .status-item:nth-child(5) { animation-delay: 0.5s; }

  /* Terminal cursor blink */
  .cursor { animation: blink 1s step-end infinite; }

  /* Badges scale in */
  .badge { animation: scaleIn 0.4s ease-out both; }

  /* Labels shimmer */
  .label-text { animation: shimmer 3s ease-in-out infinite; }
</style>'''


def add_animations_to_svg(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already animated
    if '@keyframes fadeIn' in content:
        return False

    # Detect element types and add animation classes
    modified = content

    # Add animation classes to container rect elements (colored boxes that look like containers)
    # Match colored rects that likely represent containers (have fill with specific colors)
    container_colors = ['#1f6feb', '#238636', '#b56800', '#388bfd', '#2ea043']
    for color in container_colors:
        modified = modified.replace(
            f'fill="{color}"',
            f'fill="{color}" class="container-box"',
            -1  # replace all occurrences
        )

    # Add k8s-wheel class to circles that look like Kubernetes wheel (with spokes)
    # These are typically circles with stroke (no fill or light fill) near center of diagrams
    # We'll detect circles with r="36" or similar sizes that are likely the K8s wheel
    modified = re.sub(
        r'<circle([^>]*?)r="(3[0-9]|4[0-5])"([^>]*?)fill="none"([^>]*?)stroke="#58a6ff"',
        r'<circle\1r="\2"\3fill="none"\4stroke="#58a6ff" class="k8s-wheel"',
        modified
    )

    # Add flow animation to paths that look like arrows/connections
    modified = re.sub(
        r'(<(?:line|path)[^>]*stroke-dasharray[^>]*>)',
        r'<g class="flow-arrow">\1</g>',
        modified
    )

    # Add cursor blink to terminal cursor elements (usually a rect after $ prompt)
    modified = re.sub(
        r'(<rect[^>]*fill="#3fb950"[^>]*width="[1-9]"[^>]*/>)',
        r'<rect class="cursor" \1/>',
        modified
    )

    # Insert the animation style block right after the opening <svg> tag
    # but before any existing <defs>
    if '<defs>' in modified:
        modified = modified.replace('<defs>', ANIMATION_STYLE + '\n  <defs>', 1)
    elif '<style>' in modified:
        # Already has style, inject our keyframes at the beginning
        modified = modified.replace('<style>', ANIMATION_STYLE + '\n  <style>', 1)
    else:
        # Insert after the opening svg tag
        modified = re.sub(r'(<svg[^>]*>)', r'\1\n' + ANIMATION_STYLE, modified, count=1)

    # Add floating animation to the water path in lesson headers (ship scenes)
    if 'water' in modified.lower() or 'M 60 290' in modified:
        modified = modified.replace(
            'fill="#0d2340"',
            'fill="#0d2340" style="animation: floatUD2 4s ease-in-out infinite;"'
        )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(modified)

    return True


def process_directory(base_dir):
    count = 0
    skipped = 0
    for root, dirs, files in os.walk(base_dir):
        # Only process images/ subdirectories
        if not root.endswith('/images') and '/images/' not in root:
            continue
        for filename in files:
            if filename.endswith('.svg') and filename != 'thumbnail.svg':
                filepath = os.path.join(root, filename)
                try:
                    if add_animations_to_svg(filepath):
                        count += 1
                        print(f'  ✓ {filepath[len(base_dir):]}')
                    else:
                        skipped += 1
                except Exception as e:
                    print(f'  ✗ ERROR {filepath}: {e}')

    # Also process thumbnails
    for root, dirs, files in os.walk(base_dir):
        for filename in files:
            if filename == 'thumbnail.svg':
                filepath = os.path.join(root, filename)
                try:
                    if add_animations_to_svg(filepath):
                        count += 1
                        print(f'  ✓ {filepath[len(base_dir):]}')
                    else:
                        skipped += 1
                except Exception as e:
                    print(f'  ✗ ERROR {filepath}: {e}')

    return count, skipped


if __name__ == '__main__':
    base = '/Users/reza/Github/openlearnapp/workshop-k0rdent/'
    print('Adding CSS animations to all k0rdent SVGs...\n')
    count, skipped = process_directory(base)
    print(f'\n✅ Animated: {count} SVGs | Skipped (already done): {skipped}')
