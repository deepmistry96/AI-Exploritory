import email
import os

def parse_eml(eml_path):
    with open(eml_path, 'rb') as eml_file:
        eml_message = email.message_from_binary_file(eml_file)
        print("Subject:", eml_message['Subject'])
        print("From:", eml_message['From'])
        print("To:", eml_message['To'])
        print("Date:", eml_message['Date'])
        print("\nBody:")
        # Extract and print the body of the email
        for part in eml_message.walk():
            if part.get_content_type() == 'text/plain':
                print(part.get_payload(decode=True).decode(part.get_content_charset()))

# Example usage:
eml_path = 'E:/Repo/findtitle.eml'  # Provide the full path to your EML file
if os.path.exists(eml_path):
    parse_eml(eml_path)
else:
    print("File not found:", eml_path)
