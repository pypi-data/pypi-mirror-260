# Tools kit

Desc aqui

## Instalação

Você pode instalar o pacote via pip. Execute o seguinte comando no terminal:
`pip install tools-kit`

## Constantes:
Para utilizar as constantes do pacote, basta importar os arquivos:
`from tools_rest import nome_arquivo_const`
Ex.:
```python
from tools_rest import constants_exc

pegar_conteudo = constants_exc.HTTP_400
print(pegar_conteudo) #impreme o valor: Verifique se os dados enviados estão corretos e completos.
```
Ou:
`from tools_rest.nome_arquivo_const import nome_const`
Ex.:
```python
from tools_rest.constants_exc import HTTP_400

pegar_conteudo = HTTP_400
print(pegar_conteudo) #impreme o valor: Verifique se os dados enviados estão corretos e completos.
```

### Nomes arquivos e constantes:
```python
constants_exc:
        HTTP_400
        HTTP_403
        HTTP_404
        HTTP_500
```

## Exceptions Handler
Para que o handler customizado seja ativado, basta adicionar uma chave em `settings.py`:
```json
CUSTOM_EXCEPTION = {
}
```

#### Configurando
Para adicionar o handler personalizado de exceções rest, basta adicionar o atributo `ADD_CUSTOM_HANDLER` a chave `CUSTOM_EXCEPTION` localizada no arquivo `settings.py`:
```python
CUSTOM_EXCEPTION = {
    'ADD_CUSTOM_HANDLER': True
}
```

Ao receber uma exceção 400, essa personalização irá retornar o seguinte modelo:
```python
{
    'result': null,
    'errors': [
        conteudo da constante constants_exc.HTTP_400 ou personalizado
    ],
    'success': False
}
#Obs.: Quando a exceção for de validators, o conteudo de errors sera 'nomeProp: mensagem de falha'
#Ex.: 'name: Campo obrigatório'
```

Ao receber uma exceção 403, essa personalização irá retornar o seguinte modelo:
```python
{
    'result': null,
    'errors': [
        conteudo da constante constants_exc.HTTP_403 ou personalizado
    ],
    'success': False
}
```

Ao receber uma exceção 404, essa personalização irá retornar o seguinte modelo:
```python
{
    'result': null,
    'errors': [
        conteudo da constante constants_exc.HTTP_404 ou personalizado
    ],
    'success': False
}
```

Ao receber uma exceção 500, essa personalização irá retornar o seguinte modelo:
```python
{
    'result': null,
    'errors': [
        conteudo da constante constants_exc.HTTP_500 ou personalizado
    ],
    'success': False
}
```

#### Handlers urls base
Este modelo é utilizado para não obter mensagens fora de um padrão, trazendo assim o modelo
```python
{
    'result': null,
    'errors': [
        conteudo da constante constants_exc ou personalizado
    ],
    'success': False
}
```

Para adicionar um ou mais handler de urls base, existem duas formas
1 - Adicionando um parametro a chave `CUSTOM_EXCEPTION` no arquivo `settings.py`:
```python
CUSTOM_EXCEPTION = {
    'ADD_CUSTOM_HANDLER': True,
    'URLS_HANDLER': (400, 403, 404, 500)
}
```
Não é necessario ter a chave `ADD_CUSTOM_HANDLER` para utilizar os handlers base.
Pode ter um ou mais codigos, sendo eles `400`, `403`, `404`, `500`

2 - Chamando os metodos criados diretamente no handler, para isso, basta importar os metodos customizados dentro do arquivo `urls`, no diretório que esta o `settings.py` da aplicação.
`from tools_rest.exceptions import exception_400, exception_403, exception_404, exception_500`
`from tools_rest import exceptions`
Ex.:
```python
from tools_rest.exceptions import exception_400, exception_403, exception_404, exception_500

handler400 = exception_400
handler403 = exception_403
handler404 = exception_404
handler500 = exception_500

ou

from tools_rest import exceptions

handler400 = exceptions.exception_400
handler403 = exceptions.exception_403
handler404 = exceptions.exception_404
handler500 = exceptions.exception_500
```
Não é necessario adicionar os quatro handlers, pode ser editado um ou mais.

