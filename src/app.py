import aiofiles, json, uvicorn
from data.schemas import Range
from database.core import get_db
from auth.utils import check_token
from sqlalchemy.exc import IntegrityError
from scrapers.scraper_api import get_assets
from database.core import ProgramRepository
from auth.auth import router as auth_router
from fastapi import FastAPI, Depends, status
from fastapi.exceptions import HTTPException


app = FastAPI()


@app.get('/parse_assets/{number_of_results}', status_code=status.HTTP_200_OK, summary='Запарсить ассеты с открытого api в n количестве и положить в БД')
async def parse_assets(number_of_results: int, token: str = Depends(check_token), session = Depends(get_db)):
    try:
        await get_assets(number_of_results)
        async with aiofiles.open('src/scrapers/parse_results/result_post.json', 'r', encoding='utf-8') as file:
            progs_dict: dict = json.loads((await file.read()))

        await ProgramRepository.add_all_progs(progs_dict, session)

        return progs_dict

    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, 'One of the elements already existss')

    except:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid request')


@app.get('/get_assets/{range}', summary='Достать ассеты с ценой в определенном range')
async def get_assets_in_price_range(range: Range, session = Depends(get_db), token: str = Depends(check_token)):
    from_ = int(range.title().split('...')[0])
    to = int(range.title().split('...')[1])
    try:
        result = await ProgramRepository.filter_progs(from_, to, session)
        return {"result": result}
    except Exception as e:
        print(e)
        raise HTTPException(404, 'Invalid request')
    

@app.get('/get_asset_by_id/{id}', summary='Получить asset по id')
async def get_asset_by_id(id: int, session = Depends(get_db)):
    asset = await ProgramRepository.select_asset_by_id(id, session)
    if not asset:
        raise HTTPException(404, 'Not found')
    return asset


app.include_router(auth_router, prefix='/auth', tags=['Auth'])


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
