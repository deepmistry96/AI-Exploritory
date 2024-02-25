import mailbox

def parse_mbox(file_path):
    mbox = mailbox.mbox(file_path)
    
    for message in mbox:
        print("From:", message["From"])
        print("Subject:", message["Subject"])
        print("Date:", message["Date"])
        print("Body:", message.get_payload())
        print("Done ")

parse_mbox("E:\Repo\Scratch Emails\Takeout\Mail\data.mbox")
