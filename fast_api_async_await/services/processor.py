import pandas as pd
import io
from typing import List, Dict

class DataProcessor:
    def __init__(self):
        self.description = "Pandas tabanlı veri temizleyici"

    def clean_csv_data(self, csv_content: bytes) -> List[Dict]:
        # Bayt verisini Pandas ile okuyoruz
        df = pd.read_csv(io.BytesIO(csv_content))

        # 1. Boş (NaN) satırları temizle
        df_cleaned = df.dropna()

        # 2. Basit bir manipülasyon: Sütun isimlerini küçük harf yap
        df_cleaned.columns = [col.lower() for col in df_cleaned.columns]

        # 3. Örnek bir manipülasyon: 'price' sütunu varsa %20 vergi ekle (varsayalım)
        if 'price' in df_cleaned.columns:
            df_cleaned['price_with_tax'] = df_cleaned['price'] * 1.20

        # Temiz veriyi JSON formatına (liste içinde sözlükler) dönüştür
        return df_cleaned.to_dict(orient="records")