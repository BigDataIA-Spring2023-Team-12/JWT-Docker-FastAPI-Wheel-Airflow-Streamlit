import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random


def generate_dummy_data():
    users = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank']
    endpoints = ['/login', '/signup', '/home', '/profile', '/settings']
    response_codes = [200, 200, 200, 400, 500]
    timestamps = pd.date_range(start='2022-01-01', end='2022-02-28', freq='s')
    data = []
    for ts in timestamps:
        record = {}
        record['timestamp'] = ts
        record['user_id'] = random.choice(users)
        record['endpoint'] = random.choice(endpoints)
        record['response_code'] = random.choice(response_codes)
        data.append(record)
    return pd.DataFrame(data)


def get_prev_day_data(df):
    prev_day = datetime.now().date() - timedelta(days=1)
    return df[df['timestamp'].dt.date == prev_day]


def get_last_week_data(df):
    last_week = datetime.now().date() - timedelta(days=7)
    return df[df['timestamp'] >= last_week]


def get_user_count_data(df):
    return df.groupby(['user_id', pd.Grouper(key='timestamp', freq='1D')])['endpoint'].count().reset_index()


def get_endpoint_count_data(df):
    return df.groupby('endpoint')['user_id'].count().reset_index()


def get_success_failed_data(df):
    success = df[df['response_code'] == 200].shape[0]
    failed = df[df['response_code'] != 200].shape[0]
    return success, failed


def main():
    # Load data from API
    df = generate_dummy_data()

    # Calculate metrics
    prev_day_data = get_prev_day_data(df)
    prev_day_total_calls = prev_day_data.shape[0]
    last_week_data = get_last_week_data(df)
    last_week_avg_calls = last_week_data.shape[0] / 7
    user_count_data = get_user_count_data(df)
    endpoint_count_data = get_endpoint_count_data(df)
    success, failed = get_success_failed_data(df)

    # Create the Streamlit app
    st.set_page_config(page_title="User Activity Dashboard", page_icon=":bar_chart:", layout="wide")

    st.title('User Activity Dashboard')
    st.write(
        "Welcome to the User Activity Dashboard. This dashboard provides insights into user activity on your platform.")

    # Display total API calls the previous day
    col1, col2 = st.beta_columns(2)
    with col1:
        st.subheader('Total API calls (previous day)')
        st.metric('API Calls', prev_day_total_calls)

    # Display total average calls during the last week
    with col2:
        st.subheader('Total average calls (last week)')
        st.metric('Average Calls', last_week_avg_calls)

    # Display success and failed request calls
    col3, col4 = st.beta_columns(2)
    with col3:
        st.subheader('Success vs. Failed Requests')
        st.metric('Success', success)
    with col4:
        st.metric('Failed', failed)

    # Display each endpoint total number of calls
    st.subheader('Endpoint Calls')
    fig1 = px.bar(endpoint_count_data, x='endpoint', y='user_id', labels={'user_id': 'Call Count'})
    st.plotly_chart(fig1)

    # Display count of request by each user against time
    st.subheader('User Activity Over Time')
    fig2 = px.line(user_count_data, x='timestamp', y='endpoint', color='user_id', title='User Activity Over Time')
    fig2.update_layout(xaxis_title='Date', yaxis_title='Call Count', legend_title='User ID')
    st.plotly_chart(fig2)


if __name__ == '__main__':
    main()
