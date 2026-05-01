"""
Módulo de visualização — Caso Challenger.

Gera a sigmoide do modelo logístico binário ajustado, com destaque para
3 pontos-chave: 25°C (controle), 21°C (referência) e 2°C (dia do acidente).

Autor: Felipe Apolonio
"""
from pathlib import Path

import matplotlib.patheffects as pe
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# -----------------------------------------------------------------------------
# Paleta — alinhada com a comunicação do post
# -----------------------------------------------------------------------------
PALETA = {
    "falha": "#E63946",       # vermelho — voos com falha
    "ok": "#2A9D8F",          # teal — voos sem falha
    "curva": "#1D3557",       # navy profundo — sigmoide
    "destaque": "#F77F00",    # laranja — ponto do acidente
    "fundo": "#FAFAFA",
    "grid": "#E0E0E0",
    "texto": "#1D3557",
}


def prob_falha(t: float, intercept: float, coef: float) -> float:
    """Calcula P(falha | temperatura) usando função logística."""
    z = intercept + coef * t
    return 1.0 / (1.0 + np.exp(-z))


def _anotar(ax, temp, prob, label, cor, dx, dy, ha="left"):
    """Desenha marcador destacado + caixa de anotação conectada."""
    # Marcador externo (ring)
    ax.scatter(temp, prob, s=320, color=cor, edgecolor="white",
               linewidth=3, zorder=5, marker="o")
    # Centro branco (efeito "donut")
    ax.scatter(temp, prob, s=80, color="white", zorder=6)

    # Linha conectora discreta
    ax.annotate(
        "", xy=(temp, prob), xytext=(temp + dx, prob + dy),
        arrowprops=dict(arrowstyle="-", color=cor, lw=1.5, alpha=0.6),
        zorder=2,
    )

    # Caixa com texto
    ax.text(
        temp + dx, prob + dy, label,
        fontsize=14, color="white", ha=ha, va="center", weight="bold",
        zorder=7,
        bbox=dict(boxstyle="round,pad=0.6", facecolor=cor,
                  edgecolor="white", linewidth=2),
    )


