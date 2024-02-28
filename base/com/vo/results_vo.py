from base import db

class ResultVO(db.Model):
    __tablename__ = 'results'
    result_id = db.Column('result_id', db.Integer, autoincrement=True, primary_key=True)
    image_name = db.Column('image_name', db.String(225), nullable=False)
    potholes_count = db.Column('potholes_count', db.Integer)
    cattles_count = db.Column('cattles_count', db.Integer)

    def as_dict(self):
        return {
            'result_id': self.result_id,
            'image_name': self.image_name,
            'potholes_count': self.potholes_count,
            'cattle_count':self.cattles_count,
        }

# class ImageVO(db.Model):
    

db.create_all()