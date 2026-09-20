# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

- Fazer pull de prompts do LangSmith Prompt Hub contendo prompts de baixa qualidade
- Refatorar e otimizar esses prompts usando técnicas avançadas de Prompt Engineering
- Fazer push dos prompts otimizados de volta ao LangSmith
- Avaliar a qualidade através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- Atingir pontuação mínima de 0.8 (80%) em todas as métricas de avaliação

## Exemplo no CLI

Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.8: helpfulness, correctness, f1_score, clarity, precision
```

Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:

```
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.8
```

## Tecnologias obrigatórias

- Linguagem: Python 3.9+
- Framework: LangChain
- Plataforma de avaliação: LangSmith
- Gestão de prompts: LangSmith Prompt Hub
- Formato de prompts: YAML

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

## OpenAI

- Crie uma API Key da OpenAI: https://platform.openai.com/api-keys
- Você vai precisar de um modelo de LLM para responder e de um modelo de LLM para avaliação. Consulte a documentação oficial da OpenAI para ver os modelos disponíveis.
- Custo estimado: ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma API Key da Google: https://aistudio.google.com/app/apikey
- Você vai precisar de um modelo de LLM para responder e de um modelo de LLM para avaliação. Consulte a documentação oficial do Google para ver os modelos disponíveis.
- Os limites de requisições gratuitas mudam com frequência. Consulte os limites atuais na documentação oficial do Google.

## Escolha dos modelos

Este desafio não fixa modelos. Nomes e versões mudam com frequência e alguns são descontinuados, então faz parte do desafio consultar a documentação oficial do provedor que você escolher, ver quais modelos estão disponíveis no momento e selecionar os que atendem ao objetivo. Você pode usar o mesmo modelo para responder e para avaliar, ou um modelo mais capaz na avaliação.

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de baixa qualidade publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

Tarefas:

- Configurar suas credenciais do LangSmith no arquivo .env (conforme o arquivo .env.example)
- Implementar o script src/pull_prompts.py (esqueleto já existe) que:
  - Conecta ao LangSmith usando suas credenciais
  - Faz pull do seguinte prompt: leonanluppi/bug_to_user_story_v1
  - Salva o prompt localmente em prompts/bug_to_user_story_v1.yml

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

Tarefas:

- Analisar o prompt em prompts/bug_to_user_story_v1.yml
- Criar um novo arquivo prompts/bug_to_user_story_v2.yml com suas versões otimizadas
- Aplicar obrigatoriamente Few-shot Learning (exemplos claros de entrada/saída) e pelo menos uma das seguintes técnicas adicionais:
  - Chain of Thought (CoT): Instruir o modelo a "pensar passo a passo"
  - Tree of Thought: Explorar múltiplos caminhos de raciocínio
  - Skeleton of Thought: Estruturar a resposta em etapas claras
  - ReAct: Raciocínio + Ação para tarefas complexas
  - Role Prompting: Definir persona e contexto detalhado
- Documentar no README.md quais técnicas você escolheu e por quê

Requisitos do prompt otimizado:

- Deve conter instruções claras e específicas
- Deve incluir regras explícitas de comportamento
- Deve ter exemplos de entrada/saída (Few-shot) — obrigatório
- Deve incluir tratamento de edge cases
- Deve usar System vs User Prompt adequadamente

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

Tarefas:

- Implementar o script src/push_prompts.py (esqueleto já existe) que:
  - Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
  - Faz push para o LangSmith com nomes versionados: {seu_username}/bug_to_user_story_v2
  - Adiciona metadados (tags, descrição, técnicas utilizadas)
- Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
- Deixá-lo público

### 4. Iteração

Espera-se 3-5 iterações.

- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até TODAS as métricas >= 0.8

```
Critério de Aprovação:
- Helpfulness >= 0.8
- Correctness >= 0.8
- F1-Score >= 0.8
- Clarity >= 0.8
- Precision >= 0.8

MÉDIA das 5 métricas >= 0.8
```

IMPORTANTE: TODAS as 5 métricas devem estar >= 0.8, não apenas a média!

### 5. Testes de Validação

O que você deve fazer: Edite o arquivo tests/test_prompts.py e implemente, no mínimo, os 6 testes abaixo usando pytest:

- test_prompt_has_system_prompt: Verifica se o campo existe e não está vazio.
- test_prompt_has_role_definition: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- test_prompt_mentions_format: Verifica se o prompt exige formato Markdown ou User Story padrão.
- test_prompt_has_few_shot_examples: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- test_prompt_no_todos: Garante que você não esqueceu nenhum [TODO] no texto.
- test_minimum_techniques: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

Como validar:

```
pytest tests/test_prompts.py
```

## Estrutura obrigatória do projeto

Faça um fork do repositório base: https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
```

