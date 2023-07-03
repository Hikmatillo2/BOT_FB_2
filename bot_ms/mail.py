import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mail:
    def __init__(self, text: str, subject: str, destination: list, username: str):
        self.email = 'dolgovdaniil007@gmail.com'
        self.password = 'syoeggpdefmhvwvg'
        self.server = smtplib.SMTP('smtp.gmail.com', 587)
        self.text = text
        self.subject = subject
        self.destination = destination
        self.username = username

    def server_init(self):
        self.server.starttls()
        self.server.login(self.email, self.password)
        self.server.ehlo()

    def compile_mail(self):
        email = MIMEMultipart('alternative')
        email['From'] = self.email
        email['To'] = ", ".join(self.destination)
        email['Subject'] = self.subject

        html = f"""
        <html>
          <body>
            <div style="color: green; 
            font-family: montserrat; 
            width: 100%;">
                Привет! Это бот ФБ!
            </div>
            </br>
            </br>
            <div>
                {self.text}
            </div>
            </br>
            </br>
            <div style="color: green; font-family: montserrat ">
                Это сообщение отправлено пользователем: <b>@{self.username}</b>
            </div>
          </body>
        </html>"""
        part1 = MIMEText("Это сообщение было отправлено ботом ФБ", 'plain')
        part2 = MIMEText(html, 'html')
        email.attach(part1)
        email.attach(part2)
        return email.as_string()

    def send_mail(self):
        self.server_init()
        self.server.sendmail(self.email, self.destination, self.compile_mail())
        self.quit()

    def quit(self):
        self.server.quit()
