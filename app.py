
# This content is copied from cell 2hHD8SnT0Fgq

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px

# Placeholder function for parking status
# In a real application, this would fetch data from sensors or a database
def get_parking_status():
    data = {
        "lat": [24.7138, 24.7135, 24.7140, 24.7133],
        "lon": [46.6755, 46.6750, 46.6760, 46.6745],
        "status": ["متاح", "مشغول", "متاح", "مشغول"]
    }
    # Using a numerical index for easy searching by 'parking lot number'
    return pd.DataFrame(data, index=range(1, len(data["lat"]) + 1))


# إعداد الصفحة العامة
st.set_page_config(page_title="AeroPark System", layout="wide")

# 1. إعداد القائمة الجانبية
st.sidebar.title("AeroPark")
menu = ["الرئيسية", "خريطة المواقف", "المخالفات", "الدرونز", "إدارة الازدحام"]
choice = st.sidebar.radio("القائمة", menu)

# 2. هيكلة محتوى الصفحات
if choice == "الرئيسية":
    st.title("لوحة تحكم AeroPark")
    st.write("أهلاً بك في نظام إدارة المواقف الذكي باستخدام الدرونز.")
        # إضافة لمسة إبهار للمؤشرات
    col1, col2 = st.columns(2)
    col1.metric("المواقف الشاغرة", "12")
    col2.metric("عدد الدرونز المحلقة", "5")
    st.markdown("---") # خط فاصل جمالي
    
elif choice == "خريطة المواقف":
    st.title("خريطة المواقف الحية")

    # 1. جلب البيانات
    df_parking = get_parking_status()

    # 2. ميزة البحث
    # إنشاء قائمة بأسماء أو أرقام المواقف المتاحة في البيانات
    search_options = ["الكل"] + df_parking.index.astype(str).tolist()
    search_query = st.selectbox("ابحث عن موقف محدد:", search_options)

    # 3. تصفية البيانات بناءً على البحث
    if search_query != "الكل":
        selected_lot = df_parking.loc[int(search_query)]
        map_location = [selected_lot["lat"], selected_lot["lon"]]
        zoom = 20 # زووم أكبر عند البحث عن موقف محدد
    else:
        map_location = [24.7136, 46.6753] # Center for Riyadh
        zoom = 18

    import folium
from streamlit_folium import st_folium

# ننشئ الخريطة
m = folium.Map(location=[24.7136, 46.6753], zoom_start=16)

# دالة ذكية لإضافة النقاط
for i, row in df_parking.iterrows():
    # اختيار اللون بناءً على الحالة
    color = "green" if row['status'] == "متاح" else "red"
    
    # 1. إضافة الدبوس مع معلومات تفاعلية (Popup)
    folium.Marker(
        [row['lat'], row['lon']],
        popup=f"الموقف رقم: {i} <br> الحالة: {row['status']}",
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)
    
    # 2. إضافة دائرة مراقبة الدرون (نطاق التغطية)
    folium.Circle(
        location=[row['lat'], row['lon']],
        radius=15, # نصف القطر بالمتر
        color=color,
        fill=True,
        fill_opacity=0.2
    ).add_to(m)

# عرض الخريطة في Streamlit
st_folium(m, width=700, height=500)


elif choice == "المخالفات":

    st.title("سجل المخالفات")
    st.subheader("رصد السيارات المخالفة وتوثيقها")

    # بيانات تجريبية للمخالفات
    violations_data = {
        "رقم اللوحة": ["ABC-123", "XYZ-789", "LMN-456"],
        "نوع المخالفة": ["وقوف في مكان ممنوع", "تجاوز الوقت المسموح", "وقوف مزدوج"],
        "التوقيت": ["12:10 PM", "12:15 PM", "12:20 PM"],
        "الحالة": ["تم التنبيه", "تم إصدار مخالفة", "قيد المعالجة"]
    }

    df_violations = pd.DataFrame(violations_data)

    # عرض الجدول بتنسيق جذاب
    st.table(df_violations)

    # زر لتصدير البيانات
    csv = df_violations.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="تحميل سجل المخالفات (CSV)",
        data=csv,
        file_name='parking_violations.csv',
        mime='text/csv',
    )

