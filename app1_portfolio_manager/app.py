"""
App 1: Portfolio Manager
Create and manage portfolios, import/export MDR from/to Excel
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.utils import secure_filename
import sys

# Add parent directory to path to import shared modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import db, Portfolio, User, Document, Discipline, Submission
from shared.database import init_db, get_db_uri, seed_demo_data
from shared.auth import login_required, role_required, get_current_user
from shared.excel_handler import MDRExcelExporter, MDRExcelImporter
from mdr_stages_config import STANDARD_STAGES
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['FEEDBACK_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads', 'client_feedback')
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size

# Ensure upload folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['FEEDBACK_FOLDER'], exist_ok=True)

# Allowed file extensions for client feedback
ALLOWED_FEEDBACK_EXTENSIONS = {'pdf', 'dwg', 'xlsx', 'xls', 'doc', 'docx', 'zip', 'rar', 'png', 'jpg', 'jpeg', 'msg', 'eml'}

def allowed_feedback_file(filename):
    """Check if file extension is allowed for feedback"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FEEDBACK_EXTENSIONS

# Initialize database
init_db(app)


@app.route('/')
def index():
    """Dashboard - list all portfolios"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    portfolios = Portfolio.query.order_by(Portfolio.created_at.desc()).all()
    
    # Get statistics for each portfolio
    portfolio_stats = []
    for portfolio in portfolios:
        doc_count = Document.query.filter_by(portfolio_id=portfolio.id).count()
        discipline_count = Discipline.query.filter_by(portfolio_id=portfolio.id).count()
        portfolio_stats.append({
            'portfolio': portfolio,
            'doc_count': doc_count,
            'discipline_count': discipline_count
        })
    
    return render_template('index.html', portfolio_stats=portfolio_stats, user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_role'] = user.role
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/portfolios/create', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'scheduler')
def create_portfolio():
    """Create a new portfolio"""
    if request.method == 'POST':
        code = request.form.get('code')
        name = request.form.get('name')
        description = request.form.get('description')
        
        user = get_current_user()
        
        # Check if portfolio code already exists
        existing = Portfolio.query.filter_by(code=code).first()
        if existing:
            flash('Portfolio code already exists', 'danger')
            return render_template('create_portfolio.html', user=user)
        
        portfolio = Portfolio(
            code=code,
            name=name,
            description=description,
            created_by=user.id
        )
        db.session.add(portfolio)
        db.session.commit()
        
        flash(f'Portfolio "{name}" created successfully!', 'success')
        return redirect(url_for('view_portfolio', portfolio_id=portfolio.id))
    
    return render_template('create_portfolio.html', user=get_current_user())


@app.route('/portfolios/<int:portfolio_id>')
@login_required
def view_portfolio(portfolio_id):
    """View portfolio details with documents"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    # Get documents grouped by discipline
    disciplines = Discipline.query.filter_by(portfolio_id=portfolio_id).all()
    
    documents_by_discipline = {}
    for discipline in disciplines:
        docs = Document.query.filter_by(discipline_id=discipline.id).all()
        documents_by_discipline[discipline.name] = docs
    
    # Get unassigned documents
    unassigned_docs = Document.query.filter_by(portfolio_id=portfolio_id, discipline_id=None).all()
    if unassigned_docs:
        documents_by_discipline['Unassigned'] = unassigned_docs
    
    total_docs = Document.query.filter_by(portfolio_id=portfolio_id).count()
    
    return render_template('view_portfolio.html', 
                         portfolio=portfolio,
                         documents_by_discipline=documents_by_discipline,
                         total_docs=total_docs,
                         user=get_current_user())


