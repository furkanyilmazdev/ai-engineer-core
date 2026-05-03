import asyncio
from core.exceptions import InvalidDataFormatError

class DataIngestor:
    def __init__(self):
        self.client_name = "AI-Ingestor-v1"

    async def process_data(self, payload: dict):
        # Bos veriyle islem yapma 
        if not payload or "data" not in payload:
            raise InvalidDataFormatError("Data alanı eksik veya boş gonderildi.")
        

        # 2. Mantıksal kontrol ve Hata Fırlatma
        # Eğer payload içinde 'data' anahtarı yoksa hata fırlatıyoruz
        if "data" not in payload or not payload["data"]:
            raise InvalidDataFormatError("Payload 'data' alanını içermeli ve boş olmamalıdır.")

        # 3. Başarılı senaryo
        return {"status": "success"}