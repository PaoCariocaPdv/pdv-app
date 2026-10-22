"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil
Abordagem: polling de posição + overlay place() — sem eventos de hover,
sem reflow de layout, sem flickering.
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """
    Sidebar retrátil sem flickering:
    - Frame base (70px) NUNCA muda de largura → sem reflow do grid.
    - Overlay (230px) aparece/desaparece via place() → operação O(1).
    - Mouse rastreado por polling (30ms) → sem eventos Leave falsos.
    """

    COLLAPSED_WIDTH = 70
    EXPANDED_WIDTH  = 230
    POLL_MS         = 30   # intervalo de polling (ms)

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
        self._parent           = parent
        self.navigate_callback = navigate_callback
        self._is_expanded      = False
        self.active_page       = "home"

        self._btns_base: dict[str, ctk.CTkButton] = {}  # ícones
        self._btns_over: dict[str, ctk.CTkButton] = {}  # ícone + nome

        self.grid_propagate(False)
        self._build_base()
        self._overlay = self._build_overlay()

        # Inicia o loop de polling após a janela estar pronta
        self.after(200, self._poll_mouse)

    # ------------------------------------------------------------------ #
    #  Frame base — ícones compactos, 70px fixo                           #
    # ------------------------------------------------------------------ #

    def _build_base(self):
        self.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="🖥️",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        ).grid(row=0, column=0, pady=(20, 10))

        ctk.CTkFrame(self, height=1, fg_color="#1D2E47", corner_radius=0).grid(
            row=1, column=0, sticky="ew", padx=12, pady=(6, 14),
        )

        _icon_font = ctk.CTkFont(family="Segoe UI Emoji", size=18)
        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self, text=item["icon"],
                font=_icon_font, anchor="center",
                height=44, corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=8, pady=3)
            self._btns_base[item["id"]] = btn

        ctk.CTkLabel(
            self, text=f"v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        ).grid(row=100, column=0, sticky="s", pady=16)

        self._apply_active_on(self.active_page, self._btns_base)

    # ------------------------------------------------------------------ #
    #  Overlay — ícone + nome, 230px, place() sobre o parent              #
    # ------------------------------------------------------------------ #

    def _build_overlay(self) -> ctk.CTkFrame:
        ov = ctk.CTkFrame(
            self._parent,
            width=self.EXPANDED_WIDTH,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
        )
        ov.grid_propagate(False)
        ov.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)
        ov.grid_columnconfigure(0, weight=1)

        logo = ctk.CTkFrame(ov, fg_color="transparent")
        logo.grid(row=0, column=0, sticky="ew", padx=18, pady=(20, 10))
        ctk.CTkLabel(
            logo, text="🖥️  PDV Caixa",
            font=get_font("sidebar_title"), text_color="#FFFFFF",
        ).pack(anchor="w")
        ctk.CTkLabel(
            logo, text="Sistema de Ponto de Venda",
            font=get_font("small"), text_color=COLORS["sidebar_text"],
        ).pack(anchor="w", pady=(2, 0))

        ctk.CTkFrame(ov, height=1, fg_color="#1D2E47", corner_radius=0).grid(
            row=1, column=0, sticky="ew", padx=16, pady=(6, 14),
        )

        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                ov, text=f"  {item['icon']}   {item['label']}",
                font=get_font("sidebar_item"), anchor="w",
                height=44, corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=12, pady=3)
            self._btns_over[item["id"]] = btn

        ctk.CTkLabel(
            ov, text=f"PDV v{APP_VERSION}",
            font=get_font("small"), text_color="#627594",
        ).grid(row=100, column=0, sticky="s", pady=16)

        self._apply_active_on(self.active_page, self._btns_over)
        return ov

    # ------------------------------------------------------------------ #
    #  Polling de mouse — detecta hover sem usar eventos <Enter>/<Leave>  #
    # ------------------------------------------------------------------ #

    def _poll_mouse(self):
        """Verifica posição do mouse a cada POLL_MS ms e atualiza o estado."""
        try:
            x, y = self.winfo_pointerxy()
            inside = self._mouse_in_sidebar(x, y)

            if inside and not self._is_expanded:
                self._show_overlay()
            elif not inside and self._is_expanded:
                self._hide_overlay()
        except Exception:
            pass

        # Agenda próxima verificação
        self.after(self.POLL_MS, self._poll_mouse)

    def _mouse_in_sidebar(self, x: int, y: int) -> bool:
        """Retorna True se o mouse está sobre o frame base OU sobre o overlay."""
        try:
            bx = self.winfo_rootx()
            by = self.winfo_rooty()
            bh = self.winfo_height()
            # Quando expandido, o overlay cobre 230px; senão, 70px
            bw = self.EXPANDED_WIDTH if self._is_expanded else self.COLLAPSED_WIDTH
            return bx <= x <= bx + bw and by <= y <= by + bh
        except Exception:
            return False

    # ------------------------------------------------------------------ #
    #  Mostrar / Esconder overlay                                          #
    # ------------------------------------------------------------------ #

    def _show_overlay(self):
        self._is_expanded = True
        self._overlay.place(x=0, y=0, width=self.EXPANDED_WIDTH, relheight=1.0)
        self._overlay.lift()

    def _hide_overlay(self):
        self._is_expanded = False
        self._overlay.place_forget()

    # ------------------------------------------------------------------ #
    #  Navegação e estado ativo                                            #
    # ------------------------------------------------------------------ #

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        self._apply_active_on(page_id, self._btns_base)
        self._apply_active_on(page_id, self._btns_over)

    def _apply_active_on(self, page_id, btns: dict):
        for pid, btn in btns.items():
            active = pid == page_id
            btn.configure(
                fg_color=COLORS["primary"] if active else "transparent",
                text_color="#FFFFFF" if active else COLORS["sidebar_text"],
            )
