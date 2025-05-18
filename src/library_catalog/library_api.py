import requests

class OpenLibraryAPI:
    BASE_URL = "https://openlibrary.org/search.json?"

    def search_books(self, title:str, author:str) -> dict:
        params = {
            "title": title,
            "author": author,
            "limit": 1
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json().get('docs', [])
        print(data)
        if not data:
            return {}
        doc = data[0]

        description = doc.get('first_sentence') or doc.get('subtitle') or None

        cover_id = doc.get('cover_i')
        cover_url = f"http://covers.openlibrary.org/b/id/{cover_id}-L.jpg" if cover_id else None

        first_publish_year = doc.get('first_publish_year') or None

        return {'description': description, 'cover_url': cover_url, 'first_publish_year': first_publish_year}


    

