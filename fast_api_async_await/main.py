from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from core.exceptions import InvalidDataFormatError
from services.ingestor import DataIngestor
from services.processor import DataProcessor # Yeni sınıf

app = FastAPI()
ingestor = DataIngestor()
processor = DataProcessor() # Instance oluşturma

# --- Custom Error Handler --- (Önceki aşamadan)
@app.exception_handler(InvalidDataFormatError)
async def custom_exception_handler(request: Request, exc: InvalidDataFormatError):
    return JSONResponse(status_code=400, content={"error": exc.message})

# --- Yeni Endpoint: CSV Temizleme ---
@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    # Sadece CSV dosyalarını kabul edelim
    if not file.filename.endswith(".csv"):
        raise InvalidDataFormatError("Yalnızca .csv uzantılı dosyalar kabul edilir.")

    # Dosya içeriğini asenkron oku
    content = await file.read()
    
    try:
        # Pandas ile temizleme işlemini başlat
        cleaned_data = processor.clean_csv_data(content)
        
        return {
            "filename": file.filename,
            "row_count": len(cleaned_data),
            "data": cleaned_data
        }
    except Exception as e:
        # Pandas okuma sırasında bir hata olursa yakala
        raise InvalidDataFormatError(f"CSV işlenirken hata oluştu: {str(e)}")

# Önceki ingest endpointi...
@app.post("/ingest")
async def ingest_data(payload: dict):
    result = await ingestor.process_data(payload)
    return {"status": "success", "detail": result}