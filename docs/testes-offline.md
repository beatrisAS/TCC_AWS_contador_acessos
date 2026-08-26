# Testes da simulação offline

Esta execução não usa Docker, LocalStack, conta AWS ou credenciais. Ela representa localmente o mesmo comportamento do contador: receber uma requisição, incrementar o valor e persistir o total.

## Iniciar a API

No PowerShell, a partir de `contador-de-acessos-aws`:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r .\local\requirements.txt
python .\local\server.py
```

## Verificar a saúde da API

Em outro terminal:

```powershell
curl.exe http://127.0.0.1:5000/api/health
```

Resposta esperada:

```json
{"servico":"contador-local","status":"ok"}
```

## Consultar e incrementar

```powershell
curl.exe http://127.0.0.1:5000/api/acessos
curl.exe -X POST http://127.0.0.1:5000/api/acessos
curl.exe -X POST http://127.0.0.1:5000/api/acessos
```

O valor retornado deve aumentar a cada requisição `POST`. A persistência fica em `local/data.json` com a chave `id: hits`.

## Abrir a interface

Em um terceiro terminal:

```powershell
cd .\frontend
python -m http.server 8080
```

Abra `http://localhost:8080` e clique em **Registrar meu acesso**. A interface consulta a API local e mostra o valor atualizado.

## Reiniciar o contador

```powershell
curl.exe -X POST http://127.0.0.1:5000/api/reset
```

## Correspondência com a arquitetura AWS

| Simulação offline | Arquitetura planejada na AWS |
|---|---|
| `frontend/index.html` | Página estática em Amazon S3/CloudFront |
| `local/server.py` | Amazon API Gateway + AWS Lambda |
| Função `registrar_acesso` | Código da função Lambda |
| `local/data.json` | Amazon DynamoDB, item `id = hits` |

A simulação comprova o comportamento da aplicação, mas não deve ser descrita como um deploy real na AWS.
