# Passo a Passo Para Criar o Relatorio AC3

Este documento reúne os comandos e as etapas necessárias para gerar as evidências, revisar o relatório e preparar a entrega da atividade AC3 no projeto `User-Management-Api`.

## 1. Abrir o projeto no terminal

Execute no PowerShell:

```powershell
cd "c:\Users\WILLIAM\Documents\User-Management-Api"
```

## 2. Criar e ativar ambiente virtual

Se quiser isolar as dependências do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Instalar as dependências

Se o arquivo `requirements.txt` estiver configurado:

```powershell
pip install -r .\requirements.txt
```

Se ele estiver vazio ou incompleto, instale pelo menos o Flask:

```powershell
pip install flask
```

## 4. Executar os testes automatizados e salvar a evidência

Esse comando executa os testes da pasta `tests` e salva a saída no arquivo de evidência:

```powershell
python -m unittest discover -s tests -v 2>&1 | Tee-Object -FilePath .\docs\test_execution_evidence.txt
```

Resultado esperado:

- aparecer `Ran 10 tests`
- aparecer `OK`

## 5. Abrir o relatório para revisão

Abra o relatório já montado:

```powershell
notepad .\docs\AC3_Report.md
```

Revise estes pontos:

- nome do grupo
- integrantes
- dificuldades encontradas
- dúvidas técnicas
- pontos que não conseguiram evoluir
- observações reais da execução

## 6. Criar o arquivo `.env`

Se for rodar a API localmente com banco PostgreSQL, crie o arquivo `.env` com este conteúdo:

```powershell
@"
DB_HOST=localhost
DB_PORT=5432
DB_NAME=user_management
DB_USER=postgres
DB_PASSWORD=postgres
SECRET_KEY=minha-chave-secreta
ACCESS_TOKEN_EXPIRES_IN=3600
"@ | Set-Content .env
```

## 7. Criar o banco de dados

Se o PostgreSQL estiver instalado e o comando `psql` disponível:

```powershell
psql -U postgres -c "CREATE DATABASE user_management;"
```

## 8. Aplicar o schema do banco

Execute o script SQL que está em `docs\schema.sql`:

```powershell
psql -U postgres -d user_management -f .\docs\schema.sql
```

## 9. Rodar a aplicação

Com o banco configurado, inicie a API:

```powershell
python .\run.py
```

Se tudo estiver certo, a aplicação ficará disponível localmente.

## 10. Testar a API e gerar evidências

Abra outro terminal e execute os comandos abaixo.

### 10.1 Listar usuários

```powershell
curl.exe -i http://127.0.0.1:5000/users/
```

### 10.2 Criar usuário válido

```powershell
curl.exe -i -X POST http://127.0.0.1:5000/users/ -H "Content-Type: application/json" -d "{\"name\":\"Ana\",\"email\":\"ana@email.com\",\"password\":\"Senha123\"}"
```

### 10.3 Criar usuário com payload vazio

```powershell
curl.exe -i -X POST http://127.0.0.1:5000/users/ -H "Content-Type: application/json" -d "{}"
```

### 10.4 Buscar usuário inexistente

```powershell
curl.exe -i http://127.0.0.1:5000/users/999
```

### 10.5 Atualizar usuário

```powershell
curl.exe -i -X PUT http://127.0.0.1:5000/users/1 -H "Content-Type: application/json" -d "{\"name\":\"Ana Silva\"}"
```

### 10.6 Desativar usuário

```powershell
curl.exe -i -X DELETE http://127.0.0.1:5000/users/1
```

## 11. O que precisa estar no relatório

Confira se o relatório contém:

- descrição do sistema
- escopo dos testes
- no mínimo 5 casos de teste
- execução registrada
- evidências
- testes com erro
- testes de API
- no mínimo 2 testes automatizados
- no mínimo 2 bugs
- melhorias propostas

## 12. Arquivos principais para entrega

Os arquivos mais importantes já estão no projeto:

- `docs\AC3_Report.md`
- `docs\test_execution_evidence.txt`
- `tests\test_user_service.py`
- `tests\test_user_routes.py`
- `app\schemas\validors.py`

## 13. Checklist final

Antes de enviar no AVA:

1. Execute os testes automatizados
2. Salve a saída em `docs\test_execution_evidence.txt`
3. Revise `docs\AC3_Report.md`
4. Tire prints do terminal e dos testes da API
5. Anexe o relatório e os scripts `.py`

## 14. Comando essencial

Se você quiser fazer o básico rapidamente, rode estes comandos:

```powershell
cd "c:\Users\WILLIAM\Documents\User-Management-Api"
python -m unittest discover -s tests -v 2>&1 | Tee-Object -FilePath .\docs\test_execution_evidence.txt
notepad .\docs\AC3_Report.md
```

## 15. Observação final

Se o professor pedir o arquivo em Word ou PDF, você pode usar este documento e o `AC3_Report.md` como base para copiar e colar no formato final.
