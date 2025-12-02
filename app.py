from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key_here')

# Email configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/projects')
def projects():
    # Real projects from GitHub
    projects_data = [
        {
            'title': 'Thyroid Detection',
            'description': 'Machine learning pipeline that classifies thyroid conditions using clinical datasets, model evaluation, and deployment-ready notebooks.',
            'image': 'https://via.placeholder.com/400x300?text=Thyroid+Detection',
            'link': 'https://github.com/judejjj/thyroid-detection'
        },
        {
            'title': 'Android To-Do',
            'description': 'Native Android productivity app with task scheduling, reminders, and local persistence built using Kotlin and Jetpack components.',
            'image': 'https://via.placeholder.com/400x300?text=Android+To-Do',
            'link': 'https://github.com/judejjj/android-todo'
        },
        {
            'title': 'Hand Gesture Recognition',
            'description': 'Computer vision project that recognizes hand gestures in real time with OpenCV preprocessing and TensorFlow inference.',
            'image': 'https://via.placeholder.com/400x300?text=Hand+Gesture',
            'link': 'https://github.com/judejjj/hand-gesture-recognition'
        },
        {
            'title': 'Online Movie Review',
            'description': 'Full-stack web app that ingests reviews, performs sentiment analysis, and publishes curated movie insights.',
            'image': 'https://via.placeholder.com/400x300?text=Movie+Review',
            'link': 'https://github.com/judejjj/online-movie-review'
        }
    ]
    return render_template('projects.html', title='Projects', projects=projects_data)

@app.route('/about')
def about():
    skills = [
        {'name': 'Python', 'icon': '🐍'},
        {'name': 'Django', 'icon': '🎸'},
        {'name': 'Linux', 'icon': '🐧'},
        {'name': 'C', 'icon': '©️'},
        {'name': 'SQL', 'icon': '🗄️'},
        {'name': 'AI', 'icon': '🤖'},
        {'name': 'Cybersecurity', 'icon': '🔐'},
        {'name': 'Git', 'icon': '📦'}
    ]
    
    certifications = [
        {
            'name': 'Applied Generative AI',
            'issuer': 'Infosys',
            'date': 'February 2025',
            #'link': 'https://coursera.org/verify/professional-cert/O15B0AZUSLZV',
            'icon': '🤖'
        },
        {
            'name': 'Certified Cybersecurity Analyst',
            'issuer': 'REDTEAM360',
            'date': 'November 2023',
            'link': None,
            'icon': '🛡️'
        },
        {
            'name': 'Acadamor Cyber Security',
            'issuer': 'Acadamor',
            'date': 'October 2023',
            # 'link': 'https://courses.cognitiveclass.ai/certificates/c18331ce9db54575b979654e7d68cf6f',
            'icon': '🧑‍💻'
        }
    ]
    
    return render_template('about.html', title='About Me', skills=skills, certifications=certifications)

def send_email(name, sender_email, message_text):
    """Send email using Gmail SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f'Portfolio Contact Form - Message from {name}'
        
        # Email body
        body = f"""
        New message from your portfolio contact form:
        
        Name: {name}
        Email: {sender_email}
        
        Message:
        {message_text}
        
        ---
        Reply to: {sender_email}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Check if email is configured
        if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
            flash('Email service is not configured. Please contact the administrator.', 'error')
            print("ERROR: Email credentials not found in .env file")
            return redirect(url_for('contact'))
        
        # Send email
        if send_email(name, email, message):
            flash('Thank you for your message! I will get back to you soon.', 'success')
        else:
            flash('Sorry, there was an error sending your message. Please try again later.', 'error')
        
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact')

if __name__ == '__main__':
    app.run(debug=True)
