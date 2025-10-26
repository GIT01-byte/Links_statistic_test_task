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

# @router.put('/{task_id}/edit', summary='Изменить задачу 📝')
# async def edit_task(
#     task_id: int, 
#     updated_task: TaskUpdateSchema
#     ):
#     task = await TaskRepository.get_by_id(task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="Задача не найдена")
    
#     task.name = updated_task.name
#     task.description = updated_task.description

#     updated_task = await TaskRepository.update_task(task) 
#     return {'succes': True, 'task': updated_task}

# @router.patch("/{task_id}/complete", response_model=TaskSchema)
# async def complete_task(task_id: int):
#     task = await TaskRepository.get_by_id(task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="Задача не найдена")

#     task.completed = not task.completed
#     updated_task = await TaskRepository.update_task(task)
#     return updated_task

# @router.delete('/{task_id}/delete', summary='Удалить задачу 🗑')
# async def delete_task(task_id: int):
#     task = await TaskRepository.get_by_id(task_id)
#     if task is None:
#         raise HTTPException(status_code=404, detail="Задача не найдена")
    
#     await TaskRepository.delete_task(task_id)
#     return {'succes': True} 

# @router.delete('/delete-many', summary='Удалить несколько задач 🗑')
# async def delete_tasks(task_ids: List[int] = Query(..., description="Список ID задач для удаления")):
#     for task_id in task_ids:
#         task = await TaskRepository.get_by_id(task_id)
#         if task is None:
#             raise HTTPException(status_code=404, detail=f"Задача с ID {task_id} не найдена") 

#     await TaskRepository.delete_tasks(task_ids) 
#     return {'success': True, 'deleted_count': len(task_ids)}
