from fastapi import APIRouter, HTTPException
from wt_stats_api.runner import warthunder_scraper_runner
from selenium.common.exceptions import WebDriverException

router = APIRouter()


@router.get("/search")
def search_endpoint(q: str):
    try:
        results = warthunder_scraper_runner.get_player_link(q)
    except WebDriverException as e:
        raise HTTPException(status_code=500, detail="Server error")

    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return {"results": results}


@router.get("/stats")
def stats_endpoint(url: str):
    url = url.strip('"').replace("#", "%23")
    try:
        results = warthunder_scraper_runner.get_user_stats_by_url(url)
    except WebDriverException as e:
        raise HTTPException(status_code=500, detail="Server error")

    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return {"results": results}
