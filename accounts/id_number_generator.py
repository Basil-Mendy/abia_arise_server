"""
Utility module for generating ID numbers and license numbers
Following the format:
- Individual: AB/{LGA_ACRONYM}/{SERIAL_NUMBER}
- Group: AB/PRG/{LGA_ACRONYM}/{SERIAL_NUMBER}
"""
from django.db import models

# LGA Acronyms mapping
LGA_ACRONYMS = {
    'Aba North': 'ABN',
    'Aba South': 'ABS',
    'Arochukwu': 'ARO',
    'Bende': 'BEN',
    'Ikwuano': 'IKW',
    'Isiala Ngwa North': 'ISN',
    'Isiala Ngwa South': 'ISS',
    'Isuikwuato': 'ISU',
    'Obingwu': 'OBI',
    'Ohafia': 'OHA',
    'Osisioma': 'OSI',
    'Ugwunagbo': 'UGW',
    'Umuahia North': 'UMN',
    'Ukwa East': 'UKE',
    'Ukwa West': 'UKW',
    'Umuahia South': 'UMS',
    'Umunneochi': 'UNE',
}


def get_lga_acronym(lga_name):
    """
    Get the acronym for a given LGA name.
    
    Args:
        lga_name (str): Full name of the LGA
        
    Returns:
        str: LGA acronym (3 letters), or first 3 letters if not found
    """
    # Try exact match first
    if lga_name in LGA_ACRONYMS:
        return LGA_ACRONYMS[lga_name]
    
    # Try case-insensitive match
    for key, value in LGA_ACRONYMS.items():
        if key.lower() == lga_name.lower():
            return value
    
    # Fallback: use first 3 letters uppercase
    return lga_name[:3].upper()


def generate_individual_id(lga_of_origin):
    """
    Generate individual member ID in format: AB/{LGA_ACRONYM}/{SERIAL_NUMBER}
    Example: AB/UMS/001
    
    Args:
        lga_of_origin (str): LGA of origin for the member
        
    Returns:
        str: Generated ID number
    """
    from .models import IndividualMember
    
    lga_acronym = get_lga_acronym(lga_of_origin)
    
    # Get the count of existing members with this LGA acronym
    # to determine the next serial number
    existing_ids = IndividualMember.objects.filter(
        abia_arise_id__startswith=f"AB/{lga_acronym}/"
    ).count()
    
    # Serial number starts from 001
    serial_number = str(existing_ids + 1).zfill(3)
    
    return f"AB/{lga_acronym}/{serial_number}"


def generate_group_license_number(lga):
    """
    Generate pro-group license number in format: AB/PRG/{LGA_ACRONYM}/{SERIAL_NUMBER}
    Example: AB/PRG/UMS/001
    
    Args:
        lga (str): LGA for the pro-group
        
    Returns:
        str: Generated license number
    """
    from .models import ProGroup
    
    lga_acronym = get_lga_acronym(lga)
    
    # Get the count of existing groups with this LGA acronym
    # to determine the next serial number
    existing_licenses = ProGroup.objects.filter(
        group_license_number__startswith=f"AB/PRG/{lga_acronym}/"
    ).count()
    
    # Serial number starts from 001
    serial_number = str(existing_licenses + 1).zfill(3)
    
    return f"AB/PRG/{lga_acronym}/{serial_number}"
