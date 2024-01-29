import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

plt.style.use('dark_background')

df1 = pd.read_csv('athlete_events1.csv')
df2 = pd.read_csv('athlete_events2.csv')
df = helper.df_creator(df1,df2)
region_df = pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image("Olympic_logo.png")

user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete-Wise Analysis')
)


if user_menu=='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country == 'Overall' and selected_year=='Overall':
        st.title('Overall Tally')
    if selected_country == 'Overall' and selected_year!="Overall":
        st.title(f'Medal Tally in {selected_year} Olympics')
    if selected_country != 'Overall' and selected_year=="Overall":
        st.title(f'Medal Tally of {selected_country}')
    if selected_country != 'Overall' and selected_year!="Overall":
        st.title(f'Medal Tally of {selected_country} in {selected_year}')
    st.table(medal_tally)

if user_menu == "Overall Analysis":
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_years = helper.data_over_years(df,'region')
    fig = px.line(nations_over_years,x='Year',y='count')
    st.title("Participating Nations Over Years")
    st.plotly_chart(fig)

    events_over_years = helper.data_over_years(df, 'Event')
    fig = px.line(events_over_years, x='Year', y='count')
    st.title("Event Count Over Years")
    st.plotly_chart(fig)

    athletes_over_years = helper.data_over_years(df, 'Name')
    fig = px.line(athletes_over_years, x='Year', y='count')
    st.title("Athlete Count Over Years")
    st.plotly_chart(fig)

    st.title('Number of events in all sports over the years')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True);
    st.pyplot(fig)

    st.title('Most Medals Won')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select Sport',sport_list)
    x = helper.medal_winners(df,selected_sport)
    st.table(x)

if user_menu == 'Country-Wise Analysis':

    st.sidebar.title('Country-Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a country',country_list)

    try:
        country_df = helper.yearwise_medal_tally(df,selected_country)
        fig = px.line(country_df,x='Year',y='Medal')
        st.title(f'Medal-tally Over Years for {selected_country}')
        st.plotly_chart(fig)

    except:
        raise ValueError('The entered country has no medal tally')

    try:
        st.title(f"{selected_country}'s performance in all sports")
        pt = helper.country_medal_heatmap(df,selected_country)
        fig,ax = plt.subplots(figsize=(20,20))
        ax = sns.heatmap(pt,annot=True)
        st.pyplot(fig)
    except:
        ValueError('The entered country has performance record')

    st.title(f"Top 10 Athletes of {selected_country}")
    top10_df = helper.most_successful_in_country(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete-Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == "Gold"]['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == "Silver"]['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == "Bronze"]['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'], show_rug=False,
                          show_hist=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    famous_sports = ['Basketball','Judo','Football','Tug-Of-War','Athletics',
                     'Swimming','Badminton','Sailing','Gymnastics','Art Competitions',
                     'Handball','Weightlifting','Wrestling','Shooting','Boxing',
                     'Taekwondo','Cycling','Diving','Canoeing','Tennis','Golf','Softball',
                     'Archery','Volleyball','Synchronized Swimming','Table Tennis','Baseball',
                     'Rhythmic Gymnastics','Rugby Sevens','Beach Volleyball','Triathlon',
                     'Rugby','Polo','Ice Hockey']
    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title('Distribution of Age of Gold Medalists')
    st.plotly_chart(fig)
    sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=100)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select Sport', sport_list)

    st.title('Height v/s Weight')
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=50)
    st.pyplot(fig)

    st.title('Men v/s Women : Participation Over Years')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)