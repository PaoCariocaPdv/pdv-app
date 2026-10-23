"""
PDV - Ponto de Venda
Gerador e garantidor de ícones PNG em alta definição para a barra lateral
"""

import os
import math
from PIL import Image, ImageDraw


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
