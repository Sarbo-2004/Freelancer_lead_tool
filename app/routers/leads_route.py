from fastapi import APIRouter, File, UploadFile, Response
from fastapi.responses import StreamingResponse
import pandas as pd
import shutil
import os
import io
from services.screenshot_utils import process_and_audit_batch

router = APIRouter()

@router.post("/audit_batch/")
def audit_batch(file: UploadFile = File(...), max_sites: int = 5):
    temp_path = f"temp_uploads/{file.filename}"
    os.makedirs("temp_uploads", exist_ok=True)

    # Save uploaded CSV to disk
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run batch audit (sync)
    results = process_and_audit_batch(temp_path, max_sites=max_sites)

    # Convert to CSV and stream back
    df = pd.DataFrame(results)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)

    return Response(
        content=csv_buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=audit_report.csv"},
    )
