# -*- coding:utf-8 -*-

import requests
import os

def list_ten_last_books():
    '''Lister les 10 derniers livres par leurs dates de publication'''

    req = requests.get('https://demo.api-platform.com/books?order%5BpublicationDate%5D=desc')
    all_books = req.json()['hydra:member']

    result = ['\nLes 10 derniers livres parus sont :']

    for book in all_books[:10]:
        result.append(f"""     Titre : {book['title']}
     Paru le : {book['publicationDate'][:10]}""")

    print('\n\n'.join(result))

def list_book_by(auteur='Dr. Kaitlyn Ratke'):
    '''Lister le livre écrit par l’auteur « Dr. Kaitlyn Ratke »'''

    req = requests.get(f"https://demo.api-platform.com/books?author={auteur.replace(' ','%20')}")
    book_by_ratke = req.json()['hydra:member'][0]

    print(f"\nLe livre écrit par {auteur} est : {book_by_ratke['title']}")

def list_all_comments(id='1d52ba85-97c8-4cc3-b81a-40582f3aff64'):
    '''Lister tous les commentaires du livre dont l’id est « 1d52ba85-97c8-4cc3-b81a-40582f3aff64 »'''

    req = requests.get(f'https://demo.api-platform.com/books/{id}/reviews')
    req_content = req.json()

    if 'hydra:view' in req_content.keys():
        last_page = req_content['hydra:view']['hydra:last']
        last_page = int(last_page[last_page.index('=')+1:])
    else:
        last_page = 1

    result = [f"""\nTous le commentaires du livre dont l'id est
'{id}' sont :"""]

    for i in range(1,last_page+1):
        req = requests.get(f'https://demo.api-platform.com/books/{id}/reviews?page={i}')
        all_page_comments = req.json()['hydra:member']

        for comment in all_page_comments:
            result.append(f"{comment['body']}")

    print('\n\n'.join(result))

def create_comment(auteur='Romain', comment='Voila ce que je pense de ce bouquin', note=4, id='1b08c9ab-6254-4015-ad14-bac3e5c008df'):
    '''Créer un nouveau commentaire avec le texte et la note de votre choix pour le livre dont l’id est :
        « 1b08c9ab-6254-4015-ad14-bac3e5c008df »'''

    content_review = {'author':auteur,
    'body':comment,
    'rating':note,
    'book':f'books/{id}'}

    req = requests.post('https://demo.api-platform.com/reviews', json=content_review)

    id_review = req.json()['@id']
    id_review = id_review[id_review.index('/reviews/')+len('/reviews/'):]

    print(f'\nL\'id de votre nouveau commentaire est : {id_review}')

def edit_review(id_post, auteur='Romain', comment='Mon commentaire édité'):
    '''Modifier votre nouveau commentaire en utilisant l’id qui vous a été fourni lors de sa création'''

    content_review = {'author':auteur,
    'body':comment
    }

    headers_review = {'Content-Type':'application/merge-patch+json'}

    requests.patch(f'https://demo.api-platform.com/reviews/{id_post}', json=content_review, headers=headers_review)

if __name__ == '__main__':

    while True:
        choix = input('''\n[1] Lister les 10 derniers livres par leurs dates de publication

[2] Lister le livre écrit par l’auteur « Dr. Kaitlyn Ratke »

[3] Lister tous les commentaires du livre dont l’id est :
    1d52ba85-97c8-4cc3-b81a-40582f3aff64

[4] Créer un nouveau commentaire pour le livre dont l’id est :
    1b08c9ab-6254-4015-ad14-bac3e5c008df

[5] Modifier votre nouveau commentaire

Choix : ''')

        if choix == '1':
            list_ten_last_books()
        elif choix == '2':
            list_book_by()
        elif choix == '3':
            list_all_comments()
        elif choix == '4':
            create_comment()
        elif choix == '5':
            id_comment = input('\nEntrez l\'id du commentaire à modifier : ')
            edit_review(id_comment)
        else:
            print('\nChoix incorrect!')
