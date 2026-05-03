import pandas as pd
import io
from typing import List, Dict

# services/processor.py
import pandas as pd
import io

class DataProcessor:
    def clean_csv_sync(self, content: bytes):
        """
        Ağır CPU işlemi: Veriyi DataFrame'e çevirir ve temizler.
        Bu fonksiyon senkrondur (async değildir).
        """
        # Bytes içeriğini bir dosya gibi okuyoruz
        df = pd.read_csv(io.BytesIO(content))
        
        # NaN değerleri temizleme (Örn: Boş satırları sil, sayısal yerlere 0 koy)
        df = df.dropna(how='all') # Tamamen boş satırları sil
        df = df.fillna(0)         # Geri kalan boşlukları 0 ile doldur
        
        return df.to_dict(orient="records")