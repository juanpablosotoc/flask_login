from myproyect import db, login_manager
from flask_login import UserMixin, current_user
from flask_bcrypt import Bcrypt
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin, SQLAlchemyStorage
from myproyect import google_blueprint

bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users, int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)

    def __init__(self, email, password) -> None:
        super().__init__()
        self.email = email
        self.hashed_password = bcrypt.generate_password_hash(password)
    
    def check_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.hashed_password, password)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users')


google_blueprint.storage = SQLAlchemyStorage(OAuth, db.session, user=current_user)
