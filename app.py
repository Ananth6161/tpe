import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from finalconstruction import result_list

video_bytes1 = "https://youtu.be/C7eooUU840w"
video_bytes2 = "https://youtu.be/YqnIPvc3-7A"
st.set_page_config(
    page_title="Dashboard",
    page_icon="",
    layout="wide",
)


data = pd.DataFrame({
    "customer_id": ["CUST123", "CUST456", "CUST789"],
    "score": [75, 90, 55],
    "behavioural_observed": ["Frequent purchases", "High cart abandonment", "Low engagement"],
    "status": ["Active", "At-risk", "Inactive"]
})


def button_clicked(name):
    st.video(video_bytes1)
    st.video(video_bytes2)
    

p = 0
with st.sidebar:
    st.header("Hello, Evanos")
    st.subheader("Sales Manager")
    buttons = ["Button 1", "Button 2", "Button 3"]
    colors = ["#F08080", "#ADD8E6", "#90EE90"]
    if st.button(f"Home"):
        st.write("Hello")
    if st.button(f"Dashboard"):
        p = 2
    if st.button(f"Video"):
        p = 1
        
    

st.markdown(
    """
    <style>
    [data-testid="stForm"]{
    border: 2px solid blue;
    border-radius: 10px;
    box-shadow: 5px 5px 5px pink;
    }
    </style>
    """, unsafe_allow_html=True
)

with st.form("my_form"):
    cols = st.columns(2)

    with cols[0]:
        st.title("Total Customers")
        st.metric("", "835,423", delta_color="normal")
    with cols[1]:
        st.title("New Customers")
        st.metric("", "18", delta_color="off")
        val_slider = st.slider("Active users", 0, 100, 10)
    submitted = st.form_submit_button("Customer growth")
    if submitted:
       data1 = pd.DataFrame({
          'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  'Customer Count': [100, 120, 150, 180, 210, 230, 245, 260, 280, 300, 320, 350]
})
       chart_title = "Customer Growth Over Year"
       fig = px.line(data1, x='Month', y='Customer Count', title=chart_title)
       st.plotly_chart(fig)

if p == 0:
 for index, row in data.iterrows():
  customer_id = row['customer_id']
  score = row['score']
  behavioural_observed = row['behavioural_observed']

  
  st.subheader(f"Customer: {customer_id}")

  col1,col2 = st.columns(2)
  with col1:
      with st.expander("Customer ID"):
          st.write(customer_id) 
          col_id, col_score,col3,col4 = st.columns(4)
          with col_id:
              st.write(customer_id)
             
          with col_score:
              st.write(score)

          with col3:
              st.write(behavioural_observed)
              

             
          with col4:
              if st.button(f"Action for {customer_id}", key=index):
                   p = 1
      

             
fig = px.bar(data, x="behavioural_observed", y="score", title="Behavioural Observation Distribution", hover_data=["behavioural_observed", "score"])
st.plotly_chart(fig)

if p == 1:
    st.video(video_bytes1)
    st.video(video_bytes2)
if p == 2:
   
  for output in result_list:
   emotion_dict = output[0]['emotion']
   max_emotion = max(emotion_dict, key=emotion_dict.get)
   st.title("Customer is facing the " + max_emotion + " emotion")
   max_percentage = emotion_dict[max_emotion]
   labels = list(emotion_dict.keys())
   values = [emotion_dict[label] for label in labels]
   fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
   fig.update_traces(textposition='inside', textinfo='percent+label')
   sorted_emotions = sorted(emotion_dict.items(), key=lambda x: x[1], reverse=True)
   emotions = [item[0] for item in sorted_emotions]
   values = [item[1] for item in sorted_emotions]
   fig_bar = go.Figure(data=[go.Bar(x=emotions, y=values)])
   fig_bar.update_layout(title='Emotion Distribution', xaxis_title='Emotion', yaxis_title='Percentage')
   fig_sunburst = go.Figure(go.Sunburst(
   labels=emotions,
    parents=['Emotions'] * len(emotions),
    values=values,))  
   fig_sunburst.update_layout(title='Hierarchy of Emotions')
   st.plotly_chart(fig_bar, use_container_width=True)
   st.plotly_chart(fig_sunburst, use_container_width=True)


