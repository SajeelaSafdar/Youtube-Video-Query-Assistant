import streamlit as st
import re
import time
from chatbot import load_transcript, get_response

st.set_page_config(
    page_title="YouTube Video Query Assistant",
    page_icon="🎥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 300;
    }

    .step-header {
        color: #2c3e50;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-left: 0.5rem;
        border-left: 4px solid #ff4b4b;
    }

    .video-info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }

    .video-id {
        font-family: 'Courier New', monospace;
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        letter-spacing: 1px;
    }

    .stButton > button {
        background: linear-gradient(135deg, #ff4b4b, #e63946) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #e63946, #dc2626) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(255, 75, 75, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(-1px) !important;
    }

    .response-container {
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border: 1px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-top: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }

    .success-badge {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }

    .error-badge {
        background: linear-gradient(135deg, #dc3545, #c82333);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }

    .query-section {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 1.5rem 0;
        border: 1px solid #e9ecef;
    }

    .divider {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ff4b4b, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)
def validate_youtube_url(url):
    youtube_patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/shorts/([a-zA-Z0-9_-]+)'
    ]

    for pattern in youtube_patterns:
        if re.search(pattern, url.strip()):
            return True
    return False


def extract_video_id(url):
    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be/)([0-9A-Za-z_-]{11})',
        r'(?:shorts/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def process_video_query(video_id, query):
    time.sleep(1)
    response = f"""Based on your query about the YouTube video (ID: {video_id}):

Query: "{query}"

Analysis Results:
✅ Video successfully identified and processed
🔍 Query analyzed and understood
📊 Processing completed at {time.strftime('%Y-%m-%d %H:%M:%S')}

Sample Response:
This is where your actual video analysis response would appear. You can integrate this with:
• Video transcript extraction APIs
• AI-powered content analysis
• Video metadata processing
• Custom analytics or insights

Replace the process_video_query() function with your specific logic for handling user queries about YouTube videos.

Video Information:
- Video ID: {video_id}
- Processing Status: Complete
- Query Type: General inquiry
"""

    return response.strip()

if 'video_validated' not in st.session_state:
    st.session_state.video_validated = False
if 'video_id' not in st.session_state:
    st.session_state.video_id = None
if 'video_url' not in st.session_state:
    st.session_state.video_url = ""


def main():
    # Header
    st.markdown('<h1 class="main-header">YouTube Video Query Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Analyze YouTube videos with intelligent queries</p>', unsafe_allow_html=True)

    # Step 1: Video URL Input and Validation
    st.markdown('<h3 class="step-header">📹 Step 1: Enter YouTube Video URL</h3>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        video_url = st.text_input(
            "YouTube Video URL",
            value=st.session_state.video_url,
            placeholder="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            help="Enter a valid YouTube video URL",
            label_visibility="collapsed"
        )

    with col2:
        validate_button = st.button("Validate", use_container_width=True)

    # Handle URL validation
    if validate_button:
        if not video_url:
            st.markdown('<div class="error-badge">Please enter a URL</div>', unsafe_allow_html=True)
        elif not validate_youtube_url(video_url):
            st.markdown('<div class="error-badge">Invalid YouTube URL</div>', unsafe_allow_html=True)
            st.session_state.video_validated = False
        else:
            video_id = extract_video_id(video_url)
            transcript = load_transcript(video_id)
            st.session_state.video_id = video_id
            st.session_state.video_url = video_url
            st.session_state.transcript = transcript
            st.session_state.video_validated = True

    # Show video information if validated
    if st.session_state.video_validated and st.session_state.video_id:
        st.markdown('<div class="success-badge">Valid YouTube URL detected!</div>', unsafe_allow_html=True)

        st.markdown(f'''
        <div class="video-info-card">
            <h4 style="margin-top: 0;">🎬 Video Information</h4>
            <p><strong>Video ID:</strong> <span class="video-id">{st.session_state.video_id}</span></p>
            <p><strong>URL:</strong> {st.session_state.video_url}</p>
        </div>
        ''', unsafe_allow_html=True)



        # Step 2: Query Input
        st.markdown('<div class="query-section">', unsafe_allow_html=True)
        st.markdown('<h3 class="step-header">💭 Step 2: Ask Your Question</h3>', unsafe_allow_html=True)

        user_query = st.text_area(
            "Your Query",
            placeholder="What is this video about?",
            height=120,
            help="Enter your question or query about the video",
            label_visibility="collapsed"
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            query_button = st.button("Get Answer", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Handle query processing
        if query_button:
            if not user_query.strip():
                st.markdown('<div class="error-badge">Please enter a query</div>', unsafe_allow_html=True)
            else:
                # Show processing animation
                with st.spinner('🤖 Processing your query...'):
                    try:

                        response = get_response(st.session_state.transcript, user_query)

                        # Display response
                        st.markdown("### 🎯 Query Response")
                        st.markdown('<div class="response-container">', unsafe_allow_html=True)
                        st.text_area(
                            "Answer",
                            value=response,
                            height=200,
                            label_visibility="collapsed",
                            help="AI-generated response based on your query"
                        )
                        st.markdown('</div>', unsafe_allow_html=True)

                        # Option to ask another question
                        st.markdown("---")
                        if st.button("🔄 Ask Another Question"):
                            st.rerun()

                    except Exception as e:
                        st.markdown(f'<div class="error-badge">❌ Error processing query: {str(e)}</div>',
                                    unsafe_allow_html=True)

    elif not st.session_state.video_validated:
        # Show placeholder for query section
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown('<div class="query-section" style="opacity: 0.5;">', unsafe_allow_html=True)
        st.markdown('<h3 class="step-header">💭 Step 2: Ask Your Question</h3>', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align: center; color: #999; font-style: italic;">Please validate a YouTube URL first to proceed</p>',
            unsafe_allow_html=True)
        st.text_area(
            "Your Query",
            placeholder="Enter your question about the video...",
            height=120,
            disabled=True,
            label_visibility="collapsed"
        )
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("Get Answer", disabled=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown('''
    <div style="text-align: center; padding: 2rem 0;">
        <p style="color: #666; font-size: 0.9rem; margin-bottom: 0.5rem;">
            🔧 Built with Streamlit • Replace processing functions with your custom logic
        </p>
        <p style="color: #999; font-size: 0.8rem;">
            Supports all YouTube URL formats: youtube.com, youtu.be, shorts, embed
        </p>
    </div>
    ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()