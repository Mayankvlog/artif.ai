"""
ArtifAI - AI Image Generation Platform
A web application for generating and managing AI-created images.

This is a fully consolidated file that contains all application logic:
- Flask application setup and entry point
- Database models and configuration
- Image generation functionality
- Application routes and API endpoints
"""

import os
import sys
import logging
from datetime import datetime
from urllib.parse import urlparse

# Flask and SQLAlchemy imports
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

# OpenAI
import openai

#--------------------------------------------
# Application Setup & Configuration
#--------------------------------------------
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database base class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with model class
db = SQLAlchemy(model_class=Base)

# Create Flask application
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Apply proxy fix for proper URL generation behind proxies
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
logger.info(f"Using database with URL: {app.config['SQLALCHEMY_DATABASE_URI'][:12]}...")

# Initialize database with app
db.init_app(app)

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Set up OpenAI API key
app.config['OPENAI_API_KEY'] = os.environ.get("OPENAI_API_KEY")

# Configure OpenAI
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Check if API key is set
if not openai.api_key:
    logger.warning("OpenAI API key not found in environment variables.")

#--------------------------------------------
# AI Image Generation Functionality
#--------------------------------------------
def generate_image(prompt, style=None, size="1024x1024"):
    """Generate an image using AI.
    
    Args:
        prompt (str): The text prompt to generate an image from
        style (str, optional): Style modifier for the image
        size (str, optional): Size of the generated image
    
    Returns:
        dict: Contains the URL of the generated image
    """
    try:
        # Enhance prompt with style if provided
        full_prompt = prompt
        if style and style != "default":
            style_prompts = {
                "abstract": "Create an abstract art piece with vibrant colors and geometric shapes: ",
                "realistic": "Create a photorealistic image with intricate details: ",
                "anime": "Create an anime-style illustration with vibrant colors: ",
                "painterly": "Create a painting in the style of a classical artist with visible brushstrokes: ",
                "3d": "Create a 3D rendered image with strong lighting and textures: ",
                "minimalist": "Create a minimalist design with clean lines and limited color palette: "
            }
            if style in style_prompts:
                full_prompt = style_prompts[style] + prompt
        
        # Use the API to generate an image
        response = openai.Image.create(
            model="dall-e-3",  # Image generation model
            prompt=full_prompt,
            n=1,
            size=size
        )
        
        return {"success": True, "url": response["data"][0]["url"]}
    except Exception as e:
        logger.error(f"Error generating image: {e}")
        return {"success": False, "error": str(e)}

#--------------------------------------------
# Database Models
#--------------------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    images = db.relationship('Image', backref='creator', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def __repr__(self):
        return f'<User {self.username}>'

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    style = db.Column(db.String(50), default='default')
    aspect_ratio = db.Column(db.String(20), default='1:1')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_favorite = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<Image {self.id} by User {self.user_id}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#--------------------------------------------
# Helper Functions
#--------------------------------------------
def get_sample_images():
    """Return a list of sample AI-generated images.
    
    This is used when the user hasn't generated any images or for display purposes.
    These are pre-fetched images from Unsplash.
    """
    return [
        {
            "id": "sample1",
            "url": "https://images.unsplash.com/photo-1471666875520-c75081f42081",
            "prompt": "Surreal landscape with floating islands",
            "style": "abstract"
        },
        {
            "id": "sample2",
            "url": "https://images.unsplash.com/photo-1459908676235-d5f02a50184b",
            "prompt": "Dreamy forest with luminescent elements",
            "style": "painterly"
        },
        {
            "id": "sample3",
            "url": "https://images.unsplash.com/photo-1577083552792-a0d461cb1dd6",
            "prompt": "Classical painting of mythological scene",
            "style": "realistic"
        },
        {
            "id": "sample4",
            "url": "https://images.unsplash.com/photo-1578301978018-3005759f48f7",
            "prompt": "Portrait in renaissance style",
            "style": "painterly"
        },
        {
            "id": "sample5",
            "url": "https://images.unsplash.com/photo-1579541591970-e5780dc6b31f",
            "prompt": "Abstract landscape with dramatic lighting",
            "style": "abstract"
        },
        {
            "id": "sample6",
            "url": "https://images.unsplash.com/photo-1482160549825-59d1b23cb208",
            "prompt": "Futuristic city with neon lights",
            "style": "3d"
        },
        {
            "id": "sample7",
            "url": "https://images.unsplash.com/photo-1619472032094-eadb7ec01655",
            "prompt": "Digital abstract composition with geometric shapes",
            "style": "minimalist"
        },
        {
            "id": "sample8",
            "url": "https://images.unsplash.com/photo-1619472376731-3ca648a34b69",
            "prompt": "Futuristic abstract art with flowing lines",
            "style": "abstract"
        },
        {
            "id": "sample9",
            "url": "https://images.unsplash.com/photo-1619472351888-f844a0b33f5b",
            "prompt": "Minimalist geometric composition in bold colors",
            "style": "minimalist"
        },
        {
            "id": "sample10",
            "url": "https://images.unsplash.com/photo-1506097425191-7ad538b29cef",
            "prompt": "Creative workspace with design elements",
            "style": "realistic"
        },
        {
            "id": "sample11",
            "url": "https://images.unsplash.com/photo-1523726491678-bf852e717f6a",
            "prompt": "Artistic design elements with bold colors",
            "style": "abstract"
        },
        {
            "id": "sample12",
            "url": "https://images.unsplash.com/photo-1531403009284-440f080d1e12",
            "prompt": "Digital creative workspace with geometric shapes",
            "style": "minimalist"
        },
        {
            "id": "sample13",
            "url": "https://images.unsplash.com/photo-1471666875520-c75081f42081",
            "prompt": "Digital art with natural elements",
            "style": "painterly"
        }
    ]

