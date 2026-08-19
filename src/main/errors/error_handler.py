from src.main.errors.api_key_error import ApiKeyError
from src.main.errors.http_badrequest import HttpBadRequestError
from src.main.errors.http_not_found import NotFoundError

def handler_error(error: Exception) -> dict:
    """
    Tratamento de erros. O código tem 3 tipos de erros específicos diferentes:
        1. ApiKeyError - Acontece quando a chave da API está incorreta. A própria API do clima retorna 401.
        2. HttpBadRequestError - Para erros do lado do usuário. Campo 'cep' como str, espaços ou incorretos.
        3. NotFoundError - Para quando o nome da cidade está incorreto. A própria API retorna 404.

    Se não for nenhum erro personalizado, retorna uma mensagem genérica da própria Exceção, mas formatado corretamente.
    """
    if isinstance(error, (ApiKeyError, HttpBadRequestError, NotFoundError)):
        return {
            "status_code": error.status_code,
            "data": {
                "type": error.type,
                "message": error.message
            }
        }

    return {
        "status_code": 500,
        "data": {
            "type": "Server Error",
            "message": str(error)
        }
    }