"""
COORDINATE FINE-TUNING INSTRUCTIONS

If text on your ID cards or certificates appears in the wrong location,
follow these steps to find the exact pixel coordinates and update them.

═══════════════════════════════════════════════════════════════════════════════
STEP-BY-STEP GUIDE
═══════════════════════════════════════════════════════════════════════════════

METHOD 1: Using Windows Paint (Recommended for Quick Tuning)
─────────────────────────────────────────────────────────────────────────────

1. Open Windows Paint
2. File → Open → Select template image from: backend/media/templates/
   - For ID Card: "Abia_arise_ID_card.png"
   - For Certificate: "abia_arise_progroup_cert.png"

3. Enable the Zoom to see coordinates clearly (View → Zoom → 100% or larger)

4. Move your mouse cursor over the template image

5. Look at the BOTTOM-LEFT corner of the Paint window
   You'll see coordinates like: "480, 255" (this is X, Y)

6. Position your cursor WHERE YOU WANT THE TEXT TO START

7. Note the coordinates shown

8. Open: backend/accounts/generators.py

9. Find the coordinate section:
   - For ID Card: Find "ID_CARD_COORDS"
   - For Certificate: Find "CERTIFICATE_COORDS"

10. Update the 'xy' value with your new coordinates:
    BEFORE: 'member_name': {'xy': (550, 320), ...}
    AFTER:  'member_name': {'xy': (480, 255), ...}  # Updated coordinates

11. Save the file

12. Test by registering a new member or group (auto-generation will run)

13. Check the generated file in:
    - ID Cards: backend/media/generated/id_cards/
    - Certificates: backend/media/generated/certificates/

14. If still not perfect, repeat steps 1-13


METHOD 2: Using GIMP (More Precise Control)
─────────────────────────────────────────────────────────────────────────────

1. Download and install GIMP (https://www.gimp.org/)

2. Open GIMP and File → Open template image

3. Enable grid and rulers:
   - View → Show Rulers (shows pixel scale on edges)
   - View → Show Grid (optional)

4. Use the Pointer Tool to hover over template

5. Look at the coordinates in the "Pointer" dialog (Windows → Dockable Dialogs → Pointer)

6. Position precisely on where text should appear

7. Note the X, Y coordinates

8. Update generators.py as described in METHOD 1


═══════════════════════════════════════════════════════════════════════════════
COORDINATE SYSTEM EXPLANATION
═══════════════════════════════════════════════════════════════════════════════

IMAGE COORDINATES:
- (0, 0) = Top-left corner
- (1013, 1280) = Bottom-right corner for ID card
- (3508, 1280) = Bottom-right corner for certificate

EXAMPLE:
  (0, 0)
    ╔═══════════════════════════════════════════╗
    ║ Top-left corner                           ║
    ║                                           ║
    ║  (50, 100) = 50px right, 100px down     ║
    ║  (500, 500) = 500px right, 500px down  ║
    ║                                           ║
    ║                      (1013, 1280)        ║
    ║                     ↓ (bottom-right)     ║
    ╚═══════════════════════════════════════════╝

ANCHOR TYPES:
- 'lm' (left-middle):    Text STARTS at the given X coordinate
                         Vertically centered at Y
- 'mm' (middle-middle):  Text CENTERED at both X and Y
- 'rm' (right-middle):   Text ENDS at the given X coordinate
                         Vertically centered at Y


═══════════════════════════════════════════════════════════════════════════════
COMMON ADJUSTMENTS
═══════════════════════════════════════════════════════════════════════════════

Text appears too high?           → Increase Y value (move down)
Text appears too low?            → Decrease Y value (move up)
Text appears too far left?       → Increase X value (move right)
Text appears too far right?      → Decrease X value (move left)
Text is too small?               → Increase font_size value
Text is too large?               → Decrease font_size value


═══════════════════════════════════════════════════════════════════════════════
TEMPLATE DIMENSIONS QUICK REFERENCE
═══════════════════════════════════════════════════════════════════════════════

ID CARD (1013 x 1280 px):
┌──────────────────────────────────┐
│ Top area for header/logo         │ 0-200px
├──────────────────────────────────┤
│ Left: Profile picture (100-250)  │
│ Right: Name/ID/LGA/State (550+)  │ 300-600px
├──────────────────────────────────┤
│ Bottom footer area (QR code, etc)│ 1100-1280px
└──────────────────────────────────┘

CERTIFICATE (3508 x 1280 px):
┌──────────────────────────────────┐
│ Left section (0-1000px)          │ Header area
├──────────────────────────────────┤
│ CENTER: Recipient name (1754)    │ 400-650px
│ CENTER: Award text (1754)        │ 650-850px
├──────────────────────────────────┤
│ CENTER: Date (1754)              │ 1000-1100px
│ Right section (2500-3508px)      │ Signature area
└──────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
FORMULA FOR CENTER (MM ANCHOR)
═══════════════════════════════════════════════════════════════════════════════

For certificates with 'mm' (centered) text:

X coordinate = Image width ÷ 2
Example: 3508 ÷ 2 = 1754 (horizontal center)

Y coordinate = Where you want vertically


═══════════════════════════════════════════════════════════════════════════════
WHERE TO MAKE CHANGES
═══════════════════════════════════════════════════════════════════════════════

File: backend/accounts/generators.py
Location: Lines 10-33 (CoordinateMapper class)

ID_CARD_COORDS = {
    'member_name': {'xy': (550, 320), 'anchor': 'lm', 'font_size': 32, 'color': (0, 0, 0)},
    'member_id': {'xy': (550, 380), 'anchor': 'lm', 'font_size': 24, 'color': (0, 0, 0)},
    'lga': {'xy': (550, 440), 'anchor': 'lm', 'font_size': 20, 'color': (0, 0, 0)},
    'state': {'xy': (550, 500), 'anchor': 'lm', 'font_size': 20, 'color': (0, 0, 0)},
    'date': {'xy': (100, 1200), 'anchor': 'lm', 'font_size': 16, 'color': (0, 0, 0)},
}

CERTIFICATE_COORDS = {
    'beneficiary_name': {'xy': (1754, 520), 'anchor': 'mm', 'font_size': 60, 'color': (0, 0, 0)},
    'award_text': {'xy': (1754, 720), 'anchor': 'mm', 'font_size': 48, 'color': (0, 0, 0)},
    'date': {'xy': (1754, 1050), 'anchor': 'mm', 'font_size': 32, 'color': (0, 0, 0)},
}


═══════════════════════════════════════════════════════════════════════════════
TESTING YOUR CHANGES
═══════════════════════════════════════════════════════════════════════════════

1. After updating coordinates in generators.py, save the file

2. From backend directory, run:
   python manage.py shell

3. Test ID card:
   from accounts.generators import generate_id_card
   data = {'first_name': 'Test', 'middle_name': 'M', 'last_name': 'User',
           'abia_arise_id': 'TEST01', 'lga_of_origin': 'Umuahia',
           'state_of_origin': 'Abia'}
   success, path, error = generate_id_card(data)
   print(f"Path: {path}")

4. Check the generated image in media/generated/id_cards/

5. If perfect, you're done! If not, repeat from step 1.


═══════════════════════════════════════════════════════════════════════════════
TROUBLESHOOTING COORDINATES
═══════════════════════════════════════════════════════════════════════════════

Text bleeding off edge?
  → Try negative offset (e.g., 'xy': (20, 400) instead of (0, 400))
  → Use 'rm' anchor instead of 'lm' to right-align

Text overlapping with other elements?
  → Increase Y value to move down (or decrease to move up)
  → Check that anchors are correct for your intended alignment

Cannot see coordinates in Paint?
  → Make sure you're not in selection mode, use regular pointer tool
  → Check that Image → Attributes shows 1013x1280 for ID card

Still not working?
  → Try Paint in Windows 10/11 (older versions may have issues)
  → Use GIMP as alternative (more reliable)
  → Check template image size matches expected dimensions

═══════════════════════════════════════════════════════════════════════════════

For additional help, refer to: ID_CARD_CERTIFICATE_SETUP.md
"""
