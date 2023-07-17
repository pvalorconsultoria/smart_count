from src.db.db import DB
from src.db.models.batches import BatchManager, Batch

class Api(object):
    def __init__(self, db_uri: str) -> None:
        self.db = DB(db_uri)

    def add_processed_batch(self, batch_data: dict):
        with self.db.session_manager as session:
            batch_manager = BatchManager(session)
            new_batch = Batch(**batch_data)
            batch_manager.add_batch(new_batch)

    def get_processed_batches(self):
        with self.db.session_manager as session:
            batch_manager = BatchManager(session)
            all_batches = batch_manager.get_all_batches()
            all_batches = [self._batch_to_dict(batch) for batch in all_batches]

        return all_batches

    def _batch_to_dict(self, batch: Batch) -> dict:
        return {
            "dataDeProcessamento": batch.dataDeProcessamento,
            "camera": batch.camera,
            "produto": batch.produto,
            "linhaDeProducao": batch.linhaDeProducao,
            "planta": batch.planta,
            "quantidadeContada": batch.quantidadeContada,
            "videoPath": batch.videoPath,
            "modelConfig": batch.modelConfig
        }
