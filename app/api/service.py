import re


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
        return list_urls # Возвращаем оригинальный массив с при ошибке
