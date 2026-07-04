import pandas as pd
import plotly.express as px
import streamlit as st

# ===================== دوال مساعدة =====================

def log_violation(plate_number, violation_type, file_path="violations.csv"):
    """
    تسجيل مخالفة جديدة في ملف CSV
    
    Args:
        plate_number (str): رقم لوحة المركبة
        violation_type (str): نوع المخالفة
        file_path (str): مسار ملف المخالفات
    """
    import datetime
    
    # إنشاء سجل المخالفة
    df_new = pd.DataFrame([{
        "رقم اللوحة": plate_number,
        "نوع المخالفة": violation_type,
        "التاريخ": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    
    # تحديث الملف
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_updated = df_new
        
    df_updated.to_csv(file_path, index=False)
    print(f"✅ تم تسجيل مخالفة للوحة {plate_number} بنجاح.")


def display_congestion_analysis():
    """عرض تحليل الازدحام"""
    # بيانات تجريبية
    congestion_data = pd.DataFrame({
        "الوقت": ["8:00", "10:00", "12:00", "14:00", "16:00"],
        "نسبة الازدحام": [20, 45, 80, 65, 90]
    })
    
    # رسم بياني تفاعلي
    fig = px.area(
        congestion_data, 
        x="الوقت", 
        y="نسبة الازدحام",
        title="معدل الازدحام عبر اليوم",
        color_discrete_sequence=['#FF4B4B']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # مؤشرات الأداء الرئيسية
    col1, col2, col3 = st.columns(3)
    col1.metric("مواقف متاحة", "12", "+2")
    col2.metric("مواقف مشغولة", "88", "-5")
    col3.metric("مستوى الازدحام الحالي", "High", "85%")


def display_home_page():
    """عرض الصفحة الرئيسية"""
    st.title("مرحباً بك في نظام AeroPark 🚁")
    
    st.markdown("""
    ### نظام إدارة المواقف الذكي باستخدام الدرونز
    هذا النظام مصمم لمراقبة المواقف، رصد المخالفات، وتحليل الازدحام بشكل آلي بالكامل.
    """)
    
    # بطاقات إحصائية سريعة
    col1, col2, col3 = st.columns(3)
    col1.metric("عدد الدرونز المتاحة", "2")
    col2.metric("حالة النظام", "مستقر", "Online")
    col3.metric("مخالفات اليوم", "5", "+2")
    
    st.divider()
    st.subheader("سجل التنبيهات الأخير")
    st.info("✅ تم إقلاع الدرون-01 لمسح المنطقة الجنوبية - قبل 5 دقائق")
    st.warning("⚠️ تم رصد مركبة مخالفة في الموقف رقم 12 - قبل 10 دقائق")


# ===================== الواجهة الرئيسية =====================

def main():
    """الدالة الرئيسية لتشغيل التطبيق"""
    st.set_page_config(
        page_title="AeroPark - نظام المواقف الذكي",
        page_icon="🚁",
        layout="wide"
    )
    
    # القائمة الجانبية
    st.sidebar.title("القائمة")
    choice = st.sidebar.radio(
        "اختر الصفحة",
        ["الرئيسية", "تحليل الازدحام", "تسجيل المخالفات"]
    )
    
    # عرض الصفحات
    if choice == "الرئيسية":
        display_home_page()
    elif choice == "تحليل الازدحام":
        st.title("تحليل الازدحام")
        display_congestion_analysis()
    elif choice == "تسجيل المخالفات":
        st.title("تسجيل المخالفات")
        # نموذج إدخال المخالفة
        col1, col2 = st.columns(2)
        with col1:
            plate = st.text_input("رقم اللوحة")
        with col2:
            violation = st.selectbox("نوع المخالفة", 
                                    ["وقوف خاطئ", "تجاوز السرعة", "وقوف ممنوع"])
        
        if st.button("تسجيل المخالفة"):
            if plate:
                log_violation(plate, violation)
                st.success(f"✅ تم تسجيل مخالفة للوحة {plate} بنجاح!")
            else:
                st.error("❌ الرجاء إدخال رقم اللوحة")


# ===================== نقطة الدخول =====================

if __name__ == "__main__":
    main()
