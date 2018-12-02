from wtforms import Form, StringField, PasswordField, DateTimeField, BooleanField,  StringField, PasswordField
#### DateTimeField does not have Timezone #### 


from wtforms.validators import DataRequired,length

class UserCreationForm():
    uid = None
    membership = None
    displayName = None
    phoneNumber = None
    photoURL = None

class UserCreationValidateForm(Form):

    # Can be filled with Flightstats API
    uid = StringField(u'UID', validators=[
        DataRequired('UID needs to be specified.')])

    phoneNumber = StringField(u'Phone Number',  validators=[
        DataRequired('Phone Number needs to be specified.')])

    membership = StringField(u'Membership', validators=[
        DataRequired('Membership needs to be specified.')])

    displayName = StringField(u'Name', validators=[
        DataRequired('Name needs to be specified.')])

    photoURL = StringField(u'Photo URL', validators=[
        DataRequired('Photo URL needs to be specified.')])