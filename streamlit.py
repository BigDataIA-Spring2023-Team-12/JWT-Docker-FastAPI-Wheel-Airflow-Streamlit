import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

# a. Plotting a line chart of count of request by each user against time (date)
user_request_data = pd.DataFrame({
    'user': ['user1', 'user2', 'user1', 'user3', 'user2', 'user1'],
    'date': ['2022-01-01', '2022-01-01', '2022-01-02', '2022-01-02', '2022-01-03', '2022-01-03'],
    'count': [10, 15, 20, 5, 8, 12]
})
user_request_data['date'] = pd.to_datetime(user_request_data['date'])
user_grouped_data = user_request_data.groupby(['user', pd.Grouper(key='date', freq='D')])['count'].sum().reset_index()
fig1, ax1 = plt.subplots()
for user in user_grouped_data['user'].unique():
    user_data = user_grouped_data[user_grouped_data['user'] == user]
    ax1.plot(user_data['date'], user_data['count'], label=user)
ax1.legend()
ax1.set_title('Count of Requests by Each User')
ax1.set_xlabel('Date')
ax1.set_ylabel('Count')
st.pyplot(fig1)

# b. Metric for total API calls the previous day
api_calls_data = {
    "previous_day": {
        "endpoint1": 100,
        "endpoint2": 50,
        "endpoint3": 200
    },
    "last_week": {
        "endpoint1": 750,
        "endpoint2": 500,
        "endpoint3": 1000
    },
    "total_calls": {
        "endpoint1": 5000,
        "endpoint2": 3000,
        "endpoint3": 8000
    }
}
previous_day_api_calls = api_calls_data['previous_day']
fig2, ax2 = plt.subplots()
ax2.plot(previous_day_api_calls.keys(), previous_day_api_calls.values())
ax2.set_title('Total API Calls in Previous Day')
ax2.set_xlabel('Endpoint')
ax2.set_ylabel('Count')
st.pyplot(fig2)

# c. Metric to show total average calls during the last week
last_week_api_calls = api_calls_data['last_week']
fig3, ax3 = plt.subplots()
ax3.plot(last_week_api_calls.keys(), last_week_api_calls.values())
ax3.set_title('Total Average API Calls in Last Week')
ax3.set_xlabel('Endpoint')
ax3.set_ylabel('Count')
st.pyplot(fig3)

# d. Comparison of Success (200 response code) and Failed request calls (i.e., non-200 response codes)
response_codes_data = {
    "200": 1500,
    "404": 200,
    "500": 50
}
success_data = response_codes_data['200']
failure_data = sum([response_codes_data[code] for code in response_codes_data.keys() if code != '200'])
fig4, ax4 = plt.subplots()
ax4.bar(['Success', 'Failure'], [success_data, failure_data])
ax4.set_title('Comparison of Success and Failure Requests')
ax4.set_xlabel('Response Code')
ax4.set_ylabel('Count')
st.pyplot(fig4)

# e. Each endpoint total number of calls
total_calls_data = api_calls_data['total_calls']
fig5, ax5 = plt.subplots()
ax5.bar(total_calls_data.keys(), total_calls_data.values())
ax5.set_title('Total Number of Calls for Each Endpoint')
ax5.set_xlabel('Endpoint')
ax5.set_ylabel('Count')
st.pyplot(fig5)
