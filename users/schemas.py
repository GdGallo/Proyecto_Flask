from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80), error_messages={ 
        "required": 'El nombre del usuario es obligatorio.', 
        'invalid': 'El nombre del usuario debe de ser una cedena valida.'
    })

    email = fields.Email(required=True, error_message={
        'required': 'El correo no es valido.',
        'invalid': 'El correo debe de ser valido.'
    })
    
    password = fields.Str(required=True, validate=validate.Length(min=6,max=128), error_messages={
        'required': 'La contraseña no es valida.',
        'invalid': 'La contraseña debe de ser valida.'
    })