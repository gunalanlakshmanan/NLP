from timelinepage import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    articlename = db.Column(db.String(30), nullable=False)
    timelinenumber = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Input('{self.articlename}', '{self.timelinenumber}')"