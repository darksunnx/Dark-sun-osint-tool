import random
import string

def generate_password(length=12, use_special_chars=True):
    """Generate a random password with specified length"""
    chars = string.ascii_letters + string.digits
    if use_special_chars:
        chars += string.punctuation
    
    return ''.join(random.choice(chars) for _ in range(length))

def validate_phone(phone):
    """Validate phone number format"""
    return phone.isdigit() and len(phone) >= 10

def validate_passport(passport):
    """Validate passport number format"""
    passport = passport.replace(" ", "")
    return len(passport) >= 6 and passport.isalnum()

def validate_snils(snils):
    """Validate SNILS number format"""
    return snils.isdigit() and len(snils) == 11

def format_phone(phone):
    """Format phone number for display"""
    phone = ''.join(filter(str.isdigit, phone))
    if len(phone) == 11:
        return f"+{phone[0]} ({phone[1:4]}) {phone[4:7]}-{phone[7:9]}-{phone[9:]}"
    return phone
