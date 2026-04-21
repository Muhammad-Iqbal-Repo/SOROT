# ui/report_renderer.py
import streamlit as st

from agent.schema import PersonProfile
from ui.components import badge, confidence_color, empty_state, section_header


def _render_header(profile: PersonProfile) -> None:
    """Name, aliases, and vital status."""
    st.markdown(f"## 👤 {profile.full_name}")

    if profile.also_known_as:
        st.caption(f"Alias: {', '.join(profile.also_known_as)}")

    if profile.is_alive is True:
        st.markdown(badge("✅ Masih Hidup", "#2e7d32"), unsafe_allow_html=True)
    elif profile.is_alive is False:
        st.markdown(badge("❌ Sudah Meninggal", "#c62828"), unsafe_allow_html=True)
        if profile.death_info:
            st.caption(profile.death_info)
    else:
        st.markdown(
            badge("❓ Status Tidak Diketahui", "#757575"), unsafe_allow_html=True
        )


def _render_classification_flags(profile: PersonProfile) -> None:
    """Active/inactive government classification badges."""
    section_header("🏛️", "Klasifikasi Pejabat")

    flags = {
        "Menteri": profile.is_minister,
        "Wakil Menteri": profile.is_deputy_minister,
        "Anggota DPR RI": profile.is_dpr_member,
        "Anggota DPRD": profile.is_dprd_member,
        "Staf Khusus": profile.is_staf_khusus,
        "Pejabat Tinggi Negara": profile.is_high_official,
    }
    badges_html = "".join(
        badge(label, "#1565c0" if active else "#bdbdbd")
        for label, active in flags.items()
    )
    st.markdown(badges_html, unsafe_allow_html=True)


def _render_roles_and_party(profile: PersonProfile) -> None:
    """Two-column layout: jabatan on the left, party on the right."""
    col_jabatan, col_partai = st.columns(2)

    with col_jabatan:
        section_header("💼", "Jabatan & Instansi")
        if profile.current_roles:
            st.markdown("**Saat Ini:**")
            for role in profile.current_roles:
                st.markdown(f"- {role}")
        if profile.past_roles:
            st.markdown("**Sebelumnya:**")
            for role in profile.past_roles:
                st.markdown(f"- {role}")
        if not profile.current_roles and not profile.past_roles:
            empty_state()

    with col_partai:
        section_header("🎯", "Afiliasi Partai Politik")
        if profile.party_affiliations:
            for party in profile.party_affiliations:
                st.markdown(f"- {party}")
            if profile.political_notes:
                st.caption(profile.political_notes)
        else:
            empty_state()


def _render_tni_and_corporate(profile: PersonProfile) -> None:
    """Two-column layout: TNI/Polri on the left, corporate links on the right."""
    col_tni, col_corp = st.columns(2)

    with col_tni:
        section_header("🎖️", "Status TNI / POLRI")
        t = profile.tni_polri
        if t.is_tni_polri:
            st.markdown(f"- **Kesatuan:** {t.branch or '-'}")
            st.markdown(f"- **Pangkat Terakhir:** {t.last_rank or '-'}")
            status_color = "#1b5e20" if t.status == "Aktif" else "#e65100"
            st.markdown(
                badge(t.status or "Unknown", status_color), unsafe_allow_html=True
            )
        else:
            empty_state("Bukan TNI/Polri atau tidak ditemukan")

    with col_corp:
        section_header("🏢", "Afiliasi Grup Usaha")
        if profile.corporate_affiliations:
            for corp in profile.corporate_affiliations:
                st.markdown(f"**{corp.entity_name}**")
                if corp.role:
                    st.caption(f"Jabatan: {corp.role}")
                if corp.group:
                    st.caption(f"Grup: {corp.group}")
        else:
            empty_state()


def _render_family(profile: PersonProfile) -> None:
    """Family members in a responsive column grid (max 3 columns)."""
    section_header("👨‍👩‍👧", "Relasi Keluarga")

    if not profile.family_members:
        empty_state()
        return

    num_cols = min(len(profile.family_members), 3)
    cols = st.columns(num_cols)
    for i, member in enumerate(profile.family_members):
        with cols[i % num_cols]:
            st.markdown(f"**{member.name}**")
            st.caption(f"Hubungan: {member.relation}")
            if member.role:
                st.caption(f"Peran: {member.role}")
            if member.notes:
                st.caption(member.notes)


def _render_footer(profile: PersonProfile) -> None:
    """Confidence badge, analyst notes, and collapsible sources list."""
    color = confidence_color(profile.confidence_level)
    st.markdown(
        f"**Tingkat Kepercayaan Data:** "
        f"{badge(profile.confidence_level.upper(), color)}",
        unsafe_allow_html=True,
    )

    if profile.analyst_notes:
        st.info(f"📝 **Catatan Analis:** {profile.analyst_notes}")

    with st.expander("📎 Sumber Data"):
        if profile.sources:
            for src in profile.sources:
                st.markdown(f"- [{src}]({src})")
        else:
            empty_state("Tidak ada sumber yang dicatat")


def render_profile(profile: PersonProfile) -> None:
    """
    Main entry point — renders a complete PersonProfile as a Streamlit report.

    Sections rendered (in order):
      1. Header (name, alias, vital status)
      2. Classification flags (Menteri, DPR, etc.)
      3. Jabatan & Instansi / Partai Politik
      4. TNI/Polri / Grup Usaha
      5. Relasi Keluarga
      6. Confidence level, analyst notes, sources
    """
    _render_header(profile)
    st.divider()
    _render_classification_flags(profile)
    st.divider()
    _render_roles_and_party(profile)
    st.divider()
    _render_tni_and_corporate(profile)
    st.divider()
    _render_family(profile)
    st.divider()
    _render_footer(profile)
