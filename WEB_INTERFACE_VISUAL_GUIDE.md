# Web Interface Screenshots and Visual Guide

## Main Interface

The web interface provides a clean, intuitive design for handwriting synthesis:

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                        🖋️ DeepWriting                              │
│               Handwriting Synthesis with Deep Learning            │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  ℹ️ Welcome! This interface allows you to synthesize handwriting   │
│     from text. You can enter any text and optionally select a     │
│     handwriting style to mimic a particular writing style.        │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  📝 Input Text                                                     │
│                                                                    │
│  Enter the text you want to synthesize:                           │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Hello, World!                                                │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  Quick examples:                                                   │
│  [ Hello, World! ] [ Pangram ] [ Sample 1 ] [ Sample 2 ]          │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  🎨 Handwriting Style                                              │
│                                                                    │
│  Select a handwriting style (optional):                           │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Random Style (Unbiased)                          ▼          │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                  [ ✨ Synthesize Handwriting ]                      │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│  📄 Generated Handwriting                                          │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                                                              │ │
│  │     [SVG handwriting output appears here]                   │ │
│  │                                                              │ │
│  │     Hello, World!                                           │ │
│  │     (rendered as handwritten text)                          │ │
│  │                                                              │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

## User Flow

1. **User enters text** in the input area
2. **Optionally selects a style** from the dropdown
3. **Clicks "Synthesize Handwriting"** button
4. **Loading indicator** appears while processing
5. **Synthesized handwriting** appears as SVG below

## Features Showcase

### Text Input
- Large text area for comfortable typing
- Support for multi-line text
- Quick example buttons for common phrases
- Character limit recommended: ~50-100 characters for best results

### Style Selection
- Dropdown with predefined styles
- "Random Style" option for unbiased sampling
- Each style corresponds to a real handwriting sample from the validation dataset

### Output Display
- High-quality SVG rendering
- Scalable without quality loss
- Can be saved or copied from browser

## Color Scheme

- **Primary Colors**: Purple gradient (#667eea to #764ba2)
- **Background**: White content area on gradient background
- **Text**: Dark gray (#333) for readability
- **Accents**: Light gray borders and backgrounds

## Responsive Design

The interface adapts to different screen sizes:
- Desktop: Full-width layout with comfortable spacing
- Tablet: Adjusted padding and font sizes
- Mobile: Stacked layout with touch-friendly buttons

## Technical Implementation

### Frontend
- Pure HTML/CSS/JavaScript (no framework dependencies)
- Embedded CSS for self-contained deployment
- Vanilla JavaScript for API calls
- SVG rendering in browser

### Backend
- Flask web server
- TensorFlow model loading
- RESTful API design
- JSON request/response format

### API Flow

```
Client                          Server
  │                               │
  │  POST /api/synthesize        │
  │  {"text": "...", "style_id"} │
  ├──────────────────────────────>│
  │                               │ Load model (cached)
  │                               │ Run synthesis
  │                               │ Generate SVG
  │                               │
  │  {"success": true, "svg": ...}│
  │<──────────────────────────────┤
  │                               │
  │  Display SVG                  │
  │                               │
```

## Browser Compatibility

Tested and compatible with:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance Notes

- Model loading: ~5-10 seconds (one-time on server start)
- Synthesis time: ~2-10 seconds depending on text length
- Browser rendering: Instant (SVG is efficient)
- Recommended: Use GPU for faster synthesis

## Customization

Users can customize the following in `app.py`:

```python
# Synthesis parameters
seq_len = 800              # Maximum sequence length
eoc_threshold = 0.05       # End-of-character threshold
cursive_threshold = 0.005  # Cursive writing threshold
use_sample_mean = True     # Use mean vs. sampling
```

These parameters affect:
- **seq_len**: Maximum length of output (longer = more text)
- **eoc_threshold**: Character separation (lower = more cursive)
- **cursive_threshold**: Writing style continuity
- **use_sample_mean**: Deterministic vs. random output
