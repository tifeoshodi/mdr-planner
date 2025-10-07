"""
App 3: Discipline Dashboard
User login, view assigned portfolios, submit updates, Kanban board
"""

import os
import sys
import json
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.utils import secure_filename

# Add parent directory to path to import shared modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import db, User, Portfolio, Discipline, Document, Submission, TeamMembership
from shared.database import init_db, get_db_uri
from shared.auth import login_required, get_current_user, get_user_portfolios, get_user_disciplines, user_can_access_portfolio
from mdr_stages_config import STANDARD_STAGES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-dashboard'
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size
app.config['ALLOWED_EMAIL_DOMAIN'] = 'ieslglobal.com'  # Domain restriction for email

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
init_db(app)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'dwg', 'xlsx', 'xls', 'doc', 'docx', 'zip', 'rar', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_email_domain(email):
    """Validate email domain is @ieslglobal.com"""
    if not email or '@' not in email:
        return False
    domain = email.split('@')[1].lower()
    return domain == app.config['ALLOWED_EMAIL_DOMAIN']


def get_document_stats_for_portfolio(user, portfolio_id):
    """Calculate document statistics for a user's portfolio"""
    user_disciplines = get_user_disciplines(user, portfolio_id)
    discipline_ids = [d.id for d in user_disciplines]
    
    all_docs = Document.query.filter(Document.discipline_id.in_(discipline_ids)).all()
    
    stats = {
        'total': len(all_docs),
        'pending': 0,
        'submitted': 0,
        'approved': 0,
        'overdue': 0,
        'requires_attention': []
    }
    
    for doc in all_docs:
        status = (doc.current_status or '').lower()
        
        # Check if document has client feedback (requires attention)
        for stage in STANDARD_STAGES:
            stage_code = stage['code'].lower()
            date_received = getattr(doc, f'{stage_code}_date_received', None)
            if date_received:
                # Has feedback - requires attention
                stats['requires_attention'].append(doc)
                break
        
        # Categorize by status
        if 'afc' in status or 'approved' in status:
            stats['approved'] += 1
        elif 'client' in status or 'review' in status or 'submitted' in status:
            stats['submitted'] += 1
        elif 'draft' in status or not status:
            stats['pending'] += 1
    
    return stats