elif choice == "الدرونز":
    st.title("AeroPark - لوحة تحكم")
    st.subheader("إدارة أسطول الدرونز")

    data = {
        "الدرون": ["Drone-01", "Drone-02", "Drone-03"],
        "الحالة": ["في الخدمة", "قيد الشحن", "صيانة"],
        "البطارية": ["85%", "12%", "0%"]
    }
    df = pd.DataFrame(data)
    st.table(df)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("لمسح المنطقة"):
            st.success("تم بدء عملية المسح")
    with col2:
        if st.button("إرسال"):
            st.info("جاري إقلاع الدرون...")

elif choice == "إدارة الازدحام":
    st.title("إدارة الازدحام")
    st.write("تحليل لحظي لمستويات الازدحام في المواقف.")

    import pandas as pd
import os
from datetime import datetime

def log_violation(plate_number, violation_type):
    file_path = "violations.csv"
    
    # بيانات المخالفة الجديدة
    new_violation = {
        "رقم اللوحة": [plate_number],
        "نوع المخالفة": [violation_type],
        "التوقيت": [datetime.now().strftime("%H:%M:%S")],
        "الحالة": ["قيد المعالجة"]
    }
    
    df_new = pd.DataFrame(new_violation)
    
    # إذا كان الملف موجوداً، نضيف البيانات إليه، وإذا لم يكن موجوداً ننشئه
    if os.path.exists(file_path):
        df_existing = pd.read_csv(file_path)
        df_updated = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_updated = df_new
        
    df_updated.to_csv(file_path, index=False)
    print(f"تم تسجيل مخالفة للوحة {plate_number} بنجاح.")

# --- مثال على كيفية استخدام الدالة داخل كود معالجة الصور ---
# بمجرد أن يكتشف الدرون مخالفة:
# if ai_detection_logic == True:
#     log_violation("ABC-123", "وقوف خاطئ")

    # 1. بيانات تجريبية (يمكنك ربطها لاحقاً بقاعدة بيانات حية)
    # الوقت ومعدل الازدحام (مثلاً نسبة مئوية)
    congestion_data = pd.DataFrame({
        "الوقت": ["8:00", "10:00", "12:00", "14:00", "16:00"],
        "نسبة الازدحام": [20, 45, 80, 65, 90]
    })

    # 2. رسم بياني تفاعلي (Area Chart)
    fig = px.area(congestion_data, x="الوقت", y="نسبة الازدحام",
                  title="معدل الازدحام عبر اليوم",
                  color_discrete_sequence=['#FF4B4B'])

    st.plotly_chart(fig, use_container_width=True)

    # 3. مؤشرات أداء رئيسية (KPIs)
    col1, col2, col3 = st.columns(3)
    col1.metric("مواقف متاحة", "12", "+2")
    col2.metric("مواقف مشغولة", "88", "-5")
    col3.metric("مستوى الازدحام الحالي", "High", "85%")

    if choice == "الرئيسية":
     st.title("مرحباً بك في نظام AeroPark")
        
    st.markdown("""
    ### نظام إدارة المواقف الذكي باستخدام الدرونز 🚁
    هذا النظام مصمم لمراقبة المواقف، رصد المخالفات، وتحليل الازدحام بشكل آلي بالكامل.
    """)
    
    # بطاقات إحصائية سريعة
    col1, col2, col3 = st.columns(3)
    col1.metric("عدد الدرونز المتاحة", "2")
    col2.metric("حالة النظام", "مستقر", "Online")
    col3.metric("مخالفات اليوم", "5", "+2")
    
    st.divider()
    st.subheader("سجل التنبيهات الأخير")
    st.info("تم إقلاع الدرون-01 لمسح المنطقة الجنوبية - قبل 5 دقائق")
    st.warning("تم رصد مركبة مخالفة في الموقف رقم 12 - قبل 10 دقائق")
    # كود معالجة الصور
    if مخالفة_مكتشفة:
     log_violation("رقم_اللوحة", "وقوف خاطئ")
