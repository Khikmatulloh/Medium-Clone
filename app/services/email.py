def send_email_verification(email: str, token: str):
    """Email yuborish logikasi (Mock versiya)"""
    link = f"http://localhost:8000/verify?token={token}"
    print(f"Verification email sent to {email}: {link}")
