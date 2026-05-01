# Challenger (1986) — Regressão Logística Binária

> Análise estatística que demonstra como um modelo logístico construído com dados disponíveis **antes** do lançamento poderia ter previsto a falha catastrófica do ônibus espacial Challenger.

---

## 📌 Sobre o projeto

Em 28 de janeiro de 1986, o ônibus espacial Challenger se desintegrou 73 segundos após o lançamento. A causa-raiz foi a falha dos O-rings (anéis de vedação) dos foguetes laterais, que perderam elasticidade pela baixa temperatura ambiente (≈ 2°C). Sete astronautas morreram, incluindo Christa McAuliffe — a primeira professora civil selecionada pelo programa Teacher in Space.

A Comissão Rogers, que investigou o acidente, concluiu que **os dados pré-existentes já apontavam o risco**. Este projeto reproduz o exercício clássico que sela esse caso na história da estatística aplicada: ajustar um modelo logístico binário sobre as 23 missões anteriores e mostrar o que ele teria previsto.

## 🎯 Resultados

| Temperatura | P(falha) |
|---|---|
| 25°C (77°F) | **1,1%** — zona segura |
| 21°C (70°F) | **13,1%** — risco perceptível |
| 2°C (36°F) — dia do acidente | **≈ 99,99%** — risco proibitivo |

> Modelo final: `falha ~ temperatura` | Pseudo R² = 0,45 | p-valor = 0,036

## 🔬 Metodologia

1. **Dataset:** 23 missões anteriores ao acidente (variáveis: `desgaste`, `temperatura`, `pressão`).
2. **Engenharia da target:** `falha = 1` se houve qualquer stress térmico nos O-rings, `0` caso contrário.
3. **Modelagem:** Regressão Logística Binária via Maximum Likelihood (`statsmodels.Logit`).
4. **Seleção de variáveis:** Stepwise bidirecional com p-valor limite de 0,05.
5. **Inferência:** predições para as três temperaturas-chave do estudo.

## 🗂️ Estrutura do repositório

```
challenger-logistic-regression/
├── README.md                    ← este arquivo
├── requirements.txt             ← dependências
├── .gitignore
├── data/
│   └── challenger.csv           ← dataset (23 obs × 4 vars)
├── notebooks/
│   └── 01_analysis.ipynb        ← análise completa, do EDA à conclusão
├── src/
│   └── visualization.py         ← módulo de plotagem da sigmoide
├── outputs/
│   └── challenger_sigmoide_linkedin.png
└── content/
    └── linkedin_post.md         ← texto de divulgação
```

## ▶️ Como reproduzir

```bash
# 1. Clone o repositório
git clone https://github.com/<seu-usuario>/challenger-logistic-regression.git
cd challenger-logistic-regression

# 2. Crie ambiente virtual e instale dependências
python -m venv .venv
source .venv/bin/activate          # Linux/Mac
# .venv\Scripts\activate           # Windows
pip install -r requirements.txt

# 3a. Execute o notebook
jupyter notebook notebooks/01_analysis.ipynb

# 3b. Ou apenas regenere a imagem
python src/visualization.py
```

## 💡 Por que esse caso importa?

O Challenger é um dos exemplos mais citados na história da estatística aplicada por uma razão simples: **não basta ter os dados — é preciso modelá-los e ouvir o que dizem.**

Em 1986, com os dados que a NASA já possuía e técnicas estatísticas já bem estabelecidas (Berkson, 1944; Cox, 1958), um modelo de duas linhas poderia ter sinalizado o risco com clareza brutal. Os engenheiros da Morton Thiokol, fabricante dos foguetes, alertaram a NASA na noite anterior ao lançamento — disseram explicitamente que os O-rings nunca foram testados abaixo de 53°F. Foram voto vencido.

Não faltou tecnologia. Não faltou informação. Faltou análise — e, sobretudo, disposição de ouvir o que ela diria.

## 📚 Referências

- **Dalal, S. R., Fowlkes, E. B., & Hoadley, B.** (1989). Risk analysis of the space shuttle: Pre-Challenger prediction of failure. *Journal of the American Statistical Association*, 84(408), 945–957.
- **Report of the Presidential Commission on the Space Shuttle Challenger Accident** (Rogers Commission). 6 de junho de 1986.
- **Fávero, L. P., & Belfiore, P.** (2024). *Manual de Análise de Dados.* Referência metodológica.
- Pacote [`statstests`](https://stats-tests.github.io/statstests/) (Fávero & Santos) para o procedimento Stepwise.

## 👤 Autor

**Felipe Apolonio** — Analytics Engineer

[LinkedIn](https://linkedin.com/in/felipenatanaelsp)

---

*Projeto educacional reproduzindo análise clássica para fins de divulgação científica e portfolio. Os dados seguem o dataset público do caso Challenger amplamente utilizado em literatura estatística.*
