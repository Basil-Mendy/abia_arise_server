"""
Utility module for generating ID cards and certificates with pixel-perfect precision
Supports custom font (Montserrat Bold) + auto font size reduction + text wrapping
"""

from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
from django.conf import settings


# ====================== CUSTOM FONT CONFIG ======================
# Place Montserrat-Bold.ttf in your project, e.g., settings.BASE_DIR / 'fonts/Montserrat-Bold.ttf'
# You can download it from: https://fonts.google.com/specimen/Montserrat (Bold weight)

CUSTOM_FONT_PATH = os.path.join(settings.BASE_DIR, 'fonts', 'Montserrat-Bold.ttf')


class IDCardGenerator:
    """Generate ID cards for individual members"""
    
    TEMPLATE_SIZE = (1013, 1280)
    
    POSITIONS = {
        "photo":    (22, 148),
        "name":     (405, 168),
        "state":    (405, 223),
        "lga":      (405, 278),
        "ward":     (405, 333),
        "id_no":    (405, 390),
    }
    
    MAX_WIDTHS = {          # Maximum pixel width for each field
        "name":   520,
        "state":  520,
        "lga":    520,
        "ward":   520,
        "id_no":  520,
    }
    
    BASE_FONT_SIZES = {
        "name":   32,
        "state":  19,
        "lga":    19,
        "ward":   19,
        "id_no":  24,
    }
    
    FONT_COLORS = {
        "name":   "#000000",
        "state":  "#000000",
        "lga":    "#000000",
        "ward":   "#000000",
        "id_no":  "#0066CC",
    }

    def __init__(self):
        self.output_dir = os.path.join(settings.MEDIA_ROOT, 'generated', 'id_cards')
        self.template_path = os.path.join(settings.MEDIA_ROOT, 'templates', 'Abia arise ID card updated.png')
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"ID card template not found at {self.template_path}")
        
        self.fonts = {}  # Will be loaded dynamically with size adjustment

    def _get_font(self, size):
        """Load custom Montserrat Bold with fallback"""
        if os.path.exists(CUSTOM_FONT_PATH):
            try:
                return ImageFont.truetype(CUSTOM_FONT_PATH, size)
            except Exception as e:
                print(f"Warning: Could not load custom font: {e}")
        
        # Fallback chain
        fallback_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "C:\\Windows\\Fonts\\arialbd.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ]
        for path in fallback_paths:
            if os.path.exists(path):
                try:
                    return ImageFont.truetype(path, size)
                except:
                    continue
        return ImageFont.load_default()

    def _fit_text(self, draw, text, max_width, base_size, field_name):
        """Reduce font size until text fits within max_width"""
        if not text:
            return self._get_font(base_size), text
        
        font = self._get_font(base_size)
        current_size = base_size
        
        while current_size > 10:
            font = self._get_font(current_size)
            text_width = draw.textlength(text, font=font)
            if text_width <= max_width:
                return font, text
            current_size -= 1
        
        return self._get_font(12), text  # minimum readable size

    def generate(self, member_data):
        try:
            template = Image.open(self.template_path).convert('RGB')
            img = template.copy()
            draw = ImageDraw.Draw(img)
            
            full_name = f"{member_data.get('first_name', '')} {member_data.get('middle_name', '')} {member_data.get('last_name', '')}".strip()
            
            # Paste photo
            if member_data.get('profile_picture'):
                try:
                    pic = Image.open(member_data['profile_picture'] if hasattr(member_data['profile_picture'], 'read') 
                                   else str(member_data['profile_picture']))
                    pic = pic.convert('RGB').resize((285, 255), Image.Resampling.LANCZOS)
                    img.paste(pic, self.POSITIONS["photo"])
                except Exception as e:
                    print(f"Warning: Photo error: {e}")
            
            # Draw fields with auto font sizing
            for field, base_size in self.BASE_FONT_SIZES.items():
                if field == "name":
                    text = full_name
                elif field == "state":
                    text = member_data.get('state', '')
                elif field == "lga":
                    text = member_data.get('lga', '')
                elif field == "ward":
                    text = member_data.get('ward', '')
                else:  # id_no
                    text = member_data.get('abia_arise_id', 'N/A')
                
                font, final_text = self._fit_text(draw, text, self.MAX_WIDTHS[field], base_size, field)
                color = self.FONT_COLORS.get(field, "#000000")
                
                self._draw_text(draw, final_text, self.POSITIONS[field], font, color)
            
            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            member_id = str(member_data.get('abia_arise_id', 'unknown')).replace('/', '-')
            filename = f"id_card_{member_id}_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            img.save(filepath, 'PNG', quality=95)
            return True, filepath, None
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False, None, f"ID Card failed: {str(e)}"

    def _draw_text(self, draw, text, position, font, fill):
        draw.text(position, text, fill=fill, font=font, anchor="lt")


