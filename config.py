# config.py
from dataclasses import dataclass, field

GEMINI_MODEL = "gemini-2.5-flash-lite"

APP_NAME = "SOROT"
APP_SUBTITLE = "Sistem Observasi & Riset Online Tokoh"
APP_ICON = "🔦"

# Research dimensions as an ordered dict: key -> (label, prompt_text)
# key        : used internally & as checkbox state key
# label      : shown in the UI checkbox
# prompt_text: injected into the Gemini prompt when selected
RESEARCH_DIMENSIONS: dict[str, tuple[str, str]] = {
    "jabatan": (
        "💼 Jabatan & Instansi",
        "jabatan dan instansi tempat bekerja, saat ini maupun masa lalu",
    ),
    "partai": (
        "🎯 Afiliasi Partai Politik",
        "afiliasi dan keanggotaan partai politik",
    ),
    "keluarga": (
        "👨‍👩‍👧 Relasi Keluarga",
        "relasi dan anggota keluarga beserta peran publik mereka",
    ),
    "jabatan_khusus": (
        "🏛️ Klasifikasi Pejabat (Menteri / DPR / Staf Khusus)",
        "status sebagai Menteri, Wakil Menteri, Staf Khusus, Anggota DPR/DPRD/DPD",
    ),
    "tni_polri": (
        "🎖️ Status TNI / POLRI",
        "status TNI atau POLRI (aktif atau purnawirawan) beserta pangkat terakhir",
    ),
    "usaha": (
        "🏢 Afiliasi Grup Usaha",
        "afiliasi grup usaha dan perusahaan sebagai komisaris, direktur, atau pemegang saham",
    ),
    "status_hidup": (
        "❤️ Status Hidup / Meninggal",
        "apakah masih hidup atau sudah meninggal dunia",
    ),
}


@dataclass
class AppConfig:
    page_title: str = f"{APP_NAME} — {APP_SUBTITLE}"
    page_icon: str = APP_ICON
    layout: str = "wide"
