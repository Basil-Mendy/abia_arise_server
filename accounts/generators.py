"""
Advanced ID Card and Certificate Generator using Pillow
Handles text placement on templates with pixel-perfect coordinate mapping
"""
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
from django.conf import settings
import io


class CoordinateMapper:
    """Maps data fields to exact pixel coordinates on templates"""
    
    # ID Card Coordinates (1013 x 1280 px template)
    ID_CARD_COORDS = {
        'member_name': {'xy': (550, 320), 'anchor': 'lm', 'font_size': 32, 'color': (0, 0, 0)},
        'member_id': {'xy': (550, 380), 'anchor': 'lm', 'font_size': 24, 'color': (0, 0, 0)},
        'lga': {'xy': (550, 440), 'anchor': 'lm', 'font_size': 20, 'color': (0, 0, 0)},
        'state': {'xy': (550, 500), 'anchor': 'lm', 'font_size': 20, 'color': (0, 0, 0)},
        'date': {'xy': (100, 1200), 'anchor': 'lm', 'font_size': 16, 'color': (0, 0, 0)},
    }
    
    # Certificate Coordinates (3508 x 1280 px template)
    CERTIFICATE_COORDS = {
        'beneficiary_name': {'xy': (1754, 520), 'anchor': 'mm', 'font_size': 60, 'color': (0, 0, 0)},
        'award_text': {'xy': (1754, 720), 'anchor': 'mm', 'font_size': 48, 'color': (0, 0, 0)},
        'date': {'xy': (1754, 1050), 'anchor': 'mm', 'font_size': 32, 'color': (0, 0, 0)},
    }


class FontManager:
    """Manages font loading with fallback options"""
    
    def __init__(self):
        self.fonts = {}
        self.font_dir = os.path.join(settings.BASE_DIR, 'fonts')
        os.makedirs(self.font_dir, exist_ok=True)
    
    def get_font(self, size=32):
        """
        Get font with fallback chain:
        1. Roboto-Bold.ttf (if in fonts folder)
        2. Arial (Windows system)
        3. Default PIL font
        """
        if size in self.fonts:
            return self.fonts[size]
        
        font_paths = [
            os.path.join(self.font_dir, 'Roboto-Bold.ttf'),
            os.path.join(self.font_dir, 'Roboto-Regular.ttf'),
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux
            "C:\\Windows\\Fonts\\arial.ttf",  # Windows
        ]
        
        font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, size)
                    break
                except Exception as e:
                    print(f"Failed to load font {font_path}: {e}")
                    continue
        
        # Fallback to default if no font found
        if font is None:
            font = ImageFont.load_default()
        
        self.fonts[size] = font
        return font


class IDCardGenerator:
    """Generate ID cards with text overlay on template"""
    
    def __init__(self):
        self.template_path = os.path.join(settings.MEDIA_ROOT, 'templates', 'Abia_arise_ID_card.png')
        self.output_dir = os.path.join(settings.MEDIA_ROOT, 'generated', 'id_cards')
        os.makedirs(self.output_dir, exist_ok=True)
        self.font_manager = FontManager()
    
    def generate(self, member_data):
        """
        Generate ID card with text overlay
        
        Args:
            member_data (dict): Contains:
                - first_name, middle_name, last_name
                - abia_arise_id
                - lga_of_origin
                - state_of_origin
                - profile_picture (optional)
        
        Returns:
            tuple: (success: bool, file_path: str, error_msg: str or None)
        """
        try:
            # Open template
            if not os.path.exists(self.template_path):
                return False, None, f"Template not found: {self.template_path}"
            
            img = Image.open(self.template_path).convert('RGB')
            draw = ImageDraw.Draw(img)
            
            # Extract data
            full_name = f"{member_data.get('first_name', '')} {member_data.get('middle_name', '')} {member_data.get('last_name', '')}".strip()
            member_id = member_data.get('abia_arise_id', 'N/A')
            lga = member_data.get('lga_of_origin', 'N/A')
            state = member_data.get('state_of_origin', 'N/A')
            date_str = datetime.now().strftime('%d/%m/%Y')
            
            # Place text overlays using coordinates
            coords = CoordinateMapper.ID_CARD_COORDS
            
            # Member Name
            font = self.font_manager.get_font(coords['member_name']['font_size'])
            draw.text(coords['member_name']['xy'], full_name, 
                     fill=coords['member_name']['color'], font=font, 
                     anchor=coords['member_name']['anchor'])
            
            # Member ID
            font = self.font_manager.get_font(coords['member_id']['font_size'])
            draw.text(coords['member_id']['xy'], member_id,
                     fill=coords['member_id']['color'], font=font,
                     anchor=coords['member_id']['anchor'])
            
            # LGA
            font = self.font_manager.get_font(coords['lga']['font_size'])
            draw.text(coords['lga']['xy'], lga,
                     fill=coords['lga']['color'], font=font,
                     anchor=coords['lga']['anchor'])
            
            # State
            font = self.font_manager.get_font(coords['state']['font_size'])
            draw.text(coords['state']['xy'], state,
                     fill=coords['state']['color'], font=font,
                     anchor=coords['state']['anchor'])
            
            # Date
            font = self.font_manager.get_font(coords['date']['font_size'])
            draw.text(coords['date']['xy'], date_str,
                     fill=coords['date']['color'], font=font,
                     anchor=coords['date']['anchor'])
            
            # Add profile picture if available
            if member_data.get('profile_picture'):
                self._add_profile_picture(img, member_data['profile_picture'])
            
            # Save - sanitize filename (replace invalid characters)
            safe_id = member_id.replace('/', '-').replace('\\', '-').replace(':', '-')
            filename = f"id_card_{safe_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            file_path = os.path.join(self.output_dir, filename)
            img.save(file_path, 'PNG')
            
            return True, file_path, None
        
        except Exception as e:
            error_msg = f"ID Card generation failed: {str(e)}"
            print(error_msg)
            return False, None, error_msg
    
    def _add_profile_picture(self, img, profile_picture):
        """Add profile picture to ID card at coordinates (100, 300) with size 150x200"""
        try:
            if hasattr(profile_picture, 'read'):
                pic = Image.open(profile_picture)
            else:
                pic = Image.open(str(profile_picture))
            
            pic = pic.convert('RGB')
            pic.thumbnail((150, 200), Image.Resampling.LANCZOS)
            
            # Center the picture
            paste_x = 100
            paste_y = 300
            img.paste(pic, (paste_x, paste_y))
            
        except Exception as e:
            print(f"Warning: Could not add profile picture: {e}")


