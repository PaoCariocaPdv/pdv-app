"""
PDV - Ponto de Venda
Componente: Diálogo de atualização disponível (Padronizado)
"""

import threading
import customtkinter as ctk
from config import COLORS
from fonts import get_font
from components.ui import PrimaryButton, SecondaryButton, StatusPill


class UpdateDialog(ctk.CTkToplevel):
    """Janela de notificação de nova versão disponível com o Design System oficial."""

    def __init__(self, parent, update_info: dict):
        super().__init__(parent)
        self.update_info = update_info
        self.title("Atualização Disponível")
        self.geometry("460x280")
        self.resizable(False, False)
        self.grab_set()  # Modal
        self._center(parent)
        self._build()

    def _center(self, parent):
        self.update_idletasks()
        px = parent.winfo_x() + parent.winfo_width() // 2 - 230
        py = parent.winfo_y() + parent.winfo_height() // 2 - 140
        self.geometry(f"+{px}+{py}")

    def _build(self):
        self.configure(fg_color=COLORS["card_bg"])

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=28, pady=24)

        # Header com Pill
        StatusPill(content, text="Nova Versão", status="info", icon="🔄").pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(
            content,
            text="Atualização Disponível!",
            font=get_font("subtitle"),
            text_color=COLORS["text_primary"],
        ).pack(anchor="w")

        ctk.CTkLabel(
            content,
            text=f"A versão v{self.update_info['version']} já está pronta para instalação.",
            font=get_font("body"),
            text_color=COLORS["text_secondary"],
        ).pack(anchor="w", pady=(4, 16))

        # Barra de progresso (oculta inicialmente)
        self.progress_bar = ctk.CTkProgressBar(
            content,
            width=400,
            progress_color=COLORS["primary"],
            fg_color=COLORS["selected_bg"],
        )
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(
            content,
            text="",
            font=get_font("caption"),
            text_color=COLORS["text_secondary"],
        )

        # Botões
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", pady=(12, 0))

        self.later_btn = SecondaryButton(
            btn_frame,
            text="Agora não",
            width=130,
            command=self.destroy,
        )
        self.later_btn.pack(side="right", padx=(10, 0))

        self.update_btn = PrimaryButton(
            btn_frame,
            text="Atualizar Agora",
            width=160,
            command=self._start_update,
        )
        self.update_btn.pack(side="right")

    def _start_update(self):
        """Inicia o download em background e mostra progresso."""
        self.later_btn.configure(state="disabled")
        self.update_btn.configure(state="disabled", text="Baixando...")

        self.status_label.pack(pady=(6, 2))
        self.progress_bar.pack(pady=(0, 8))
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        def _on_progress(percent):
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.stop()
            self.progress_bar.set(percent / 100)
            self.status_label.configure(text=f"Baixando nova versão... {percent}%")

        def _run():
            try:
                from updater import download_and_install
                download_and_install(
                    self.update_info["download_url"],
                    on_progress=lambda p: self.after(0, _on_progress, p),
                )
            except Exception as e:
                self.after(0, self._show_error, str(e))

        threading.Thread(target=_run, daemon=True).start()

    def _show_error(self, msg):
        self.progress_bar.stop()
        self.status_label.configure(
            text=f"Erro no download: {msg}", text_color=COLORS["status_danger"]
        )
        self.later_btn.configure(state="normal")
        self.update_btn.configure(state="normal", text="Tentar novamente")
