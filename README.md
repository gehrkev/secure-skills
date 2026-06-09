# secure-skills

Um framework de *agent skills* para **geração segura de código** assistida por LLMs,
desenvolvido no Trabalho de Conclusão de Curso do Bacharelado em Engenharia de Software
da Universidade do Estado de Santa Catarina (UDESC), 2026/1.

O framework enriquece o contexto da geração com conhecimento do domínio da codificação
segura. O artefato avaliado é um MVP centrado no componente de conhecimento externo
(`c_know`, RAG sobre uma base de fraquezas CWE) acoplado a um protótipo de instruções
estruturadas (`c_instr`). Os componentes de memória adaptativa (`c_mem`) e a forma plena
da função de montagem são concepção teórica, deixados como trabalho futuro.

Duas skills:

- **`secure`** — injeta contexto de segurança (CWE) em tarefas de geração de código
  Python. É o componente `c_know`: RAG sobre a união da MITRE CWE View 1003 e da CWE
  Top 25 (133 fraquezas), via ChromaDB e *embeddings* `all-MiniLM-L6-v2`.
- **`codeql-eval`** — roda análise estática (CodeQL, suíte *security-extended*) num
  arquivo `.py` e devolve os achados mapeados por CWE. Verifica o que a `secure` gera.

## Estrutura do repositório

```
.claude/skills/
├── secure/        # skill secure (c_know + protótipo de c_instr)
└── codeql-eval/   # skill auxiliar de verificação por análise estática
eval/
├── runner/        # pipeline de avaliação A/B (preparação → geração → avaliação → agregação → análise)
├── runs/          # resultados versionados da execução (m3_20260601_150010)
└── SALLM/         # conjunto de prompts (apenas Dataset/dataset.jsonl; ver NOTICE)
```

Aqui está só o código-fonte: ambientes virtuais, base vetorial (ChromaDB), XMLs das
CWEs e imagem Docker do CodeQL **não** são versionados (são recriados pelo *bootstrap*).

## Como usar as skills

Copie as duas pastas para o `.claude/skills/` do seu projeto:

```bash
cp -r .claude/skills/secure .claude/skills/codeql-eval /caminho/do/seu/projeto/.claude/skills/
```

Na primeira utilização, o próprio agente (Claude Code), ao ser informado das skills pelo
*harness* e orientado pelo `SKILL.md` de cada uma, executa o *bootstrap*, sem necessidade
de intervenção manual. Para montá-las à mão:

```bash
# secure: cria a .venv, baixa os XMLs do MITRE CWE e constrói a base ChromaDB
bash .claude/skills/secure/scripts/bootstrap.sh

# codeql-eval: builda a imagem Docker fixada do CodeQL (precisa de Docker rodando)
bash .claude/skills/codeql-eval/scripts/bootstrap.sh
```

Depois disso, o Claude Code dispara a `secure` automaticamente sempre que a tarefa toca
uma superfície de vulnerabilidade (e oferece a `codeql-eval` para verificar o resultado).
As skills também podem ser chamadas por `/secure` e `/codeql-eval`.

## O experimento

O TCC avalia a `secure` num teste pareado A/B no Claude Code (modelo fixado em
`claude-haiku-4-5`, modo *headless*): as mesmas tarefas são geradas com a skill presente
(*treatment*) e ausente (*control*), em duas modalidades de entrada — **NL** (tarefa em
linguagem natural) e **stub** (código a completar). São 100 tarefas do conjunto SALLM
× k=5 candidatos × 2 braços × 2 modalidades = **2000 sessões**.

A segurança de cada candidato é medida depois, num passo separado: o *runner* chama o
script `run_eval.py` da `codeql-eval` sobre os `.py` salvos. A skill `codeql-eval` **não**
roda nas sessões de geração (não está presente em nenhum braço), tanto para manter geração
e avaliação independentes quanto para não introduzir um sinal de segurança que enviese o
modelo, sobretudo no braço *control*.

**Resultado principal:** a presença da skill reduziu o `vulnerable@k` de 0,340 para 0,265
e elevou o `security@k` de 0,715 para 0,860, sem custo de funcionalidade (`pass@k` ≈ 0,91),
com significância pareada (McNemar) nas duas modalidades e nenhuma regressão de segurança
detectável em 200 comparações pareadas.

O documento textual, presente no TCC, será disponibilizado após defesa em banca.

### Reproduzir

```bash
# do estágio bruto (precisa do bootstrap da secure + Docker da codeql-eval):
python3 eval/runner/dataset/build_treated_dataset.py
# ... geração, avaliação, agregação (ver eval/runner/)

# da agregação/análise (a partir dos artefatos já versionados em eval/runs/):
python3 eval/runner/aggregate/aggregate.py --run-id m3_20260601_150010
python3 eval/runner/analysis/explore_m3.py  --run-id m3_20260601_150010
python3 eval/runner/analysis/cost_rollup.py --run-id m3_20260601_150010
```

Um notebook Jupyter está localizado em `eval/runner/analysis/m3_resultados_visual.ipynb` 
para exibir interativamente a análise realizada acima pelo conjunto 
`aggregate`, `explore_m3` e `cost_rollup` da run `m3_20260601_150010` disponibilizada,
a qual foi utilizada no TCC.

## Créditos e licença

O conjunto de *prompts* em `eval/SALLM/Dataset/dataset.jsonl` provém do projeto
[SALLM](https://github.com/s2e-lab/SALLM) (Siddiq et al.), sob a licença Apache 2.0;
ver `eval/SALLM/LICENSE` e `eval/SALLM/NOTICE`. Apenas o dataset é utilizado; a
verificação de segurança aqui é feita por análise estática com CodeQL, não pelo *harness*
dinâmico do SALLM.