#### Customizando mensagens
Para customizar mensagens, é necessário adicionar à chave `CUSTOM_EXCEPTION` localizada em `settings.py` o seguinte comando:
```json
CUSTOM_EXCEPTION = {
    'EXCEPTIONS':{
        'HTTP_400': 'Mensagem personalizada para o erro 400',
        'HTTP_403': 'Mensagem personalizada para o erro 403',
        'HTTP_404': 'Mensagem personalizada para o erro 404',
        'HTTP_500': 'Mensagem personalizada para o erro 500'
    }
}
```
Pode alterar um ou mais status, porem, a que não for mencionada a essa chave, utilizarão as padrões que existem.

## Modelo padrão de resultado:
ResultViewModel é um modelo utilizado para padronizar retornos, facilitando a integração de frontend e backend.

```python
{
    'result': 'Modelo generico, podendo ser enviado qualquer tipo de dado',
    'errors': 'Lista de texto de erros',
    'success': 'Boleano que informa se a requisição foi verdadeira ou falsa'
}
```

Para utilizar esse modelo, basta importar:
```python
from tools_rest.response_view import ResultViewModel, sucesso, bad_request, response
```

#### ResultViewModel
Podem ou não receber parametros na criação, sendo eles:
errors = lista de erro.
result = objeto que ira retornar, podendo ser nulo ou não.

Retorno result:
```python
{
    'result': 'modelo' or null,
    'errors': [
        'erros aqui'
    ]
    'success': 'boleano, caso exista alguma msg '
}
```

para criar o modelo, deve-se utilizar o invocador padrão de objetos:
```python
result = ResultViewModel()

ou

result = ResultViewModel('Erro um', 'Erro dois')

ou

lista = []
lista.append('erro um')
lista.append('erro dois')
result = ResultViewModel(lista)

ou

result = ResultViewModel(result=True)
```

#### Funçoes internas
```python
Recebe um modelo por default, retornando ele no função externo response()

def add_result(model)
Retorno:
{
    'result': modelo enviado,
    'errors': []
    'success': True
}
```

```python

Recebe um texto, varios em sequencia e/ou uma lista de erros para utilizar na função exterma response()

def add_errors(*msg:str)
Retorno:
{
    'result': null
    'errors': [
        'Erro aqui'
    ]
    'success': False
}
```

#### Funções externas
```python
Result: Recebe um modelo de retorno.
Errors: Lista de erros virá vazia.
Success: True como resultado.
Essa requisição retorna um status code 200
Retorna um Response()

def sucesso(model)
Retorno:
{
    'result': modelo enviado,
    'errors': []
    'success': True
}
```

```python
Result: Aqui ficará como null.
Errors: Recebe uma str, list(str) ou multiplas str. ex.:bad_request('erro1', 'erro2')
Success: False como resultado.
Essa requisição retorna um status code 400
Retorna um Response()

def bad_request(*msg)
Retorno:
{
    'result': null,
    'errors': [
        'erro1',
        'erro2'
    ]
    'success': True
}
```

```python
Retorna um response totalmente customizado, podendo vir como sucesso ou erro, mas devera ser informado um ResultViewModel como parametro
StatusCode é opcional.
Retorna, 200 se enviado um modelo ao ResultViewModel
         400 se enviado errors ao ResultViewModel
         Personalizado caso o status code seja enviado

def response(resultview : ResultViewModel, status_code: int = None)
Retorno:
{
    'result': 'Modelo enviado',
    'errors': 'Erro(s) enviado(s)',
    'success': 'Caso possua errors, sera False, senão True'
}
```