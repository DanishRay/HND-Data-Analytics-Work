import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# LOAD & CLEAN DATA
df = pd.read_csv('video-games-2022.csv')

# Standardize column names (lowercase and no parentheses)
df.columns = (df.columns
              .str.lower()
              .str.replace(' ', '_')
              .str.replace('(', '', regex=False)
              .str.replace(')', '', regex=False))

# FEATURE ENGINEERING
df['platform_count'] = df['platforms'].str.split(',').str.len().fillna(0)
df['genre_count'] = df['genres'].str.split(',').str.len().fillna(0)
df['developer_count'] = df['developers'].str.split(',').str.len().fillna(0)
df['total_tags'] = df['platform_count'] + df['genre_count'] + df['developer_count']

# MappingPlatform Ratio
df['platform_ratio'] = (df['platform_count'] / df['total_tags']).round(4)

# MappingMetadata Volume
df['metadata_volume'] = pd.qcut(df['total_tags'], q=3, labels=['Low', 'Medium', 'High'], duplicates='drop')

df['month'] = df['month'].str.title()

st.set_page_config(page_title="2022 Video Game Analytics", layout="wide")
st.title("🎮 2022 Video Game Data Analytics")
st.header("Section 2: Functional & Relevant Game Filters")

# --- SIDEBAR: 10 RELEVANT FILTERS ---
st.sidebar.header("Filter Dashboard")

# Filter 1: Text Search
search_title = st.sidebar.text_input("1. Search Game Title", "")

# Filter 2: Platforms (Handling multiple platforms per game)
all_plats = sorted(list(set([p.strip() for sublist in df['platforms'].str.split(',').tolist() for p in sublist])))
sel_plats = st.sidebar.multiselect("2. Select Platforms", all_plats, default=all_plats)

# Filter 3: Months
months = st.sidebar.multiselect("3. Select Release Month", df['month'].unique(), default=df['month'].unique())

# Filter 4 & 5: Numerical Ranges
t_min, t_max = int(df['total_tags'].min()), int(df['total_tags'].max())
tag_range = st.sidebar.slider("4. Total Tags Range", t_min, t_max, (t_min, t_max))
day_range = st.sidebar.slider("5. Day of Month Range", 1, 31, (1, 31))

# Filter 6, 7, & 8: Specific Min counts
min_p = st.sidebar.number_input("6. Min Platform Count", 0, value=0)
min_g = st.sidebar.number_input("7. Min Genre Count", 0, value=0)
min_d = st.sidebar.number_input("8. Min Developer Count", 0, value=0)

# Filter 9: Calculated Threshold
min_ratio = st.sidebar.slider("9. Min Platform Focus (%)", 0, 100, 0) / 100

# Filter 10: Volume Category
vol_choice = st.sidebar.radio("10. Metadata Volume Category", ["All", "Low", "Medium", "High"])

# --- APPLYING FILTER LOGIC ---
# Custom filter for the comma-separated platforms string
def plat_check(plat_str, selected):
    game_plats = [p.strip() for p in plat_str.split(',')]
    return any(p in selected for p in game_plats)

mask = (
    df['title'].str.contains(search_title, case=False, na=False) &
    df['month'].isin(months) &
    df['total_tags'].between(tag_range[0], tag_range[1]) &
    df['day'].between(day_range[0], day_range[1]) &
    (df['platform_count'] >= min_p) &
    (df['genre_count'] >= min_g) &
    (df['developer_count'] >= min_d) &
    (df['platform_ratio'] >= min_ratio)
)

filtered_df = df[mask]
filtered_df = filtered_df[filtered_df['platforms'].apply(lambda x: plat_check(x, sel_plats))]

if vol_choice != "All":
    filtered_df = filtered_df[filtered_df['metadata_volume'] == vol_choice]

# --- DISPLAY DATA ---
st.write(f"### Games Found: {len(filtered_df)}")
st.dataframe(filtered_df, use_container_width=True)

# --- DISPLAY VISUALS ---
if not filtered_df.empty:
    st.subheader("Visual Analysis of Filtered Data")
    fig, ax = plt.subplots(figsize=(10, 5))
    # Bar chart showing the Top 10 filtered games by their metadata richness
    sns.barplot(data=filtered_df.head(10), x='total_tags', y='title', hue='month', ax=ax)
    plt.title("Filtered Performance: Top 10 Games by Metadata Volume")
    st.pyplot(fig) 
else:
    st.warning("No games found matching these criteria.")
