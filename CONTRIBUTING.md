# Contributing — k0rdent Workshop

## Add a New Language

This project uses the [Open Learn](https://open-learn.app) format. You can contribute a translation by copying an existing language folder.

### Step 1: Create the folder

Copy an existing language folder (e.g. `english/`) and rename it:

| Language | Folder | Code |
|----------|--------|------|
| Deutsch | `deutsch` | `de-DE` |
| English | `english` | `en-US` |
| Farsi | `farsi` | `fa-IR` |
| Arabic | `arabic` | `ar-SA` |
| Français | `francais` | `fr-FR` |
| Español | `espanol` | `es-ES` |

### Step 2: Translate the content

In each `content.yaml`:

| Field | Translate? |
|-------|-----------|
| `title`, `description` | ✅ Yes |
| `explanation` | ✅ Yes |
| `q` (questions) | ✅ Yes (IT workshop) |
| `a` (answers) | ✅ Yes |
| Section `title` | ✅ Yes |
| `options[].text` | ✅ Yes |
| `rel[1]` (meaning) | ✅ Yes |
| `rel[0]` (ID) | ❌ No — never change |
| `labels`, `type`, `correct` | ❌ No |
| Technical terms | ❌ No — keep: k0rdent, kubectl, helm, Kubernetes, docker, KCM, KSM, KOF |

### Step 3: Extend index.yaml

Add your language to `index.yaml`:

```yaml
languages:
  - folder: english
    code: en-US
  - folder: deutsch
    code: de-DE
  - folder: your-language   # NEW
    code: xx-XX
```

### Step 4: Open a Pull Request

Please verify before opening a PR:

- [ ] All `content.yaml` files are valid YAML
- [ ] `lessons.yaml` lists all lesson folders
- [ ] `workshops.yaml` has `title` and `description` translated
- [ ] `index.yaml` includes your new language
- [ ] No `rel` IDs changed
