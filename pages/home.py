"""
PDV - Ponto de Venda
Página: Início / Dashboard (Padronizada com o Design System Oficial)
"""

import customtkinter as ctk
from config import COLORS
from database import is_connected
from fonts import get_font
from components.ui import (
    StandardCard,
    SelectedCard,
    AttentionCard,
    TotalCard,
    PrimaryButton,
    SecondaryButton,
    CancelButton,
    StatusPill,
)


class HomePage(ctk.CTkScrollableFrame):
    """Página inicial com visão geral do sistema e apresentação do design system."""

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_screen"],
            corner_radius=0,
            **kwargs
        )
        self._build()

    def _build(self):
        # Container principal com padding
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=32, pady=28)

        # ── 1. Header ─────────────────────────────────────────────────────────
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 24))

        titles_col = ctk.CTkFrame(header, fg_color="transparent")
        titles_col.pack(side="left", anchor="w")

        ctk.CTkLabel(
            titles_col,
            text="Visão Geral do PDV",
            font=get_font("screen_title"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            titles_col,
            text="Controle de vendas, caixa e estoque em tempo real",
            font=get_font("subtitle"),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(4, 0))

        # Status de conexão (Pílula)
        status_side = ctk.CTkFrame(header, fg_color="transparent")
        status_side.pack(side="right", anchor="e")

        if is_connected():
            StatusPill(status_side, text="Banco Conectado", status="success", icon="●").pack()
        else:
            StatusPill(status_side, text="Modo Offline (Local)", status="warning", icon="●").pack()

        # ── 2. Cards de Métricas (Demonstração dos Cards Padronizados) ────────
        cards_row = ctk.CTkFrame(content, fg_color="transparent")
        cards_row.pack(fill="x", pady=(0, 28))
        cards_row.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="metric_cards")

        # [Card Total] - Fundo #0B1B33, texto branco, total destacado
        c_total = TotalCard(cards_row)
        c_total.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        c_total_inner = ctk.CTkFrame(c_total, fg_color="transparent")
        c_total_inner.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(
            c_total_inner,
            text="TOTAL DO DIA",
            font=get_font("caption"),
            text_color=COLORS["sidebar_text"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            c_total_inner,
            text="R$ 3.842,90",
            font=get_font("total"),
            text_color="#FFFFFF",
        ).pack(anchor="w", pady=(4, 8))

        StatusPill(c_total_inner, text="Meta Atingida", status="success", icon="✓").pack(anchor="w")

        # [Card Selecionado] - Fundo #EAF0FF, borda 2px #1D4ED8
        c_selected = SelectedCard(cards_row)
        c_selected.grid(row=0, column=1, sticky="nsew", padx=5)
        c_sel_inner = ctk.CTkFrame(c_selected, fg_color="transparent")
        c_sel_inner.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(
            c_sel_inner,
            text="CAIXA SELECIONADO",
            font=get_font("caption"),
            text_color=COLORS["primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            c_sel_inner,
            text="Caixa #01 — Aberto",
            font=get_font("card_price"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(6, 8))

        ctk.CTkLabel(
            c_sel_inner,
            text="Operador: Caixa Central",
            font=get_font("body"),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        # [Card Padrão] - Fundo branco, borda #DDE3EC
        c_std = StandardCard(cards_row)
        c_std.grid(row=0, column=2, sticky="nsew", padx=5)
        c_std_inner = ctk.CTkFrame(c_std, fg_color="transparent")
        c_std_inner.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(
            c_std_inner,
            text="VENDAS REALIZADAS",
            font=get_font("caption"),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            c_std_inner,
            text="128 pedidos",
            font=get_font("card_price"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(6, 8))

        StatusPill(c_std_inner, text="Ticket Médio R$ 30,02", status="info").pack(anchor="w")

        # [Card Atenção] - Fundo #FFF4DC, borda #F3D391, texto #8A4B08
        c_warn = AttentionCard(cards_row)
        c_warn.grid(row=0, column=3, sticky="nsew", padx=(10, 0))
        c_warn_inner = ctk.CTkFrame(c_warn, fg_color="transparent")
        c_warn_inner.pack(fill="both", expand=True, padx=20, pady=18)

        ctk.CTkLabel(
            c_warn_inner,
            text="ALERTA DE ESTOQUE",
            font=get_font("caption"),
            text_color=COLORS["status_warning_text"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            c_warn_inner,
            text="3 itens críticos",
            font=get_font("card_price"),
            text_color=COLORS["status_warning_text"],
        ).pack(anchor="w", pady=(6, 8))

        StatusPill(c_warn_inner, text="Estoque Baixo", status="warning", icon="⚠").pack(anchor="w")

        # ── 3. Painel de Ações Rápidas (Botões e Medidas Oficiais) ───────────
        actions_card = StandardCard(content)
        actions_card.pack(fill="x", pady=(0, 28))
        actions_inner = ctk.CTkFrame(actions_card, fg_color="transparent")
        actions_inner.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(
            actions_inner,
            text="Ações Rápidas do Caixa",
            font=get_font("subtitle"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 16))

        btn_row = ctk.CTkFrame(actions_inner, fg_color="transparent")
        btn_row.pack(fill="x")

        # Botão Primário de Finalizar Venda (Altura 60px)
        btn_finish = PrimaryButton(
            btn_row,
            text="⚡  Finalizar Venda (60px)",
            is_finish=True,
            command=lambda: self._trigger_nav("caixa"),
        )
        btn_finish.pack(side="left", padx=(0, 12))

        # Botão Primário Padrão (Altura 48px)
        btn_primary = PrimaryButton(
            btn_row,
            text="🛒  Abrir Caixa (48px)",
            command=lambda: self._trigger_nav("caixa"),
        )
        btn_primary.pack(side="left", padx=(0, 12))

        # Botão Secundário (Fundo branco com borda #1D4ED8)
        btn_sec = SecondaryButton(
            btn_row,
            text="🔍  Consultar Preço",
            command=lambda: self._trigger_nav("produtos"),
        )
        btn_sec.pack(side="left", padx=(0, 12))

        # Botão de Cancelar (#C62828)
        btn_cancel = CancelButton(
            btn_row,
            text="✕  Cancelar Venda",
        )
        btn_cancel.pack(side="left")

        # ── 4. Galeria de Status e Amostras do Design System ─────────────────
        status_card = StandardCard(content)
        status_card.pack(fill="x")
        status_inner = ctk.CTkFrame(status_card, fg_color="transparent")
        status_inner.pack(fill="both", expand=True, padx=24, pady=20)

        ctk.CTkLabel(
            status_inner,
            text="Etiquetas de Status (Formato de Pílula)",
            font=get_font("subtitle"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w", pady=(0, 12))

        pills_row = ctk.CTkFrame(status_inner, fg_color="transparent")
        pills_row.pack(anchor="w")

        StatusPill(pills_row, text="Sucesso / Pago", status="success", icon="✓").pack(side="left", padx=(0, 10))
        StatusPill(pills_row, text="Atenção / Pendente", status="warning", icon="⏳").pack(side="left", padx=(0, 10))
        StatusPill(pills_row, text="Erro / Cancelado", status="danger", icon="✕").pack(side="left", padx=(0, 10))
        StatusPill(pills_row, text="Informação do Sistema", status="info", icon="ℹ").pack(side="left")

    def _trigger_nav(self, page_id: str):
        # Encontra o aplicativo raiz e navega
        root = self.winfo_toplevel()
        if hasattr(root, "navigate"):
            root.navigate(page_id)
