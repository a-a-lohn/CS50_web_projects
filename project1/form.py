from wtforms import Form, StringField, SelectField

class BookSearch(Form):
    choices = [('ISBN', 'ISBN'),
               ('Title', 'Title'),
               ('Author', 'Author')]
    select = SelectField('Search for a book:', choices=choices)
    search = StringField('')