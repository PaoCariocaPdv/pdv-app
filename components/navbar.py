"""
PDV - Ponto de Venda
Componente: Barra de Navegação no Topo (Header / Navbar Superior)
"""

import os
import sys
import customtkinter as ctk
from PIL import Image
from config import COLORS, APP_VERSION
from fonts import get_font


class TopNavbar(ctk.CTkFrame):
    """
    Barra de navegação horizontal no topo:
    - Logotipo "Pão Carioca" com badge PDV à esquerda
    - Abas com ícone e texto (Início, Caixa, Produtos, etc.) ao centro
    - Indicador de status do Caixa e versão à direita
    """

    NAV_ITEMS = [
        {"id": "home",      "label": "Início"},
        {"id": "caixa",     "label": "Caixa"},
        {"id": "produtos",  "label": "Produtos"},
        {"id": "vendas",    "label": "Vendas"},
        {"id": "clientes",  "label": "Clientes"},
        {"id": "relatorio", "label": "Relatórios"},
        {"id": "config",    "label": "Configurações"},
    ]

    def __init__(self, parent, navigate_callback, **kwargs):
        super().__init__(
            parent,
            height=64,
            fg_color="#FFFFFF",
            border_color="#E2E8F0",
            border_width=1,
            corner_radius=0,
            **kwargs
        )
        self.pack_propagate(False)
        self.navigate_callback = navigate_callback
        self.active_page = "home"

        self._btns = {}
        self._icons = {}

        self._load_icons()
        self._build_ui()

    def _load_icons(self):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icons_dir = os.path.join(base_dir, "assets", "icons")
        from components.sidebar_icons import ensure_sidebar_icons
        ensure_sidebar_icons(icons_dir)

        for k in ["logo", "home", "caixa", "produtos", "vendas", "clientes", "relatorio", "config"]:
            im_def = Image.open(os.path.join(icons_dir, f"{k}_default.png"))
            im_act = Image.open(os.path.join(icons_dir, f"{k}_active.png"))
            im_hov = Image.open(os.path.join(icons_dir, f"{k}_hover.png"))
            self._icons[k] = {
                "default": ctk.CTkImage(light_image=im_def, dark_image=im_def, size=(18, 18)),
                "active":  ctk.CTkImage(light_image=im_act, dark_image=im_act, size=(18, 18)),
                "hover":   ctk.CTkImage(light_image=im_hov, dark_image=im_hov, size=(18, 18)),
            }

    def _build_ui(self):
        # 1. Esquerda: Logotipo e Identidade da Marca
        left_box = ctk.CTkFrame(self, fg_color="transparent")
        left_box.pack(side="left", padx=(20, 14), pady=12)

        logo_lbl = ctk.CTkLabel(
            left_box, text="", image=self._icons["logo"]["hover"],
            width=22, height=22
        )
        logo_lbl.pack(side="left", padx=(0, 10))

        brand_lbl = ctk.CTkLabel(
            left_box, text="Pão Carioca",
            font=get_font("subtitle"),
            text_color=COLORS.get("primary", "#1D4ED8")
        )
        brand_lbl.pack(side="left")

        badge = ctk.CTkFrame(left_box, fg_color="#EFF6FF", corner_radius=6)
        badge.pack(side="left", padx=(10, 0))
        ctk.CTkLabel(
            badge, text="PDV",
            font=get_font("small"),
            text_color=COLORS.get("primary", "#1D4ED8")
        ).pack(padx=6, pady=2)

        # Divisor vertical sutil
        div = ctk.CTkFrame(self, width=1, height=28, fg_color="#E2E8F0", corner_radius=0)
        div.pack(side="left", padx=10, pady=18)

        # 2. Centro: Abas de Navegação (Pills arredondados)
        nav_box = ctk.CTkFrame(self, fg_color="transparent")
        nav_box.pack(side="left", padx=8, fill="y")

        for item in self.NAV_ITEMS:
            pid = item["id"]
            active = (pid == self.active_page)

            btn = ctk.CTkButton(
                nav_box,
                text=f"  {item['label']}",
                image=self._icons[pid]["active" if active else "default"],
                compound="left",
                font=get_font("body_bold" if active else "body"),
                height=38,
                corner_radius=10,
                fg_color=COLORS.get("primary", "#1D4ED8") if active else "transparent",
                hover_color=COLORS.get("primary_hover", "#1E40AF") if active else COLORS.get("sidebar_hover", "#EFF6FF"),
                text_color="#FFFFFF" if active else COLORS.get("sidebar_text", "#64748B"),
                cursor="hand2",
                command=lambda x=pid: self._on_click(x)
            )
            btn.pack(side="left", padx=3, pady=13)
            self._btns[pid] = btn

            # Hover unificado
            btn.bind("<Enter>", lambda e, x=pid: self._on_hover_enter(x))
            btn.bind("<Leave>", lambda e, x=pid: self._on_hover_leave(x))

        # 3. Direita: Status e Versão
        right_box = ctk.CTkFrame(self, fg_color="transparent")
        right_box.pack(side="right", padx=(16, 24), pady=12)

        status_badge = ctk.CTkFrame(right_box, fg_color="#E3F6EC", corner_radius=8)
        status_badge.pack(side="left", padx=(0, 14))
        ctk.CTkLabel(
            status_badge, text="● Caixa Aberto",
            font=get_font("small"),
            text_color="#0E7A4F"
        ).pack(padx=10, pady=4)

        ctk.CTkLabel(
            right_box, text=f"v{APP_VERSION}",
            font=get_font("small"),
            text_color="#94A3B8"
        ).pack(side="left")

    def _on_hover_enter(self, pid):
        if pid != self.active_page:
            self._btns[pid].configure(
                text_color=COLORS.get("primary", "#1D4ED8"),
                image=self._icons[pid]["hover"]
            )

    def _on_leave(self, pid):
        pass

    def _on_hover_leave(self, pid):
        if pid != self.active_page:
            self._btns[pid].configure(
                text_color=COLORS.get("sidebar_text", "#64748B"),
                image=self._icons[pid]["default"]
            )

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        for pid, btn in self._btns.items():
            active = (pid == page_id)
            btn.configure(
                fg_color=COLORS.get("primary", "#1D4ED8") if active else "transparent",
                hover_color=COLORS.get("primary_hover", "#1E40AF") if active else COLORS.get("sidebar_hover", "#EFF6FF"),
                text_color="#FFFFFF" if active else COLORS.get("sidebar_text", "#64748B"),
                font=get_font("body_bold" if active else "body"),
                image=self._icons[pid]["active" if active else "default"]
            )
