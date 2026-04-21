# app.py
import streamlit as st
from dotenv import load_dotenv

from config import APP_ICON, APP_NAME, APP_SUBTITLE, AppConfig, RESEARCH_DIMENSIONS
from agent.orchestrator import PersonIntelAgent
from ui.report_renderer import render_profile
from utils.cache import cache_profile, clear_cache, get_cached_profile

load_dotenv()

cfg = AppConfig()
st.set_page_config(
    page_title=cfg.page_title,
    page_icon=cfg.page_icon,
    layout=cfg.layout,
)


def _sidebar() -> list[str]:
    """
    Renders the sidebar with dimension checkboxes and cache controls.

    Returns:
        List of selected dimension keys to pass to the agent.
    """
    with st.sidebar:
        st.markdown(f"# {APP_ICON} {APP_NAME}")
        st.caption(APP_SUBTITLE)
        st.divider()

        st.subheader("🗂️ Pilih Informasi yang Dicari")
        st.caption("Centang kategori yang ingin ditampilkan dalam profil.")

        selected_keys: list[str] = []
        for key, (label, _) in RESEARCH_DIMENSIONS.items():
            checked = st.checkbox(label, value=True, key=f"dim_{key}")
            if checked:
                selected_keys.append(key)

        st.divider()
        if st.button("🗑️ Hapus Cache Sesi", use_container_width=True):
            clear_cache()
            st.success("Cache berhasil dihapus.")

        st.divider()
        st.caption("© Muhammad Iqbal 2026")

    return selected_keys


def _run_search(name: str, selected_keys: list[str]) -> None:
    """Checks cache, runs the agent if needed, then renders the result."""
    if not selected_keys:
        st.warning("⚠️ Pilih minimal satu kategori informasi di sidebar sebelum mencari.")
        return

    # Build a cache key that includes which dimensions were selected
    cache_key = f"{name}|{'_'.join(sorted(selected_keys))}"
    cached = get_cached_profile(cache_key)
    if cached:
        st.success("✅ Hasil dari cache sesi ini")
        render_profile(cached)
        return

    progress_bar = st.progress(0)
    status_text = st.empty()

    def update_progress(step: str, pct: float) -> None:
        progress_bar.progress(pct)
        status_text.text(step)

    try:
        agent = PersonIntelAgent()
        profile, raw_json = agent.run(
            name,
            selected_keys=selected_keys,
            progress_callback=update_progress,
        )

        progress_bar.progress(1.0)
        status_text.empty()

        if profile:
            cache_profile(cache_key, profile)
            render_profile(profile)
            with st.expander("🔧 Raw JSON Output"):
                st.code(raw_json, language="json")
        else:
            st.error(
                "Gemini mengembalikan respons yang tidak dapat diparsing. "
                "Coba lagi atau periksa nama yang dimasukkan."
            )
            with st.expander("Raw Output"):
                st.code(raw_json)

    except EnvironmentError as exc:
        st.error(f"Konfigurasi error: {exc}")
    except Exception as exc:
        st.error(f"Terjadi kesalahan tak terduga: {exc}")
        raise


def main() -> None:
    selected_keys = _sidebar()

    # ── Hero header ───────────────────────────────────────────────────────────
    st.markdown(
        f"<h1 style='font-size:2.8rem;margin-bottom:0'>{APP_ICON} {APP_NAME}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='font-size:1rem;color:gray;margin-top:4px'>{APP_SUBTITLE}</p>",
        unsafe_allow_html=True,
    )
    st.caption(
        "Telusuri profil publik tokoh Indonesia — jabatan, afiliasi partai, "
        "keluarga, TNI/Polri, dan grup usaha — dalam satu laporan terstruktur."
    )
    st.divider()

    # ── Search form ───────────────────────────────────────────────────────────
    with st.form("search_form"):
        name = st.text_input(
            "🔎 Nama lengkap tokoh:",
            placeholder="Contoh: Prabowo Subianto",
        )
        submitted = st.form_submit_button(
            f"{APP_ICON} Sorot Tokoh Ini", use_container_width=True
        )

    if not submitted or not name.strip():
        st.info("💡 Masukkan nama lengkap lalu klik **Sorot Tokoh Ini**.")
        return

    _run_search(name.strip(), selected_keys)


if __name__ == "__main__":
    main()
