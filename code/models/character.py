from db import db


class CharacterModel(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_character = db.Column(db.Integer)
    name = db.Column(db.String(80))

    def __init__(self, id_user, id_character, name):
        self.id_user = id_user
        self.id_character = id_character
        self.name = name

    @classmethod
    def find_by_id(cls, id_user, id_character):
        return cls.query.filter_by(id_user=id_user, id_character=id_character).first()

    @classmethod
    def find_user_characters(cls, id_user, name=None):
        if name == None:
            result = cls.query.filter_by(id_user=id_user).all()
        else:
            cls.query.filter_by(id_user=id_user).filter(
                cls.query.name.like(f"{name}%")).all()
        return [value.id_character for value in result]

    @classmethod
    def find_user_characters_by_ids(cls, id_user, ids_character_list):
        result = cls.query.filter(cls.id_character.in_(
            ids_character_list)).filter_by(id_user=id_user).all()
        return [value.id_character for value in result]

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()
