import datetime
import pytz

from fastapi import APIRouter, Body, Query

from db.orm import AsyncOrm
from api.service import extract_domain_with_regex
from api.dependencies import PaginationParamsDep

from models.links import LinksOrm
from schemas.links import LinksCreateRequest


router = APIRouter(
    tags=['Links Statstic']
)


@router.get('/get_links',
            summary='Получить все ссылки')
async def get_links(pagination: PaginationParamsDep,):
    links = await AsyncOrm.get_all_links(pagination.limit, pagination.offset)
    return {
            "status": 'ok',
            'data': links,
            }

@router.get('/visited_domains',
            summary='Получить все посещенные домены')
async def get_visited_domains(pagination: PaginationParamsDep, 
                                time_from: int = Query(...),
                                time_to: int = Query(...),):
    links = await AsyncOrm.get_all_domain_with_timestamp(
        time_from, time_to,
        pagination.limit, pagination.offset,)
    return {
        "status": 'ok',
        'date': links,
        }

@router.post('/links_create',
            summary='Добавить ссылки',)
async def add_links(request_data: LinksCreateRequest = Body(..., description='Объект с массивом ссылок')):
    current_time_utc = datetime.datetime.now(pytz.utc).timestamp()
    links = extract_domain_with_regex(request_data.links)
    for link in set(links):
        await AsyncOrm.add_link(LinksOrm(link=link, timestamp=current_time_utc))
    return {
        "status": 'ok',
        "received_links_count": len(request_data.links),
        "links_processed_example": request_data.links,
        "message": f"Обработано {len(set(links))} ссылок.",
    }
