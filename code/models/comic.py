from db import db


class ComicModel(db.Model):
    __tablename__ = 'comic'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    id_comic = db.Column(db.Integer)
    name = db.Column(db.String(80))

    def __init__(self, id_user, id_comic, name):
        self.id_user = id_user
        self.id_comic = id_comic
        self.name = name

    @classmethod
    def find_by_id(cls, id_user, id_comic):
        return cls.query.filter_by(id_user=id_user, id_comic=id_comic).first()

    @classmethod
    def find_user_comics(cls, id_user, name=None):
        if name == None:
            result = cls.query.filter_by(id_user=id_user).all()
        else:
            result = cls.query.filter_by(id_user=id_user).filter(
                cls.name.like(f"{name}%")).all()
        return [value.id_comic for value in result]

    @classmethod
    def find_user_comics_by_ids(cls, id_user, ids_comic_list):
        result = cls.query.filter(cls.id_comic.in_(
            ids_comic_list)).filter_by(id_user=id_user).all()
        return [value.id_comic for value in result]

    def save_to_database(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()
