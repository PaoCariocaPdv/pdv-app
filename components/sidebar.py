"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil (Hover para expandir/recolher)
Performance optimizada: animação suave por interpolação, sem binding recursivo.
"""

import customtkinter as ctk
from config import COLORS, APP_VERSION
from fonts import get_font


class Sidebar(ctk.CTkFrame):
    """Barra lateral de navegação retrátil com transição suave de largura."""

    COLLAPSED_WIDTH = 70
    EXPANDED_WIDTH  = 230
    # Parâmetros de animação
    ANIM_STEP_MS   = 12    # intervalo entre cada frame (ms)
    ANIM_STEPS     = 10    # número de passos da animação

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
        self.active_page       = "home"
        self._is_expanded      = False
        self._anim_job         = None   # ID do after() de animação corrente
        self._collapse_job     = None   # ID do after() de debounce de collapse
        self._current_width    = float(self.COLLAPSED_WIDTH)
        self._target_width     = float(self.COLLAPSED_WIDTH)
        self._buttons: dict[str, ctk.CTkButton] = {}

        self._build()
        # Aplica estado recolhido SEM animação no arranque
        self._apply_collapsed_look()

    # ------------------------------------------------------------------ #
    #  Construção do layout                                                #
    # ------------------------------------------------------------------ #

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
        # Inicia oculto — mostrado somente quando expandido

        # Separador
        self.sep = ctk.CTkFrame(self, height=1, fg_color="#1D2E47", corner_radius=0)
        self.sep.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 14))

        # Botões de navegação
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

        # Binding de hover apenas no frame raiz da sidebar.
        # O Tkinter propaga <Enter>/<Leave> do filho para o pai automaticamente
        # quando usamos bind_all — mas isso seria global. A melhor abordagem
        # sem binding recursivo é checar a posição do ponteiro periodicamente
        # ao entrar/sair, usando um único par de bindings no frame principal.
        self.bind("<Enter>", self._on_enter, add="+")
        self.bind("<Leave>", self._on_leave, add="+")

        # Vincula também no canvas interno do CTkFrame (necessário no CTk)
        if hasattr(self, "_canvas"):
            self._canvas.bind("<Enter>", self._on_enter, add="+")
            self._canvas.bind("<Leave>", self._on_leave, add="+")

        # Vincula nos filhos diretos apenas (não recursivo)
        self._bind_direct_children(self)

    def _bind_direct_children(self, widget):
        """Vincula <Enter>/<Leave> apenas nos filhos diretos — sem recursão profunda."""
        for child in widget.winfo_children():
            try:
                child.bind("<Enter>", self._on_enter, add="+")
                child.bind("<Leave>", self._on_leave, add="+")
            except Exception:
                pass
            # Um nível abaixo para capturar o canvas interno dos CTkButton
            for sub in child.winfo_children():
                try:
                    sub.bind("<Enter>", self._on_enter, add="+")
                    sub.bind("<Leave>", self._on_leave, add="+")
                except Exception:
                    pass

    # ------------------------------------------------------------------ #
    #  Criação dos botões                                                  #
    # ------------------------------------------------------------------ #

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
                btn.configure(fg_color=COLORS["primary"], text_color="#FFFFFF")
            else:
                btn.configure(fg_color="transparent", text_color=COLORS["sidebar_text"])

    # ------------------------------------------------------------------ #
    #  Animação suave de largura                                           #
    # ------------------------------------------------------------------ #

    def _animate_to(self, target: float):
        """Inicia (ou redireciona) a animação de largura para 'target' px."""
        # Cancela animação corrente se houver
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None

        self._target_width = target
        self._step_animation()

    def _step_animation(self):
        """Executa um passo da animação de interpolação linear."""
        diff = self._target_width - self._current_width
        if abs(diff) < 1.0:
            # Chegou ao destino
            self._current_width = self._target_width
            self.configure(width=int(self._current_width))
            # Atualiza a aparência SOMENTE quando terminar de animar
            if self._target_width == self.EXPANDED_WIDTH:
                self._apply_expanded_look()
            else:
                self._apply_collapsed_look()
            self._anim_job = None
            return

        # Move 1/ANIM_STEPS do caminho restante a cada frame (ease-out)
        step = diff / self.ANIM_STEPS
        self._current_width += step
        self.configure(width=int(self._current_width))
        self._anim_job = self.after(self.ANIM_STEP_MS, self._step_animation)

    # ------------------------------------------------------------------ #
    #  Aparência: expandido / recolhido                                   #
    # ------------------------------------------------------------------ #

    def _apply_expanded_look(self):
        """Atualiza textos e alinhamentos para o estado expandido."""
        self._is_expanded = True

        self.logo_frame.grid_configure(padx=18, pady=(20, 10))
        self.logo_title.pack_configure(anchor="w")
        self.logo_title.configure(text="🖥️  PDV Caixa", font=get_font("sidebar_title"))
        self.logo_subtitle.pack(anchor="w", pady=(2, 0))
        self.sep.grid_configure(padx=16)

        for item in self.NAV_ITEMS:
            btn = self._buttons[item["id"]]
            btn.grid_configure(padx=12)
            btn.configure(
                text=f"  {item['icon']}   {item['label']}",
                font=get_font("sidebar_item"),
                anchor="w",
            )

        self.footer_label.configure(text=f"PDV v{APP_VERSION}")

        # Vincula novos filhos que possam ter sido criados
        self._bind_direct_children(self)

    def _apply_collapsed_look(self):
        """Atualiza textos e alinhamentos para o estado recolhido."""
        self._is_expanded = False

        self.logo_frame.grid_configure(padx=6, pady=(16, 10))
        self.logo_title.pack_configure(anchor="center")
        self.logo_title.configure(text="🖥️", font=get_font("sidebar_title"))
        try:
            self.logo_subtitle.pack_forget()
        except Exception:
            pass
        self.sep.grid_configure(padx=10)

        for item in self.NAV_ITEMS:
            btn = self._buttons[item["id"]]
            btn.grid_configure(padx=8)
            btn.configure(
                text=item["icon"],
                font=ctk.CTkFont(family="Segoe UI Emoji", size=18),
                anchor="center",
            )

        self.footer_label.configure(text=f"v{APP_VERSION}")

    # ------------------------------------------------------------------ #
    #  Eventos de hover                                                    #
    # ------------------------------------------------------------------ #

    def _on_enter(self, event=None):
        """Mouse entrou na sidebar ou num filho."""
        # Cancela qualquer collapse agendado
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
            self._collapse_job = None

        if not self._is_expanded and self._target_width != self.EXPANDED_WIDTH:
            self._animate_to(self.EXPANDED_WIDTH)

    def _on_leave(self, event=None):
        """Mouse saiu de algum widget — aguarda um pouco antes de recolher."""
        if self._collapse_job:
            self.after_cancel(self._collapse_job)
        # Debounce de 80 ms para evitar flickering ao mover entre filhos
        self._collapse_job = self.after(80, self._check_and_collapse)

    def _check_and_collapse(self):
        """Verifica se o ponteiro realmente saiu da área da sidebar."""
        self._collapse_job = None
        try:
            x, y = self.winfo_pointerxy()
            sx  = self.winfo_rootx()
            sy  = self.winfo_rooty()
            sw  = self.winfo_width()
            sh  = self.winfo_height()
            inside = sx <= x <= sx + sw and sy <= y <= sy + sh
        except Exception:
            inside = False

        if not inside and self._target_width != self.COLLAPSED_WIDTH:
            self._animate_to(self.COLLAPSED_WIDTH)
