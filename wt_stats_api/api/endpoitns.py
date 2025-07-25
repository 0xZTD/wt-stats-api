from fastapi import APIRouter, HTTPException

from wt_stats_api.runner.warthunder_scraper_runner import get_player_link

router = APIRouter()


@router.get("/search")
def search_endpoint(q: str):
    results = get_player_link(q)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return {"results": results}


@router.get("/stats")
def stats_endpoint(url: str):
    pass
