from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from services.discoverer import search_google_places
from io import StringIO
import pandas as pd
import csv

router = APIRouter()

@router.get("/leads")
async def get_leads(keyword: str = Query(..., min_length=3)):
    try:
        # Get search results
        results = search_google_places(keyword)
        
        # Check if we got valid results
        # if not results:
        #     raise HTTPException(status_code=404, detail="No results found")
        
        # # Prepare CSV output
        # output = StringIO()
        # writer = csv.writer(output)
        
        # # Write header row if we have dictionary results
        # if isinstance(results, list) and len(results) > 0:
        #     if isinstance(results[0], dict):
        #         headers = results[0].keys()
        #         writer.writerow(headers)
        #         for item in results:
        #             writer.writerow(item.values())
        #     else:
        #         writer.writerows(results)
        
        # output.seek(0)
        df = pd.DataFrame(results)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        # Create the streaming response
        return StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"}
    )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))