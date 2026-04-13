# Fonts Directory

This folder stores custom fonts used for ID card and certificate text rendering.

## Font Installation

### Step 1: Download a Font
Download a TrueType font (`.ttf`) or OpenType font (`.otf`):
- **Roboto Bold**: https://fonts.google.com/specimen/Roboto
- **DejaVu Sans Bold**: Included with most systems
- **Arial**: Standard Windows font

### Step 2: Add Font File
1. Extract the font file (usually named like `Roboto-Bold.ttf`)
2. Place it in this directory: `backend/fonts/`

### Step 3: Update generators.py
Open `backend/accounts/generators.py` and locate the `FontManager` class.

Update the `font_paths` list to include your font:

```python
font_paths = [
    os.path.join(self.font_dir, 'Roboto-Bold.ttf'),      # Add this
    os.path.join(self.font_dir, 'Roboto-Regular.ttf'),
    os.path.join(self.font_dir, 'Your-Font.ttf'),        # Add this
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",
]
```

### Step 4: Test
```bash
python manage.py shell
from accounts.generators import FontManager
fm = FontManager()
font = fm.get_font(32)
print(f"Font loaded successfully: {font}")
```

## Recommended Fonts

| Font | Purpose | Download |
|------|---------|----------|
| **Roboto Bold** | Modern, clean default | https://fonts.google.com/specimen/Roboto |
| **DejaVu Sans** | Universal compatibility | System default on Linux |
| **Arial** | Windows standard | System default on Windows |
| **Open Sans** | Professional | https://fonts.google.com/specimen/Open+Sans |
| **Lato** | Friendly, readable | https://fonts.google.com/specimen/Lato |

## Font File Format

Currently supported formats:
- `.ttf` (TrueType Font) - Recommended
- `.otf` (OpenType Font) - Also supported
- `.ttc` (TrueType Collection) - May work

## File Organization

```
fonts/
├── README.md                    ← This file
├── Roboto-Bold.ttf             ← Primary font (if using Roboto)
├── Roboto-Regular.ttf
└── DejaVuSans-Bold.ttf        ← Backup font
```

## Fallback Chain

If a font file is missing, the system tries the next one in order:

1. `Roboto-Bold.ttf` (in this folder)
2. `Roboto-Regular.ttf` (in this folder)
3. Linux system font: `/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf`
4. Windows system font: `C:\Windows\Fonts\arial.ttf`
5. PIL default font (if nothing else works)

This ensures your app always has a working font, even if custom fonts are missing.

## License Consideration

When adding fonts, ensure you have the license to use them:
- **Google Fonts** - All free and open source
- **System fonts** - Licensed by your OS provider
- **Commercial fonts** - Check vendor terms before use

## Troubleshooting

### Font not loading?
1. Check file is actually `.ttf` format: `Roboto-Bold.ttf` (not `Roboto-Bold.pdf` or renamed file)
2. Verify filename matches exactly in `generators.py`
3. Test: Run the test command above
4. Check permissions: `ls -la fonts/` (Linux/Mac)

### Text looks blurry?
- Use a higher quality font (Google Fonts recommended)
- Ensure font size matches your template proportions

### Text keeps defaulting to basic font?
- Check console for error messages
- Verify font file exists: `python -c "import os; print(os.path.exists('backend/fonts/Roboto-Bold.ttf'))"`
- Try system font path directly in `generators.py`

## Font Size Guidelines

For your template dimensions:

**ID Card (1013 x 1280 px):**
- Member Name: 28-40px
- Member ID: 20-28px
- LGA/State: 16-24px
- Date: 12-18px

**Certificate (3508 x 1280 px):**
- Group Name: 50-70px
- Award Text: 40-52px
- Date: 28-36px

Adjust based on text length to ensure it fits within your template layout.

## Adding System Fonts (Alternative Method)

Instead of copying fonts here, you can reference system fonts directly:

**Windows:**
```python
"C:\\Windows\\Fonts\\georgia.ttf"
"C:\\Windows\\Fonts\\times.ttf"
```

**Linux:**
```python
"/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
"/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
```

**macOS:**
```python
"/Library/Fonts/Arial.ttf"
"/System/Library/Fonts/Helvetica.ttc"
```

## Support

For issues, check:
1. `ID_CARD_CERTIFICATE_SETUP.md` for complete setup guide
2. `COORDINATE_TUNING_GUIDE.py` for text placement help
3. `backend/accounts/generators.py` for font loading logic
