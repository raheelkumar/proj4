# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectMultipleField, SelectField, TextAreaField, DateField, validators

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///isv_tracker.db'
db = SQLAlchemy(app)

# Domain choices - can be moved to a separate configuration file
DOMAIN_CHOICES = [
    ('business intelligence', 'Business Intelligence'),
    ('extract transform load', 'Extract Transform Load'),
    ('data integration', 'Data Integration'),
    ('data marketing', 'Data Marketing'),
    ('data governance', 'Data Governance'),
    ('machine learning', 'Machine Learning'),
    ('data analytics', 'Data Analytics'),
    ('data virtualization', 'Data Virtualization'),
    ('advanced analytics', 'Advanced Analytics'),
    ('master data management', 'Master Data Management'),
    ('reverse etl', 'Reverse ETL'),
    ('data security', 'Data Security'),
    ('data monitoring', 'Data Monitoring'),
    ('data observability', 'Data Observability'),
    ('spatial analytics', 'Spatial Analytics'),
    ('data quality', 'Data Quality'),
    ('customer data platform', 'Customer Data Platform'),
    ('marketing analytics', 'Marketing Analytics'),
    ('data activation', 'Data Activation'),
    ('behavioural data platform', 'Behavioural Data Platform'),
    ('graph database', 'Graph Database'),
    ('data modeler', 'Data Modeler'),
    ('data api', 'Data API'),
    ('mobile first bi', 'Mobile First BI'),
    ('data app development', 'Data App Development'),
    ('deep data observability', 'Deep Data Observability'),
    ('finops', 'FinOps'),
    ('dataops', 'DataOps'),
    ('real time etl', 'Real Time ETL'),
    ('product analytics platform', 'Product Analytics Platform'),
    ('synthetic data generation', 'Synthetic Data Generation'),
    ('data visualization', 'Data Visualization'),
    ('artificial intelligence', 'Artificial Intelligence'),
    ('generative ai', 'Generative AI'),
    ('automation', 'Automation'),
]

# Models
class ISV(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    domains = db.Column(db.String(500), nullable=False)  # Stored as comma-separated values
    certification_type = db.Column(db.String(20), nullable=False)
    version = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    team_members = db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    poc = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Forms
class ISVForm(FlaskForm):
    name = StringField('ISV Name', validators=[validators.DataRequired(), validators.Length(min=2, max=100)])
    domains = SelectMultipleField('Domains', choices=DOMAIN_CHOICES, validators=[validators.DataRequired()])
    certification_type = SelectField('Certification Type',
                                   choices=[('lite', 'Lite'), ('detailed', 'Detailed')],
                                   validators=[validators.DataRequired()])
    version = StringField('Version', validators=[validators.DataRequired()])
    description = TextAreaField('Description', validators=[validators.DataRequired()])
    team_members = StringField('Team Members', validators=[validators.DataRequired()])
    start_date = DateField('Start Date', validators=[validators.DataRequired()])
    end_date = DateField('End Date', validators=[validators.Optional()])
    poc = StringField('POC', validators=[validators.DataRequired()])
    status = SelectField('Status',
                        choices=[('not_started', 'Not Started'),
                                ('in_progress', 'In Progress'),
                                ('completed', 'Completed')],
                        validators=[validators.DataRequired()])

    def validate_end_date(self, field):
        if field.data and self.start_date.data:
            if field.data < self.start_date.data:
                raise validators.ValidationError('End date must be after start date')

# Routes
@app.route('/')
def index():
    return redirect(url_for('current_isvs'))

@app.route('/add_isv', methods=['GET', 'POST'])
def add_isv():
    form = ISVForm()
    if form.validate_on_submit():
        domains_str = ','.join(form.domains.data)
        isv = ISV(
            name=form.name.data,
            domains=domains_str,
            certification_type=form.certification_type.data,
            version=form.version.data,
            description=form.description.data,
            team_members=form.team_members.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            poc=form.poc.data,
            status=form.status.data
        )
        db.session.add(isv)
        db.session.commit()
        flash('ISV added successfully!', 'success')
        return redirect(url_for('current_isvs'))
    return render_template('add_isv.html', form=form)

@app.route('/current_isvs')
def current_isvs():
    isvs = ISV.query.filter(ISV.status != 'completed').order_by(ISV.created_at.desc()).all()
    return render_template('current_isvs.html', isvs=isvs)

@app.route('/isv_history')
def isv_history():
    isvs = ISV.query.filter_by(status='completed').order_by(ISV.created_at.desc()).all()
    return render_template('isv_history.html', isvs=isvs)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)