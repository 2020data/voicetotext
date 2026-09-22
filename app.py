import streamlit as st
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# 設定網頁標題
st.set_page_config(page_title="語音轉文字 Web App", page_icon="🎤")
st.title("🎤 語音辨識網頁應用")
st.write("點擊下方麥克風圖示開始錄音，再次點擊停止錄音。")

# 建立錄音按鈕 (會自動調用電腦或手機的麥克風)
audio_bytes = audio_recorder(
    text="點此錄音 / 停止",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="2x"
)

# 當接收到錄音檔時開始處理
if audio_bytes:
    # 在網頁上播放剛錄製的聲音
    st.audio(audio_bytes, format="audio/wav")
    
    st.info("🔄 正在辨識語音中，請稍候...")
    
    # 將音訊位元組轉換為類檔案物件，供 SpeechRecognition 讀取
    audio_file = io.BytesIO(audio_bytes)
    
    # 初始化語音辨識器
    recognizer = sr.Recognizer()
    
    try:
        # 讀取音訊檔
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            
        # 使用 Google Web Speech API 進行辨識 (預設語言設為繁體中文)
        text = recognizer.recognize_google(audio_data, language="zh-TW")
        
        # 將辨識結果呈現在網頁上
        st.success("✅ 辨識成功！")
        st.write("### 辨識結果：")
        st.code(text, language="text")
        
    except sr.UnknownValueError:
        st.error("❌ 無法辨識語音，請確認您有說話或環境是否過於吵雜。")
    except sr.RequestError as e:
        st.error(f"❌ 語音辨識服務發生錯誤，請檢查網路連線狀態。詳細錯誤: {e}")
    except Exception as e:
        st.error(f"❌ 發生未知的錯誤: {e}")