class CertificateGenerator:
    """Generate Pro Group Certificates with text wrapping and auto sizing"""
    
    TEMPLATE_SIZE = (3508, 2480)
    
    POSITIONS = {
        "group_name":     (140, 355),
        "license_no":     (380, 480),
        "chairman_name":  (180, 645),
        "secretary_name": (760, 645),
    }
    
    MAX_WIDTHS = {
        "group_name":     2200,   # Large box for group name
        "license_no":     800,
        "chairman_name":  700,
        "secretary_name": 700,
    }
    
    BASE_FONT_SIZES = {
        "group_name":    72,
        "license_no":    62,
        "chairman_name": 56,
        "secretary_name":56,
    }
    
    def __init__(self):
        self.output_dir = os.path.join(settings.MEDIA_ROOT, 'generated', 'certificates')
        self.template_path = os.path.join(settings.MEDIA_ROOT, 'templates', 'abia_arise_progroup_cert.png')
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Certificate template not found at {self.template_path}")

    def _get_font(self, size):
        if os.path.exists(CUSTOM_FONT_PATH):
            try:
                return ImageFont.truetype(CUSTOM_FONT_PATH, size)
            except:
                pass
        # fallback chain same as above...
        fallback = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "C:\\Windows\\Fonts\\arialbd.ttf"]
        for p in fallback:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except:
                    continue
        return ImageFont.load_default()

    def _wrap_and_fit_text(self, draw, text, max_width, base_size, line_height_factor=1.2):
        """Reduce size + wrap text if still too long"""
        if not text:
            return self._get_font(base_size), [text]
        
        size = base_size
        while size > 20:
            font = self._get_font(size)
            words = text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                if draw.textlength(test_line, font=font) <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Check if wrapped version fits
            total_height = len(lines) * (size * line_height_factor)
            if len(lines) <= 3 and draw.textlength(lines[0], font=font) <= max_width:  # reasonable limit
                return font, lines
            size -= 2  # reduce size
        
        # Final fallback
        return self._get_font(36), [text[:50] + "..." if len(text) > 50 else text]

    def generate(self, group_data):
        try:
            template = Image.open(self.template_path).convert('RGB')
            img = template.copy()
            draw = ImageDraw.Draw(img)
            
            group_name = group_data.get('name', 'N/A')
            license_no = group_data.get('group_license_number', 'N/A')
            chairman   = group_data.get('chairman_name', 'N/A')
            secretary  = group_data.get('secretary_name', 'N/A')
            
            # Group Name - with wrapping + auto size
            font, lines = self._wrap_and_fit_text(draw, group_name, self.MAX_WIDTHS["group_name"], 
                                                 self.BASE_FONT_SIZES["group_name"], line_height_factor=1.1)
            
            y = self.POSITIONS["group_name"][1]
            for line in lines:
                draw.text((self.POSITIONS["group_name"][0], y), line, 
                         font=font, fill="#000000", anchor="lt")
                y += font.size * 1.15   # line spacing
            
            # License No (centered)
            font = self._get_font(self.BASE_FONT_SIZES["license_no"])
            draw.text(self.POSITIONS["license_no"], license_no, 
                     font=font, fill="#000000", anchor="mm")
            
            # Chairman & Secretary
            for field, text, pos in [
                ("chairman_name", chairman, self.POSITIONS["chairman_name"]),
                ("secretary_name", secretary, self.POSITIONS["secretary_name"])
            ]:
                font, _ = self._fit_text(draw, text, self.MAX_WIDTHS[field], 
                                       self.BASE_FONT_SIZES[field], field)  # reuse fit logic
                draw.text(pos, text, font=font, fill="#000000", anchor="lt")
            
            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_license = str(license_no).replace('/', '_').replace(' ', '_')
            filename = f"progroup_cert_{safe_license}_{timestamp}.png"
            filepath = os.path.join(self.output_dir, filename)
            
            img.save(filepath, 'PNG', quality=95)
            return True, filepath, None
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return False, None, f"Certificate failed: {str(e)}"

    def _fit_text(self, draw, text, max_width, base_size, field_name):
        font = self._get_font(base_size)
        current_size = base_size
        while current_size > 20:
            font = self._get_font(current_size)
            if draw.textlength(text, font=font) <= max_width:
                return font, text
            current_size -= 1
        return self._get_font(36), text