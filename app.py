import streamlit as st
import datetime
import pandas as pd

# -------------------------------------------------------------------
# การตั้งค่าหน้าตาแอปพลิเคชัน
# -------------------------------------------------------------------

st.set_page_config(
    page_title="EarlyBird - แอปพลิเคชันช่วยตื่นทันเรียน/ทำงาน",
    page_icon="⏰",
    layout="wide"
)

# กำหนดค่าเริ่มต้นของระบบ
if "screen_time_limit" not in st.session_state:
    st.session_state["screen_time_limit"] = 45
if "screen_time_used" not in st.session_state:
    st.session_state["screen_time_used"] = 15
if "alarm_active" not in st.session_state:
    st.session_state["alarm_active"] = False
if "steps_walked" not in st.session_state:
    st.session_state["steps_walked"] = 0
if "target_steps" not in st.session_state:
    st.session_state["target_steps"] = 10
if "streak_days" not in st.session_state:
    st.session_state["streak_days"] = 5
if "logs" not in st.session_state:
    st.session_state["logs"] = [
        {"วันที่": "2026-10-01", "เวลาเข้านอน": "22:45", "ตื่นทันเวลา": "ทันเวลาสบายๆ", "วิธีปิดปลุก": "เดิน 10 ก้าว + สแกน QR"},
        {"วันที่": "2026-10-02", "เวลาเข้านอน": "22:55", "ตื่นทันเวลา": "ทันเวลาสบายๆ", "วิธีปิดปลุก": "เดิน 10 ก้าว + สแกน QR"},
    ]

# ส่วนหัวข้อแอปพลิเคชัน
st.title("⏰ EarlyBird: แอปพลิเคชันช่วยตื่นทันเรียน/ทำงาน")
st.caption("แก้ปัญหาเป็นคนตื่นดึกและตื่นสายอย่างยั่งยืน โดยไม่ต้องพึ่งยานอนหลับ และไม่ต้องหักดิบงดเล่นมือถือ")

# แถบเมนูด้านข้าง
st.sidebar.title("📌 เมนูหลัก")
page = st.sidebar.radio(
    "เลือกหน้าการทำงาน :",
    [
        "🌙 เข้านอน & ตารางเรียน",
        "🚨 ปลุกบังคับเดิน + เสียงเตือนสติ",
        "📱 จำกัดเวลาเล่นมือถือ",
        "🏆 สถิติ & เหรียญรางวัล"
    ]
)

# -------------------------------------------------------------------
# หน้าที่ 1: เข้านอน & ตารางเรียน
# -------------------------------------------------------------------

if page == "🌙 เข้านอน & ตารางเรียน":
    st.header("🌙 เตือนเข้าขอนอนก่อน 23:00 น.")
    class_time = st.time_input("📚 เวลาเรียน/ทำงานคาบแรกพรุ่งนี้ :", datetime.time(8, 0))
    prep_min = st.number_input("🚗 เวลาเตรียมตัวและเดินทาง (นาที) :", value=60, step=15)
    
    st.info("💡 เป้าหมายเข้านอน: **ไม่เกิน 23:00 น.** เพื่อการพักผ่อนที่เพียงพออย่างน้อย 8 ชั่วโมง")
    
    st.subheader("📋 เช็คลิสต์เตรียมตัวเข้านอน")
    c1 = st.checkbox("ปิดไฟห้องนอนเพื่อเตรียมความพร้อม")
    c2 = st.checkbox("วางมือถือไว้ห่างจากเตียง (บังคับเดินไปปิดพรุ่งนี้เช้า)")
    c3 = st.checkbox("จัดกระเป๋า/เตรียมชุดสำหรับวันพรุ่งนี้เรียบร้อย")
    
    if c1 and c2 and c3:
        st.success("✨ พร้อมสำหรับการนอนแล้ว ราตรีสวัสดิ์ครับ!")

# -------------------------------------------------------------------
# หน้าที่ 2: ปลุกบังคับเดิน + เสียงเตือนสติ
# -------------------------------------------------------------------

elif page == "🚨 ปลุกบังคับเดิน + เสียงเตือนสติ":
    st.header("🚨 ปลุกบังคับเดิน 10 ก้าว + เสียงเตือนสติ")
    reason = st.text_input("💬 ข้อความเตือนสติเมื่อนาฬิกาปลุกดัง :", "ตื่นไปเรียนวิชาฟิสิกส์ 08:00 น. ได้แล้ว! ลุกขึ้นเตรียมตัวเพื่ออนาคตของคุณ!")
    
    if st.button("🔔 ทดสอบนาฬิกาปลุก (Test Alarm)", type="primary"):
        st.session_state["alarm_active"] = True
        st.session_state["steps_walked"] = 0
        
    if st.session_state["alarm_active"]:
        st.error(f"🔊 เสียงพูดเตือนสติ: '{reason}'")
        st.warning("⚠️ กรุณาลุกเดินสะสมสิบก้าวออกจากเตียงเพื่อปิดปลุก!")
        
        progress = min(1.0, st.session_state["steps_walked"] / st.session_state["target_steps"])
        st.progress(progress)
        st.write(f"🚶 ก้าวเดินปัจจุบัน: **{st.session_state['steps_walked']} / {st.session_state['target_steps']} ก้าว**")
        
        if st.session_state["steps_walked"] < st.session_state["target_steps"]:
            if st.button("🐾 เดิน 5 ก้าว (จำลอง Sensor)"):
                st.session_state["steps_walked"] += 5
                st.rerun()
        else:
            st.success("✅ เดินครบ 10 ก้าวแล้ว! กรุณาสแกน QR Code หน้าอ่างล้างหน้าเพื่อดับเสียงปลุกสำเร็จ")
            if st.button("📸 สแกน QR Code หน้าห้องน้ำสำเร็จ"):
                st.session_state["alarm_active"] = False
                st.success("🎉 ปิดนาฬิกาปลุกสำเร็จ สมองตื่นสมบูรณ์แล้ว!")
                st.rerun()

# -------------------------------------------------------------------
# หน้าที่ 3: จำกัดเวลาเล่นมือถือ
# -------------------------------------------------------------------

elif page == "📱 จำกัดเวลาเล่นมือถือ":
    st.header("📱 จำกัดเวลาเล่นมือถือก่อนนอน")
    limit = st.slider("โควตาเวลาเล่นมือถือช่วงค่ำ (นาที) :", 15, 90, st.session_state["screen_time_limit"], step=5)
    st.session_state["screen_time_limit"] = limit
    
    used = st.session_state["screen_time_used"]
    st.metric("ใช้งานไปแล้ว", f"{used} / {limit} นาที")
    st.progress(min(1.0, used / limit))
    
    if st.button("▶️ จำลองเล่นมือถือเพิ่ม 10 นาที"):
        st.session_state["screen_time_used"] += 10
        st.rerun()

# -------------------------------------------------------------------
# หน้าที่ 4: สถิติ & เหรียญรางวัล
# -------------------------------------------------------------------

elif page == "🏆 สถิติ & เหรียญรางวัล":
    st.header("🏆 สถิติตื่นทันเวลา")
    st.success(f"🔥 ตื่นติดต่อกัน: **{st.session_state['streak_days']} วัน**")
    
    df = pd.DataFrame(st.session_state["logs"])
    st.dataframe(df, use_container_width=True)