def gerar_sigmoide(
    df: pd.DataFrame,
    intercept: float,
    coef_temp: float,
    output_path: str | Path,
    *,
    pseudo_r2: float = 0.4536,
    p_valor: float = 0.036,
) -> Path:
    """
    Gera e salva a figura principal do projeto: sigmoide com pontos reais
    e anotações para 25°C / 21°C / 2°C.

    Parameters
    ----------
    df : DataFrame
        Deve conter as colunas `temperatura` (°F) e `falha` (0/1).
    intercept, coef_temp : float
        Coeficientes do modelo logístico estimado.
    output_path : str | Path
        Caminho de saída do PNG.
    pseudo_r2, p_valor : float
        Métricas exibidas no rodapé.

    Returns
    -------
    Path : caminho do arquivo gerado.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Curva contínua para a sigmoide
    x_curve = np.linspace(30, 85, 500)
    y_curve = prob_falha(x_curve, intercept, coef_temp)

    fig, ax = plt.subplots(figsize=(12, 12), dpi=100)
    fig.patch.set_facecolor(PALETA["fundo"])
    ax.set_facecolor(PALETA["fundo"])

    # Sigmoide com sombra suave
    ax.plot(x_curve, y_curve, color=PALETA["curva"], linewidth=4.5, zorder=3,
            path_effects=[pe.SimpleLineShadow(offset=(2, -2), alpha=0.15),
                          pe.Normal()])

    # Linha de referência P=0.5
    ax.axhline(y=0.5, color="#999999", linestyle=":", linewidth=1.5,
               alpha=0.7, zorder=1)

    # Scatter dos voos reais
    mask_ok = df["falha"] == 0
    mask_falha = df["falha"] == 1
    n_ok, n_falha = mask_ok.sum(), mask_falha.sum()

    ax.scatter(df.loc[mask_ok, "temperatura"], df.loc[mask_ok, "falha"],
               s=200, color=PALETA["ok"], alpha=0.75, edgecolor="white",
               linewidth=2, zorder=4, label=f"Voos sem falha (n={n_ok})")
    ax.scatter(df.loc[mask_falha, "temperatura"], df.loc[mask_falha, "falha"],
               s=200, color=PALETA["falha"], alpha=0.85, edgecolor="white",
               linewidth=2, zorder=4, label=f"Voos com falha (n={n_falha})")

    # 3 pontos-chave
    p36 = prob_falha(36, intercept, coef_temp)
    # Trunca em 99,99% para evitar arredondamento para 100% (que seria impreciso)
    p36_label = min(p36 * 100, 99.99)
    _anotar(ax, 36, p36,
            f"  36°F (2°C)\n  P(falha) = {p36_label:.2f}%\n  ⚠ Dia do acidente  ",
            PALETA["destaque"], dx=8, dy=-0.18, ha="left")

    p70 = prob_falha(70, intercept, coef_temp)
    _anotar(ax, 70, p70,
            f"  70°F (21°C)\n  P(falha) = {p70*100:.1f}%  ",
            PALETA["curva"], dx=-12, dy=0.25, ha="right")

    p77 = prob_falha(77, intercept, coef_temp)
    _anotar(ax, 77, p77,
            f"  77°F (25°C)\n  P(falha) = {p77*100:.1f}%  ",
            PALETA["ok"], dx=-3, dy=0.25, ha="right")

    # Eixos
    ax.set_xlim(30, 85)
    ax.set_ylim(-0.08, 1.12)
    ax.set_xlabel("Temperatura no lançamento (°F)", fontsize=16,
                  color=PALETA["texto"], weight="bold", labelpad=15)
    ax.set_ylabel("Probabilidade de falha dos O-rings", fontsize=16,
                  color=PALETA["texto"], weight="bold", labelpad=15)
    ax.tick_params(axis="both", labelsize=13, colors=PALETA["texto"])
    ax.set_xticks(np.arange(30, 86, 5))
    ax.set_yticks(np.arange(0, 1.01, 0.2))
    ax.grid(True, linestyle="--", alpha=0.4, color=PALETA["grid"], zorder=0)

    # Bordas
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for spine in ["left", "bottom"]:
        ax.spines[spine].set_color(PALETA["texto"])
        ax.spines[spine].set_linewidth(1.5)

    # Legenda
    legend = ax.legend(loc="center left", fontsize=13, frameon=True,
                       facecolor="white", edgecolor=PALETA["grid"],
                       bbox_to_anchor=(0.02, 0.55))
    legend.get_frame().set_linewidth(1)

    # Títulos
    fig.suptitle("Challenger (1986): o que a Regressão Logística diria?",
                 fontsize=22, color=PALETA["texto"], weight="bold",
                 y=0.965, x=0.5)
    fig.text(0.5, 0.92,
             "Modelo treinado com dados de 23 missões anteriores ao acidente",
             fontsize=14, color="#666666", ha="center", style="italic")

    # Footer com métricas
    fig.text(
        0.5, 0.025,
        f"falha ~ temperatura  |  Pseudo R² = {pseudo_r2:.2f}  "
        f"|  p-valor = {p_valor:.3f}",
        fontsize=12, color="#888888", ha="center", family="monospace",
    )

    plt.tight_layout(rect=[0, 0.04, 1, 0.91])
    plt.savefig(output_path, dpi=120, bbox_inches="tight",
                facecolor=PALETA["fundo"], edgecolor="none")
    plt.close(fig)

    return output_path


if __name__ == "__main__":
    # Permite rodar standalone: python src/visualization.py
    df = pd.read_csv("data/challenger.csv")
    df["falha"] = (df["desgaste"] != 0).astype(int)

    # Coeficientes do modelo final (após Stepwise) — ver notebook
    INTERCEPT = 23.7750
    COEF_TEMP = -0.3667

    path = gerar_sigmoide(
        df, INTERCEPT, COEF_TEMP,
        "outputs/challenger_sigmoide_linkedin.png",
    )
    print(f"✓ Imagem gerada: {path}")

    # Validação rápida
    print("\nPredições do modelo:")
    for t in [77, 70, 36]:
        p = prob_falha(t, INTERCEPT, COEF_TEMP)
        print(f"  T = {t}°F → P(falha) = {p*100:.4f}%")
