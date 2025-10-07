"""
Authentication and authorization utilities
"""

from functools import wraps
from flask import session, redirect, url_for, flash, request
from shared.models import User, TeamMembership


def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    """Decorator to require specific role(s)"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('login'))
            
            user = User.query.get(session['user_id'])
            if not user or user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    """Get currently logged in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


def get_user_portfolios(user):
    """Get all portfolios accessible by a user"""
    if not user:
        return []
    
    # Admins and schedulers see all portfolios
    if user.role in ['admin', 'scheduler']:
        from shared.models import Portfolio
        return Portfolio.query.all()
    
    # Regular users only see portfolios they're assigned to via disciplines
    portfolio_ids = set()
    for membership in user.team_memberships:
        portfolio_ids.add(membership.discipline.portfolio_id)
    
    from shared.models import Portfolio
    return Portfolio.query.filter(Portfolio.id.in_(portfolio_ids)).all()


def user_can_access_portfolio(user, portfolio_id):
    """Check if user can access a specific portfolio"""
    if not user:
        return False
    
    # Admins and schedulers can access all
    if user.role in ['admin', 'scheduler']:
        return True
    
    # Check if user is assigned to any discipline in this portfolio
    for membership in user.team_memberships:
        if membership.discipline.portfolio_id == portfolio_id:
            return True
    
    return False


def get_user_disciplines(user, portfolio_id=None):
    """Get disciplines assigned to a user, optionally filtered by portfolio"""
    if not user:
        return []
    
    disciplines = []
    for membership in user.team_memberships:
        if portfolio_id is None or membership.discipline.portfolio_id == portfolio_id:
            disciplines.append(membership.discipline)
    
    return disciplines

