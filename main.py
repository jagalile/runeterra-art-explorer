import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


BATCH = 12
REGIONS = {
    "all": "All",
    "bandlecity": "Bandle City",
    "bilgewater": "Bilgewater",
    "demacia": "Demacia",
    "freljord": "Freljord",
    "ionia": "Ionia",
    "noxus": "Noxus",
    "piltoverzaun": "Piltover & Zaun",
    "runeterra": "Runeterra",
    "shadowisles": "Shadow Isles",
    "shurima": "Shurima",
    "targon": "Targon",
}


@app.get("/", response_class=HTMLResponse)
async def root(request: Request) -> HTMLResponse:

    return templates.TemplateResponse(
        request=request,
        name="base.html",
        context={"cards": [], "index": 0, "region": "all"},
    )


@app.get("/pagination", response_class=HTMLResponse)
async def pagination(request: Request, index: int, region: str) -> HTMLResponse:
    start = index
    end = start + BATCH

    cards = await read_cards()
    cards = filter_cards_by_region(cards=cards, region=region)
    cards = get_pagination_cards(cards=cards, start=start, end=end)

    if len(cards) == 0:
        return templates.TemplateResponse(
            request=request,
            name="footer.html",
            context={"cards": [], "index": start, "region": region},
        )

    return templates.TemplateResponse(
        request=request,
        name="cards.html",
        context={"cards": cards, "index": end, "region": region},
    )


@app.get("/region/{region}", response_class=HTMLResponse)
async def region_cards(request: Request, region: str) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="base.html",
        context={"cards": [], "index": 0, "region": region},
    )


async def read_cards() -> list:
    with open("data/cards.json") as f:
        cards = json.load(f)

    return cards


def filter_cards_by_region(cards: list, region: str = "all") -> list:
    if REGIONS[region] == "All":
        return cards
    return [card for card in cards if REGIONS[region] in card["regions"]]


def get_pagination_cards(cards: list, start: int, end: int) -> list:
    return cards[start:end]
