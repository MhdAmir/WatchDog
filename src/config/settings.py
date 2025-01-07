class Config:
    def __init__(self, models=None, cctvs=None):
        self.models = models if models is not None else [
            {
                "name": "ppe",
                "model_path": "models/ppe_model.tflite",
                "label_path": "models/ppe_labels.txt",
                "threshold": 0.5
            },
            {
                "name": "person",
                "model_path": "models/person_model.tflite",
                "label_path": "models/person_labels.txt",
                "threshold": 0.5
            }
        ]
        self.cctvs = cctvs if cctvs is not None else [
            {
                "device_name": "CCTV_1",
                "stream_url": "http://",
                "detection_configs": {
                    "crop_area": (100, 50, 500, 400),
                    "models": ["ppe", "person"]
                }
            }
        ]
    