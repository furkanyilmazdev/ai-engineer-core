from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from core.exceptions import InvalidDataFormatError
from services.ingestor import DataIngestor
from services.processor import DataProcessor

# Uygulama tanımı ve Metadata
app = FastAPI(
    title="FastAPI Async/Await Örnek Projesi",
    description="Bu proje, FastAPI framework'ünün async/await yapısını kullanarak veri işleme ve hata yönetimi örneği sunar.",
    version="1.0.0"
)
# Servislerin başlatılması (Instance Creation)  
ingestor = DataIngestor()
processor = DataProcessor()

# --- MİMARİ KATMAN: Merkezi Hata Yakalayıcı (Global Exception Handler) ---
# Uygulamanın herhangi bir yerinde fırlatılan InvalidDataFormatError'ı yakalar.
@app.exception_handler(InvalidDataFormatError)
async def custom_exception_handler(request: Request, exc: InvalidDataFormatError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "InvalidDataFormatError",
            "message": exc.message,
            "hint": "Lütfen gönderdiğiniz verinin formatını ve içeriğini kontrol edin."
        }
    )

# --- ENDPOINTS ---

@app.get("/")
async def root():
    return {"status": "online", "message": "FastAPI Async/Await yapısı çalışıyor."}

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Dışarıdan gelen CSV dosyasını asenkron olarak kabul eder, 
    Pandas ile temizler ve JSON olarak döndürür.
    """
    # 1. Dosya uzantısı kontrolü
    if not file.filename.endswith(".csv"):
        raise InvalidDataFormatError("Yalnızca .csv uzantılı dosyalar kabul edilir.")

    # 2. Dosya içeriğini asenkron oku
    content = await file.read()
    
    try:
        # 3. Veri işleme katmanına (Processor) gönder
        cleaned_data = processor.clean_csv_data(content)
        
        return {
            "filename": file.filename,
            "row_count": len(cleaned_data),
            "data": cleaned_data
        }
    except Exception as e:
        # Alt katmanlardan gelen beklenmedik hataları paketleyip yukarı fırlatıyoruz
        raise InvalidDataFormatError(f"Veri işleme sırasında teknik bir hata oluştu: {str(e)}")

@app.post("/ingest")
async def ingest_data(payload: dict):
    """
    Ham JSON verisini asenkron olarak işleyen endpoint.
    """
    # DataIngestor sınıfı içindeki 'process_data' metodu da 
    # InvalidDataFormatError fırlatacak şekilde kurgulanmıştır.
    result = await ingestor.process_data(payload)
    return {"status": "success", "detail": result}