@app.route('/portfolios/<int:portfolio_id>/import', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'scheduler')
def import_excel(portfolio_id):
    """Import MDR from Excel"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        if file and file.filename.endswith('.xlsx'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Import Excel data
                importer = MDRExcelImporter(filepath)
                docs_imported = importer.import_to_portfolio(portfolio)
                
                flash(f'Successfully imported {docs_imported} documents!', 'success')
                
                # Clean up uploaded file with retry for Windows file locking
                import time
                for attempt in range(3):
                    try:
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        break
                    except PermissionError:
                        if attempt < 2:
                            time.sleep(0.5)  # Wait a bit for Windows to release the file
                        else:
                            # File will be cleaned up later, don't fail the import
                            pass
                
                return redirect(url_for('view_portfolio', portfolio_id=portfolio_id))
            except Exception as e:
                flash(f'Error importing Excel: {str(e)}', 'danger')
                # Try to clean up, but don't fail if we can't
                try:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                except:
                    pass
        else:
            flash('Please upload an Excel file (.xlsx)', 'danger')
    
    return render_template('import_excel.html', portfolio=portfolio, user=get_current_user())


@app.route('/portfolios/<int:portfolio_id>/export')
@login_required
def export_excel(portfolio_id):
    """Export MDR to Excel"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    try:
        # Generate Excel file
        exporter = MDRExcelExporter(portfolio)
        filename = f"{portfolio.code}_MDR.xlsx"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        exporter.export(filepath)
        
        return send_file(filepath, 
                        as_attachment=True,
                        download_name=filename,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    except Exception as e:
        flash(f'Error exporting Excel: {str(e)}', 'danger')
        return redirect(url_for('view_portfolio', portfolio_id=portfolio_id))


@app.route('/portfolios/<int:portfolio_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_portfolio(portfolio_id):
    """Delete a portfolio"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    db.session.delete(portfolio)
    db.session.commit()
    flash(f'Portfolio "{portfolio.name}" deleted', 'success')
    return redirect(url_for('index'))


@app.route('/seed-demo')
@login_required
@role_required('admin')
def seed_demo():
    """Seed demo data"""
    with app.app_context():
        seed_demo_data()
    flash('Demo data seeded successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/portfolios/<int:portfolio_id>/spreadsheet')
@login_required
def spreadsheet_view(portfolio_id):
    """Excel-like spreadsheet view of MDR"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    user = get_current_user()
    return render_template('spreadsheet_view.html', portfolio=portfolio, user=user)


@app.route('/api/portfolios/<int:portfolio_id>/spreadsheet-data')
@login_required
def get_spreadsheet_data(portfolio_id):
    """API endpoint to get spreadsheet data in JSON format"""
    from flask import jsonify
    
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    # Group documents by discipline
    documents_by_discipline = {}
    for doc in Document.query.filter_by(portfolio_id=portfolio_id).order_by(Document.s_no).all():
        discipline_name = doc.discipline.name if doc.discipline else "Unassigned"
        if discipline_name not in documents_by_discipline:
            documents_by_discipline[discipline_name] = []
        documents_by_discipline[discipline_name].append(doc)
    
    # Build data array with discipline headers
    data = []
    for discipline_name in sorted(documents_by_discipline.keys()):
        # Add discipline header row
        discipline_row = {
            's_no': 'DISCIPLINE',
            'doc_number': discipline_name,
            'doc_title': '',
            'discipline_name': discipline_name,
            'is_discipline_header': True
        }
        data.append(discipline_row)
        
        # Add document rows
        for doc in documents_by_discipline[discipline_name]:
            doc_data = {
                'id': doc.id,
                's_no': doc.s_no,
                'doc_number': doc.doc_number,
                'doc_title': doc.doc_title,
                'current_revision': doc.current_revision or '',
                'current_status': doc.current_status or '',
                'current_transmittal_no': doc.current_transmittal_no or '',
                'remarks': doc.remarks or '',
                'is_discipline_header': False
            }
            
            # Add all stage fields
            stages = ['ifr', 'ifh', 'ifd', 'ift', 'ifp', 'ifa', 'ifc', 'afc']
            for stage in stages:
                doc_data[f'{stage}_date_planned'] = getattr(doc, f'{stage}_date_planned', '') or ''
                doc_data[f'{stage}_date_actual'] = getattr(doc, f'{stage}_date_actual', '') or ''
                doc_data[f'{stage}_tr_no'] = getattr(doc, f'{stage}_tr_no', '') or ''
                doc_data[f'{stage}_date_sent'] = getattr(doc, f'{stage}_date_sent', '') or ''
                doc_data[f'{stage}_rev_status'] = getattr(doc, f'{stage}_rev_status', '') or ''
                doc_data[f'{stage}_issue_for'] = getattr(doc, f'{stage}_issue_for', '') or ''
                doc_data[f'{stage}_date_received'] = getattr(doc, f'{stage}_date_received', '') or ''
                doc_data[f'{stage}_tr_received'] = getattr(doc, f'{stage}_tr_received', '') or ''
                
                # Next Rev (all except IFR and AFC)
                if stage not in ['ifr', 'afc']:
                    doc_data[f'{stage}_next_rev'] = getattr(doc, f'{stage}_next_rev', '') or ''
            
            data.append(doc_data)
    
    return jsonify(data)


@app.route('/api/portfolios/<int:portfolio_id>/update-spreadsheet', methods=['POST'])
@login_required
@role_required('admin', 'scheduler')
def update_spreadsheet(portfolio_id):
    """API endpoint to update documents from spreadsheet"""
    from flask import jsonify
    
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    data = request.json.get('documents', [])
    
    updated_count = 0
    
    for row in data:
        # Skip discipline header rows
        if row.get('is_discipline_header') or row.get('s_no') == 'DISCIPLINE':
            continue
        
        doc_id = row.get('id')
        if not doc_id:
            continue
        
        doc = Document.query.get(doc_id)
        if not doc or doc.portfolio_id != portfolio_id:
            continue
        
        # Update basic fields
        doc.doc_number = row.get('doc_number', '')
        doc.doc_title = row.get('doc_title', '')
        doc.current_revision = row.get('current_revision', '')
        doc.current_status = row.get('current_status', '')
        doc.current_transmittal_no = row.get('current_transmittal_no', '')
        doc.remarks = row.get('remarks', '')
        
        # Update all stage fields
        stages = ['ifr', 'ifh', 'ifd', 'ift', 'ifp', 'ifa', 'ifc', 'afc']
        for stage in stages:
            setattr(doc, f'{stage}_date_planned', row.get(f'{stage}_date_planned', ''))
            setattr(doc, f'{stage}_date_actual', row.get(f'{stage}_date_actual', ''))
            setattr(doc, f'{stage}_tr_no', row.get(f'{stage}_tr_no', ''))
            setattr(doc, f'{stage}_date_sent', row.get(f'{stage}_date_sent', ''))
            setattr(doc, f'{stage}_rev_status', row.get(f'{stage}_rev_status', ''))
            setattr(doc, f'{stage}_issue_for', row.get(f'{stage}_issue_for', ''))
            setattr(doc, f'{stage}_date_received', row.get(f'{stage}_date_received', ''))
            setattr(doc, f'{stage}_tr_received', row.get(f'{stage}_tr_received', ''))
            
            # Next Rev (all except IFR and AFC)
            if stage not in ['ifr', 'afc']:
                setattr(doc, f'{stage}_next_rev', row.get(f'{stage}_next_rev', ''))
        
        updated_count += 1
    
    db.session.commit()
    
    return jsonify({'success': True, 'updated': updated_count})


@app.route('/documents/<int:document_id>/post-feedback', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'scheduler')
def post_client_feedback(document_id):
    """Post client feedback for a document"""
    document = Document.query.get_or_404(document_id)
    
    if request.method == 'POST':
        stage = request.form.get('stage')
        
        if not stage or stage not in [s['code'] for s in STANDARD_STAGES]:
            flash('Invalid submission stage', 'danger')
            return redirect(url_for('post_client_feedback', document_id=document_id))
        
        stage_code = stage.lower()
        
        # Get form data
        date_received = request.form.get('date_received', '').strip()
        tr_received = request.form.get('tr_received', '').strip()
        rev_status = request.form.get('rev_status', '').strip()
        issue_for = request.form.get('issue_for', '').strip()
        next_rev = request.form.get('next_rev', '').strip() if stage != 'AFC' else ''
        notes = request.form.get('notes', '').strip()
        
        # Validate required fields
        if not date_received:
            flash('Date Received is required', 'danger')
            return redirect(url_for('post_client_feedback', document_id=document_id))
        
        # Update document MDR fields
        setattr(document, f'{stage_code}_date_received', date_received)
        setattr(document, f'{stage_code}_tr_received', tr_received)
        setattr(document, f'{stage_code}_rev_status', rev_status)
        setattr(document, f'{stage_code}_issue_for', issue_for)
        
        if stage != 'AFC':
            setattr(document, f'{stage_code}_next_rev', next_rev)
        
        # Add notes to remarks if provided
        if notes:
            existing_remarks = document.remarks or ''
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            new_remark = f"[{stage} Feedback - {timestamp}]: {notes}"
            document.remarks = f"{existing_remarks}\n{new_remark}" if existing_remarks else new_remark
        
        # Handle file uploads
        uploaded_files = []
        files = request.files.getlist('files')
        
        for file in files:
            if file and file.filename and allowed_feedback_file(file.filename):
                filename = secure_filename(file.filename)
                # Create unique filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"{document.doc_number}_{stage}_{timestamp}_{filename}"
                filepath = os.path.join(app.config['FEEDBACK_FOLDER'], unique_filename)
                file.save(filepath)
                uploaded_files.append({
                    'filename': filename,
                    'stored_as': unique_filename,
                    'path': filepath
                })
        
        # Store file information as JSON in remarks or create separate tracking
        if uploaded_files:
            # Store file metadata in a format we can retrieve later
            file_metadata = json.dumps([{
                'filename': f['filename'],
                'stored_as': f['stored_as'],
                'stage': stage,
                'uploaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            } for f in uploaded_files])
            
            # Append file info to remarks for now (or could use a separate field/table)
            file_note = f"\n[{stage} Feedback Files - {len(uploaded_files)} file(s)]"
            document.remarks = (document.remarks or '') + file_note
            
            flash(f'Uploaded {len(uploaded_files)} file(s) for {stage} feedback', 'success')
        
        db.session.commit()
        
        flash(f'Client feedback for {stage} posted successfully!', 'success')
        return redirect(url_for('view_portfolio', portfolio_id=document.portfolio_id))
    
    # GET request - show form
    return render_template('post_feedback.html',
                         document=document,
                         stages=STANDARD_STAGES,
                         user=get_current_user())


@app.route('/documents/<int:document_id>/view-feedback')
@login_required
def view_document_feedback(document_id):
    """View all feedback for a document (DCC view)"""
    document = Document.query.get_or_404(document_id)
    
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
    
    # Get client feedback files from directory
    feedback_files = []
    if os.path.exists(app.config['FEEDBACK_FOLDER']):
        for filename in os.listdir(app.config['FEEDBACK_FOLDER']):
            if filename.startswith(document.doc_number):
                feedback_files.append({
                    'filename': filename,
                    'path': os.path.join(app.config['FEEDBACK_FOLDER'], filename)
                })
    
    # Get discipline submissions
    submissions = Submission.query.filter_by(document_id=document_id).order_by(Submission.created_at.desc()).all()
    
    return render_template('view_document_feedback.html',
                         document=document,
                         feedback_data=feedback_data,
                         feedback_files=feedback_files,
                         submissions=submissions,
                         user=get_current_user())


@app.route('/download/feedback/<path:filename>')
@login_required
def download_feedback_file(filename):
    """Download client feedback file"""
    filepath = os.path.join(app.config['FEEDBACK_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        flash('File not found', 'danger')
        return redirect(url_for('index'))
    
    # Extract original filename (after timestamp)
    parts = filename.split('_', 3)
    original_name = parts[3] if len(parts) > 3 else filename
    
    return send_file(filepath, 
                    as_attachment=True,
                    download_name=original_name)


@app.route('/download/submission/<int:submission_id>')
@login_required
def download_submission_file(submission_id):
    """Download discipline submission file"""
    submission = Submission.query.get_or_404(submission_id)
    
    if not submission.file_path or not os.path.exists(submission.file_path):
        flash('File not found', 'danger')
        return redirect(url_for('index'))
    
    # Extract original filename
    filename = os.path.basename(submission.file_path)
    parts = filename.split('_', 1)
    original_name = parts[1] if len(parts) > 1 else filename
    
    return send_file(submission.file_path,
                    as_attachment=True,
                    download_name=original_name)


if __name__ == '__main__':
    app.run(debug=True, port=5001)

