import asyncio
from core.exceptions import InvalidDataFormatError

class DataIngestor:
    def __init__(self):
        self.client_name = "AI-Ingestor-v1"

    async def process_data(self, payload: dict):
        # 1. Dış API çağrısını simüle et (Network I/O)
        print(f"[{self.client_name}] Dış API'ye bağlanılıyor...")
        await asyncio.sleep(2) 

        # 2. Mantıksal kontrol ve Hata Fırlatma
        # Eğer payload içinde 'data' anahtarı yoksa hata fırlatıyoruz
        if "data" not in payload or not payload["data"]:
            raise InvalidDataFormatError("Payload 'data' alanını içermeli ve boş olmamalıdır.")

        # 3. Başarılı senaryo
        return {"status": "processed", "length": len(payload["data"])}