import smtplib
import csv
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging


def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def main():
    message_template = read_template('template.txt')
    MY_ADDRESS = "your_email@gmail.com"
    PASSWORD = "your_password"

    logging.basicConfig(filename='email_log.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)

    with open("details.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for lines in csv_reader:
            msg = MIMEMultipart()
            message = message_template.substitute(PERSON_NAME=lines[0], MATH=lines[2], ENG=lines[3], SCI=lines[4])
            msg['From'] = MY_ADDRESS
            msg['To'] = lines[1]
            msg['Subject'] = "Mid term grades"
            msg.attach(MIMEText(message, 'plain'))

            filename = "attachment.pdf"
            attachment = open("path_to_attachment/attachment.pdf", "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {filename}")
            msg.attach(part)

            try:
                s.send_message(msg)
                logging.info(f"Email sent to {lines[1]}")
            except Exception as e:
                logging.error(f"Failed to send email to {lines[1]}: {str(e)}")

            del msg

    s.quit()


if __name__ == '__main__':
    main()
