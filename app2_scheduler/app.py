"""
App 2: Scheduler
Manage disciplines, invite users, assign teams to disciplines
"""

import os
import sys
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash

# Add parent directory to path to import shared modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.models import db, Portfolio, User, Discipline, TeamMembership, Document
from shared.database import init_db, get_db_uri
from shared.auth import login_required, role_required, get_current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production-scheduler'
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)


@app.route('/')
def index():
    """Dashboard - list all portfolios"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    portfolios = Portfolio.query.order_by(Portfolio.created_at.desc()).all()
    return render_template('index.html', portfolios=portfolios, user=user)


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


@app.route('/portfolios/<int:portfolio_id>')
@login_required
@role_required('admin', 'scheduler')
def view_portfolio(portfolio_id):
    """View portfolio with disciplines and team management"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    disciplines = Discipline.query.filter_by(portfolio_id=portfolio_id).all()
    
    # Get team assignments for each discipline
    discipline_teams = {}
    for discipline in disciplines:
        members = TeamMembership.query.filter_by(discipline_id=discipline.id).all()
        discipline_teams[discipline.id] = members
    
    # Get all users for assignment dropdown
    all_users = User.query.order_by(User.name).all()
    
    return render_template('view_portfolio.html', 
                         portfolio=portfolio,
                         disciplines=disciplines,
                         discipline_teams=discipline_teams,
                         all_users=all_users,
                         user=get_current_user())


@app.route('/portfolios/<int:portfolio_id>/disciplines/add', methods=['POST'])
@login_required
@role_required('admin', 'scheduler')
def add_discipline(portfolio_id):
    """Add a new discipline to portfolio"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    
    name = request.form.get('name')
    if not name:
        flash('Discipline name is required', 'danger')
        return redirect(url_for('view_portfolio', portfolio_id=portfolio_id))
    
    # Check if discipline already exists
    existing = Discipline.query.filter_by(portfolio_id=portfolio_id, name=name).first()
    if existing:
        flash('Discipline already exists', 'danger')
        return redirect(url_for('view_portfolio', portfolio_id=portfolio_id))
    
    discipline = Discipline(
        portfolio_id=portfolio_id,
        name=name
    )
    db.session.add(discipline)
    db.session.commit()
    
    flash(f'Discipline "{name}" added successfully!', 'success')
    return redirect(url_for('view_portfolio', portfolio_id=portfolio_id))


@app.route('/disciplines/<int:discipline_id>/delete', methods=['POST'])
@login_required
@role_required('admin', 'scheduler')
def delete_discipline(discipline_id):
    """Delete a discipline"""
    discipline = Discipline.query.get_or_404(discipline_id)
    portfolio_id = discipline.portfolio_id
    
    db.session.delete(discipline)
    db.session.commit()
    
    flash(f'Discipline "{discipline.name}" deleted', 'success')
    return redirect(url_for('view_portfolio', portfolio_id=portfolio_id))


@app.route('/disciplines/<int:discipline_id>/assign', methods=['POST'])
@login_required
@role_required('admin', 'scheduler')
def assign_user(discipline_id):
    """Assign a user to a discipline"""
    discipline = Discipline.query.get_or_404(discipline_id)
    
    user_id = request.form.get('user_id')
    role = request.form.get('role', 'member')
    
    if not user_id:
        flash('Please select a user', 'danger')
        return redirect(url_for('view_portfolio', portfolio_id=discipline.portfolio_id))
    
    # Check if assignment already exists
    existing = TeamMembership.query.filter_by(
        discipline_id=discipline_id,
        user_id=user_id
    ).first()
    
    if existing:
        flash('User is already assigned to this discipline', 'warning')
        return redirect(url_for('view_portfolio', portfolio_id=discipline.portfolio_id))
    
    membership = TeamMembership(
        discipline_id=discipline_id,
        user_id=user_id,
        role=role
    )
    db.session.add(membership)
    db.session.commit()
    
    user = User.query.get(user_id)
    flash(f'User "{user.name}" assigned to "{discipline.name}"', 'success')
    return redirect(url_for('view_portfolio', portfolio_id=discipline.portfolio_id))


@app.route('/memberships/<int:membership_id>/remove', methods=['POST'])
@login_required
@role_required('admin', 'scheduler')
def remove_membership(membership_id):
    """Remove a user from a discipline"""
    membership = TeamMembership.query.get_or_404(membership_id)
    portfolio_id = membership.discipline.portfolio_id
    
    user_name = membership.user.name
    discipline_name = membership.discipline.name
    
    db.session.delete(membership)
    db.session.commit()
    
    flash(f'Removed "{user_name}" from "{discipline_name}"', 'success')
    return redirect(url_for('view_portfolio', portfolio_id=portfolio_id))


@app.route('/users')
@login_required
@role_required('admin', 'scheduler')
def list_users():
    """List all users"""
    users = User.query.order_by(User.created_at.desc()).all()
    
    # Get team counts for each user
    user_teams = {}
    for user in users:
        user_teams[user.id] = TeamMembership.query.filter_by(user_id=user.id).count()
    
    return render_template('users.html', users=users, user_teams=user_teams, user=get_current_user())


@app.route('/users/invite', methods=['GET', 'POST'])
@login_required
@role_required('admin', 'scheduler')
def invite_user():
    """Invite a new user (create account)"""
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        role = request.form.get('role', 'member')
        
        # Check if user already exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('User with this email already exists', 'danger')
            return render_template('invite_user.html', user=get_current_user())
        
        # Create new user
        new_user = User(
            email=email,
            name=name,
            role=role
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'User "{name}" created successfully! They can now log in with: {email}', 'success')
        return redirect(url_for('list_users'))
    
    return render_template('invite_user.html', user=get_current_user())


@app.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@role_required('admin')
def delete_user(user_id):
    """Delete a user"""
    user_to_delete = User.query.get_or_404(user_id)
    
    # Don't allow deleting yourself
    current_user = get_current_user()
    if user_to_delete.id == current_user.id:
        flash('You cannot delete your own account', 'danger')
        return redirect(url_for('list_users'))
    
    db.session.delete(user_to_delete)
    db.session.commit()
    
    flash(f'User "{user_to_delete.name}" deleted', 'success')
    return redirect(url_for('list_users'))


@app.route('/wbs/<int:portfolio_id>')
@login_required
@role_required('admin', 'scheduler')
def work_breakdown(portfolio_id):
    """Work Breakdown Structure view"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    disciplines = Discipline.query.filter_by(portfolio_id=portfolio_id).all()
    
    # Get documents grouped by discipline
    wbs_data = {}
    for discipline in disciplines:
        documents = Document.query.filter_by(discipline_id=discipline.id).all()
        team_count = TeamMembership.query.filter_by(discipline_id=discipline.id).count()
        wbs_data[discipline.name] = {
            'documents': documents,
            'team_count': team_count,
            'discipline_id': discipline.id
        }
    
    return render_template('wbs.html', 
                         portfolio=portfolio,
                         wbs_data=wbs_data,
                         user=get_current_user())


if __name__ == '__main__':
    app.run(debug=True, port=5002)

