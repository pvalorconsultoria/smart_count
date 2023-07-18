from src.db.models.batches import Batch, BatchManager
from src.db.db import DB

batches = [
    {
        "dataDeProcessamento": "13/07/2023",
        "camera": "001",
        "produto": "Peça de Metal",
        "linhaDeProducao": "Padrão",
        "planta": "Padrão",
        "quantidadeContada": 42,
        "videoPath": "assets\\video.mp4",
        "modelConfig": "config\\basic.yaml"
    },
    {
        "dataDeProcessamento": "13/07/2023",
        "camera": "001",
        "produto": "Peça de Metal",
        "linhaDeProducao": "Padrão",
        "planta": "Padrão",
        "quantidadeContada": 42,
        "videoPath": "assets\\video2.mp4",
        "modelConfig": "config\\basic.yaml"
    },
    {
        "dataDeProcessamento": "13/07/2023",
        "camera": "001",
        "produto": "Rosca de Metal",
        "linhaDeProducao": "Campo Limpo Paulista",
        "planta": "Thyssen-Krupp",
        "quantidadeContada": 42,
        "videoPath": "assets\\video_thyssen.mp4",
        "modelConfig": "config\\thyssen_krupp.yaml"
    },
    {
        "dataDeProcessamento": "13/07/2023",
        "camera": "001",
        "produto": "Clips de Metal",
        "linhaDeProducao": "Casa",
        "planta": "Belo Horizonte",
        "quantidadeContada": 42,
        "videoPath": "assets\\video_clips.mp4",
        "modelConfig": "config\\clips.yaml"
    },
    {
        "dataDeProcessamento": "13/07/2023",
        "camera": "001",
        "produto": "Webcam",
        "linhaDeProducao": "Casa",
        "planta": "São Paulo",
        "quantidadeContada": 42,
        "videoPath": 0,
        "modelConfig": "config\\webcam.yaml"
    }
]

def run_migrations(db: DB):
    
    with db.session_manager as session:
        batch_manager = BatchManager(session)

        batch_manager.create_all(db.engine)

        for batch in batches:
            batch_obj = Batch(**batch)  # Create a Batch object
            batch_manager.add_batch(batch_obj)