O que você deve implementar:

- prompts/bug_to_user_story_v2.yml — Criar do zero com seu prompt otimizado
- src/pull_prompts.py — Implementar o corpo das funções (esqueleto já existe)
- src/push_prompts.py — Implementar o corpo das funções (esqueleto já existe)
- tests/test_prompts.py — Implementar os 6 testes de validação (esqueleto já existe)
- README.md — Documentar seu processo de otimização

O que já vem pronto (não alterar):

- src/evaluate.py — Script de avaliação completo
- src/metrics.py — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- src/utils.py — Funções auxiliares
- datasets/bug_to_user_story.jsonl — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Ordem de execução

1. Executar pull dos prompts ruins

```
python src/pull_prompts.py
```

2. Refatorar prompts

Edite manualmente o arquivo prompts/bug_to_user_story_v2.yml aplicando as técnicas aprendidas no curso.

3. Fazer push dos prompts otimizados

```
python src/push_prompts.py
```

4. Executar avaliação

```
python src/evaluate.py
```

## Entregável

1. Repositório público no GitHub (fork do repositório base) contendo:

- Todo o código-fonte implementado
- Arquivo prompts/bug_to_user_story_v2.yml 100% preenchido e funcional
- Arquivo README.md atualizado

2. README.md deve conter:

A) Seção "Técnicas Aplicadas (Fase 2)":

- Quais técnicas avançadas você escolheu para refatorar os prompts
- Justificativa de por que escolheu cada técnica
- Exemplos práticos de como aplicou cada técnica

B) Seção "Resultados Finais":

- Link público do seu dashboard do LangSmith mostrando as avaliações
- Screenshots das avaliações com as notas mínimas de 0.8 atingidas
- Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

C) Seção "Como Executar":

- Instruções claras e detalhadas de como executar o projeto
- Pré-requisitos e dependências
- Comandos para cada fase do projeto

3. Evidências no LangSmith:

- Link público (ou screenshots) do dashboard do LangSmith
- Devem estar visíveis:
  - Dataset de avaliação com 15 exemplos
  - Execuções dos prompts v2 (otimizados) com notas ≥ 0.8
  - Tracing detalhado de pelo menos 3 exemplos

## Dicas Finais

- Lembre-se da importância da especificidade, contexto e persona ao refatorar prompts
- Use Few-shot Learning com 2-3 exemplos claros para melhorar drasticamente a performance
- Chain of Thought (CoT) é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- Use o Tracing do LangSmith como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- Não altere os datasets de avaliação - apenas os prompts em prompts/bug_to_user_story_v2.yml
- Itere, itere, itere - é normal precisar de 3-5 iterações para atingir 0.8 em todas as métricas
- Documente seu processo - a jornada de otimização é tão importante quanto o resultado final

---

# Documentação do Processo

## Técnicas Aplicadas (Fase 2)

Para otimizar o prompt `prompts/bug_to_user_story_v2.yml`, apliquei **4 técnicas de Prompt Engineering** — incluindo as obrigatórias do desafio (Few-shot Learning + pelo menos uma técnica avançada):

### 1. Role Prompting — persona de Senior Product Manager

**O que foi feito:** o system prompt define a persona *"Senior Product Manager com 10+ anos de experiência em metodologias ágeis (Scrum e Kanban), especialista em converter relatos de bugs em User Stories de alta qualidade, prontas para o time de desenvolvimento executar"*.

**Por quê:** um papel claro fixa o estilo de escrita, o nível de profundidade e a prioridade profissional da resposta. O modelo passa a escrever "como um PM", entregando User Stories acionáveis em vez de respostas genéricas de assistente.

**Exemplo aplicado no prompt:**
```text
Você é um Senior Product Manager com 10+ anos de experiência em metodologias ágeis (Scrum e Kanban), especialista em converter relatos de bugs em User Stories de alta qualidade, prontas para o time de desenvolvimento executar.
```

### 2. Chain of Thought (CoT) — raciocínio passo a passo

**O que foi feito:** o prompt instrui o modelo a raciocinar em ordem antes de redigir a resposta final: 1) analisar o bug (problema raiz, sintoma, impacto e **todos** os problemas listados) → 2) identificar a persona → 3) definir o objetivo/valor de negócio → 4) redigir a User Story → 5) definir os Critérios de Aceitação → 6) completar a estrutura conforme a complexidade.

