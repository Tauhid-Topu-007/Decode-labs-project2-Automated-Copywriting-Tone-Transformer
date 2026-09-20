import streamlit as st
from models import CopyRequest, GeneratedCopy, Platform, Tone
from provider import generate_copy

# ──────────────────────────────────────────────
# Page config
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Copywriting & Tone Transformer",
    page_icon="✍️",
    layout="wide",
)

st.title("✍️ Automated Copywriting & Tone Transformer")
st.caption("Powered by Groq · DecodeLabs Project 2")


# ──────────────────────────────────────────────
# Session State — persist generated copy across reruns
# ──────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "result_meta" not in st.session_state:
    st.session_state.result_meta = None


# ──────────────────────────────────────────────
# Secrets helper — reads st.secrets safely
# ──────────────────────────────────────────────
def get_secret(key: str) -> str | None:
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        return None


GROQ_KEY = get_secret("GROQ_API_KEY")


# ──────────────────────────────────────────────
# Sidebar — Configuration
# ──────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuration")

    if not GROQ_KEY:
        st.error("No API key configured. Add `GROQ_API_KEY` to secrets.")
        st.stop()

    provider = "groq"
    st.success("Groq API connected")

    st.divider()
    st.markdown("**Platform limits enforced:**")
    st.markdown("- Twitter / X: 280 chars, 3 hashtags")
    st.markdown("- Instagram: 2,200 chars, 8 hashtags")
    st.markdown("- LinkedIn: 3,000 chars, 5 hashtags")
    st.markdown("- Email: 5,000 chars, 0 hashtags")

    st.divider()
    st.markdown("**Groq free tier:**")
    st.markdown("- 14,400 requests/day")
    st.markdown("- 6,000 tokens/minute")
    st.markdown("- Ultra-low latency inference [citation:6]")


# ──────────────────────────────────────────────
# Input Form
# ──────────────────────────────────────────────
with st.form("copy_form"):
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        product_name = st.text_input(
            "Product Name",
            placeholder="e.g., ErgoDesk Pro Standing Desk",
        )
    with col2:
        platform = st.selectbox("Platform", options=list(Platform.__args__))
    with col3:
        tone = st.selectbox("Tone", options=list(Tone.__args__))

    raw_description = st.text_area(
        "Raw Product Description",
        placeholder="Describe the product in plain, factual language...",
        height=120,
    )

    submitted = st.form_submit_button("🚀 Generate Copy", use_container_width=True)


# ──────────────────────────────────────────────
# Generation
# ──────────────────────────────────────────────
if submitted:
    if not product_name or not raw_description:
        st.warning("Please fill in both Product Name and Description.")
    else:
        req = CopyRequest(
            product_name=product_name,
            platform=platform,
            tone=tone,
            raw_description=raw_description,
        )

        with st.spinner("Generating with Groq..."):
            try:
                result = generate_copy(req, provider, GROQ_KEY)
                st.session_state.result = result
                st.session_state.result_meta = {
                    "provider": provider,
                    "platform": platform,
                    "tone": tone,
                }
            except Exception as e:
                st.error(f"Generation failed: {e}")
                st.session_state.result = None


# ──────────────────────────────────────────────
# Output Display
# ──────────────────────────────────────────────
if st.session_state.result:
    result: GeneratedCopy = st.session_state.result
    meta = st.session_state.result_meta

    st.divider()
    st.subheader("📝 Generated Copy")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Provider", meta["provider"].upper())
    col_b.metric("Platform", meta["platform"])
    col_c.metric("Tone", meta["tone"])

    with st.container(border=True):
        st.markdown(f"### {result.headline}")
        st.markdown(result.body)
        st.markdown(f"**{result.call_to_action}**")
        if result.hashtags:
            st.markdown(" ".join(f"`{tag}`" for tag in result.hashtags))

    st.caption(f"Character count: {result.character_count}")

    # Raw JSON for debugging
    with st.expander("🔍 Raw Structured Output (JSON)"):
        st.json(result.model_dump())

    # Download button
    st.download_button(
        label="⬇️ Download as JSON",
        data=result.model_dump_json(indent=2),
        file_name=f"copy_{meta['platform'].lower()}_{meta['tone']}.json",
        mime="application/json",
    )