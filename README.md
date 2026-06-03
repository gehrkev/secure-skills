# Secure - skills

Framework de skills Claude Code **Secure** (`c_know` MVP), desenvolvidas no Trabalho de Conclusão de Curso para o Bacharelado em Engenharia de Software - Universidade do Estado de Santa Catarina (UDESC) - 2026/1.

No momento este repo contém somente as skills desenvolvidas; em breve será incluído o código de avaliação (`eval/runner`), os resultados (`eval/runs`) e o documento do TCC.

Duas skills aqui:

- **`secure/`** - injeta contexto de segurança (CWE) em tarefas de geração de
  código Python. É o componente `c_know` (RAG sobre uma base de CWEs).
- **`codeql-eval/`** - roda análise estática (CodeQL, suíte *security-extended*)
  num arquivo `.py` e devolve os achados mapeados por CWE. Valida o que a
  `secure` gera.

## O experimento

O TCC avalia a `secure` num teste A/B no Claude Code: as mesmas tarefas são
geradas com a skill presente (*treatment*) e ausente (*control*), em dois ramos
de prompt - **NL** (tarefa descrita em linguagem natural) e **stub** (código a
completar). São 500 gerações por célula (100 tarefas × k=5) em 4 células
(2 braços × 2 ramos) = 2000 sessões.

A segurança de cada candidato é medida depois, num passo separado: o runner chama
o script `run_eval.py` da `codeql-eval` sobre os `.py` salvos; a skill `codeql-eval` em si
**não** roda nas sessões de geração (ela não está presente em nenhum dos braços), tanto
para manter geração e avaliação independentes, quanto para não introduzir um sinal de segurança 
que enviese o modelo, principalmente no braço *control*).

## Como usar

Copie as pastas para o `.claude/skills/` do seu projeto:

```bash
cp -r secure codeql-eval /caminho/do/seu/projeto/.claude/skills/
```

Aqui está só o código-fonte (sem venv, sem base vetorial, sem cache, sem o XML
das CWEs). Na primeira vez, cada skill se monta sozinha:

```bash
# secure: cria a .venv e constrói a base de conhecimento (ChromaDB) + baixa os XMLs
bash .claude/skills/secure/scripts/bootstrap.sh

# codeql-eval: builda a imagem Docker do CodeQL (precisa de Docker rodando)
bash .claude/skills/codeql-eval/scripts/bootstrap.sh
```

Depois disso o Claude Code já reconhece e dispara as skills normalmente.

## A seguir (TODO)

- código de avaliação (runner do experimento A/B)
- resultados
- documento do TCC