**Por quê:** converter bug → User Story é uma tarefa de decomposição (problema, impacto, persona, valor). O CoT força uma análise ordenada e completa, reduzindo omissões de detalhes técnicos (alavanca para F1-Score e Precision) e de partes do relato.

**Exemplo aplicado no prompt:**
```text
Antes de escrever a resposta final, raciocine internamente na seguinte ordem:
1. ANALISAR o relato de bug: identifique o problema raiz, o sintoma observado, o impacto no usuário/negócio e TODOS os problemas listados (um relato pode conter MÚLTIPLOS problemas diferentes).
```

### 3. Few-shot Learning (obrigatória) — exemplos entrada → saída

**O que foi feito:** inclui 2 exemplos completos de entrada/saída:
- **Exemplo 1 (bug simples):** botão "Salvar" sem resposta na aba de notificações → User Story + 5 critérios Given-When-Then.
- **Exemplo 2 (bug complexo):** checkout com XSS + timeout no gateway + race condition em cupom + loading infinito → estrutura completa com critérios agrupados por categoria (Segurança, Integração, Lógica de Negócio, UX), contexto do bug e tasks técnicas.

**Por quê:** exemplos concretos fixam o formato de saída desejado e o nível de detalhe esperado por complexidade. O modelo imita a estrutura demonstrada — técnica com maior impacto na consistência do formato.

**Exemplo aplicado no prompt:**
```text
## Exemplo 1 — Bug simples
**Entrada:** O botão "Salvar" da tela de configurações não responde quando o usuário está na aba "Notificações".
**Saída esperada:** ## User Story ... ## Critérios de Aceitação ...
```

### 4. Structured Output — formato controlado (Markdown + Given-When-Then)

**O que foi feito:** o prompt exige um formato obrigatório em Markdown: seção `## User Story` com "Como / Eu quero / Para que", seção `## Critérios de Aceitação` em Given-When-Then, e níveis de complexidade (simples/médio/complexo) que adicionam seções — `Contexto Técnico`, `Critérios Técnicos`, `Contexto do Bug` e `Tasks Técnicas Sugeridas` — quando aplicável.

**Por quê:** as métricas (Clarity, F1, Precision) premiam respostas organizadas e completas. Um formato rígido e validável reduz respostas soltas e garante a cobertura exigida.

**Exemplo aplicado no prompt:**
```text
## User Story
**Como** um [persona específica], **eu quero** [ação/funcionalidade desejada], **para que** [benefício/valor real para o usuário ou negócio].

## Critérios de Aceitação
- Dado que [contexto inicial]
- Quando [ação executada]
- Então [resultado esperado]
- E [condições adicionais quando aplicável]
```

### Regras de comportamento e edge cases

Além das técnicas, o prompt define regras explícitas (requisito do desafio):
- **Anti-alucinação:** nunca inventar informações, dados, endpoints, logs ou contextos que não estejam no relato.
- **Preservação de detalhes técnicos:** valores, códigos de erro, stack traces, z-index, tempos, versões.
- **Multi-problemas:** se o relato contém vários bugs, **todos** devem ser cobertos.
- **Edge cases:** segurança (XSS), concorrência (race condition), performance (timeouts), UX (loading infinito).
- **System vs User adequados:** todo contexto/regras/exemplos ficam no **system prompt**; o **user prompt** contém apenas o `{bug_report}`.

## Resultados Finais

A avaliação foi executada no **LangSmith** com o dataset `prompt-optimization-challenge-resolved-eval` (criado a partir de `datasets/bug_to_user_story.jsonl`, **15 exemplos** — 5 simples, 7 médios, 3 complexos), usando o modelo `gemini-3.5-flash-lite` (Google AI Studio, camada gratuita) tanto para gerar quanto para julgar.

### Tabela comparativa v1 (ruim) × v2 (otimizado)

| Métrica | v1 `leonanluppi/bug_to_user_story_v1` | v2 `sandrosantos-eng/bug_to_user_story_v2` |
|---|---|---|
| Helpfulness | 0.91 ✓ | 0.91 ✓ |
| Correctness | 0.89 ✓ | **0.90** ✓ |
| F1-Score | 0.87 ✓ | **0.89** ✓ |
| Clarity | 0.91 ✓ | 0.91 ✓ |
| Precision | 0.91 ✓ | 0.91 ✓ |
| **MÉDIA GERAL** | **0.8976** | **0.9063** ✓ |

