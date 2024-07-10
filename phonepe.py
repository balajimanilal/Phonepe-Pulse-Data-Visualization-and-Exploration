import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json

#Dataframe Creation

#SQL Connection
mydb=psycopg2.connect(host="localhost",
                      user="postgres",
                      port="5432",
                      database="phonepe_data",
                      password="12345")
cursor=mydb.cursor()

#Dataframe - Aggregated_Insurance
cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance=pd.DataFrame(table1,columns=("States", "Years", "Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))


#Dataframe - Aggregated_Transaction
cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table2,columns=("States", "Years", "Quarter","Transaction_type",
                                             "Transaction_count","Transaction_amount"))

#Dataframe - Aggregated_User
cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user=pd.DataFrame(table3,columns=("States", "Years", "Quarter","Brands",
                                             "Transaction_count","Percentage"))

#Dataframe - Map_Insurance
cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

Map_insurance=pd.DataFrame(table4,columns=("States", "Years", "Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))

#Dataframe - Map_Transaction
cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

Map_transaction=pd.DataFrame(table5,columns=("States", "Years", "Quarter","Districts",
                                             "Transaction_count","Transaction_amount"))

#Dataframe - Map_User
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

Map_user=pd.DataFrame(table6,columns=("States", "Years", "Quarter","Districts",
                                             "RegisteredUsers","AppOpens"))

#Dataframe - Top_Insurance
cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_insurance=pd.DataFrame(table7,columns=("States", "Years", "Quarter","Pincodes",
                                             "Transaction_count","Transaction_amount"))

#Dataframe - Top_Transaction
cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

Top_transaction=pd.DataFrame(table8,columns=("States", "Years", "Quarter","Pincodes",
                                             "Transaction_count","Transaction_amount"))

#Dataframe - Top_User
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

Top_user=pd.DataFrame(table9,columns=("States", "Years", "Quarter","Pincodes",
                                             "RegisteredUsers"))



def Transaction_amount_count_Y(df,year):

    tacy=df[df["Years"] == year]
    tacy.reset_index(drop = True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg, x="States", y="Transaction_amount", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650,width=600)
        st.plotly_chart(fig_count)


    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)    
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title=f"{year} TRANSACTION COUNT", fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)    
        st.plotly_chart(fig_india_2)

    return tacy


def Transaction_amount_count_Y_Q(df,quarter):
    tacy=df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Agsunset, height=650,width=600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count=px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=650,width=600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:

        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_amount", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),
                                hover_name= "States", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)    
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_count", color_continuous_scale="Rainbow",
                                range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),
                                hover_name= "States", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations",
                                height=600,width=600)
        fig_india_2.update_geos(visible=False)    
        st.plotly_chart(fig_india_2)

    return tacy


def Aggre_Tran_Transaction_type(df,state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop = True, inplace=True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_pie_1=px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_amount", 
                        width=600, title= f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)
        st.plotly_chart(fig_pie_1)

    with col2:

        fig_pie_2=px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_count", 
                        width=600, title= f"{state.upper()} TRANSACTION COUNT", hole=0.5)
        st.plotly_chart(fig_pie_2)


