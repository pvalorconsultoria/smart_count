from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Batch(Base):
    __tablename__ = 'batches'

    id = Column(Integer, primary_key=True)
    dataDeProcessamento = Column(String)
    camera = Column(String)
    produto = Column(String)
    linhaDeProducao = Column(String)
    planta = Column(String)
    quantidadeContada = Column(Integer)
    videoPath = Column(String)
    modelConfig = Column(String)

class BatchManager:
    def __init__(self, session):
        self.session = session

    def add_batch(self, batch):
        self.session.add(batch)
        self.session.commit()

    def get_all_batches(self):
        return self.session.query(Batch).all()

    def get_batch_by_id(self, id):
        return self.session.query(Batch).filter_by(id=id).first()

    def update_batch(self, id, new_data):
        batch = self.session.query(Batch).filter_by(id=id).first()
        for key, value in new_data.items():
            setattr(batch, key, value)
        self.session.commit()

    def delete_batch(self, id):
        batch = self.session.query(Batch).filter_by(id=id).first()
        self.session.delete(batch)
        self.session.commit()

    def create_all(self, engine):
        Base.metadata.create_all(engine)
