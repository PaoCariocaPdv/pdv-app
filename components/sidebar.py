"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil (Overlay Drawer)
Estilo e comportamento idênticos ao Caixa Bolo (caixa-bolo.vercel.app):
- Abre e fecha suavemente ao passar o mouse (hover), sem piscar.
- Funciona como um overlay (drawer) flutuante por cima do conteúdo.
- O conteúdo principal nunca é empurrado nem recalculado, eliminando qualquer flickering.
- Dois sub-painéis pré-renderizados garantem troca instantânea sem reconstrução de widgets.
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """
    Barra lateral moderna com abertura suave por sobreposição (Overlay Drawer).
    """

    COLLAPSED_WIDTH = 70
    EXPANDED_WIDTH  = 240

    NAV_ITEMS = [
        {"id": "home",      "icon": "🏠", "label": "Início"},
        {"id": "caixa",     "icon": "🛒", "label": "Caixa"},
        {"id": "produtos",  "icon": "📦", "label": "Produtos"},
        {"id": "vendas",    "icon": "📊", "label": "Vendas"},
        {"id": "clientes",  "icon": "👤", "label": "Clientes"},
        {"id": "relatorio", "icon": "📋", "label": "Relatórios"},
        {"id": "config",    "icon": "⚙️",  "label": "Configurações"},
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

        self._btns_col: dict[str, ctk.CTkButton] = {}
        self._btns_exp: dict[str, ctk.CTkButton] = {}

        self.grid_propagate(False)
        self._build_subframes()
        self.after(50, self._setup_mouse_tracking)

    # ------------------------------------------------------------------ #
    #  Construção das interfaces pré-renderizadas                         #
    # ------------------------------------------------------------------ #

    def _build_subframes(self):
        # 1. Painel Recolhido (apenas ícones centralizados, largura fixa 70px)
        self.frame_col = ctk.CTkFrame(
            self,
            width=self.COLLAPSED_WIDTH,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
        )
        self.frame_col.place(x=0, y=0, relheight=1.0)
        self.frame_col.grid_propagate(False)
        self.frame_col.grid_columnconfigure(0, weight=1)

        logo_col = ctk.CTkLabel(
            self.frame_col, text="🖥️",
            font=get_font("sidebar_title"), text_color="#FFFFFF",
        )
        logo_col.grid(row=0, column=0, pady=(20, 10))

        sep_col = ctk.CTkFrame(self.frame_col, height=1, fg_color="#1D2E47", corner_radius=0)
        sep_col.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 14))

        _icon_font = ctk.CTkFont(family="Segoe UI Emoji", size=18)
        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self.frame_col, text=item["icon"],
                font=_icon_font, anchor="center",
                height=44, corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=8, pady=3)
            self._btns_col[item["id"]] = btn

        footer_col = ctk.CTkLabel(
            self.frame_col, text=f"v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        )
        footer_col.grid(row=100, column=0, sticky="s", pady=16)
        self.frame_col.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)

        # 2. Painel Expandido (ícone + texto legível, largura 240px)
        self.frame_exp = ctk.CTkFrame(
            self,
            width=self.EXPANDED_WIDTH,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
        )
        self.frame_exp.place(x=0, y=0, relheight=1.0)
        self.frame_exp.grid_propagate(False)
        self.frame_exp.grid_columnconfigure(0, weight=1)

        logo_exp = ctk.CTkFrame(self.frame_exp, fg_color="transparent")
        logo_exp.grid(row=0, column=0, sticky="ew", padx=18, pady=(20, 10))
        ctk.CTkLabel(
            logo_exp, text="🖥️  PDV Caixa",
            font=get_font("sidebar_title"), text_color="#FFFFFF",
        ).pack(anchor="w")
        ctk.CTkLabel(
            logo_exp, text="Sistema de Ponto de Venda",
            font=get_font("small"), text_color=COLORS["sidebar_text"],
        ).pack(anchor="w", pady=(2, 0))

        sep_exp = ctk.CTkFrame(self.frame_exp, height=1, fg_color="#1D2E47", corner_radius=0)
        sep_exp.grid(row=1, column=0, sticky="ew", padx=16, pady=(6, 14))

        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self.frame_exp, text=f"  {item['icon']}   {item['label']}",
                font=get_font("sidebar_item"), anchor="w",
                height=44, corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=12, pady=3)
            self._btns_exp[item["id"]] = btn

        footer_exp = ctk.CTkLabel(
            self.frame_exp, text=f"PDV v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        )
        footer_exp.grid(row=100, column=0, sticky="s", pady=16)
        self.frame_exp.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)

        # Estado inicial recolhido
        self.frame_col.lift()
        self._apply_active(self.active_page)

    # ------------------------------------------------------------------ #
    #  Rastreamento do mouse (Global Motion) — Sem eventos falsos        #
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
    #  Animação suave de abertura e fechamento                           #
    # ------------------------------------------------------------------ #

    def _expand(self):
        self._is_expanded = True
        self._animating = True
        self.frame_exp.lift()
        steps = [110, 160, 205, self.EXPANDED_WIDTH]
        self._run_steps(steps, 0)

    def _collapse(self):
        self._collapse_timer = None
        self._is_expanded = False
        self._animating = True
        steps = [190, 140, 100, self.COLLAPSED_WIDTH]

        def _finish():
            self.frame_col.lift()
            self._animating = False

        self._run_steps(steps, 0, on_done=_finish)

    def _run_steps(self, steps, idx, on_done=None):
        if idx >= len(steps):
            if on_done:
                on_done()
            else:
                self._animating = False
            return
        self.configure(width=steps[idx])
        self.after(16, lambda: self._run_steps(steps, idx + 1, on_done))

    # ------------------------------------------------------------------ #
    #  Navegação e itens ativos                                          #
    # ------------------------------------------------------------------ #

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        self._apply_active(page_id)

    def _apply_active(self, page_id):
        for pid in self._btns_col:
            active = (pid == page_id)
            c = COLORS["primary"] if active else "transparent"
            t = "#FFFFFF" if active else COLORS["sidebar_text"]
            self._btns_col[pid].configure(fg_color=c, text_color=t)
            self._btns_exp[pid].configure(fg_color=c, text_color=t)
