"""
PDV - Ponto de Venda
Página: Caixa / PDV (Implementada rigorosamente com o Design System Oficial)
"""

import customtkinter as ctk
from config import COLORS
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


class CaixaPage(ctk.CTkFrame):
    """Tela de Ponto de Venda (Caixa) completa com o Design System padronizado."""

    SAMPLE_PRODUCTS = [
        {"id": "1", "name": "Pão Francês Tradicional", "price": 0.95, "unit": "un", "stock": 180, "cat": "Padaria"},
        {"id": "2", "name": "Bolo Caseiro de Cenoura", "price": 28.50, "unit": "un", "stock": 4, "cat": "Confeitaria"},
        {"id": "3", "name": "Café Espresso Duplo",     "price": 7.00,  "unit": "un", "stock": 95, "cat": "Bebidas"},
        {"id": "4", "name": "Croissant de Presunto",   "price": 12.00, "unit": "un", "stock": 2, "cat": "Salgados"},
        {"id": "5", "name": "Suco de Laranja 500ml",   "price": 9.50,  "unit": "un", "stock": 25, "cat": "Bebidas"},
        {"id": "6", "name": "Pão de Queijo Mineiro",   "price": 4.50,  "unit": "un", "stock": 42, "cat": "Salgados"},
    ]

    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            fg_color=COLORS["bg_screen"],
            corner_radius=0,
            **kwargs
        )
        self.cart = [
            {"name": "Pão Francês Tradicional", "qty": 10, "unit_price": 0.95, "total": 9.50},
            {"name": "Café Espresso Duplo",     "qty": 2,  "unit_price": 7.00, "total": 14.00},
            {"name": "Bolo Caseiro de Cenoura", "qty": 1,  "unit_price": 28.50,"total": 28.50},
        ]
        self.selected_cart_index = 0
        self._build()

    def _build(self):
        # Grid com 2 colunas: Catálogo de Produtos (esquerda, flex) + Cupom / Total (direita, 380px)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        # ── COLUNA ESQUERDA: CATÁLOGO DE PRODUTOS ─────────────────────────────
        left_panel = ctk.CTkFrame(self, fg_color="transparent")
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(28, 14), pady=24)
        left_panel.grid_rowconfigure(1, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        # Header da esquerda
        header_left = ctk.CTkFrame(left_panel, fg_color="transparent")
        header_left.grid(row=0, column=0, sticky="ew", pady=(0, 16))

        ctk.CTkLabel(
            header_left,
            text="Caixa / Venda Rápida",
            font=get_font("screen_title"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            header_left,
            text="Clique nos produtos para adicionar ao cupom da venda",
            font=get_font("subtitle"),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(2, 0))

        # Grid de produtos com scroll
        catalog_scroll = ctk.CTkScrollableFrame(
            left_panel,
            fg_color="transparent",
            corner_radius=0,
        )
        catalog_scroll.grid(row=1, column=0, sticky="nsew")
        catalog_scroll.grid_columnconfigure((0, 1, 2), weight=1, uniform="prod_col")

        # Renderiza os cards de produtos
        for i, prod in enumerate(self.SAMPLE_PRODUCTS):
            r = i // 3
            c = i % 3
            self._render_product_card(catalog_scroll, prod, r, c)

        # ── COLUNA DIREITA: CUPOM FISCAL & TOTAL ──────────────────────────────
        right_panel = ctk.CTkFrame(self, width=390, fg_color="transparent")
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(14, 28), pady=24)
        right_panel.grid_propagate(False)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        # Cabeçalho do Cupom
        cupom_header = ctk.CTkFrame(right_panel, fg_color="transparent")
        cupom_header.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        ctk.CTkLabel(
            cupom_header,
            text="Itens da Venda",
            font=get_font("subtitle"),
            text_color=COLORS["text_primary"],
        ).pack(side="left")

        StatusPill(cupom_header, text=f"{len(self.cart)} itens", status="info").pack(side="right")

        # Lista de itens no cupom (Cards padrão vs Card Selecionado)
        cart_scroll = ctk.CTkScrollableFrame(
            right_panel,
            fg_color="transparent",
            corner_radius=0,
        )
        cart_scroll.grid(row=1, column=0, sticky="nsew", pady=(0, 16))

        for idx, item in enumerate(self.cart):
            is_selected = (idx == self.selected_cart_index)
            CardClass = SelectedCard if is_selected else StandardCard
            
            card = CardClass(cart_scroll)
            card.pack(fill="x", pady=4)

            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(fill="both", expand=True, padx=14, pady=10)

            # Linha superior: Nome do item + Preço total
            top_line = ctk.CTkFrame(inner, fg_color="transparent")
            top_line.pack(fill="x")

            ctk.CTkLabel(
                top_line,
                text=item["name"],
                font=get_font("body_bold"),
                text_color=COLORS["text_primary"],
            ).pack(side="left")

            ctk.CTkLabel(
                top_line,
                text=f"R$ {item['total']:.2f}".replace(".", ","),
                font=get_font("body_bold"),
                text_color=COLORS["primary"],
            ).pack(side="right")

            # Linha inferior: Quantidade x Unitário
            bot_line = ctk.CTkFrame(inner, fg_color="transparent")
            bot_line.pack(fill="x", pady=(2, 0))

            ctk.CTkLabel(
                bot_line,
                text=f"{item['qty']} un  ×  R$ {item['unit_price']:.2f}".replace(".", ","),
                font=get_font("caption"),
                text_color=COLORS["text_secondary"],
            ).pack(side="left")

            if is_selected:
                StatusPill(bot_line, text="Selecionado", status="info").pack(side="right")

        # ── PAINEL DE TOTAL & BOTÕES INFERIORES ──────────────────────────────
        footer_area = ctk.CTkFrame(right_panel, fg_color="transparent")
        footer_area.grid(row=2, column=0, sticky="ew")

        # Card de Total: fundo #0B1B33, texto branco, total destacado 36-44px
        total_card = TotalCard(footer_area)
        total_card.pack(fill="x", pady=(0, 14))

        tc_inner = ctk.CTkFrame(total_card, fg_color="transparent")
        tc_inner.pack(fill="both", expand=True, padx=20, pady=16)

        ctk.CTkLabel(
            tc_inner,
            text="TOTAL A PAGAR",
            font=get_font("caption"),
            text_color=COLORS["sidebar_text"],
        ).pack(anchor="w")

        total_val = sum(i["total"] for i in self.cart)
        ctk.CTkLabel(
            tc_inner,
            text=f"R$ {total_val:.2f}".replace(".", ","),
            font=get_font("total"),
            text_color="#FFFFFF",
        ).pack(anchor="w", pady=(2, 4))

        ctk.CTkLabel(
            tc_inner,
            text="Descontos aplicados: R$ 0,00",
            font=get_font("small"),
            text_color=COLORS["sidebar_text"],
        ).pack(anchor="w")

        # Botão Primário: "Finalizar Venda" (Altura 60px, fundo #1D4ED8, texto branco, raio 12px)
        btn_finalize = PrimaryButton(
            footer_area,
            text="⚡  FINALIZAR VENDA",
            is_finish=True,
            command=self._on_finalize,
        )
        btn_finalize.pack(fill="x", pady=(0, 10))

        # Botões Secundários: Adicionar Desconto + Cancelar
        actions_row = ctk.CTkFrame(footer_area, fg_color="transparent")
        actions_row.pack(fill="x")

        SecondaryButton(
            actions_row,
            text="Desconto / Cupom",
            width=180,
        ).pack(side="left", padx=(0, 6))

        CancelButton(
            actions_row,
            text="Cancelar",
            width=180,
            command=self._on_cancel,
        ).pack(side="right")

    def _render_product_card(self, parent, prod, row, col):
        is_low_stock = prod["stock"] <= 3

        # Se estoque estiver muito baixo, usa AttentionCard, senão StandardCard
        CardWidget = AttentionCard if is_low_stock else StandardCard
        card = CardWidget(parent)
        card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=16, pady=16)

        # Categoria & Estoque
        top_row = ctk.CTkFrame(inner, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            top_row,
            text=prod["cat"].upper(),
            font=get_font("small"),
            text_color=COLORS["text_secondary"] if not is_low_stock else COLORS["status_warning_text"],
        ).pack(side="left")

        if is_low_stock:
            StatusPill(top_row, text=f"Resta {prod['stock']}", status="warning", icon="⚠").pack(side="right")
        else:
            ctk.CTkLabel(
                top_row,
                text=f"Estoque: {prod['stock']}",
                font=get_font("caption"),
                text_color=COLORS["text_secondary"],
            ).pack(side="right")

        # Nome do produto: Inter 600, 16px
        ctk.CTkLabel(
            inner,
            text=prod["name"],
            font=get_font("body_bold"),
            text_color=COLORS["text_primary"],
            wraplength=180,
            justify="left",
        ).pack(anchor="w", pady=(0, 10))

        # Preço: Plus Jakarta Sans 800, 22px (#1D4ED8)
        price_row = ctk.CTkFrame(inner, fg_color="transparent")
        price_row.pack(fill="x", pady=(4, 12))

        ctk.CTkLabel(
            price_row,
            text=f"R$ {prod['price']:.2f}".replace(".", ","),
            font=get_font("card_price"),
            text_color=COLORS["primary"],
        ).pack(side="left")

        # Botão rápido de adicionar
        add_btn = PrimaryButton(
            inner,
            text="+ Adicionar",
            height=38,
            command=lambda p=prod: self._add_to_cart(p),
        )
        add_btn.pack(fill="x")

    def _add_to_cart(self, prod):
        self.cart.append({
            "name": prod["name"],
            "qty": 1,
            "unit_price": prod["price"],
            "total": prod["price"],
        })
        self.selected_cart_index = len(self.cart) - 1
        # Reconstrói a tela
        for w in self.winfo_children():
            w.destroy()
        self._build()

    def _on_finalize(self):
        # Exibe mensagem de sucesso
        pass

    def _on_cancel(self):
        self.cart.clear()
        for w in self.winfo_children():
            w.destroy()
        self._build()
