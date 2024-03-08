import tls_client as tls
import json


from charaiPY.AsyncPyCAI2 import PyAsyncCAI2

# ______         ______ _______ _______ ______ 
# |   __ \ __ __ |      |   _   |_     _|__    |
# |    __/|  |  ||   ---|       |_|   |_|    __|
# |___|   |___  ||______|___|___|_______|______|
#         |_____|                                 

                                                           
# BUILD BY @Falco_TK (https://github.com/FalcoTK)
# CODE  BY @kramcat  (https://github.com/kramcat)
# PATCH BY @kpopdev  (https://github.com/kpopdev)

# PLEASE IF YOU HAVE SOMTING WRONG DM ME IN DISCORD ASAP! (discord: tokaifalco_)                                                  
# ==================================================

class PyCAI2EX(Exception):
    pass

class ServerError(PyCAI2EX):
    pass

class LabelError(PyCAI2EX):
    pass

class AuthError(PyCAI2EX):
    pass

class PostTypeError(PyCAI2EX):
    pass

__all__ = ['PyCAI2', 'PyAsyncCAI2']

class PyCAI2:
    def __init__(
        self, token: str = None, plus: bool = False
    ):
        self.token = token

        if plus: sub = 'plus'
        else: sub = 'beta'

        self.session = tls.Session(
            client_identifier='chrome112'
        )

        setattr(self.session, 'url', f'https://{sub}.character.ai/')
        setattr(self.session, 'token', token)


        self.chat = self.chat(token, self.session)

    def request(
        url: str, session: tls.Session,
        *, token: str = None, method: str = 'GET',
        data: dict = None, split: bool = False,
        neo: bool = False
    ):
        if neo:
            link = f'https://neo.character.ai/{url}'
        else:
            link = f'{session.url}{url}'

        if token == None:
            key = session.token
        else:
            key = token

        headers = {
            'User-Agent': 'okhttp/5.0.0-SNAPSHOT',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://beta.character.ai/',
            'Authorization': f'Token {key}',
            'Origin': 'https://beta.character.ai',
        }

        if method == 'GET':
            response = session.get(
                link, headers=headers
            )

        elif method == 'POST':
            response = session.post(
                link, headers=headers, json=data
            )

        elif method == 'PUT':
            response = session.put(
                link, headers=headers, json=data
            )

        if split:
            data = json.loads(response.text.split('\n')[-2])
        else:
            data = response.json()

        if str(data).startswith("{'command': 'neo_error'"):
            raise ServerError(data['comment'])
        elif str(data).startswith("{'detail': 'Auth"):
            raise AuthError('Invalid token')
        elif str(data).startswith("{'status': 'Error"):
            raise ServerError(data['status'])
        elif str(data).startswith("{'error'"):
            raise ServerError(data['error'])
        else:
            return data

    def ping(self):
        return self.session.get(
            'https://neo.character.ai/ping/'
        ).json()
    
    class chat:
        def __init__(
            self, token: str, session: tls.Session
        ):
            self.token = token
            self.session = session

        def next_message(
            self, history_id: str, parent_msg_uuid: str,
            tgt: str, *, token: str = None, **kwargs
        ):
            response = PyCAI2.request(
                'chat/streaming/', self.session,
                token=token, method='POST', split=True,
                data={
                    'history_external_id': history_id,
                    'parent_msg_uuid': parent_msg_uuid,
                    'tgt': tgt,
                    **kwargs
                }
            )
            return response

        def get_histories(
            self, char: str, *, number: int = 50,
            token: str = None
        ):
            return PyCAI2.request(
                'chat/character/histories_v2/', self.session,
                token=token, method='POST',
                data={'external_id': char, 'number': number},
            )

        def get_history(
            self, history_id: str = None,
            *, token: str = None
        ):
            return PyCAI2.request(
                'chat/history/msgs/user/?'
                f'history_external_id={history_id}',
                self.session, token=token
            )

        def get_chat(
            self, char: str = None, *,
            token: str = None, **kwargs
        ):
            return PyCAI2.request(
                'chat/history/continue/', self.session,
                token=token, method='POST',
                data={
                    'character_external_id': char,
                    **kwargs
                }
            )

        def send_message(
            self, history_id: str, tgt: str, text: str,
            *, token: str = None, **kwargs
        ):
            return PyCAI2.request(
                'chat/streaming/', self.session,
                token=token, method='POST', split=True,
                data={
                    'history_external_id': history_id,
                    'tgt': tgt,
                    'text': text,
                    **kwargs
                }
            )

        def delete_message(
            self, history_id: str, uuids_to_delete: list,
            *, token: str = None, **kwargs
        ):
            return PyCAI2.request(
                'chat/history/msgs/delete/', self.session,
                token=token, method='POST',
                data={
                    'history_id': history_id,
                    'uuids_to_delete': uuids_to_delete,
                    **kwargs
                }
            )

        def new_chat(
            self, char: str, *, token: str = None
        ):
            return PyCAI2.request(
                'chat/history/create/', self.session,
                token=token, method='POST',
                data={
                    'character_external_id': char
                }
            )