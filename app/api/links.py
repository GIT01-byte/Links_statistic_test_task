import datetime
import re
from typing import Dict, List
import pytz

from fastapi import APIRouter, Body, Query
from db.orm import AsyncOrm

from models.links import LinksOrm
from schemas.links import LinksCreateRequest

def extract_domain_with_regex(urls: list[str]) -> list[str]:
    """
    Извлекает доменное имя из URL-адреса с помощью регулярного выражения.
    """
    list_urls = []
    try:
        for url in urls:
            # 1. Убираем протокол (http://, https://, ftp://)
            url_no_protocol = re.sub(r'^[a-zA-Z]+://', '', url)
            
            # 2. Убираем все, что идет после первого '/' или '?'
            domain_part = re.split(r'[/?:#]', url_no_protocol)[0]
            
            # 3. Убираем порт, если он есть
            domain = domain_part.split(':')[0]
            
            # Если получилось пустое доменное имя (например, после парсинга 'invalid-url-format'),
            # попробуем вернуть оригинал или пустую строку.
            if not domain:
                list_urls.append(url) # Добавляем оригинал 
                
            # Проверка, что это похоже на домен (содержит точку и не является просто словами)
            # Можно добавить более строгие проверки, если нужно.
            if '.' in domain and len(domain) > 2:
                list_urls.append(domain)
            else:
                # Если результат не похож на домен, добавляем оригинал (или пустую строку)
                list_urls.append(url)
            
        return list_urls
    except Exception as e:
        print(f"Ошибка при парсинге URL '{url}' с помощью regex: {e}")
        return list_urls # Возвращаем оригинал при ошибке

router = APIRouter(
    tags=['Links Statstic']
)


@router.get('/get_links',
            summary='Получить все ссылки')
async def get_links():
    links = await AsyncOrm.get_all_links()
    return {'data': links}

@router.get('/visited_domains',
            summary='Получить все посещенные домены')
async def get_visited_domains(time_from: int = Query(...), time_to: int = Query(...)):
    links = await AsyncOrm.get_all_domain_with_timestamp(time_from, time_to)
    return {'date': links}

@router.post('/links_create',
            summary='Добавить ссылки',)
async def add_links(request_data: LinksCreateRequest = Body(..., description='Объект с массивом ссылок')):
    current_time_utc = datetime.datetime.now(pytz.utc).timestamp()
    links = extract_domain_with_regex(request_data.links)
    for link in set(links):
        await AsyncOrm.add_link(LinksOrm(link=link, timestamp=current_time_utc))
    return {
        "succes": True,
        "received_links_count": len(request_data.links),
        "links_processed_example": request_data.links,
        "status": "success",
        "message": f"Обработано {len(set(links))} ссылок."
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
