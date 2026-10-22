"""
PDV - Ponto de Venda
Componente: Diálogo de atualização disponível
"""

import threading
import customtkinter as ctk
from config import COLORS


class UpdateDialog(ctk.CTkToplevel):
    """Janela de notificação de nova versão disponível."""

    def __init__(self, parent, update_info: dict):
        super().__init__(parent)
        self.update_info = update_info
        self.title("Atualização Disponível")
        self.geometry("420x260")
        self.resizable(False, False)
        self.grab_set()  # Modal
        self._center(parent)
        self._build()

    def _center(self, parent):
        self.update_idletasks()
        px = parent.winfo_x() + parent.winfo_width() // 2 - 210
        py = parent.winfo_y() + parent.winfo_height() // 2 - 130
        self.geometry(f"+{px}+{py}")

    def _build(self):
        self.configure(fg_color=COLORS["bg_primary"])

        # Ícone + título
        ctk.CTkLabel(
            self, text="🔄", font=ctk.CTkFont(size=40)
        ).pack(pady=(24, 4))

        ctk.CTkLabel(
            self,
            text="Atualização Disponível!",
            font=ctk.CTkFont("Inter", 18, "bold"),
            text_color=COLORS["text_primary"],
        ).pack()

        ctk.CTkLabel(
            self,
            text=f"Nova versão: v{self.update_info['version']}",
            font=ctk.CTkFont("Inter", 13),
            text_color=COLORS["accent"],
        ).pack(pady=(4, 16))

        # Barra de progresso (oculta inicialmente)
        self.progress_bar = ctk.CTkProgressBar(self, width=340)
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont("Inter", 11),
            text_color=COLORS["text_secondary"],
        )

        # Botões
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=4)

        self.later_btn = ctk.CTkButton(
            btn_frame,
            text="Agora não",
            width=140,
            height=38,
            fg_color=COLORS["bg_secondary"],
            hover_color=COLORS["border"],
            text_color=COLORS["text_primary"],
            font=ctk.CTkFont("Inter", 13),
            command=self.destroy,
        )
        self.later_btn.grid(row=0, column=0, padx=8)

        self.update_btn = ctk.CTkButton(
            btn_frame,
            text="✅  Atualizar agora",
            width=160,
            height=38,
            fg_color=COLORS["accent"],
            hover_color=COLORS["accent_hover"],
            font=ctk.CTkFont("Inter", 13, "bold"),
            command=self._start_update,
        )
        self.update_btn.grid(row=0, column=1, padx=8)

    def _start_update(self):
        """Inicia o download em background e mostra progresso."""
        self.later_btn.configure(state="disabled")
        self.update_btn.configure(state="disabled", text="Baixando...")

        self.status_label.pack(pady=(8, 2))
        self.progress_bar.pack(pady=(0, 8))
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        def _on_progress(percent):
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.stop()
            self.progress_bar.set(percent / 100)
            self.status_label.configure(text=f"Baixando... {percent}%")

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
            text=f"❌ Erro: {msg}", text_color=COLORS["danger"]
        )
        self.later_btn.configure(state="normal")
        self.update_btn.configure(state="normal", text="Tentar novamente")
