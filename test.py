import requests
import random
import time




user_email = "mahdiahmadi.1208@gmail.com"





otp_storage = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp, app_name="rubka"):
    url = "https://mail.rubka.ir"
    html_body = (
        '<!DOCTYPE html>'
        '<html lang="en">'
        '<head>'
            '<meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<style>'
                'body { font-family: \'Segoe UI\', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 0; background-color: #f4f7f6; }'
                '.container { max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); overflow: hidden; }'
                '.header { background: linear-gradient(135deg, #4a90e2 0%, #50e3c2 100%); color: white; padding: 40px; text-align: center; }'
                '.header h1 { margin: 0; font-size: 28px; }'
                '.content { padding: 30px 40px; color: #555; line-height: 1.7; }'
                '.content p { margin: 0 0 20px; }'
                '.otp-code { display: block; width: fit-content; margin: 20px auto; padding: 15px 30px; background-color: #eef5ff; border: 1px dashed #4a90e2; border-radius: 8px; font-size: 36px; font-weight: bold; color: #0d47a1; letter-spacing: 5px; }'
                '.warning { font-size: 14px; color: #888; text-align: center; }'
                '.footer { background-color: #f4f7f6; padding: 20px 40px; text-align: center; font-size: 12px; color: #aaa; border-top: 1px solid #e0e0e0; }'
            '</style>'
        '</head>'
        '<body>'
            f'<div class="container">'
                '<div class="header">'
                    '<h1>Verification Code</h1>'
                '</div>'
                '<div class="content">'
                    '<p>Hello,</p>'
                    f'<p>Thank you for registering with <strong>{app_name}</strong>. Please use the following One-Time Password (OTP) to complete your action.</p>'
                    f'<div class="otp-code">{otp}</div>'
                    '<p class="warning">This code is valid for 5 minutes. If you did not request this code, please ignore this email.</p>'
                '</div>'
                '<div class="footer">'
                    f'&copy; {time.strftime("%Y")} {app_name}. All rights reserved.'
                '</div>'
            '</div>'
        '</body>'
        '</html>'
    )
    data = {
        "to": email,
        "subject": f"Your {app_name} Verification Code",
        "body": html_body,
        "title": "Support" 
    }

    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the email: {e}")
        return {"status": "error", "message": str(e)}

def request_otp(email):
    otp = generate_otp()
    otp_storage[email] = {
        "code": otp,
        "timestamp": time.time(),
        "attempts": 0
    }
    print(f"Generated OTP {otp} for {email}")
    return send_otp_email(email, otp, app_name="rubka")

def verify_otp(email, user_input_otp):
    if email not in otp_storage:
        return False, "No OTP was requested for this email address. Please request a new one."
    
    otp_info = otp_storage[email]
    
    if time.time() - otp_info["timestamp"] > 300:
        del otp_storage[email]  
        return False, "The OTP has expired. Please request a new one."
    
    if otp_info["code"] == user_input_otp:
        del otp_storage[email]  
        return True, "OTP verification successful!"
    else:
        
        otp_storage[email]["attempts"] += 1
        if otp_storage[email]["attempts"] >= 3:
            del otp_storage[email]
            return False, "Invalid OTP. You have reached the maximum number of attempts."
        return False, "Invalid OTP. Please try again."


if __name__ == "__main__":

    print("Requesting OTP...")
    response = request_otp(user_email)
    print("API Response:", response)
    if response.get('status') == 'success':
        user_code = input("Please enter the 6-digit OTP you received in your email: ")
        is_successful, message = verify_otp(user_email, user_code.strip())
        print(f"\nVerification Status: {is_successful}")
        print(f"Message: {message}")