#Aggregated User Analysis 1
def Aggre_user_plot_1(df, year):
    aguy=df[df["Years"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg=pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggregated User Analysis 2
def Aggre_user_plot_2(df,quater):
    aguyq=df[df["Quarter"]==quater]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_2=px.bar(aguyqg, x="Brands", y="Transaction_count", title=f"{quater} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width=1000, color_discrete_sequence=px.colors.sequential.deep_r, hover_name="Brands")
    st.plotly_chart(fig_bar_2)

    return aguyq


#Aggregated User Analysis 3
def Aggre_user_plot_3(df, state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1=px.line(auyqs, x="Brands", y="Transaction_count", hover_data="Percentage",
                    title=f"{state.upper()}. BRANDS. TRANSACTION COUNT. PERCENTAGE", width=1000, markers=True)
    st.plotly_chart(fig_line_1)


#Map Insurance District
def Map_insur_District(df,state):

    tacy=df[df["States"] == state]
    tacy.reset_index(drop = True, inplace=True)

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_bar_1=px.bar(tacyg, x="Transaction_amount", y="Districts", orientation="h", height=600,
                        title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2=px.bar(tacyg, x="Transaction_count", y="Districts", orientation="h", height=600, 
                        title= f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Magenta_r)
        st.plotly_chart(fig_bar_2)


#Map User Plot 1
def Map_user_plot_1(df,year):
    muy=df[df["Years"]==year]
    muy.reset_index(drop=True, inplace=True)

    muyg=muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace=True)


    fig_line_1=px.line(muyg, x="States", y=["RegisteredUsers", "AppOpens"],
                    title=f"{year} REGISTERED USER AND APPOPENS", width=1000, height=800, markers=True)
    st.plotly_chart(fig_line_1)

    return muy


#Map User Plot 2
def Map_user_plot_2(df,quarter):
    muyq=df[df["Quarter"]==quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg=muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace=True)


    fig_line_2=px.line(muyqg, x="States", y=["RegisteredUsers", "AppOpens"],
                    title=f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER AND APPOPENS", width=1000, height=800, markers=True,
                    color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_2)

    return muyq

#Map User Plot 3
def Map_user_plot_3(df,states):
    muyqs=df[df["States"]==states]
    muyqs.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_map_user_bar_1=px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation="h",
                                title= f"{states.upper()} REGISTERED USER", height=800, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2=px.bar(muyqs, x="AppOpens", y="Districts", orientation="h",
                                title= f"{states.upper()} APPOPENS", height=800, color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_map_user_bar_2)


#Top Insurance Plot 1
def Top_insurance_plot_1(df,state):
    tiy=df[df["States"]==state]
    tiy.reset_index(drop=True, inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_top_insur_bar_1=px.bar(tiy, x="Quarter", y="Transaction_amount", hover_data= "Pincodes",
                                title= "TRANSACTION AMOUNT", height=650, width=600, color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2=px.bar(tiy, x="Quarter", y="Transaction_count", hover_data= "Pincodes",
                                title= "TRANSACTION COUNT", height=650, width=600, color_discrete_sequence=px.colors.sequential.Purp_r)
        st.plotly_chart(fig_top_insur_bar_2)


#Top User Plot 1
def Top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)


    fig_top_plot_1=px.bar(tuyg, x= "States", y="RegisteredUsers", color="Quarter", width=1000, height=800,
                        color_discrete_sequence=px.colors.sequential.Burgyl, hover_name="States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


# Top User Plot 2
def Top_user_plot_2(df,state):
    tuys=df[df["States"]==state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2=px.bar(tuys, x="Quarter", y="RegisteredUsers", title= "Registered Users. PINCODES. QUARTER",
                        width=1000, height=800, color="RegisteredUsers", hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)


#Query Plots
def Top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="12345")
    cursor=mydb.cursor()

# Transaction Amount Query Plot 
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="states", y="transaction_amount", title= "TOP 10 OF TRANSACTION AMOUNT", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Agsunset, height=650,width=600)
        st.plotly_chart(fig_amount_1)


# Query Plot 2
    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount 
                LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states", "transaction_amount"))

    with col2:
        fig_amount_2=px.bar(df_2, x="states", y="transaction_amount", title= "LAST 10 OF TRANSACTION AMOUNT", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount_2)


# Query Plot 3
    query3= f'''SELECT states, AVG(transaction_amount) AS transaction_amount 
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3=px.bar(df_3, x="transaction_amount", y="states", title= "AVERAGE OF TRANSACTION AMOUNT", hover_name="states", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)


#Transaction Count Query Plot
def Top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="12345")
    cursor=mydb.cursor()

# Query Plot 1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count 
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states", "transaction_count"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="states", y="transaction_count", title= "TOP 10 OF TRANSACTION COUNT", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Agsunset, height=650,width=600)
        st.plotly_chart(fig_amount_1)


# Query Plot 2
    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count 
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count 
                LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_amount_2=px.bar(df_2, x="states", y="transaction_count", title= "LAST 10 OF TRANSACTION COUNT", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount_2)


# Query Plot 3
    query3= f'''SELECT states, AVG(transaction_count) AS transaction_count 
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3=px.bar(df_3, x="transaction_count", y="states", title= "AVERAGE OF TRANSACTION COUNT", hover_name="states", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)


#Registered User Query Plot
def Top_chart_registered_user(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="12345")
    cursor=mydb.cursor()

    # Query Plot 1
    query1= f'''SELECT districts, SUM(registeredusers) AS registereduser
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts", "registereduser"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="districts", y="registereduser", title= "TOP 10 OF REGISTERED USER", hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Agsunset, height=650,width=600)
        st.plotly_chart(fig_amount_1)


    # Query Plot 2
    query2= f'''SELECT districts, SUM(registeredusers) AS registereduser
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registereduser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_amount_2=px.bar(df_2, x="districts", y="registereduser", title= "LAST 10 OF REGISTERED USER", hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount_2)


    # Query Plot 3
    query3= f'''SELECT districts, AVG(registeredusers) AS registereduser
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY registereduser;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts", "registereduser"))

    fig_amount_3=px.bar(df_3, x="registereduser", y="districts", title= "AVERAGE OF REGISTERED USER", hover_name="districts", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)


#Appopens Query Plot
def Top_chart_appopens(table_name, state):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="12345")
    cursor=mydb.cursor()

    # Query Plot 1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts", "appopens"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount_1=px.bar(df_1, x="districts", y="appopens", title= "TOP 10 OF APPOPENS", hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Agsunset, height=650,width=600)
        st.plotly_chart(fig_amount_1)


    # Query Plot 2
    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts", "appopens"))

    with col2:
        fig_amount_2=px.bar(df_2, x="districts", y="appopens", title= "LAST 10 OF APPOPENS", hover_name="districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount_2)


    # Query Plot 3
    query3= f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states='{state}'
                GROUP BY districts
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3=px.bar(df_3, x="appopens", y="districts", title= "AVERAGE OF APPOPENS", hover_name="districts", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)


#Registered User for Top_User Query Plot
def Top_chart_registered_users(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        port="5432",
                        database="phonepe_data",
                        password="12345")
    cursor=mydb.cursor()

    # Query Plot 1
    query1= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states", "registeredusers"))

    col1,col2=st.columns(2)
    with col1:

        fig_amount_1=px.bar(df_1, x="states", y="registeredusers", title= "TOP 10 OF REGISTERED USERS", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Agsunset, height=650,width=600)
        st.plotly_chart(fig_amount_1)


    # Query Plot 2
    query2= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers
                LIMIT 10;'''

    cursor.execute(query2)
    table_2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states", "registeredusers"))

    with col2:
        fig_amount_2=px.bar(df_2, x="states", y="registeredusers", title= "LAST 10 OF REGISTERED USERS", hover_name="states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650,width=600)
        st.plotly_chart(fig_amount_2)


    # Query Plot 3
    query3= f'''SELECT states, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states", "registeredusers"))

    fig_amount_3=px.bar(df_3, x="registeredusers", y="states", title= "AVERAGE OF REGISTERED USERS", hover_name="states", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height=800,width=1000)
    st.plotly_chart(fig_amount_3)


#Streamlit

st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    
    select= option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

if select == "HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("/Users/balajibm/New Folder/PhonePe - Introduction.mp4")

    col3,col4= st.columns(2)
    
    with col3:
        st.video("/Users/balajibm/New Folder/PhonePe_2.mp4")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.video("/Users/balajibm/New Folder/PhonePe_3.mp4")


elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method=st.radio("Select The Method", ["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarters)

        elif method == "Transaction Analysis":
            
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State", Aggre_tran_tac_Y["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_Ty", Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y_Q,states)

        elif method == "User Analysis":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year",Aggre_user["Years"].min(),2021,Aggre_user["Years"].min())
            Aggre_user_Y=Aggre_user_plot_1(Aggre_user, years)


            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State", Aggre_user_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_user_Y_Q,states)


    with tab2:

        method_2=st.radio("Select The Method", ["Map Insurance", "Map Transaction", "Map User"])

        if method_2 == "Map Insurance":
            
            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year_MI",Map_insurance["Years"].min(),Map_insurance["Years"].max(),Map_insurance["Years"].min())
            Map_insur_tac_Y=Transaction_amount_count_Y(Map_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MI", Map_insur_tac_Y["States"].unique())

            Map_insur_District(Map_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_MI",Map_insur_tac_Y["Quarter"].min(),Map_insur_tac_Y["Quarter"].max(),Map_insur_tac_Y["Quarter"].min())
            Map_insur_tac_Y_Q=Transaction_amount_count_Y_Q(Map_insur_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States", Map_insur_tac_Y_Q["States"].unique())

            Map_insur_District(Map_insur_tac_Y_Q,states)


        elif method_2 == "Map Transaction":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year_MT",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            Map_tran_tac_Y=Transaction_amount_count_Y(Map_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MT", Map_tran_tac_Y["States"].unique())

            Map_insur_District(Map_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_MT",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Map_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The States", Map_tran_tac_Y_Q["States"].unique())

            Map_insur_District(Map_tran_tac_Y_Q,states)

        elif method_2 == "Map User":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year_MU",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            Map_user_Y=Map_user_plot_1(Map_user,years)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_MU",Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q=Map_user_plot_2(Map_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_MU", Map_user_Y_Q["States"].unique())

            Map_user_plot_3(Map_user_Y_Q,states)


    with tab3:

        method_3=st.radio("Select The Method", ["Top Insurance", "Top Transaction", "Top User"])

        if method_3 == "Top Insurance":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year_TI",Top_insurance["Years"].min(),Top_insurance["Years"].max(),Top_insurance["Years"].min())
            Top_insur_tac_Y=Transaction_amount_count_Y(Top_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_TI", Top_insur_tac_Y["States"].unique())

            Top_insurance_plot_1(Top_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_TI",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min())
            Top_insur_tac_Y_Q=Transaction_amount_count_Y_Q(Top_insur_tac_Y,quarters)

        elif method_3 == "Top Transaction":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year_TT",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_tran_tac_Y=Transaction_amount_count_Y(Top_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_TT", Top_tran_tac_Y["States"].unique())

            Top_insurance_plot_1(Top_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:
                
                quarters=st.slider("Select The Quarter_TT",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Top_tran_tac_Y,quarters)

        elif method_3 == "Top User":

            col1,col2=st.columns(2)
            with col1:

                years=st.slider("Select The Year_TU",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_Y=Top_user_plot_1(Top_user,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select The State_TU", Top_user_Y["States"].unique())

            Top_user_plot_2(Top_user_Y,states)

elif select == "TOP CHARTS":

    question=st.selectbox("Select The Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User"
                                                    ])
    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        Top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        Top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered users of Map User":
        
        states=st.selectbox("Select the State",Map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        Top_chart_registered_user("map_user", states)

    elif question == "9. App opens of Map User":
        
        states=st.selectbox("Select the State",Map_user["States"].unique())
        st.subheader("APPOPENS")
        Top_chart_appopens("map_user", states)

    elif question == "10. Registered users of Top User":
        
        st.subheader("REGISTERED USERS")
        Top_chart_registered_users("top_user")