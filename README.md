# Email Sending and Validation Script

## Overview
This script allows users to send an email with a generated login code. It uses an external API to send the email and validates the code entered by the user. The email contains a unique login code that the user needs to input for authentication.

## Components
1. **EmailResponse Class**: Handles the response received after sending the email, parsing essential details from the API response.
2. **EmailSender Class**: 
   - Sends the email to a recipient using an external API.
   - Validates email formats before sending.

### EmailResponse Class
This class is used to store information about the email sending operation, including:
- **code**: A status code returned from the API.
- **rubika**: A response related to Rubika (if applicable).
- **success**: Boolean indicating whether the email was sent successfully.
- **email_info**: Information about the email (sender, recipient, subject, body).
- **to**: The recipient email address.
- **subject**: The subject of the email.
- **body**: The body/content of the email.
- **from_name**: The name of the sender.
- **from_email**: The sender's email address.
- **send_time**: The time the email was sent.
- **response_state**: Boolean representing the success/failure state of the email sending operation.

### EmailSender Class
This class contains methods for:
- **send_email**: Sends an email via an API.
- **validate_email**: Validates email format using regex.

#### `send_email` Method
Sends an email with a randomly generated code:
- **Parameters**:
  - `to`: The recipient's email address.
  - `subject`: The subject of the email.
  - `body`: The body content of the email.
  - `title`: The sender’s name (default is "Support").
- **Process**:
  - Creates a payload with the provided details.
  - Sends a GET request to the email API.
  - Handles responses: If successful, returns an `EmailResponse` object with email details.
  
#### `validate_email` Method
Validates if the provided email is in the correct format using a regex pattern:
- **Returns**: `True` if valid, `False` otherwise.

## Script Flow
1. The script generates a random login code.
2. The user is prompted to enter an email address.
3. The `send_email` method sends an email to the provided address containing the login code.
4. The user is prompted to input the code they received.
5. If the code entered matches the sent code, the user is logged in successfully. Otherwise, a failure message is displayed.

## Example

```bash
Email You ? user@example.com
```
The user will receive an email with the subject "Login app" and the body containing the generated login code.

```bash
Enter the Code Login: 12345
```
If the correct code is entered, the user is authenticated.

Dependencies
httpx: HTTP client for making requests to the external email API.

re: Regular expression library for email validation.

Conclusion
This script demonstrates how to send a validation code to a user via email and authenticate the user based on the code they provide. It's useful for implementing basic email-based authentication in applications.
