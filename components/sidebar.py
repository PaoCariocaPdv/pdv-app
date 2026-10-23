"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil (Overlay Drawer)
- Ícones matematicamente fixos na mesma posição (x = 24px) o tempo todo.
- Ao abrir o menu, os nomes vão surgindo suavemente da esquerda para a direita.
- O botão se expande de 54px para 224px sem qualquer salto ou reposicionamento de ícones.
"""

import os
import sys
import customtkinter as ctk
from PIL import Image
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """
    Barra lateral com ícones perfeitamente estáticos e expansão suave da esquerda para a direita.
    """

    COLLAPSED_WIDTH = 70
    EXPANDED_WIDTH  = 240

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
            width=self.COLLAPSED_WIDTH,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
            **kwargs,
        )
        self.navigate_callback = navigate_callback
        self.active_page = "home"

        self._is_expanded = False
        self._animating = False
        self._collapse_timer = None

        self._btns: dict[str, ctk.CTkButton] = {}
        self._icons = {}

        self._load_icons()
        self.pack_propagate(False)
        self._build_ui()
        self.after(50, self._setup_mouse_tracking)

    def _load_icons(self):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icons_dir = os.path.join(base_dir, "assets", "icons")

        from components.sidebar_icons import ensure_sidebar_icons
        ensure_sidebar_icons(icons_dir)

        keys = ["logo", "home", "caixa", "produtos", "vendas", "clientes", "relatorio", "config"]
        for k in keys:
            def_path = os.path.join(icons_dir, f"{k}_default.png")
            act_path = os.path.join(icons_dir, f"{k}_active.png")
            im_def = Image.open(def_path)
            im_act = Image.open(act_path)
            self._icons[k] = {
                "default": ctk.CTkImage(light_image=im_def, dark_image=im_def, size=(22, 22)),
                "active": ctk.CTkImage(light_image=im_act, dark_image=im_act, size=(22, 22)),
            }

    def _build_ui(self):
        # ── 1. Topo: Logo (Ícone estático a x=8, texto a x=68) ────────────────
        self.logo_icon = ctk.CTkLabel(
            self,
            text="",
            image=self._icons["logo"]["active"],
            width=54,
            height=44,
        )
        self.logo_icon.place(x=8, y=20)

        self.logo_text = ctk.CTkFrame(self, fg_color="transparent")
        self.logo_text.place(x=68, y=20)

        self.title_lbl = ctk.CTkLabel(
            self.logo_text,
            text="PDV Caixa",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        )
        self.title_lbl.pack(anchor="w")

        self.sub_lbl = ctk.CTkLabel(
            self.logo_text,
            text="Sistema de Ponto de Venda",
            font=get_font("small"),
            text_color=COLORS["sidebar_text"],
        )
        self.sub_lbl.pack(anchor="w", pady=(1, 0))

        # ── 2. Separador ──────────────────────────────────────────────────────
        self.sep = ctk.CTkFrame(self, width=46, height=1, fg_color="#1D2E47", corner_radius=0)
        self.sep.place(x=12, y=74)

        # ── 3. Botões de Navegação Únicos ─────────────────────────────────────
        # Todos com border_spacing=16 para travar o ícone exatamente a x=24
        for i, item in enumerate(self.NAV_ITEMS):
            y_pos = 92 + i * 50
            btn = ctk.CTkButton(
                self,
                text="",
                image=self._icons[item["id"]]["default"],
                compound="left",
                anchor="w",
                width=54,
                height=44,
                corner_radius=10,
                border_spacing=16,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                font=get_font("sidebar_item"),
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.place(x=8, y=y_pos)
            self._btns[item["id"]] = btn

        # ── 4. Rodapé de Versão ───────────────────────────────────────────────
        self.footer = ctk.CTkLabel(
            self,
            text=f"v{APP_VERSION}",
            font=get_font("small"),
            text_color="#627594",
            width=54,
        )
        self.footer.place(x=8, rely=1.0, y=-38)

        self._apply_active(self.active_page)

    # ------------------------------------------------------------------ #
    #  Rastreamento do mouse (Global Motion)                             #
    # ------------------------------------------------------------------ #

    def _setup_mouse_tracking(self):
        top = self.winfo_toplevel()
        top.bind_all("<Motion>", self._on_global_motion, add="+")
        top.bind("<Leave>", self._on_window_leave, add="+")

    def _on_global_motion(self, event):
        try:
            sx = self.winfo_rootx()
            sy = self.winfo_rooty()
            sw = self.winfo_width()
            sh = self.winfo_height()
            is_over = (sx <= event.x_root <= sx + sw and sy <= event.y_root <= sy + sh)
        except Exception:
            is_over = False

        if is_over:
            if self._collapse_timer:
                self.after_cancel(self._collapse_timer)
                self._collapse_timer = None
            if not self._is_expanded and not self._animating:
                self._expand()
        else:
            if self._is_expanded and not self._collapse_timer:
                self._collapse_timer = self.after(100, self._collapse)

    def _on_window_leave(self, event):
        if self._is_expanded and not self._collapse_timer:
            self._collapse_timer = self.after(80, self._collapse)

    # ------------------------------------------------------------------ #
    #  Expansão e Recolhimento Suaves sem reposicionar ícones             #
    # ------------------------------------------------------------------ #

    def _expand(self):
        self._is_expanded = True
        self._animating = True

        # Revela os textos dos botões à direita dos ícones
        for item in self.NAV_ITEMS:
            self._btns[item["id"]].configure(text=f"   {item['label']}")
        self.footer.configure(text=f"PDV v{APP_VERSION}")

        steps = [105, 145, 185, 215, self.EXPANDED_WIDTH]
        self._run_steps(steps, 0)

    def _collapse(self):
        self._collapse_timer = None
        self._is_expanded = False
        self._animating = True

        steps = [210, 170, 130, 95, self.COLLAPSED_WIDTH]

        def _finish():
            # No estado final recolhido, esconde textos para manter botões 54px arredondados
            for item in self.NAV_ITEMS:
                self._btns[item["id"]].configure(text="", width=54)
            self.footer.configure(text=f"v{APP_VERSION}", width=54)
            self.sep.configure(width=46)
            self.configure(width=self.COLLAPSED_WIDTH)
            self._animating = False

        self._run_steps(steps, 0, on_done=_finish)

    def _run_steps(self, steps, idx, on_done=None):
        if idx >= len(steps):
            if on_done:
                on_done()
            else:
                self._animating = False
            return

        w = steps[idx]
        self.configure(width=w)
        btn_w = w - 16
        for btn in self._btns.values():
            btn.configure(width=btn_w)
        self.sep.configure(width=max(46, w - 24))

        self.after(16, lambda: self._run_steps(steps, idx + 1, on_done))

    # ------------------------------------------------------------------ #
    #  Navegação e Itens Ativos                                          #
    # ------------------------------------------------------------------ #

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        self._apply_active(page_id)

    def _apply_active(self, page_id):
        for pid, btn in self._btns.items():
            active = (pid == page_id)
            c = COLORS["primary"] if active else "transparent"
            t = "#FFFFFF" if active else COLORS["sidebar_text"]
            icon_type = "active" if active else "default"

            btn.configure(
                fg_color=c,
                text_color=t,
                image=self._icons[pid][icon_type],
            )
