"""
PDV - Ponto de Venda
Arquivo principal — ponto de entrada do aplicativo
"""

import customtkinter as ctk
from config import APP_NAME, APP_WIDTH, APP_HEIGHT, APP_MIN_WIDTH, APP_MIN_HEIGHT, COLORS
from database import initialize_firebase
from components.sidebar import Sidebar
from components.update_dialog import UpdateDialog
from pages.home import HomePage
from pages.placeholder import PlaceholderPage
from updater import check_update_async


class PDVApp(ctk.CTk):
    """Janela principal do aplicativo PDV."""

    def __init__(self):
        super().__init__()

        # Configuração da janela
        self.title(APP_NAME)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(APP_MIN_WIDTH, APP_MIN_HEIGHT)
        self.configure(fg_color=COLORS["bg_primary"])

        # Centraliza a janela na tela
        self._center_window()

        # Inicializa o Firebase em segundo plano
        initialize_firebase()

        # Monta o layout
        self._build_layout()

        # Navega para a página inicial
        self.navigate("home")

        # Verifica atualização em background (3s após abrir)
        self.after(3000, self._check_for_updates)

    def _center_window(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - APP_WIDTH) // 2
        y = (sh - APP_HEIGHT) // 2
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}+{x}+{y}")

    def _build_layout(self):
        """Monta o layout principal: sidebar à esquerda + área de conteúdo."""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self, navigate_callback=self.navigate)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Área de conteúdo
        self.content_area = ctk.CTkFrame(
            self,
            fg_color=COLORS["bg_primary"],
            corner_radius=0,
        )
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        # Mapa de páginas
        self._pages: dict[str, ctk.CTkFrame] = {}
        self._current_page = None

    def _get_page(self, page_id: str) -> ctk.CTkFrame:
        """Retorna ou cria a página solicitada (lazy loading)."""
        if page_id not in self._pages:
            page = self._create_page(page_id)
            page.grid(row=0, column=0, sticky="nsew", in_=self.content_area)
            self._pages[page_id] = page
        return self._pages[page_id]

    def _create_page(self, page_id: str) -> ctk.CTkFrame:
        """Instancia a página correta pelo ID."""
        titles = {
            "caixa":    "Caixa / PDV",
            "produtos": "Produtos",
            "vendas":   "Vendas",
            "clientes": "Clientes",
            "relatorio":"Relatórios",
            "config":   "Configurações",
        }
        if page_id == "home":
            return HomePage(self.content_area)
        return PlaceholderPage(self.content_area, title=titles.get(page_id, page_id.capitalize()))

    def navigate(self, page_id: str):
        """Navega para a página indicada."""
        # Esconde página atual
        if self._current_page:
            self._current_page.grid_remove()

        # Exibe a nova página
        page = self._get_page(page_id)
        page.grid()
        self._current_page = page

        # Atualiza o estado ativo na sidebar
        self.sidebar.set_active(page_id)

    def _check_for_updates(self):
        """Verifica atualizações em background sem travar a UI."""
        def _on_result(update_info):
            if update_info:
                self.after(0, lambda: UpdateDialog(self, update_info))
        check_update_async(_on_result)


def main():
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = PDVApp()
    app.mainloop()


if __name__ == "__main__":
    main()
