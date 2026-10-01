import streamlit as st

def subject_card(name, code, section, stats, footer_callback=None,action_type='share'):
    """
    Renders a styled subject card with metric tracking blocks and a built-in share button.
    """
    # 1. Card Container outline
    with st.container(border=True):
        
        # Header Area
        c1, c2 = st.columns([3, 1])
        with c1:
            st.subheader(f"📚 {name}")
            st.caption(f"**Code:** {code} | **Section:** {section}")
        with c2:
            # Displays a subtle status tag in the top right corner
            st.html("<span style='color: gray; font-size: 0.85rem; float: right;'>Active</span>")
            
        st.divider()
        
        # 2. Dynamic Metric Stats Layout Row
        if stats:
            stat_cols = st.columns(len(stats))
            for col, (emoji, label, value) in zip(stat_cols, stats):
                with col:
                    st.metric(label=f"{emoji} {label}", value=value)
                    
        st.divider()
        
        # Render button based on action_type
        if footer_callback:
            if action_type == 'unenroll':
                # Dynamically renders the Unenroll button with a unique key
                if st.button('Unenroll from this course', key=f"unenroll_{code}", type='tertiary', use_container_width=True):
                    footer_callback()
            else:
                # Default fallback fallback to original Share button behavior
                st.button(f"Share Code: {code}", key=f"share_{code}", icon=":material/share:", use_container_width=True)
                    # footer_callback(name, code)
