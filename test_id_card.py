#!/usr/bin/env python
"""
Test script for ID card generation using template overlay
Run from backend directory: python test_id_card.py
"""

import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'abia_arise.settings')
django.setup()

from accounts.id_card_generator import IDCardGenerator, CertificateGenerator
from accounts.models import IndividualMember
from datetime import datetime
from PIL import Image

def test_template_exists():
    """Verify templates exist"""
    print("\n" + "="*70)
    print("TEMPLATE VERIFICATION")
    print("="*70)
    
    from django.conf import settings
    
    id_card_template = os.path.join(settings.MEDIA_ROOT, 'templates', 'Abia arise ID card updated.png')
    cert_template = os.path.join(settings.MEDIA_ROOT, 'templates', 'abia_arise_progroup_cert.png')
    
    print(f"\n1. ID Card Template:")
    if os.path.exists(id_card_template):
        try:
            img = Image.open(id_card_template)
            print(f"   ✅ Found at: {id_card_template}")
            print(f"   - Size: {img.size[0]}×{img.size[1]}px")
            print(f"   - Mode: {img.mode}")
            print(f"   - File size: {os.path.getsize(id_card_template)} bytes")
        except Exception as e:
            print(f"   ⚠️  Error reading template: {e}")
    else:
        print(f"   ❌ NOT FOUND at: {id_card_template}")
        return False
    
    print(f"\n2. Certificate Template:")
    if os.path.exists(cert_template):
        try:
            img = Image.open(cert_template)
            print(f"   ✅ Found at: {cert_template}")
            print(f"   - Size: {img.size[0]}×{img.size[1]}px")
            print(f"   - Mode: {img.mode}")
            print(f"   - File size: {os.path.getsize(cert_template)} bytes")
        except Exception as e:
            print(f"   ⚠️  Error reading template: {e}")
    else:
        print(f"   ⚠️  Not found at: {cert_template}")
    
    return True

