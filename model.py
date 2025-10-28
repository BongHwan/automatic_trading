from framework import app, db
import os
from .plugin import logger, package_name

app.config['SQLALCHEMY_BINDS'][package_name] = f"sqlite:///{os.path.join(os.path.dirname(__file__), package_name+'.db')}"

class ModelSetting(db.Model):
    __tablename__ = f'{package_name}_setting'
    __bind_key__ = package_name

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String, nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    @staticmethod
    def get(key):
        item = db.session.query(ModelSetting).filter_by(key=key).first()
        return item.value if item else None

    @staticmethod
    def set(key, value):
        item = db.session.query(ModelSetting).filter_by(key=key).first()
        if item:
            item.value = value
        else:
            item = ModelSetting(key, value)
            db.session.add(item)
        db.session.commit()

    @staticmethod
    def to_dict():
        return {x.key: x.value for x in db.session.query(ModelSetting).all()}

    @staticmethod
    def setting_save(req):
        for key, value in req.form.items():
            if key in ['scheduler', 'is_running']:
                continue
            ModelSetting.set(key, value)
        return True
