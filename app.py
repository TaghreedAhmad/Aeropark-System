import os
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
import random

# ===================== دوال مساعدة =====================

def get_drone_status():
    """محاكاة حالة الدرونز"""
    return {
        "الدرون-01": {"الحالة": "نشط", "الموقع": "المنطقة الجنوبية"},
        "الدرون-02": {"الحالة": "نشط", "الموقع": "المنطقة الشمالية"},
        "الدرون-03": {"الحالة": "في الصيانة", "الموقع": "المستودع"},
    }

def get_daily_violations():
    """محاكاة عدد المخالفات اليومية"""
    return random.randint(3, 15)

def get_system_status():
    """الحالة العامة للنظام"""
    return "مستقر", "🟢 Online"

def get_recent_alerts():
    """محاكاة التنبيهات الأخيرة"""
    return [
        {
            "النوع": "info",
            "الرسالة": "تم إقلاع الدرون-01 لمسح المنطقة الجنوبية",
            "الوقت": "قبل 5 دقائق"
        },
        {
            "النوع": "warning",
            "الرسالة": "تم رصد مركبة مخالفة في الموقف رقم 12",
            "الوقت": "قبل 10 دقائق"
        },
        {
            "النوع": "success",
            "الرسالة": "تم تسجيل مخالفة جديدة للوحة HJK-789",
            "الوقت": "قبل 15 دقيقة"
        }
    ]

def log_violation(plate_number, violation_type, file_path="violations.csv"):
    """تسجيل مخالفة جديدة"""
    df_new = pd.DataFrame([{
        "رقم اللوحة": plate_number,
        "نوع المخالفة": violation_type,
        "التاريخ": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_updated = df_new
        
    df_updated.to_csv(file_path, index=False)
    return f"✅ تم تسجيل مخالفة للوحة {plate_number}"


def display_home_page():
    """عرض الصفحة الرئيسية"""
    st.title("مرحباً بك في نظام AeroPark 🚁")
    
    st.markdown("""
    ### نظام إدارة المواقف الذكي باستخدام الدرونز
    هذا النظام مصمم لمراقبة المواقف، رصد المخالفات، وتحليل الازدحام بشكل آلي بالكامل.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    drones = get_drone_status()
    available_drones = sum(1 for d in drones.values() if d["الحالة"] == "نشط")
    status, status_icon = get_system_status()
    violations = get_daily_violations()
    
    col1.metric("عدد الدرونز المتاحة", f"{available_drones} / {len(drones)}")
    col2.metric("حالة النظام", status, status_icon)
    col3.metric("مخالفات اليوم", violations, f"+{violations-5}" if violations > 5 else "")
    
    st.divider()
    st.subheader("سجل التنبيهات الأخير")
    
    alerts = get_recent_alerts()
    for alert in alerts:
        if alert["النوع"] == "info":
            st.info(f"ℹ️ {alert['الرسالة']} - {alert['الوقت']}")
        elif alert["النوع"] == "warning":
            st.warning(f"⚠️ {alert['الرسالة']} - {alert['الوقت']}")
        elif alert["النوع"] == "success":
            st.success(f"✅ {alert['الرسالة']} - {alert['الوقت']}")


def display_congestion_analysis():
    """عرض تحليل الازدحام"""
    congestion_data = pd.DataFrame({
        "الوقت": ["8:00", "10:00", "12:00", "14:00", "16:00"],
        "نسبة الازدحام": [20, 45, 80, 65, 90]
    })
    
    fig = px.area(
        congestion_data, 
        x="الوقت", 
        y="نسبة الازدحام",
        title="معدل الازدحام عبر اليوم",
        color_discrete_sequence=['#FF4B4B']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("مواقف متاحة", "12", "+2")
    col2.metric("مواقف مشغولة", "88", "-5")
    col3.metric("مستوى الازدحام الحالي", "High", "85%")


# ===================== صفحة الدرونز الجديدة =====================

def display_drones_page():
    """عرض صفحة بث مباشر من الدرون"""
    st.title("🚁 بث مباشر من الدرون")
    
    # 1. حالة النظام المباشرة
    col1, col2 = st.columns(2)
    col1.metric("ارتفاع الدرون", "45 متر")
    col2.metric("حالة البطارية", "88%")
    
    # 2. محاكاة رؤية الدرون مع تحليل ذكاء اصطناعي
    st.subheader("رؤية الكاميرا الحية")
    
    

    try:
        # هنا يتم عرض صورة الدرون
        st.image("drone_view.jpg", caption="بث مباشر: رصد السيارات في المواقف", use_container_width=True)
        
     
        st.success("✅ تم اكتشاف 3 سيارات - حالة النظام: سليم")
        st.warning("⚠️ تنبيه: تم اكتشاف سيارة مخالفة في الموقف رقم 12")
    except:
        st.error("جاري انتظار بث الكاميرا... تأكدي من مسار الصورة.")


# ===================== الواجهة الرئيسية =====================

def main():
    """الدالة الرئيسية"""
    st.set_page_config(
        page_title="AeroPark - نظام المواقف الذكي",
        page_icon="🚁",
        layout="wide"
    )
    
    st.sidebar.title("القائمة")
    choice = st.sidebar.radio(
        "اختر الصفحة",
        ["الرئيسية", "تحليل الازدحام", "تسجيل المخالفات", "الدرونز"]  
    )
    
    if choice == "الرئيسية":
        display_home_page()
        
    elif choice == "تحليل الازدحام":
        st.title("تحليل الازدحام")
        display_congestion_analysis()
        
    elif choice == "إرسال تنبية":
        st.title("إرسال تنبية")
        
        col1, col2 = st.columns(2)
        
        with col1:
            plate = st.text_input("رقم اللوحة")
        
        with col2:
            violation = st.selectbox(
                "نوع التنبية",
                ["وقوف خاطئ", "تجاوز السرعة", "وقوف ممنوع"]
            )
        
        if st.button("إرسال تنبية"):
            if plate:
                result = log_violation(plate, violation)
                st.success(result)
            else:
                st.error("❌ الرجاء إدخال رقم اللوحة")
    
    # ====== الصفحة الجديدة ======
    elif choice == "الدرونز":
        display_drones_page()


if __name__ == "__main__":
    main()