#--------------------------------------------
# Routes
#--------------------------------------------
@app.route('/')
def index():
    """Home page route, displays introduction to ArtifAI"""
    samples = get_sample_images()[:6]  # Get first 6 sample images
    return render_template('index.html', samples=samples)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route"""
    if current_user.is_authenticated:
        return redirect(url_for('generator'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user)
        
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('generator')
        
        return redirect(next_page)
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('generator'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout route"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/generator')
@login_required
def generator():
    """Image generation interface route"""
    return render_template('generator.html')

@app.route('/api/generate', methods=['POST'])
@login_required
def api_generate():
    """API endpoint for image generation"""
    data = request.json
    prompt = data.get('prompt')
    style = data.get('style', 'default')
    aspect_ratio = data.get('aspectRatio', '1:1')
    
    if not prompt:
        return jsonify({'success': False, 'error': 'Prompt is required'}), 400
    
    # Map aspect ratio to image generation service compatible size
    size_map = {
        '1:1': '1024x1024',
        '16:9': '1792x1024',
        '9:16': '1024x1792'
    }
    size = size_map.get(aspect_ratio, '1024x1024')
    
    # Generate image using the image generation service
    result = generate_image(prompt, style, size)
    
    if not result.get('success'):
        return jsonify(result), 500
    
    # Save image to database
    image = Image(
        user_id=current_user.id,
        prompt=prompt,
        image_url=result['url'],
        style=style,
        aspect_ratio=aspect_ratio
    )
    
    db.session.add(image)
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'image': {
            'id': image.id,
            'url': image.image_url,
            'prompt': image.prompt,
            'style': image.style,
            'aspect_ratio': image.aspect_ratio,
            'created_at': image.created_at.isoformat()
        }
    })

@app.route('/gallery')
@login_required
def gallery():
    """User's gallery of generated images"""
    return render_template('gallery.html')

@app.route('/api/images')
@login_required
def api_images():
    """API endpoint to get user's images"""
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    
    # Query images
    images_query = Image.query.filter_by(user_id=current_user.id)
    
    # Sort by newest first
    images_query = images_query.order_by(Image.created_at.desc())
    
    # Paginate
    images_paginated = images_query.paginate(page=page, per_page=per_page)
    
    # Format response
    images = []
    for img in images_paginated.items:
        images.append({
            'id': img.id,
            'url': img.image_url,
            'prompt': img.prompt,
            'style': img.style,
            'aspect_ratio': img.aspect_ratio,
            'created_at': img.created_at.isoformat(),
            'is_favorite': img.is_favorite
        })
    
    return jsonify({
        'images': images,
        'total': images_paginated.total,
        'pages': images_paginated.pages,
        'page': page
    })

@app.route('/api/images/<int:image_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(image_id):
    """Toggle favorite status of an image"""
    image = Image.query.filter_by(id=image_id, user_id=current_user.id).first()
    
    if not image:
        return jsonify({'success': False, 'error': 'Image not found'}), 404
    
    image.is_favorite = not image.is_favorite
    db.session.commit()
    
    return jsonify({'success': True, 'is_favorite': image.is_favorite})

@app.route('/api/images/<int:image_id>', methods=['DELETE'])
@login_required
def delete_image(image_id):
    """Delete an image"""
    image = Image.query.filter_by(id=image_id, user_id=current_user.id).first()
    
    if not image:
        return jsonify({'success': False, 'error': 'Image not found'}), 404
    
    db.session.delete(image)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/profile')
@login_required
def profile():
    """User profile page"""
    # Count total images
    image_count = Image.query.filter_by(user_id=current_user.id).count()
    
    # Count favorite images
    favorite_count = Image.query.filter_by(user_id=current_user.id, is_favorite=True).count()
    
    return render_template('profile.html', image_count=image_count, favorite_count=favorite_count)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('index.html'), 500

#--------------------------------------------
# Database Status
#--------------------------------------------
@app.route('/api/database-status')
@login_required
def database_status():
    """API endpoint to check database connection status"""
    try:
        # Check if we can query the database
        user_count = User.query.count()
        image_count = Image.query.count()
        
        db_type = "Unknown"
        if "mysql" in app.config["SQLALCHEMY_DATABASE_URI"]:
            db_type = "MySQL"
        elif "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"]:
            db_type = "SQLite"
        elif "postgresql" in app.config["SQLALCHEMY_DATABASE_URI"]:
            db_type = "PostgreSQL"
            
        return jsonify({
            'status': 'connected',
            'database_type': db_type,
            'user_count': user_count,
            'image_count': image_count
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

#--------------------------------------------
# Database Initialization
#--------------------------------------------
with app.app_context():
    db.create_all()

#--------------------------------------------
# Main Entry Point
#--------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)