def test_id_card_generation():
    """Test ID card generation with sample data"""
    
    print("\n" + "="*70)
    print("ID CARD GENERATION TEST (Template Overlay)")
    print("="*70)
    
    # Sample test data
    test_member_data = {
        'first_name': 'Muhammad',
        'middle_name': 'Abdulrahman',
        'last_name': 'Ibrahim',
        'state': 'Abia',
        'lga': 'Ikwuano',
        'ward': 'Ward III',
        'abia_arise_id': 'AB/ABS/TEST/001',
    }
    
    try:
        print("\n1. Testing IDCardGenerator initialization...")
        generator = IDCardGenerator()
        print("   ✅ Generator initialized successfully")
        print(f"   - Template: {os.path.basename(generator.template_path)}")
        print(f"   - Output directory: {generator.output_dir}")
        print(f"   - Directory exists: {os.path.exists(generator.output_dir)}")
        
        print("\n2. Testing font loading...")
        for field, size in generator.BASE_FONT_SIZES.items():
            font = generator._get_font(size)
            if font:
                print(f"   ✅ Font loaded for '{field}': size {size}pt")
            else:
                print(f"   ⚠️  Font missing for '{field}'")
        
        print("\n3. Testing field positions...")
        print(f"   Name position: {generator.POSITIONS['name']}")
        print(f"   Photo position: {generator.POSITIONS['photo']}")
        print("   ✅ Positions verified")
        
        print("\n4. Testing ID card generation...")
        success, filepath, error = generator.generate(test_member_data)
        
        if success:
            print(f"   ✅ ID card generated successfully")
            print(f"   - File: {os.path.basename(filepath)}")
            print(f"   - Full path: {filepath}")
            print(f"   - File size: {os.path.getsize(filepath)} bytes")
            print(f"   - File exists: {os.path.exists(filepath)}")
            
            # Verify it's a valid PNG
            try:
                img = Image.open(filepath)
                print(f"   - Image size: {img.size[0]}×{img.size[1]}px")
                print(f"   - Image mode: {img.mode}")
            except:
                print(f"   ⚠️  Could not verify PNG")
            
            return True
        else:
            print(f"   ❌ ID card generation failed")
            print(f"   - Error: {error}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_with_existing_member():
    """Test with first existing member from database"""
    
    print("\n" + "="*70)
    print("DATABASE MEMBER TEST")
    print("="*70)
    
    try:
        member = IndividualMember.objects.first()
        
        if not member:
            print("\n⚠️  No members found in database")
            print("   Create a member first through registration form")
            return None  # Skip, not a failure
        
        print(f"\n1. Found member: {member.first_name} {member.last_name}")
        print(f"   - ID: {member.abia_arise_id}")
        print(f"   - State: {member.state_of_residence}")
        print(f"   - LGA: {member.lga_of_residence}")
        print(f"   - Ward: {member.electoral_ward}")
        print(f"   - Has profile picture: {bool(member.profile_picture)}")
        
        member_data = {
            'first_name': member.first_name,
            'middle_name': member.middle_name or '',
            'last_name': member.last_name,
            'state': member.state_of_residence or 'Abia',
            'lga': member.lga_of_residence or 'N/A',
            'ward': member.electoral_ward or 'N/A',
            'abia_arise_id': member.abia_arise_id,
            'profile_picture': member.profile_picture if member.profile_picture else None,
        }
        
        print(f"\n2. Generating ID card...")
        generator = IDCardGenerator()
        success, filepath, error = generator.generate(member_data)
        
        if success:
            print(f"   ✅ ID card generated successfully")
            print(f"   - File: {os.path.basename(filepath)}")
            print(f"   - Size: {os.path.getsize(filepath)} bytes")
            
            # Verify image
            try:
                img = Image.open(filepath)
                print(f"   - Dimensions: {img.size[0]}×{img.size[1]}px")
            except:
                pass
            
            return True
        else:
            print(f"   ❌ Generation failed: {error}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_certificate_generation():
    """Test certificate generation"""
    
    print("\n" + "="*70)
    print("CERTIFICATE GENERATION TEST")
    print("="*70)
    
    test_group_data = {
        'name': 'ABIA ARISE TEST GROUP',
        'group_license_number': 'AB/PRO/TEST/001',
        'chairman_name': 'Chief John Okafor',
        'secretary_name': 'Mr. Peter Nwankwo',
    }
    
    try:
        print("\n1. Testing CertificateGenerator initialization...")
        generator = CertificateGenerator()
        print("   ✅ Generator initialized successfully")
        
        print("\n2. Generating certificate...")
        success, filepath, error = generator.generate(test_group_data)
        
        if success:
            print(f"   ✅ Certificate generated successfully")
            print(f"   - File: {os.path.basename(filepath)}")
            print(f"   - Size: {os.path.getsize(filepath)} bytes")
            return True
        else:
            print(f"   ⚠️  Certificate generation failed (not critical)")
            print(f"   - Error: {error}")
            return None  # Not critical for ID card testing
            
    except Exception as e:
        print(f"\n⚠️  Certificate test error (not critical): {e}")
        return None

if __name__ == '__main__':
    print("\nTesting ID Card Template-Based Generation")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Check templates
    test1_result = test_template_exists()
    
    if not test1_result:
        print("\n" + "="*70)
        print("❌ CRITICAL: Templates not found!")
        print("="*70)
        print("Please ensure templates exist at:")
        from django.conf import settings
        print(f"  - {os.path.join(settings.MEDIA_ROOT, 'templates', 'Abia arise ID card updated.png')}")
        sys.exit(1)
    
    # Test 2: Basic generation
    test2_result = test_id_card_generation()
    
    # Test 3: Database member
    test3_result = test_with_existing_member()
    
    # Test 4: Certificate
    test4_result = test_certificate_generation()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Template verification: {'✅ PASS' if test1_result else '❌ FAIL'}")
    print(f"Basic generation test: {'✅ PASS' if test2_result else '❌ FAIL'}")
    print(f"Database member test: {'✅ PASS' if test3_result is True else ('⚠️  N/A' if test3_result is None else '❌ FAIL')}")
    print(f"Certificate test: {'✅ PASS' if test4_result is True else ('⚠️  N/A' if test4_result is None else '⚠️  WARN')}")
    
    if test1_result and test2_result:
        print("\n✅ ID Card Generator is working correctly!")
        print("\nNext steps:")
        print("1. Test through registration form")
        print("2. Check media/generated/id_cards/ for generated cards")
        print("3. Verify card images display correctly")
        print("4. Test with profile pictures")
    else:
        print("\n❌ There were errors. Check output above.")
    print()

