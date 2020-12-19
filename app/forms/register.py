from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    billing_addr1= StringField("Billing Address Line 1")
    billing_addr2= StringField("Billing Address Line 2")
    biliing_city= StringField("Billing City")
    billing_state= StringField("Billing State")
    billing_postalcode= StringField("Billing Postal Code")
    billing_country= StringField("Billing Country")
    shipping_addr1= StringField("Shipping Address Line 1")
    shipping_addr2= StringField("Shipping Address Line 2")
    shipping_city= StringField("Shipping City")
    shipping_state= StringField("Shipping State")
    shipping_postalcode= StringField("Shipping Postal Code")
    shipping_contry= StringField("Shipping Contry")
    phone= StringField("Phone")
    phone_alt= StringField("Phone Alternative")
    submit = SubmitField("Submit")