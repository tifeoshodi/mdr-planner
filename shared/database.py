"""
Database initialization and utility functions
"""

import os
from shared.models import db, User, Portfolio, Discipline, TeamMembership, Document, Submission


def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("[OK] Database tables created")
        
        # Create default admin user if none exists
        admin_user = User.query.filter_by(email='admin@mdr.local').first()
        if not admin_user:
            admin_user = User(
                email='admin@mdr.local',
                name='Admin User',
                role='admin'
            )
            admin_user.set_password('admin123')  # Change this in production!
            db.session.add(admin_user)
            db.session.commit()
            print("[OK] Default admin user created (admin@mdr.local / admin123)")
        
        return db


def get_db_uri(db_name='mdr_system.db'):
    """
    Get database URI - supports both SQLite (development) and PostgreSQL (production)
    
    In production, Railway automatically provides DATABASE_URL environment variable.
    For local development, falls back to SQLite.
    """
    # Check for production database URL (Railway, Heroku, etc.)
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Fix for SQLAlchemy 1.4+ (postgres:// -> postgresql://)
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        print(f"[OK] Using production database (PostgreSQL)")
        return database_url
    
    # Local development - use SQLite
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_name)
    print(f"[OK] Using development database (SQLite): {db_name}")
    return f'sqlite:///{db_path}'


def init_db_standalone():
    """Initialize database for standalone (non-Flask) applications like Tkinter"""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import scoped_session, sessionmaker
    
    # Get database URI
    db_uri = get_db_uri()
    
    # Create engine
    engine = create_engine(db_uri)
    
    # Bind the engine to the db instance
    db.metadata.bind = engine
    
    # Create a session factory
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    
    # Replace db.session with our standalone session
    db.session = Session()
    
    # Create all tables
    db.metadata.create_all(engine)
    
    print(f"[OK] Database connected: {db_uri}")
    
    return db


def seed_demo_data():
    """Seed database with demo data for testing"""
    # Check if demo data already exists
    if Portfolio.query.count() > 0:
        print("Demo data already exists, skipping seed")
        return
    
    # Create demo admin
    admin = User.query.filter_by(email='admin@mdr.local').first()
    
    # Create a demo portfolio
    portfolio = Portfolio(
        code='EPC-2024-001',
        name='Gas Processing Plant',
        description='Comprehensive gas processing facility project',
        created_by=admin.id
    )
    db.session.add(portfolio)
    db.session.commit()
    
    # Create disciplines
    disciplines_list = [
        'Project Management & Administration',
        'Technical Safety',
        'Process',
        'Piping',
        'Instrumentation',
        'Electrical',
        'Civil & Structural',
        'Mechanical',
        'Corrosion',
        'Telecommunications'
    ]
    
    for disc_name in disciplines_list:
        discipline = Discipline(
            portfolio_id=portfolio.id,
            name=disc_name
        )
        db.session.add(discipline)
    
    db.session.commit()
    print(f"[OK] Demo portfolio '{portfolio.name}' created with {len(disciplines_list)} disciplines")

