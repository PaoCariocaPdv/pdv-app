"""
PDV - Ponto de Venda
Componente: Barra lateral de navegação retrátil (Overlay Drawer)
- Ícones matematicamente alinhados em coluna com imagens ultra-nítidas
- Cores padronizadas (#0B1B33, #1D4ED8, #B8C4DA)
- Abre e fecha suavemente ao passar o mouse (hover) sem flicker
"""

import os
import sys
import math
import customtkinter as ctk
from PIL import Image, ImageDraw
from config import COLORS, APP_VERSION
from fonts import get_font


def ensure_sidebar_icons(icons_dir: str):
    """Garante que todos os ícones PNG existam em alta definição."""
    os.makedirs(icons_dir, exist_ok=True)
    required = ["logo", "home", "caixa", "produtos", "vendas", "clientes", "relatorio", "config"]
    missing = False
    for k in required:
        if not os.path.exists(os.path.join(icons_dir, f"{k}_default.png")) or \
           not os.path.exists(os.path.join(icons_dir, f"{k}_active.png")):
            missing = True
            break

    if not missing:
        return

    palette = {
        "default": (184, 196, 218, 255),  # #B8C4DA
        "active": (255, 255, 255, 255),   # #FFFFFF
    }

    for cname, color in palette.items():
        # 1. Logo (Monitor / Terminal)
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([20, 24, 108, 84], radius=10, outline=color, width=8)
        d.line([64, 84, 64, 100], fill=color, width=8)
        d.line([42, 100, 86, 100], fill=color, width=8)
        im.resize((48, 48), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, f"logo_{cname}.png"))

        # 2. Home (Início)
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.line([(22, 56), (64, 22), (106, 56)], fill=color, width=8, joint="curve")
        d.line([(32, 54), (32, 104), (96, 104), (96, 54)], fill=color, width=8, joint="curve")
        d.line([(52, 104), (52, 74), (76, 74), (76, 104)], fill=color, width=8, joint="curve")
        im.resize((48, 48), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, f"home_{cname}.png"))

        # 3. Caixa (Carrinho PDV)
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.line([(20, 28), (34, 28), (48, 76), (100, 76)], fill=color, width=8, joint="curve")
        d.line([(36, 42), (108, 42), (100, 76)], fill=color, width=8, joint="curve")
        d.ellipse([48, 88, 64, 104], fill=color)
        d.ellipse([86, 88, 102, 104], fill=color)
        im.resize((48, 48), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, f"caixa_{cname}.png"))

        # 4. Produtos (Caixa 3D)
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.polygon([(64, 22), (106, 44), (64, 66), (22, 44)], outline=color, width=8)
        d.line([(22, 44), (22, 84), (64, 106), (106, 84), (106, 44)], fill=color, width=8, joint="curve")
        d.line([(64, 66), (64, 106)], fill=color, width=8)
        im.resize((48, 48), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, f"produtos_{cname}.png"))

        # 5. Vendas (Gráfico de Barras)
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([24, 70, 44, 104], radius=4, fill=color)
        d.rounded_rectangle([54, 48, 74, 104], radius=4, fill=color)
        d.rounded_rectangle([84, 26, 104, 104], radius=4, fill=color)
        im.resize((48, 48), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, f"vendas_{cname}.png"))

        # 6. Clientes (Usuário)
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.ellipse([46, 22, 82, 58], outline=color, width=8)
        d.arc([22, 70, 106, 130], 180, 0, fill=color, width=8)
        im.resize((48, 48), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, f"clientes_{cname}.png"))

        # 7. Relatório (Prancheta)
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([26, 32, 102, 106], radius=10, outline=color, width=8)
        d.rounded_rectangle([44, 20, 84, 38], radius=6, fill=color)
        d.line([(42, 54), (86, 54)], fill=color, width=7)
        d.line([(42, 70), (86, 70)], fill=color, width=7)
        d.line([(42, 86), (72, 86)], fill=color, width=7)
        im.resize((48, 48), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, f"relatorio_{cname}.png"))

        # 8. Configurações (Engrenagem)
        im = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy, r_out, r_in = 64, 64, 40, 22
        for angle in range(0, 360, 45):
            rad = math.radians(angle)
            x1 = cx + (r_out - 6) * math.cos(rad)
            y1 = cy + (r_out - 6) * math.sin(rad)
            x2 = cx + (r_out + 10) * math.cos(rad)
            y2 = cy + (r_out + 10) * math.sin(rad)
            d.line([(x1, y1), (x2, y2)], fill=color, width=12)
        d.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out], outline=color, width=8)
        d.ellipse([cx - r_in, cy - r_in, cx + r_in, cy + r_in], outline=color, width=8)
        im.resize((48, 48), Image.Resampling.LANCZOS).save(os.path.join(icons_dir, f"config_{cname}.png"))


