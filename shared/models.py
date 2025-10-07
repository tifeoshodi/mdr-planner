"""
SQLAlchemy ORM Models for MDR Management System
All three Flask apps share these models via the same SQLite database
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))
    role = db.Column(db.String(50), nullable=False, default='member')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    created_portfolios = db.relationship('Portfolio', back_populates='creator', foreign_keys='Portfolio.created_by')
    team_memberships = db.relationship('TeamMembership', back_populates='user', cascade='all, delete-orphan')
    submissions = db.relationship('Submission', back_populates='submitter')
    
    __table_args__ = (
        db.CheckConstraint("role IN ('admin','scheduler','discipline_lead','member')", name='check_user_role'),
    )
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class Portfolio(db.Model):
    """Portfolio represents a project MDR"""
    __tablename__ = 'portfolios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(100), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    client = db.Column(db.String(255))  # Client/customer name
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', back_populates='created_portfolios', foreign_keys=[created_by])
    disciplines = db.relationship('Discipline', back_populates='portfolio', cascade='all, delete-orphan')
    documents = db.relationship('Document', back_populates='portfolio', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Portfolio {self.code}: {self.name}>'


class Discipline(db.Model):
    """Discipline within a portfolio (e.g., Mechanical, Electrical, Civil)"""
    __tablename__ = 'disciplines'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    portfolio = db.relationship('Portfolio', back_populates='disciplines')
    team_memberships = db.relationship('TeamMembership', back_populates='discipline', cascade='all, delete-orphan')
    documents = db.relationship('Document', back_populates='discipline')
    
    def __repr__(self):
        return f'<Discipline {self.name}>'


class TeamMembership(db.Model):
    """Users assigned to disciplines"""
    __tablename__ = 'team_memberships'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='member')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    discipline = db.relationship('Discipline', back_populates='team_memberships')
    user = db.relationship('User', back_populates='team_memberships')
    
    __table_args__ = (
        db.UniqueConstraint('discipline_id', 'user_id', name='unique_discipline_user'),
        db.CheckConstraint("role IN ('lead','member')", name='check_membership_role'),
    )
    
    def __repr__(self):
        return f'<TeamMembership user={self.user_id} discipline={self.discipline_id}>'


class Document(db.Model):
    """Document/deliverable in the MDR with full stage tracking"""
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id', ondelete='CASCADE'), nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('disciplines.id', ondelete='SET NULL'))
    s_no = db.Column(db.Integer)
    doc_number = db.Column(db.String(255), nullable=False, index=True)
    doc_title = db.Column(db.String(500), nullable=False)
    doc_type = db.Column(db.String(255))
    deliverable_category = db.Column(db.String(255))
    current_revision = db.Column(db.String(50))
    current_status = db.Column(db.String(100))
    current_transmittal_no = db.Column(db.String(100))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # IFR (Information For Review) fields
    ifr_date_planned = db.Column(db.String(50))
    ifr_date_actual = db.Column(db.String(50))
    ifr_tr_no = db.Column(db.String(100))
    ifr_date_sent = db.Column(db.String(50))
    ifr_rev_status = db.Column(db.String(50))
    ifr_issue_for = db.Column(db.String(100))
    ifr_date_received = db.Column(db.String(50))
    ifr_tr_received = db.Column(db.String(100))
    
    # IFH (Information For HAZOP) fields
    ifh_date_planned = db.Column(db.String(50))
    ifh_date_actual = db.Column(db.String(50))
    ifh_tr_no = db.Column(db.String(100))
    ifh_date_sent = db.Column(db.String(50))
    ifh_rev_status = db.Column(db.String(50))
    ifh_issue_for = db.Column(db.String(100))
    ifh_date_received = db.Column(db.String(50))
    ifh_tr_received = db.Column(db.String(100))
    ifh_next_rev = db.Column(db.String(50))
    
    # IFD (Information For Design) fields
    ifd_date_planned = db.Column(db.String(50))
    ifd_date_actual = db.Column(db.String(50))
    ifd_tr_no = db.Column(db.String(100))
    ifd_date_sent = db.Column(db.String(50))
    ifd_rev_status = db.Column(db.String(50))
    ifd_issue_for = db.Column(db.String(100))
    ifd_date_received = db.Column(db.String(50))
    ifd_tr_received = db.Column(db.String(100))
    ifd_next_rev = db.Column(db.String(50))
    
    # IFT (Information For Tender) fields
    ift_date_planned = db.Column(db.String(50))
    ift_date_actual = db.Column(db.String(50))
    ift_tr_no = db.Column(db.String(100))
    ift_date_sent = db.Column(db.String(50))
    ift_rev_status = db.Column(db.String(50))
    ift_issue_for = db.Column(db.String(100))
    ift_date_received = db.Column(db.String(50))
    ift_tr_received = db.Column(db.String(100))
    ift_next_rev = db.Column(db.String(50))
    
    # IFP (Information For Procurement) fields
    ifp_date_planned = db.Column(db.String(50))
    ifp_date_actual = db.Column(db.String(50))
    ifp_tr_no = db.Column(db.String(100))
    ifp_date_sent = db.Column(db.String(50))
    ifp_rev_status = db.Column(db.String(50))
    ifp_issue_for = db.Column(db.String(100))
    ifp_date_received = db.Column(db.String(50))
    ifp_tr_received = db.Column(db.String(100))
    ifp_next_rev = db.Column(db.String(50))
    
    # IFA (Information For Approval) fields
    ifa_date_planned = db.Column(db.String(50))
    ifa_date_actual = db.Column(db.String(50))
    ifa_tr_no = db.Column(db.String(100))
    ifa_date_sent = db.Column(db.String(50))
    ifa_rev_status = db.Column(db.String(50))
    ifa_issue_for = db.Column(db.String(100))
    ifa_date_received = db.Column(db.String(50))
    ifa_tr_received = db.Column(db.String(100))
    ifa_next_rev = db.Column(db.String(50))
    
    # IFC (Information For Construction) fields
    ifc_date_planned = db.Column(db.String(50))
    ifc_date_actual = db.Column(db.String(50))
    ifc_tr_no = db.Column(db.String(100))
    ifc_date_sent = db.Column(db.String(50))
    ifc_rev_status = db.Column(db.String(50))
    ifc_issue_for = db.Column(db.String(100))
    ifc_date_received = db.Column(db.String(50))
    ifc_tr_received = db.Column(db.String(100))
    ifc_next_rev = db.Column(db.String(50))
    
    # AFC (Approved For Construction) fields
    afc_date_planned = db.Column(db.String(50))
    afc_date_actual = db.Column(db.String(50))
    afc_tr_no = db.Column(db.String(100))
    afc_date_sent = db.Column(db.String(50))
    afc_rev_status = db.Column(db.String(50))
    afc_issue_for = db.Column(db.String(100))
    afc_date_received = db.Column(db.String(50))
    afc_tr_received = db.Column(db.String(100))
    
    # Relationships
    portfolio = db.relationship('Portfolio', back_populates='documents')
    discipline = db.relationship('Discipline', back_populates='documents')
    submissions = db.relationship('Submission', back_populates='document', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Document {self.doc_number}: {self.doc_title}>'


class Submission(db.Model):
    """Submission history for document revisions"""
    __tablename__ = 'submissions'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    stage = db.Column(db.String(50))
    submitted_revision = db.Column(db.String(50))
    transmittal_no = db.Column(db.String(100))
    date_sent = db.Column(db.Date)
    response_status = db.Column(db.String(100))
    response_date = db.Column(db.Date)
    comments = db.Column(db.Text)
    file_path = db.Column(db.String(500))
    days_with_client = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    document = db.relationship('Document', back_populates='submissions')
    submitter = db.relationship('User', back_populates='submissions')
    
    __table_args__ = (
        db.CheckConstraint("stage IN ('IFR','IFH','IFD','IFT','IFP','IFA','IFC','AFC')", name='check_submission_stage'),
    )
    
    def __repr__(self):
        return f'<Submission {self.stage} for doc={self.document_id}>'