@app.route('/')
def index():
    """Main Dashboard Home - shows widgets, quick actions, and actionable items"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    # Get all portfolios user has access to
    portfolios = get_user_portfolios(user)
    
    # Aggregate stats across all portfolios
    total_stats = {
        'pending': 0,
        'submitted': 0,
        'approved': 0,
        'overdue': 0,
        'requires_attention': []
    }
    
    portfolio_stats = []
    for portfolio in portfolios:
        stats = get_document_stats_for_portfolio(user, portfolio.id)
        portfolio_stats.append({
            'portfolio': portfolio,
            'stats': stats
        })
        
        # Aggregate
        total_stats['pending'] += stats['pending']
        total_stats['submitted'] += stats['submitted']
        total_stats['approved'] += stats['approved']
        total_stats['overdue'] += stats['overdue']
        total_stats['requires_attention'].extend(stats['requires_attention'])
    
    # Get recent submissions
    user_discipline_ids = []
    for portfolio in portfolios:
        user_disciplines = get_user_disciplines(user, portfolio.id)
        user_discipline_ids.extend([d.id for d in user_disciplines])
    
    recent_submissions = Submission.query.filter_by(submitted_by=user.id).order_by(
        Submission.created_at.desc()
    ).limit(5).all()
    
    return render_template('dashboard_home.html',
                         user=user,
                         portfolio_stats=portfolio_stats,
                         total_stats=total_stats,
                         recent_submissions=recent_submissions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with email domain validation"""
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        
        # Validate email domain
        if not validate_email_domain(email):
            flash(f'Invalid email domain. Only @{app.config["ALLOWED_EMAIL_DOMAIN"]} emails are allowed.', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash(f'Welcome, {user.name}!', 'success')
            
            # Redirect to next URL if provided
            next_url = request.args.get('next')
            if next_url:
                return redirect(next_url)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', allowed_domain=app.config['ALLOWED_EMAIL_DOMAIN'])


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/portfolios/<int:portfolio_id>')
@login_required
def view_portfolio(portfolio_id):
    """View portfolio - redirect to document list"""
    return redirect(url_for('document_list', portfolio_id=portfolio_id))


@app.route('/portfolios/<int:portfolio_id>/documents')
@login_required
def document_list(portfolio_id):
    """Document List View - filterable and sortable table"""
    user = get_current_user()
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    # Check access
    if not user_can_access_portfolio(user, portfolio_id):
        flash('You do not have access to this portfolio', 'danger')
        return redirect(url_for('index'))
    
    # Get user's disciplines
    user_disciplines = get_user_disciplines(user, portfolio_id)
    discipline_ids = [d.id for d in user_disciplines]
    
    # Get all documents for user's disciplines
    documents = Document.query.filter(Document.discipline_id.in_(discipline_ids)).order_by(Document.doc_number).all()
    
    # Get statistics
    stats = get_document_stats_for_portfolio(user, portfolio_id)
    
    return render_template('document_list.html',
                         portfolio=portfolio,
                         documents=documents,
                         user_disciplines=user_disciplines,
                         stats=stats,
                         user=user)


@app.route('/portfolios/<int:portfolio_id>/kanban')
@login_required
def kanban_board(portfolio_id):
    """Kanban board view for user's documents"""
    user = get_current_user()
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    # Check access
    if not user_can_access_portfolio(user, portfolio_id):
        flash('You do not have access to this portfolio', 'danger')
        return redirect(url_for('index'))
    
    # Get user's disciplines
    user_disciplines = get_user_disciplines(user, portfolio_id)
    discipline_ids = [d.id for d in user_disciplines]
    
    # Get all documents for user's disciplines
    all_docs = Document.query.filter(Document.discipline_id.in_(discipline_ids)).all()
    
    # Organize documents by stage (To Do, Submitted, Client Review, Approved)
    kanban_columns = {
        'To Do': [],
        'Submitted': [],
        'Client Review': [],
        'Approved': []
    }
    
    for doc in all_docs:
        status = (doc.current_status or '').lower()
        
        # Determine which column based on status
        if 'afc' in status or 'approved for construction' in status:
            kanban_columns['Approved'].append(doc)
        elif 'client' in status or 'review' in status or 'awaiting' in status:
            kanban_columns['Client Review'].append(doc)
        elif 'submitted' in status or any(getattr(doc, f'{s["code"].lower()}_date_sent', None) for s in STANDARD_STAGES):
            kanban_columns['Submitted'].append(doc)
        else:
            kanban_columns['To Do'].append(doc)
    
    # Get statistics
    stats = get_document_stats_for_portfolio(user, portfolio_id)
    
    return render_template('kanban_view.html',
                         portfolio=portfolio,
                         kanban_columns=kanban_columns,
                         stats=stats,
                         user=user)


@app.route('/documents/<int:document_id>')
@login_required
def view_document(document_id):
    """View document details and feedback"""
    return redirect(url_for('view_feedback', document_id=document_id))


@app.route('/documents/<int:document_id>/feedback')
@login_required
def view_feedback(document_id):
    """Client Feedback Viewer - shows all client feedback for document"""
    user = get_current_user()
    document = Document.query.get_or_404(document_id)
    
    # Check if user has access to this document's portfolio
    if not user_can_access_portfolio(user, document.portfolio_id):
        flash('You do not have access to this document', 'danger')
        return redirect(url_for('index'))
    
    # Get submission history
    submissions = Submission.query.filter_by(document_id=document_id).order_by(Submission.created_at.desc()).all()
    
    # Collect feedback data from MDR for all stages
    feedback_data = []
    for stage in STANDARD_STAGES:
        stage_code = stage['code'].lower()
        date_received = getattr(document, f'{stage_code}_date_received', None)
        
        if date_received:
            feedback_data.append({
                'stage': stage['code'],
                'stage_name': stage['name'],
                'date_received': date_received,
                'tr_received': getattr(document, f'{stage_code}_tr_received', ''),
                'rev_status': getattr(document, f'{stage_code}_rev_status', ''),
                'issue_for': getattr(document, f'{stage_code}_issue_for', ''),
                'next_rev': getattr(document, f'{stage_code}_next_rev', '') if stage['has_next_rev'] else None,
                'date_sent': getattr(document, f'{stage_code}_date_sent', ''),
                'tr_no': getattr(document, f'{stage_code}_tr_no', '')
            })
    
    return render_template('feedback_viewer.html',
                         document=document,
                         feedback_data=feedback_data,
                         submissions=submissions,
                         stages=STANDARD_STAGES,
                         user=user)


@app.route('/documents/<int:document_id>/submit', methods=['GET', 'POST'])
@login_required
def submit_document(document_id):
    """Submit document update (draft or final submission with files)"""
    user = get_current_user()
    document = Document.query.get_or_404(document_id)
    
    # Check access
    if not user_can_access_portfolio(user, document.portfolio_id):
        flash('You do not have access to this document', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get('action')  # 'draft' or 'submit'
        stage = request.form.get('stage')
        
        if not stage:
            flash('Please select a submission stage', 'danger')
            return redirect(url_for('submit_document', document_id=document_id))
        
        # Validate stage
        if stage not in [s['code'] for s in STANDARD_STAGES]:
            flash('Invalid submission stage', 'danger')
            return redirect(url_for('submit_document', document_id=document_id))
        
        stage_code = stage.lower()
        
        # Get form data
        revision = request.form.get('revision', '').strip()
        status = request.form.get('status', '').strip()
        planned_date = request.form.get('planned_date', '').strip()
        actual_date = request.form.get('actual_date', '').strip()
        notes = request.form.get('notes', '').strip()
        
        # Update document MDR fields (both draft and submit update MDR immediately)
        setattr(document, f'{stage_code}_date_planned', planned_date)
        setattr(document, f'{stage_code}_date_actual', actual_date)
        
        # Update current status
        document.current_revision = revision
        document.current_status = status
        if notes:
            document.remarks = notes
        
        file_path = None
        
        # If final submission (not draft), require file upload
        if action == 'submit':
            if 'file' not in request.files or not request.files['file'].filename:
                flash('Please attach a file for submission', 'danger')
                return redirect(url_for('submit_document', document_id=document_id))
            
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # Update date_sent in MDR
                setattr(document, f'{stage_code}_date_sent', datetime.now().strftime('%Y-%m-%d'))
                
                # Create submission record
                submission = Submission(
                    document_id=document_id,
                    submitted_by=user.id,
                    stage=stage,
                    submitted_revision=revision,
                    date_sent=datetime.now().date() if actual_date else None,
                    comments=notes,
                    file_path=file_path
                )
                db.session.add(submission)
                
                flash(f'Document {document.doc_number} submitted successfully for {stage}!', 'success')
            else:
                flash('Invalid file type. Allowed types: PDF, DWG, XLSX, DOC, ZIP, etc.', 'danger')
                return redirect(url_for('submit_document', document_id=document_id))
        else:
            # Draft save
            flash(f'Draft saved successfully! Changes reflected in MDR.', 'info')
        
        db.session.commit()
        return redirect(url_for('view_feedback', document_id=document_id))
    
    # GET request - show form
    return render_template('submit_document.html',
                         document=document,
                         stages=STANDARD_STAGES,
                         user=user)


@app.route('/download/submission/<int:submission_id>')
@login_required
def download_submission(submission_id):
    """Download file from a submission"""
    user = get_current_user()
    submission = Submission.query.get_or_404(submission_id)
    
    # Check access via document portfolio
    document = Document.query.get(submission.document_id)
    if not user_can_access_portfolio(user, document.portfolio_id):
        flash('You do not have access to this file', 'danger')
        return redirect(url_for('index'))
    
    if not submission.file_path or not os.path.exists(submission.file_path):
        flash('File not found', 'danger')
        return redirect(url_for('view_feedback', document_id=document.id))
    
    return send_file(submission.file_path, as_attachment=True)


@app.route('/api/documents/<int:document_id>/feedback-files')
@login_required
def get_feedback_files(document_id):
    """API endpoint to get client feedback files for a document"""
    from flask import jsonify
    
    document = Document.query.get_or_404(document_id)
    
    # Check access
    if not user_can_access_portfolio(get_current_user(), document.portfolio_id):
        return jsonify({'error': 'Access denied'}), 403
    
    # Get feedback files from Portfolio Manager's feedback folder
    feedback_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'app1_portfolio_manager', 
        'uploads', 
        'client_feedback'
    )
    
    files = []
    if os.path.exists(feedback_folder):
        for filename in os.listdir(feedback_folder):
            if filename.startswith(document.doc_number):
                files.append({
                    'filename': filename,
                    'download_url': f'/download/feedback/{filename}'
                })
    
    return jsonify({'files': files})


@app.route('/download/feedback/<path:filename>')
@login_required
def download_feedback_file_discipline(filename):
    """Download client feedback file (from Portfolio Manager's folder)"""
    user = get_current_user()
    
    feedback_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'app1_portfolio_manager', 
        'uploads', 
        'client_feedback'
    )
    filepath = os.path.join(feedback_folder, filename)
    
    if not os.path.exists(filepath):
        flash('File not found', 'danger')
        return redirect(url_for('index'))
    
    # Extract original filename (after timestamp)
    parts = filename.split('_', 3)
    original_name = parts[3] if len(parts) > 3 else filename
    
    return send_file(filepath, 
                    as_attachment=True,
                    download_name=original_name)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration with email domain validation"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validate email domain
        if not validate_email_domain(email):
            flash(f'Invalid email domain. Only @{app.config["ALLOWED_EMAIL_DOMAIN"]} emails are allowed.', 'danger')
            return render_template('register.html', allowed_domain=app.config['ALLOWED_EMAIL_DOMAIN'])
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'danger')
            return render_template('register.html', allowed_domain=app.config['ALLOWED_EMAIL_DOMAIN'])
        
        # Validate password
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html', allowed_domain=app.config['ALLOWED_EMAIL_DOMAIN'])
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return render_template('register.html', allowed_domain=app.config['ALLOWED_EMAIL_DOMAIN'])
        
        # Create user
        new_user = User(
            email=email,
            name=name,
            role='member'  # Default role
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', allowed_domain=app.config['ALLOWED_EMAIL_DOMAIN'])


if __name__ == '__main__':
    app.run(debug=True, port=5003)

