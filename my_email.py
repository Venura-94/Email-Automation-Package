import content
import os
from dotenv import load_dotenv
from pathlib import Path
import smtplib
from email.message import EmailMessage
import datetime

# Load environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# Read environment variables
sender_email = os.getenv("SENDER_EMAIL")
password_email = os.getenv("SENDER_PASSWORD")

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

class DailyDigestEmail:
    def __init__(self):
        self.sender_credentials = {'email': sender_email, 'password': password_email} 
        self.recipients_list = ['venurajithmal@gmail.com']
        self.load_content()

    def load_content(self):
        """
        Load content for the email.
        """
        self.content = {
            'quote': {'include': True, 'content': content.get_random_quote()},
            'weather': {'include': True, 'content': content.get_weather_forecast()},
            'wikipedia': {'include': True, 'content': content.get_wikipedia_article()}
        }
    
    def send_email(self):
        # build email message
        msg = EmailMessage()
        msg['Subject'] = f'Daily Digest - {datetime.date.today().strftime("%d %b %Y")}'
        msg['From'] = self.sender_credentials['email']
        msg['To'] = ', '.join(self.recipients_list)

        # add Plaintext and HTML content
        msg_body = self.format_message()
        msg.set_content(msg_body['text'])
        msg.add_alternative(msg_body['html'], subtype='html')

        # secure connection with STMP server and send email
        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()
            server.login(self.sender_credentials['email'], self.sender_credentials['password'])
            server.send_message(msg)

    def format_message(self):
        ## Generate Plaintext ##
        text = f'*~*~*~*~* Daily Digest - {datetime.date.today().strftime("%d %b %Y")} *~*~*~*~*\n\n'

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            text += '*~*~* Quote of the Day *~*~*\n\n'
            text += f'"{self.content["quote"]["content"]["quote"]}" - {self.content["quote"]["content"]["author"]}\n\n'

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            text += f'*~*~* Forecast for {self.content["weather"]["content"]["city"]}, {self.content["weather"]["content"]["country"]} *~*~*\n\n'
            for forecast in self.content['weather']['content']['periods']:
                text += f'{forecast["timestamp"].strftime("%d %b %H%M")} - {forecast["temp"]}\u00B0C | {forecast["description"]}\n'
            text += '\n'

        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            text += '*~*~* Daily Random Learning *~*~*\n\n'
            text += f'{self.content["wikipedia"]["content"]["title"]}\n{self.content["wikipedia"]["content"]["extract"]}'
        
       ## Generate HTML ##
        html = f"""<html>
    <body>
    <center>
        <h1>Daily Digest - {datetime.date.today().strftime('%d %b %Y')}</h1>
        """

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            html += f"""
        <h2>Quote of the Day</h2>
        <i>"{self.content['quote']['content']['quote']}"</i> - {self.content['quote']['content']['author']}
        """

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            html += f"""
        <h2>Forecast for {self.content['weather']['content']['city']}, {self.content['weather']['content']['country']}</h2> 
        <table>
                    """

            for forecast in self.content['weather']['content']['periods']:
                html += f"""
            <tr>
                <td>
                    {forecast['timestamp'].strftime('%d %b %H%M')}
                </td>
                <td>
                    <img src="{forecast['icon']}">
                </td>
                <td>
                    {forecast['temp']}\u00B0C | {forecast['description']}
                </td>
            </tr>
                        """               

            html += """
            </table>
                    """
        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            html += f"""
        <h2>Daily Random Learning</h2>
        <h3><a href="{self.content['wikipedia']['content']['url']}">{self.content['wikipedia']['content']['title']}</a></h3>
        <table width="800">
            <tr>
                <td>{self.content['wikipedia']['content']['extract']}</td>
            </tr>
        </table>
                    """

        # footer
        html += """
    </center>
    </body>
</html>
                """

        return {'text': text, 'html': html}

if __name__ == '__main__':
    email = DailyDigestEmail()

    ##### test format_message() #####
    print('\nTesting email body generation...')
    message = email.format_message()

    # print Plaintext and HTML messages
    print('\nPlaintext email body is...')
    print(message['text'])
    print('\n------------------------------------------------------------')
    print('\nHTML email body is...')
    print(message['html'])

    # save Plaintext and HTML messages to file
    with open('message_text.txt', 'w', encoding='utf-8') as f:
        f.write(message['text'])
    with open('message_html.html', 'w', encoding='utf-8') as f:
        f.write(message['html'])


    ##### test send_email() #####
    print('\nSending test email...')
    email.send_email()
