from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from services.discoverer import search_google_places
from io import StringIO
import pandas as pd

router = APIRouter()

@router.get("/leads")
def get_leads(keyword: str = Query(..., min_length=3)):
    print(f"📥 Keyword received: {keyword}")

    try:
        results = search_google_places(keyword)
        print(f"🔍 Results found: {len(results)}")

        if not results:
            raise HTTPException(status_code=404, detail="No leads found.")

        df = pd.DataFrame(results)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        return StreamingResponse(
            csv_buffer,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=data.csv"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
