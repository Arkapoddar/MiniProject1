import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")



df=pd.read_csv("startup_cleaned.csv")
df['date']=pd.to_datetime(df["date"],errors="coerce")
df["year"]=df["date"].dt.year
df["month"]=df["date"].dt.month

def load_overall_analysis():
    st.title("Overall Analysis")
    col1, col2, col3,col4 = st.columns(4)

    total=round(df["amount"].sum())
    max=df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
    avg=df.groupby("startup")["amount"].sum().mean()
    count=df['startup'].nunique()


    with col1:
        st.metric("Total",str(total),"cr")
    with col2:
        st.metric("max", str(max), "cr")
    with col3:
        st.metric("avg", str(round(avg)), "cr")
    with col4:
        st.metric("funded startup", str(count))


    st.header("MoM graph")
    temp_df = df.groupby(["year", 'month'])['amount'].sum().reset_index()
    temp_df["x_axis"] = temp_df['year'].astype('str') + "-" + temp_df["month"].astype("str")
    fig1, ax1 = plt.subplots()
    ax1.plot(temp_df["x_axis"], temp_df["amount"])
    st.pyplot(fig1)




def load_investor_detail(selected_invester):
    st.title(selected_invester)


    last_df=df[df["investors"].str.contains(selected_invester)].head()[["date", 'startup', "vertical", "city", "round", 'amount']]
    st.subheader("Most recent Investment")
    st.dataframe(last_df)



    col1,col2=st.columns(2)
    with col1:
        big_series=df[df["investors"].str.contains(selected_invester)].groupby("startup")['amount'].sum().head().sort_values(ascending=False)
        st.subheader("Most Biggest Investment")
        fig, ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series=df[df["investors"].str.contains(selected_invester)].groupby("vertical")['amount'].sum()
        st.subheader("Sector Investment In")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index)
        st.pyplot(fig1)



    col1, col2 = st.columns(2)
    with col1:
        stage=df[df["investors"].str.contains(selected_invester)].groupby("round")['amount'].sum()
        st.subheader("Most stageInvestment")
        fig, ax = plt.subplots()
        ax.pie(stage, labels=stage.index)
        st.pyplot(fig)

    with col2:
        city_series = df[df["investors"].str.contains(selected_invester)].groupby("city")['amount'].sum()
        st.subheader("Sector Investment In City")
        fig1, ax1 = plt.subplots()
        ax1.pie(city_series, labels=city_series.index)
        st.pyplot(fig1)

    df["year"] = df["date"].dt.year
    yoy_series =df[df["investors"].str.contains(selected_invester)].groupby("year")['amount'].sum()
    st.subheader("yoy_investment")
    fig, ax = plt.subplots()
    ax.plot(yoy_series.index,yoy_series.values)
    st.pyplot(fig)








st.sidebar.title("Startup Funding analysis")

option=st.sidebar.selectbox('select one',["overall analysis","Start Up","investor"])

if option=="overall analysis":
    btn0=st.sidebar.button("Show Overall Analysis")
    if btn0:
        load_overall_analysis()



elif option=="Start Up":
    st.title("START UP")
    st.sidebar.selectbox('choose startup',sorted(df["startup"].unique().tolist()))
    btn1=st.sidebar.button("Find Startup Detail")
else:

    selected_invester=st.sidebar.selectbox("choose investers",sorted(set(df["investors"].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Invester Detail")
    if btn2:
        load_investor_detail(selected_invester)
