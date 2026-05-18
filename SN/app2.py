import streamlit as st
import streamlit.components.v1 as components
import time
import os
import base64

# --- CẤU HÌNH TRANG WEB TỐI ƯU MOBILE ---
st.set_page_config(
    page_title="Chúc Mừng Sinh Nhật Hà Anh 🎉",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- THIẾT KẾ GIAO DIỆN (CSS) TÔNG HỒNG PASTEL NHẸ NHÀNG ---
st.markdown("""
    <style>
        /* Tối ưu hóa phông nền và khoảng cách tổng thể */
        .stApp {
            background-color: #FFF0F2; /* Màu nền hồng sữa cực nhẹ */
        }
        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
            padding-left: 1.2rem;
            padding-right: 1.2rem;
            max-width: 450px; /* Định dạng khung chuẩn màn hình di động */
            margin: auto;
        }
        
        /* -----------------------------------------------------------------
           KỸ THUẬT ÉP KHUNG CHỨA HIỆU ỨNG VÀ NHẠC PHỦ KÍN TOÀN MÀN HÌNH
           ----------------------------------------------------------------- */
        
        /* Đưa toàn bộ hiệu ứng nền ra SAU CÙNG để không chặn vuốt cuộn trang trên Mobile */
        iframe[srcdoc*="global-effects-layer"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            pointer-events: none !important;
            z-index: -1 !important; /* Quan trọng nhất: Nằm dưới cùng để lướt màn hình mượt mà */
        }
        
        /* Giữ ô nhạc nằm gọn gàng đúng vị trí thăng bằng 90px trong trang */
        iframe[srcdoc*="music-player-container"] {
            position: relative !important;
            width: 100% !important;
            height: 90px !important;
            border: none !important;
            z-index: 10 !important;
        }
        
        /* Khung chứa pháo giấy phụ khi bấm nút dưới cùng */
        iframe[srcdoc*="btn-confetti-trigger"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            border: none !important;
            pointer-events: none !important;
            z-index: 999999 !important;
        }
        
        /* Giao diện khu vực lời chúc */
        .wish-box {
            background-color: #FFFFFF;
            border: 1.5px solid #FADadd;
            border-radius: 20px;
            padding: 22px;
            text-align: center;
            box-shadow: 0px 8px 20px rgba(250, 218, 221, 0.6);
            margin: 20px 0 10px 0;
            position: relative;
            z-index: 2;
        }
        .wish-title {
            color: #D4A373; /* Tông màu đất ấm áp cho tiêu đề */
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            font-family: 'Arial', sans-serif;
        }
        .wish-text {
            color: #6C584C; /* Chữ màu nâu đất dịu mắt */
            font-size: 16px;
            line-height: 1.7;
            text-align: justify;
            font-family: 'Arial', sans-serif;
        }
        
        /* CSS cho Giao diện Chờ (Lớp phủ mượt mà) */
        .welcome-container {
            text-align: center;
            padding: 40px 20px;
            background: #FFFFFF;
            border-radius: 24px;
            border: 2px solid #FADadd;
            box-shadow: 0 10px 25px rgba(250, 218, 221, 0.5);
            margin-top: 30vh;
            transform: translateY(-20%);
        }
        .welcome-title {
            font-size: 20px;
            color: #B5828C;
            font-weight: bold;
            line-height: 1.5;
            margin-bottom: 30px;
        }
        .countdown-text {
            font-size: 45px;
            font-weight: bold;
            color: #D4A373;
            margin: 20px 0;
            animation: pulse 1s infinite;
        }
        
        /* Khung chứa ảnh vuốt ngang tỉ lệ 4:3 */
        .carousel-container {
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            gap: 12px;
            padding: 15px 5px;
            scrollbar-width: none; /* Ẩn thanh cuộn Firefox */
        }
        .carousel-container::-webkit-scrollbar {
            display: none; /* Ẩn thanh cuộn Chrome, Safari */
        }
        .carousel-item {
            flex: 0 0 180px; /* Chiều rộng ảnh trên mobile */
            aspect-ratio: 4 / 3; /* Khóa tỷ lệ 4:3 chuẩn đẹp */
            scroll-snap-align: start;
            object-fit: cover;
            border-radius: 16px;
            border: 3px solid #FFFFFF;
            box-shadow: 0px 6px 12px rgba(212, 163, 115, 0.15);
            transition: transform 0.2s;
        }
        
        /* Hiệu ứng nhịp đập cho số đếm ngược */
        @keyframes pulse {
            0% { transform: scale(0.9); }
            50% { transform: scale(1.1); }
            100% { transform: scale(0.9); }
        }
        
        /* Tùy chỉnh nút bấm của Streamlit sang tone hồng ấm áp */
        div.stButton > button {
            background-color: #FFB5A7 !important;
            color: white !important;
            border-radius: 25px !important;
            border: none !important;
            padding: 10px 24px !important;
            font-size: 16px !important;
            font-weight: bold !important;
            box-shadow: 0 4px 10px rgba(255, 181, 167, 0.4) !important;
            transition: all 0.3s ease;
        }
        div.stButton > button:active {
            transform: scale(0.95);
        }
    </style>
""", unsafe_allow_html=True)

# --- HÀM MÃ HÓA AUDIO TRÊN MÁY TÍNH THÀNH CHUỖI BASE64 ---
def get_base64_audio(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as file:
                encoded = base64.b64encode(file.read()).decode()
            return f"data:audio/mp3;base64,{encoded}"
        except Exception:
            pass
    return ""


# --- QUẢN LÝ TRẠNG THÁI GIAO DIỆN (STATE) ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'waiting'  # Bắt đầu tại màn hình chờ
if 'countdown' not in st.session_state:
    st.session_state.countdown = False  # Trạng thái đếm ngược kích hoạt


# --- 1. MÀN HÌNH CHỜ (WELCOME SCREEN) ---
if st.session_state.stage == 'waiting':
    
    # Nếu chưa bắt đầu đếm ngược, hiển thị câu hỏi và 2 nút lựa chọn
    if not st.session_state.countdown:
        st.markdown("""
            <div class="welcome-container">
                <div class="welcome-title">🌸 Hà Anh đã sẵn sàng đón tuổi 20 chưa nè? 🌸</div>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Sẵn sàng! ✨", use_container_width=True):
                st.session_state.stage = 'main'
                st.rerun()
                
        with col2:
            if st.button("Chưa sẵn sàng... 🥺", use_container_width=True):
                st.session_state.countdown = True
                st.rerun()
                
    # Nếu chọn "Chưa sẵn sàng", hiển thị đếm ngược ép buộc cực kỳ hóm hỉnh
    else:
        st.markdown("""
            <div class="welcome-container">
                <div class="welcome-title">😜 Ê nha phải sẵn sàng chứ!</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Vòng lặp đếm ngược 3, 2, 1
        placeholder = st.empty()
        for i in range(3, 0, -1):
            placeholder.markdown(f'<div class="countdown-text">{i}</div>', unsafe_allow_html=True)
            time.sleep(1.0)
            
        # Chuyển tiếp tự động vào màn hình chính sau khi đếm xong
        st.session_state.stage = 'main'
        st.session_state.countdown = False
        st.rerun()


# --- 2. GIAO DIỆN CHÍNH (MAIN SCREEN) ---
elif st.session_state.stage == 'main':
    
    # Mã hóa tệp âm nhạc sinh nhật vui tươi từ máy tính của bạn
    bday_music_base64 = get_base64_audio("happy_birthday.mp3")
    
    # --- KHỐI HIỆU ỨNG CHẠY TOÀN MÀN HÌNH PHÍA SAU NỀN ---
    # Chứa pháo hoa tự rơi và bong bóng lơ lửng, nằm dưới cùng nên không bao giờ cản trở lướt màn hình
    global_effects_html = """
    <div id="global-effects-layer" style="position:fixed; top:0; left:0; width:100vw; height:100vh; pointer-events:none; overflow:hidden;"></div>

    <!-- Thư viện pháo giấy confetti -->
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>

    <script>
        // 1. Kích hoạt pháo giấy tông màu đất ấm áp bắn chéo bao phủ TOÀN MÀN HÌNH
        function triggerConfetti() {
            var duration = 5 * 1000;
            var end = Date.now() + duration;
            var earthColors = ['#D4A373', '#E9C46A', '#F4A261', '#E76F51', '#A26967', '#C89F9C'];

            (function frame() {
                confetti({
                    particleCount: 3,
                    angle: 60,
                    spread: 55,
                    origin: { x: 0, y: 0.8 },
                    colors: earthColors
                });
                confetti({
                    particleCount: 3,
                    angle: 120,
                    spread: 55,
                    origin: { x: 1, y: 0.8 },
                    colors: earthColors
                });

                if (Date.now() < end) {
                    requestAnimationFrame(frame);
                }
            }());
        }
        
        // Gọi pháo hoa rực rỡ ngay lập tức khi mở trang
        triggerConfetti();

        // 2. Hiệu ứng bong bóng và trái tim bay lướt nhẹ nhàng khắp màn hình nền
        const bubbleContainer = document.getElementById('global-effects-layer');
        const icons = ['🌸', '🎈', '💖', '✨', '💕', '🧸'];
        
        function createBubble() {
            const bubble = document.createElement('div');
            bubble.innerText = icons[Math.floor(Math.random() * icons.length)];
            bubble.style.position = 'absolute';
            bubble.style.bottom = '-50px';
            bubble.style.left = Math.random() * 100 + 'vw';
            bubble.style.fontSize = (Math.random() * 20 + 15) + 'px';
            bubble.style.opacity = Math.random() * 0.4 + 0.2; // Nhẹ nhàng tinh tế ở phía sau
            bubble.style.pointerEvents = 'none';
            
            const duration = Math.random() * 6 + 6;
            bubble.style.transition = 'transform ' + duration + 's linear, opacity ' + duration + 's ease-out';
            
            bubbleContainer.appendChild(bubble);
            
            setTimeout(() => {
                const sideMovement = (Math.random() - 0.5) * 150;
                bubble.style.transform = 'translate(' + sideMovement + 'px, -110vh)';
                bubble.style.opacity = '0';
            }, 100);
            
            setTimeout(() => {
                bubble.remove();
            }, duration * 1000);
        }

        setInterval(createBubble, 500);
    </script>
    """
    
    # --- KHỐI Ô PHÁT NHẠC MANUAL ĐỘC LẬP (CAO 90PX) ---
    custom_music_player_html = """
    <div class="music-player-container" style="
        display: flex;
        align-items: center;
        background-color: #FFFFFF;
        border: 2px solid #FADadd;
        border-radius: 16px;
        padding: 10px 15px;
        box-shadow: 0px 4px 12px rgba(250, 218, 221, 0.4);
        font-family: 'Arial', sans-serif;
        justify-content: space-between;
        height: 70px;
        box-sizing: border-box;
    ">
        <div style="display: flex; align-items: center; gap: 12px;">
            <!-- Đĩa nhạc xoay tròn xinh xắn -->
            <div id="vinyl-disc" style="
                width: 44px;
                height: 44px;
                background: radial-gradient(circle, #333 30%, #FFB5A7 31%, #FFB5A7 40%, #333 41%);
                border-radius: 50%;
                border: 2px solid #FFFFFF;
                box-shadow: 0px 2px 5px rgba(0,0,0,0.2);
                display: flex;
                align-items: center;
                justify-content: center;
                animation: spin 3s linear infinite;
                animation-play-state: paused;
            ">
                <span style="font-size: 14px;">🌸</span>
            </div>
            
            <!-- Tên bài hát rộn rã vui tươi -->
            <div>
                <div style="font-size: 14px; font-weight: bold; color: #8C6239; margin-bottom: 3px;">Nhạc Sinh Nhật Vui Tươi 🎵</div>
                <div style="font-size: 11px; color: #B5828C; font-style: italic;">Chạm nút bên cạnh để nghe nhé</div>
            </div>
        </div>

        <!-- Nút phát nhạc thủ công màu hồng pastel xinh xắn -->
        <button id="play-btn" style="
            background-color: #FFB5A7;
            color: white;
            border: none;
            border-radius: 50%;
            width: 38px;
            height: 38px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0px 3px 6px rgba(255,181,167,0.5);
            outline: none;
            font-size: 14px;
            font-weight: bold;
        ">▶</button>
    </div>

    <audio id="birthday-audio" loop preload="auto">
        <source src="{bday_music_base64}" type="audio/mp3">
        <source src="https://dl.dropboxusercontent.com/scl/fi/7iyn97i8b958j525g0shx/happy_birthday_vocals.mp3?rlkey=26i7eon6jkyom1d1dfsmf1z9e&dl=1" type="audio/mpeg">
    </audio>

    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>

    <script>
        const audio = document.getElementById('birthday-audio');
        const playBtn = document.getElementById('play-btn');
        const vinyl = document.getElementById('vinyl-disc');
        
        audio.volume = 0.8;

        playBtn.addEventListener('click', () => {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            if (AudioContext) {
                const context = new AudioContext();
                if (context.state === 'suspended') {
                    context.resume();
                }
            }

            if (audio.paused) {
                audio.play().then(() => {
                    playBtn.innerText = '⏸';
                    vinyl.style.animationPlayState = 'running';
                }).catch(err => {
                    console.log("Lỗi phát nhạc:", err);
                });
            } else {
                audio.pause();
                playBtn.innerText = '▶';
                vinyl.style.animationPlayState = 'paused';
            }
        });
    </script>
    """.replace("{bday_music_base64}", bday_music_base64)
    
    # Nhúng hiệu ứng nền bay phía sau cùng (Tuyệt đối không chặn cử chỉ lướt màn hình)
    components.html(global_effects_html)
    
    # Biểu tượng hộp quà phía trên tiêu đề lời chúc
    st.markdown("<p style='text-align: center; font-size: 35px; margin-bottom: 0;'>🎁✨</p>", unsafe_allow_html=True)
    
    # Hộp lời chúc sinh nhật viết riêng cho Hà Anh
    st.markdown("""
        <div class="wish-box">
            <div class="wish-title">Happy Birthday Hà Anh! 🌸</div>
            <div class="wish-text">
                Chúc cho tuổi 20 của Hà Anh sẽ nhẹ nhàng như những tiếng đàn mà Hà Anh đánh, 
                và cũng sẽ rực rỡ như cách Hà Anh cười. 
                <br><br>
                Chắc chắn cũng sẽ có những áp lực, và mệt mỏi nhưng cứ tự tin làm những thứ mình thích nha. 
                Chúc mừng sinh nhật cô bé dễ thương =)).
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Nhúng ô trình phát nhạc Pastel xinh xắn độc lập (Đặt bình thường trong trang)
    components.html(custom_music_player_html, height=90)
    
    # Nhãn danh sách album ảnh vuốt ngang
    st.markdown('<div style="padding-left: 10px; font-weight: bold; color: #8C6239; font-size: 16px; margin-top: 15px;">📸 Những mảnh kỷ niệm đáng nhớ:</div>', unsafe_allow_html=True)
    
    # --- ALBUM 8 ẢNH THẬT TRÊN INTERNET CỦA BẠN (POSTIMAGES) ---
    list_anh = [
        "https://i.postimg.cc/9z0vGpXK/01.jpg",
        "https://i.postimg.cc/mz5pdvZ5/02.jpg",
        "https://i.postimg.cc/vgN2PJ8C/03.jpg",
        "https://i.postimg.cc/sQNHnkfL/04.jpg",
        "https://i.postimg.cc/ftrqHGT4/05.jpg",
        "https://i.postimg.cc/JD2YTf41/06.jpg",
        "https://i.postimg.cc/8ffKxZj6/07.png",
        "https://i.postimg.cc/p55G3sph/08.jpg"
    ]
    
    # Tạo cấu trúc HTML băng chuyền ảnh vuốt ngang tỉ lệ 4:3
    html_carousel = '<div class="carousel-container">'
    for url in list_anh:
        html_carousel += f'<img class="carousel-item" src="{url}">'
    html_carousel += '</div>'
    
    st.markdown(html_carousel, unsafe_allow_html=True)
    
    # Chú thích nhỏ hướng dẫn Hà Anh tương tác vuốt ảnh
    st.markdown("<p style='text-align: center; font-size: 12px; color: #9C897E; font-style: italic; margin-top: -5px;'>👈 (Vuốt sang trái để xem thêm ảnh của Hà Anh nè) 👉</p>", unsafe_allow_html=True)
    
    st.write("") # Khoảng đệm trống nhỏ
    
    # Nút bấm tương tác thêm ở dưới cùng (Pháo giấy bùng nổ khi nhấn nút)
    btn_confetti_js = """
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
    <script>
        confetti({
            particleCount: 150,
            spread: 80,
            origin: { y: 0.65 },
            colors: ['#D4A373', '#E9C46A', '#F4A261', '#E76F51', '#A26967', '#C89F9C']
        });
    </script>
    """
    
    if st.button("Nhấn để nhận thêm niềm vui! 🥳✨", use_container_width=True):
        components.html(btn_confetti_js, height=1, width=1)