**Resultado:** o prompt otimizado (v2) atingiu **TODAS as 5 métricas ≥ 0.8** com média **0.9063** → **APROVADO ✅**. A maior evolução sobre o v1 está em **F1-Score** (0.89 vs 0.87) e **Correctness** (0.90 vs 0.89), reflexo do Few-shot e do CoT na completude dos critérios de aceitação e do formato estruturado. O v1 já entrega ~0.90 por ser um prompt funcional e por o juiz LLM tender a ser generoso; a v2 supera em precisão de conteúdo e consistência de formato.

### Notas por exemplo (v2)

```text
[1/15]  F1:0.97  Clarity:0.85  Precision:0.93
[2/15]  F1:0.92  Clarity:0.85  Precision:0.93
[3/15]  F1:1.00  Clarity:0.85  Precision:0.95
[4/15]  F1:0.84  Clarity:0.95  Precision:0.87
[5/15]  F1:0.82  Clarity:0.90  Precision:0.87
[6/15]  F1:0.82  Clarity:0.85  Precision:0.87
[7/15]  F1:0.97  Clarity:0.95  Precision:1.00
[8/15]  F1:0.87  Clarity:0.95  Precision:0.93
[9/15]  F1:0.82  Clarity:0.95  Precision:0.83
[10/15] F1:0.87  Clarity:0.95  Precision:0.90
[11/15] F1:0.92  Clarity:0.85  Precision:0.93
[12/15] F1:0.82  Clarity:0.95  Precision:0.83
[13/15] F1:0.92  Clarity:0.95  Precision:1.00
[14/15] F1:0.95  Clarity:0.95  Precision:1.00
[15/15] F1:0.85  Clarity:0.88  Precision:0.87
```

### Evidências no LangSmith

- Dashboard de avaliação: https://smith.langchain.com/projects/prompt-optimization-challenge-resolved
- Prompt público otimizado (v2): https://smith.langchain.com/prompts/bug_to_user_story_v2/033a4799?organizationId=a586146c-6a59-4103-9fa3-04de5d710152
- Dataset de avaliação: `prompt-optimization-challenge-resolved-eval` (15 exemplos)

> **Screenshots:** adicione aqui os prints do dashboard (dataset com 15 exemplos, execuções do v2 com notas ≥ 0.8 e o tracing detalhado de pelo menos 3 exemplos).

## Como Executar

### Pré-requisitos

- Python 3.10+ (recomendado 3.12)
- Conta no LangSmith ([smith.langchain.com](https://smith.langchain.com)) com API Key (`LANGSMITH_API_KEY`)
- API Key do Google AI Studio ([aistudio.google.com](https://aistudio.google.com/apikey)) — modelo gratuito `gemini-3.5-flash-lite`

### 1. Configurar as variáveis de ambiente

```bash
cp .env.example .env
```

Preencha no `.env`:
- `LANGSMITH_API_KEY` — sua chave do LangSmith
- `GOOGLE_API_KEY` — sua chave do Google AI Studio
- `USERNAME_LANGSMITH_HUB` — seu username do LangSmith Hub (ex.: `sandrosantos-eng`)

> ⚠️ O arquivo `.env` NÃO deve ser versionado (contém credenciais). Ele já está no `.gitignore`.

### 2. Criar o ambiente virtual e instalar as dependências

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Validar os testes

```bash
pytest tests/test_prompts.py -v
```

### 4. Fazer o pull do prompt de baixa qualidade

```bash
python src/pull_prompts.py
```

Gera `prompts/bug_to_user_story_v1.yml` a partir do LangSmith Hub (`leonanluppi/bug_to_user_story_v1`).

### 5. Publicar o prompt otimizado

```bash
python src/push_prompts.py
```

Publica `prompts/bug_to_user_story_v2.yml` como `{username}/bug_to_user_story_v2` (público, com tags e metadados de técnicas).

### 6. Avaliar

```bash
python src/evaluate.py
```

Cria/atualiza o dataset no LangSmith, puxa o prompt v2 do Hub, executa contra os 15 bugs e calcula as 5 métricas (Helpfulness, Correctness, F1-Score, Clarity, Precision). Critério de aprovação: **todas as métricas ≥ 0.8** e média ≥ 0.8.

### Observações

- **Limites do plano gratuito:** os modelos `gemini-flash` têm cota diária limitada (ex.: `gemini-3.6-flash` ≈ 20 req/dia). Por isso a avaliação usa `gemini-3.5-flash-lite` (cota maior). Ajuste `LLM_MODEL`/`EVAL_MODEL` no `.env` conforme os limites atuais do Google.
- **Rede corporativa/SSL:** se as chamadas ao Gemini falharem por certificado, o `src/utils.py` já injeta `truststore` e usa `transport="rest"` — mesmo padrão do desafio anterior (`mba-ia-desafio-ingestao-busca`).