class Sidebar(ctk.CTkFrame):
    """
    Barra lateral moderna com alinhamento perfeito de ícones e expansão suave.
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

        self._btns_col: dict[str, ctk.CTkButton] = {}
        self._btns_exp: dict[str, ctk.CTkButton] = {}
        self._icons = {}

        self._load_icons()
        self.grid_propagate(False)
        self._build_subframes()
        self.after(50, self._setup_mouse_tracking)

    def _load_icons(self):
        if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icons_dir = os.path.join(base_dir, "assets", "icons")
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

    # ------------------------------------------------------------------ #
    #  Construção das interfaces pré-renderizadas                         #
    # ------------------------------------------------------------------ #

    def _build_subframes(self):
        # 1. Painel Recolhido (Largura fixa 70px, botões de 54px centralizados com padx=8)
        self.frame_col = ctk.CTkFrame(
            self,
            width=self.COLLAPSED_WIDTH,
            fg_color=COLORS["sidebar_bg"],
            corner_radius=0,
        )
        self.frame_col.place(x=0, y=0, relheight=1.0)
        self.frame_col.grid_propagate(False)
        self.frame_col.grid_columnconfigure(0, weight=1)

        # Logo perfeitamente alinhado na mesma coluna
        logo_col = ctk.CTkLabel(
            self.frame_col,
            text="",
            image=self._icons["logo"]["active"],
            width=54,
            height=44,
        )
        logo_col.grid(row=0, column=0, padx=8, pady=(20, 10))

        sep_col = ctk.CTkFrame(self.frame_col, height=1, fg_color="#1D2E47", corner_radius=0)
        sep_col.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 14))

        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self.frame_col,
                text="",
                image=self._icons[item["id"]]["default"],
                anchor="center",
                width=54,
                height=44,
                corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, padx=8, pady=3)
            self._btns_col[item["id"]] = btn

        footer_col = ctk.CTkLabel(
            self.frame_col,
            text=f"v{APP_VERSION}",
            font=get_font("small"),
            text_color="#627594",
        )
        footer_col.grid(row=100, column=0, sticky="s", pady=16)
        self.frame_col.grid_rowconfigure(len(self.NAV_ITEMS) + 2, weight=1)

        # 2. Painel Expandido (Ícone alinhado + texto legível)
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
        logo_exp.grid(row=0, column=0, sticky="ew", padx=8, pady=(20, 10))

        header_row = ctk.CTkFrame(logo_exp, fg_color="transparent")
        header_row.pack(fill="x")

        ctk.CTkLabel(
            header_row,
            text="",
            image=self._icons["logo"]["active"],
            width=36,
            height=36,
        ).pack(side="left", padx=(10, 10))

        text_col = ctk.CTkFrame(header_row, fg_color="transparent")
        text_col.pack(side="left", fill="both")

        ctk.CTkLabel(
            text_col,
            text="PDV Caixa",
            font=get_font("sidebar_title"),
            text_color="#FFFFFF",
        ).pack(anchor="w")

        ctk.CTkLabel(
            text_col,
            text="Sistema de Ponto de Venda",
            font=get_font("small"),
            text_color=COLORS["sidebar_text"],
        ).pack(anchor="w", pady=(1, 0))

        sep_exp = ctk.CTkFrame(self.frame_exp, height=1, fg_color="#1D2E47", corner_radius=0)
        sep_exp.grid(row=1, column=0, sticky="ew", padx=12, pady=(6, 14))

        for i, item in enumerate(self.NAV_ITEMS):
            btn = ctk.CTkButton(
                self.frame_exp,
                text=f"   {item['label']}",
                image=self._icons[item["id"]]["default"],
                compound="left",
                anchor="w",
                height=44,
                corner_radius=10,
                fg_color="transparent",
                hover_color=COLORS["sidebar_active"],
                text_color=COLORS["sidebar_text"],
                font=get_font("sidebar_item"),
                command=lambda p=item["id"]: self._on_click(p),
            )
            btn.grid(row=i + 2, column=0, sticky="ew", padx=8, pady=3)
            self._btns_exp[item["id"]] = btn

        footer_exp = ctk.CTkLabel(
            self.frame_exp,
            text=f"PDV v{APP_VERSION}",
            font=get_font("small"),
            text_color="#627594",
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
            icon_type = "active" if active else "default"

            self._btns_col[pid].configure(
                fg_color=c,
                image=self._icons[pid][icon_type],
            )
            self._btns_exp[pid].configure(
                fg_color=c,
                text_color=t,
                image=self._icons[pid][icon_type],
            )
