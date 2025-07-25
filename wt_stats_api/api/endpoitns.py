from fastapi import APIRouter, HTTPException
from wt_stats_api.runner import warthunder_scraper_runner

router = APIRouter()


@router.get("/search")
def search_endpoint(q: str):
    results = warthunder_scraper_runner.get_player_link(q)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return {"results": results}


@router.get("/stats")
def stats_endpoint(url: str):
    url = url.strip('"').replace("#", "%23")
    results = warthunder_scraper_runner.get_user_stats_by_url(url)
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return {"results": results}
