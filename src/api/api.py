
class Api(object):
    def __init__(self) -> None:
        pass

    def get_processed_batches(self):
        return [
            {
                "dataDeProcessamento": "13/07/2023",
                "camera": "001",
                "produto": "Peça de Metal",
                "linhaDeProducao": "Padrão",
                "planta": "Padrão",
                "quantidadeContada": 42,
                "videoPath": "assets\\video.mp4"
            },
            {
                "dataDeProcessamento": "13/07/2023",
                "camera": "001",
                "produto": "Peça de Metal",
                "linhaDeProducao": "Padrão",
                "planta": "Padrão",
                "quantidadeContada": 42,
                "videoPath": "assets\\video2.mp4"
            },
            {
                "dataDeProcessamento": "13/07/2023",
                "camera": "001",
                "produto": "Rosca de Metal",
                "linhaDeProducao": "Campo Limpo Paulista",
                "planta": "Thyssen-Krupp",
                "quantidadeContada": 42,
                "videoPath": "assets\\video_thyssen.mp4"
            },
            {
                "dataDeProcessamento": "13/07/2023",
                "camera": "001",
                "produto": "Clips de Metal",
                "linhaDeProducao": "Casa",
                "planta": "Belo Horizonte",
                "quantidadeContada": 42,
                "videoPath": "assets\\video_clips.mp4"
            }
        ]