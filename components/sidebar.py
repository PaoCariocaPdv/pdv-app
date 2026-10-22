"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil (Hover para expandir/recolher)
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """Barra lateral de navegação retrátil: exibe apenas ícones por padrão e expande ao passar o mouse."""

    COLLAPSED_WIDTH = 70
    EXPANDED_WIDTH = 230

    NAV_ITEMS = [
        {"id": "home",     "icon": "🏠", "label": "Início"},
        {"id": "caixa",    "icon": "🛒", "label": "Caixa"},
        {"id": "produtos", "icon": "📦", "label": "Produtos"},
        {"id": "vendas",   "icon": "📊", "label": "Vendas"},
        {"id": "clientes", "icon": "👤", "label": "Clientes"},
        {"id": "relatorio","icon": "📋", "label": "Relatórios"},
        {"id": "config",   "icon": "⚙️", "label": "Configurações"},
    ]

    def __init__(self, parent, navigate_callback, **kwargs):
        super().__init__(
            parent,
            width=self.COLLAPSED_WIDTH,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
            **kwargs
        )
        self.navigate_callback = navigate_callback
        self.active_page = "home"
        self.is_expanded = False
        self._collapse_job = None
        self._buttons: dict[str, ctk.CTkButton] = {}

        self._build()
        self.collapse()  # Inicia recolhido por padrão

    def _build(self):
        self.grid_propagate(False)
        self.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header / Logo
        self.logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(20, 10))

        self.logo_title = ctk.CTkLabel(
            self.logo_frame,
            text="🖥️",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        )
        self.logo_title.pack(anchor="center")

        self.logo_subtitle = ctk.CTkLabel(
            self.logo_frame,
            text="Sistema de Ponto de Venda",
            font=get_font("small"),
            text_color=COLORS["sidebar_text"],
        )
        # Inicia sem o subtítulo visível

        # Separador elegante
        self.sep = ctk.CTkFrame(self, height=1, fg_color="#1D2E47", corner_radius=0)
        self.sep.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 14))

        # Itens de navegação
        for i, item in enumerate(self.NAV_ITEMS):
            btn = self._make_nav_button(item)
            btn.grid(row=i + 2, column=0, sticky="ew", padx=10, pady=3)
            self._buttons[item["id"]] = btn

        # Rodapé / Versão
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.grid(row=100, column=0, sticky="s", pady=16)

        self.footer_label = ctk.CTkLabel(
            self.footer_frame,
            text=f"v{APP_VERSION}",
            font=get_font("small"),
            text_color="#627594",
        )
        self.footer_label.pack(anchor="center")

        self.set_active("home")

        # Conecta eventos de mouse para expandir / recolher
        self._bind_hover_recursive(self)

    def _make_nav_button(self, item):
        btn = ctk.CTkButton(
            self,
            text=item["icon"],
            font=get_font("sidebar_title"),
            anchor="center",
            height=44,
            corner_radius=10,
            fg_color="transparent",
            hover_color=COLORS["sidebar_active"],
            text_color=COLORS["sidebar_text"],
            command=lambda p=item["id"]: self._on_click(p),
        )
        return btn

    def _on_click(self, page_id):
        self.set_active(page_id)
        self.navigate_callback(page_id)

    def set_active(self, page_id):
        self.active_page = page_id
        for pid, btn in self._buttons.items():
            if pid == page_id:
                btn.configure(
                    fg_color=COLORS["primary"],
                    text_color="#FFFFFF",
                )
            else:
                btn.configure(
                    fg_color="transparent",
                    text_color=COLORS["sidebar_text"],
                )

    def expand(self):
        """Expande a barra lateral exibindo ícones e nomes."""
        self.is_expanded = True
        self.configure(width=self.EXPANDED_WIDTH)

        # Ajusta logo
        self.logo_frame.grid_configure(padx=18, pady=(20, 10))
        self.logo_title.pack_configure(anchor="w")
        self.logo_title.configure(text="🖥️  PDV Caixa", font=get_font("sidebar_title"))
        self.logo_subtitle.pack(anchor="w", pady=(2, 0))

        # Ajusta separador
        self.sep.grid_configure(padx=16)

        # Atualiza botões com ícone + nome alinhado à esquerda
        for item in self.NAV_ITEMS:
            btn = self._buttons[item["id"]]
            btn.grid_configure(padx=12)
            btn.configure(
                text=f"  {item['icon']}   {item['label']}",
                font=get_font("sidebar_item"),
                anchor="w",
            )

        # Rodapé
        self.footer_label.configure(text=f"PDV v{APP_VERSION}")

    def collapse(self):
        """Recolhe a barra lateral exibindo apenas os ícones."""
        self.is_expanded = False
        self.configure(width=self.COLLAPSED_WIDTH)

        # Ajusta logo
        self.logo_frame.grid_configure(padx=6, pady=(16, 10))
        self.logo_title.pack_configure(anchor="center")
        self.logo_title.configure(text="🖥️", font=get_font("sidebar_title"))
        self.logo_subtitle.pack_forget()

        # Ajusta separador
        self.sep.grid_configure(padx=10)

        # Atualiza botões com apenas ícone centralizado
        for item in self.NAV_ITEMS:
            btn = self._buttons[item["id"]]
            btn.grid_configure(padx=8)
            btn.configure(
                text=item["icon"],
                font=ctk.CTkFont(family="Segoe UI Emoji", size=18),
                anchor="center",
            )

        # Rodapé compacto
        self.footer_label.configure(text=f"v{APP_VERSION}")

    def _on_enter(self, event=None):
        """Disparado quando o mouse entra na sidebar ou em seus botões."""
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
            self._collapse_job = None

        if not self.is_expanded:
            self.expand()

    def _on_leave(self, event=None):
        """Disparado quando o mouse sai de algum widget da sidebar."""
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
        self._collapse_job = self.after(120, self._check_and_collapse)

    def _check_and_collapse(self):
        """Verifica se o cursor do mouse realmente saiu da área da sidebar."""
        self._collapse_job = None
        try:
            x, y = self.winfo_pointerxy()
            widget = self.winfo_containing(x, y)
            if widget is None or not str(widget).startswith(str(self)):
                self.collapse()
        except Exception:
            self.collapse()

    def _bind_hover_recursive(self, widget):
        """Vincula eventos de hover recursivamente em todos os filhos."""
        try:
            widget.bind("<Enter>", self._on_enter, add="+")
            widget.bind("<Leave>", self._on_leave, add="+")
        except Exception:
            pass

        # Vincula também em canvases ou labels internos de widgets CTk
        for attr in ("_canvas", "_label", "_image_label", "_text_label"):
            sub = getattr(widget, attr, None)
            if sub:
                try:
                    sub.bind("<Enter>", self._on_enter, add="+")
                    sub.bind("<Leave>", self._on_leave, add="+")
                except Exception:
                    pass

        for child in widget.winfo_children():
            self._bind_hover_recursive(child)
