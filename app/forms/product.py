from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    category = StringField("Category", validators=[DataRequired()])
    description = StringField("Fescription", validators=[DataRequired()])
    img = StringField("Image URL", validators=[DataRequired()])
    shipping_price = StringField("Shipping Price", validators=[DataRequired()])
    brand_name = StringField("Brand Name", validators=[DataRequired()])
    submit = SubmitField("Submit")