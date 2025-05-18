import os
import json
from fastapi import HTTPException
import requests
from .setings import API_KEYS, BIN_ID
from .library_api import OpenLibraryAPI



class JsonBinClient:
    def __init__(self):
        self.api_key = API_KEYS
        self.base_url = 'https://api.jsonbin.io/v3/b/'
        self.bin_id = BIN_ID
    
    def get_books(self) -> dict:
        url = f'{self.base_url}{self.bin_id}'
        headers = {'X-Access-Key': self.api_key}
        response = requests.get(url, headers=headers)
        return response.json()
    
    def get_book(self, title: str) -> dict:
        url = f'{self.base_url}{self.bin_id}'
        headers = {'X-Access-Key': self.api_key}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()['record']
        for book in data:
            if book['title'] == title:
                return book

        raise HTTPException(status_code=404, detail='Book not found')
    
    def add_book(self, book: dict) -> dict:

        get_url = f'{self.base_url}{self.bin_id}/latest'
        headers = {
            'X-Master-Key': '$2a$10$VTBr0cpzUWdfTIfyl3Rb5u60I6TjkpAlesONyjYW6YoDpu1jlSbGe',  # именно Master-Key для записи
            'Content-Type': 'application/json'
        }
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()

        data = response.json()['record']

        if any(b['id'] == book['id'] for b in data):
            raise HTTPException(status_code=400, detail='Книга уже существует')
        
        ol_client = OpenLibraryAPI()
        extra = ol_client.search_books(title=book['title'], author=book['author'])

        book['description'] = extra.get('description')
        book['cover_url'] = extra.get('cover_url')
        
        if not book.get('year') and extra.get('first_publish_year'):
            book['year'] = extra['first_publish_year']
    
        data.append(book)

        put_url = f'{self.base_url}{self.bin_id}'
        response = requests.put(put_url, headers=headers, json=data)
        response.raise_for_status()
        return book
    
    def update_book(self, book: dict) -> dict:
        get_url = f'{self.base_url}{self.bin_id}/latest'
        headers = {
            'X-Master-Key': '$2a$10$VTBr0cpzUWdfTIfyl3Rb5u60I6TjkpAlesONyjYW6YoDpu1jlSbGe',  
            'Content-Type': 'application/json'
        }
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()

        data = response.json()['record']

        for i, b in enumerate(data):
            if b['id'] == book['id']:
                data[i] = book
                break

        put_url = f'{self.base_url}{self.bin_id}'
        response = requests.put(put_url, headers=headers, json=data)
        response.raise_for_status()
        return book
    
    def delete_book(self, book_id: int) -> dict:
        get_url = f'{self.base_url}{self.bin_id}/latest'
        headers = {
            'X-Master-Key': '$2a$10$VTBr0cpzUWdfTIfyl3Rb5u60I6TjkpAlesONyjYW6YoDpu1jlSbGe',  
            'Content-Type': 'application/json'
        }
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()

        data = response.json()['record']

        for i, b in enumerate(data):
            if b['id'] == book_id:
                del data[i]
                break

        put_url = f'{self.base_url}{self.bin_id}'
        response = requests.put(put_url, headers=headers, json=data)
        response.raise_for_status()
        return data