class CertificateGenerator:
    """Generate certificates with text overlay on template"""
    
    def __init__(self):
        self.template_path = os.path.join(settings.MEDIA_ROOT, 'templates', 'abia_arise_progroup_cert.png')
        self.output_dir = os.path.join(settings.MEDIA_ROOT, 'generated', 'certificates')
        os.makedirs(self.output_dir, exist_ok=True)
        self.font_manager = FontManager()
    
    def generate(self, group_data):
        """
        Generate certificate with text overlay
        
        Args:
            group_data (dict): Contains:
                - group_name
                - group_license_number
                - state
                - lga
        
        Returns:
            tuple: (success: bool, file_path: str, error_msg: str or None)
        """
        try:
            # Open template
            if not os.path.exists(self.template_path):
                return False, None, f"Template not found: {self.template_path}"
            
            img = Image.open(self.template_path).convert('RGB')
            draw = ImageDraw.Draw(img)
            
            # Extract data
            group_name = group_data.get('group_name', 'N/A')
            license_num = group_data.get('group_license_number', 'N/A')
            date_str = datetime.now().strftime('%d %B %Y')
            award_text = f"Certificate of Recognition\n{license_num}"
            
            # Place text overlays using coordinates
            coords = CoordinateMapper.CERTIFICATE_COORDS
            
            # Beneficiary Name (Group Name)
            font = self.font_manager.get_font(coords['beneficiary_name']['font_size'])
            draw.text(coords['beneficiary_name']['xy'], group_name,
                     fill=coords['beneficiary_name']['color'], font=font,
                     anchor=coords['beneficiary_name']['anchor'])
            
            # Award Text
            font = self.font_manager.get_font(coords['award_text']['font_size'])
            draw.text(coords['award_text']['xy'], award_text,
                     fill=coords['award_text']['color'], font=font,
                     anchor=coords['award_text']['anchor'])
            
            # Date
            font = self.font_manager.get_font(coords['date']['font_size'])
            draw.text(coords['date']['xy'], date_str,
                     fill=coords['date']['color'], font=font,
                     anchor=coords['date']['anchor'])
            
            # Save - sanitize filename (replace invalid characters)
            safe_license = license_num.replace('/', '-').replace('\\', '-').replace(':', '-')
            filename = f"certificate_{safe_license}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            file_path = os.path.join(self.output_dir, filename)
            img.save(file_path, 'PNG')
            
            return True, file_path, None
        
        except Exception as e:
            error_msg = f"Certificate generation failed: {str(e)}"
            print(error_msg)
            return False, None, error_msg


def generate_id_card(member_data, member_instance=None):
    """
    Convenience function for ID card generation
    
    Args:
        member_data (dict): Member data to use for generation
        member_instance (IndividualMember, optional): Member model instance to save file path to
    
    Returns:
        tuple: (success: bool, file_path: str, error_msg: str or None)
    """
    generator = IDCardGenerator()
    success, file_path, error = generator.generate(member_data)
    
    # If generation successful and member_instance provided, save path to database
    if success and member_instance and file_path:
        try:
            # Calculate relative path from media root
            media_root = settings.MEDIA_ROOT
            relative_path = os.path.relpath(file_path, media_root)
            member_instance.id_card_file = relative_path
            member_instance.save()
            print(f"ID card path saved to database: {relative_path}")
        except Exception as e:
            print(f"Warning: Could not save ID card path to database: {e}")
            # Don't fail the overall operation if DB save fails
    
    return success, file_path, error


def generate_certificate(group_data, group_instance=None):
    """
    Convenience function for certificate generation
    
    Args:
        group_data (dict): Group data to use for generation
        group_instance (ProGroup, optional): Group model instance to save file path to
    
    Returns:
        tuple: (success: bool, file_path: str, error_msg: str or None)
    """
    generator = CertificateGenerator()
    success, file_path, error = generator.generate(group_data)
    
    # If generation successful and group_instance provided, save path to database
    if success and group_instance and file_path:
        try:
            # Calculate relative path from media root
            media_root = settings.MEDIA_ROOT
            relative_path = os.path.relpath(file_path, media_root)
            group_instance.certificate_file = relative_path
            group_instance.save()
            print(f"Certificate path saved to database: {relative_path}")
        except Exception as e:
            print(f"Warning: Could not save certificate path to database: {e}")
            # Don't fail the overall operation if DB save fails
    
    return success, file_path, error
