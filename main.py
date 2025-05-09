import httpx
import json

class EmailResponse:
    def __init__(self, code, rubika, success, email_info,to,subject,body,from_name,from_email,send_time,response_state):
        self.code = code
        self.rubika = rubika
        self.success = success
        self.email_info = email_info
        self.send_time = send_time
        self.to = to
        self.subject = subject
        self.body = body
        self.from_name = from_name
        self.from_email = from_email
        self.response_state = response_state

class EmailSender:
    def __init__(self, base_url="https://v3.api-free.ir/email"):
        self.base_url = base_url

    def send_email(self, to, subject, body, title="Support"):
        """
        Sends an email via the specified email sending API.

        :param to: The recipient's email address.
        :param subject: The subject of the email.
        :param body: The body/content of the email.
        :param title: The title of the sender (default: "Support").
        :return: A response message indicating success or failure.
        """
        payload = {
            'to': to,
            'subject': subject,
            'body': body,
            'title': title
        }

        try:
            with httpx.Client(follow_redirects=True) as client:
                response = client.get(self.base_url, params=payload, timeout=20)
            if response.status_code == 200:
                result = response.json()
                if result.get("ok"):
                    email_info = result.get('email_info')
                    return EmailResponse(
                        response_state=result.get('ok'),
                        code=result.get('code'),
                        rubika=result.get('rubika'),
                        success=result.get('success'),
                        email_info=result.get('email_info'),
                        to=email_info.get('to'),
                        subject=email_info.get('subject'),
                        body=email_info.get('body'),
                        from_name=email_info.get('from_name'),
                        from_email=email_info.get('from_email'),
                        send_time=email_info.get('send_time'),
                    )
                else:
                    print(f"Email sending failed: {result.get('error')}")
            else:
                print(f"Error in sending request to the API: {response.status_code} - {response.text}")
        
        except httpx.RequestError as e:
            print(f"An error occurred while connecting to the email service API: {e}")

    def validate_email(self, email):
        import re
        email_regex = r"(^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA0-9]{2,}$)"
        return re.match(email_regex, email) is not None

client = EmailSender()
import random
while True:
    code = random.randint(11111,99999)
    to_email = input("Email You ? ")
    subject = "Login app"
    body = f"Code Login in App : {code}"
    title = "Login"
    response = client.send_email(to_email, subject, body, title)
    if response.response_state:
        code_input : int = int(input("Enter the Code Login : "))
        if code == code_input:
            print("Login Ok")
            break
        else:
            print("Login No")
