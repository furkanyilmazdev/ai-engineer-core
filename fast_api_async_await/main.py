from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from core.exceptions import InvalidDataFormatError
from services.ingestor import DataIngestor
from services.processor import DataProcessor
from starlette.concurrency import run_in_threadpool
import time 

# Uygulama tanımı ve Metadata
app = FastAPI(
    title="FastAPI Async/Await Örnek Projesi",
    description="Bu proje, FastAPI framework'ünün async/await yapısını kullanarak veri işleme ve hata yönetimi örneği sunar.",
    version="1.0.0"
)

# Servislerin başlatılması (Instance Creation)  
ingestor = DataIngestor()
processor = DataProcessor()

# --- MİMARİ KATMAN: Merkezi Hata Yakalayıcı ---
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
async def upload_csv_optimized(file: UploadFile = File(...)):
    start_time = time.time()  # 1. BAŞLANGIÇ ZAMANI
    
    if not file.filename.endswith(".csv"):
        raise InvalidDataFormatError("Yalnızca .csv uzantılı dosyalar kabul edilir.")

    content = await file.read()
    
    try:
        # Ağır işlemi thread pool'a gönderiyoruz
        cleaned_data = await run_in_threadpool(processor.clean_csv_sync, content)
        
        # 2. SÜREYİ HESAPLA (Return'den önce!)
        process_time = time.time() - start_time
        
        # 3. TERMİNALE YAZDIR
        print(f"\n--- Islem Suresi: {process_time:.4f} saniye ---")
        
        return {
            "process_time": f"{process_time:.4f}s", # Swagger'da görmek için
            "filename": file.filename,
            "row_count": len(cleaned_data),
            "data": cleaned_data
        }
    except Exception as e:
        raise InvalidDataFormatError(f"Veri işleme sırasında teknik bir hata oluştu: {str(e)}")

@app.post("/ingest")
async def ingest_data(payload: dict):
    result = await ingestor.process_data(payload)
    return {"status": "success", "detail": result}