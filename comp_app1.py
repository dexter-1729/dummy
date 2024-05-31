
import streamlit as st
from sqlalchemy import create_engine
import pandas as pd


def upload_to_db(df):
   
    # append,replace,fail

    # fail -> fail if a table aldready exists
    # replace ->  replace the data(truncate & load) 
    # append- > appending on the monthly basis
    
    df.to_sql('complaints',engine,if_exists='append')
    
    


st.header('Python Web App')

#st.subheader('header 1')



user = st.sidebar.text_input('Enter Username')


password = st.sidebar.text_input('ENter Password',type="password")


if 'submit' not in st.session_state:
    st.session_state['submit'] = False

submit = st.sidebar.button('SUBMIT')

if submit:
  st.session_state['submit'] =True   

if st.session_state['submit']:
 
  #st.write(user,password)
  #st.write(password)
  engine = create_engine('mysql+mysqlconnector://root:##########@localhost:3306/cbe') 
  login_validate = engine.execute(f''' select * from cbe.app_access where 
                                  username='{user}' and password='{password}' ''').fetchall()
  #st.write(login_validate)
  
  if len(login_validate) != 0:
      
      
      st.success(f'Login Success,{login_validate[0][0]} logged in as {login_validate[0][2]} ')
      #st.write(login_validate[0][0],login_validate[0][2])
      
      if login_validate[0][2] =='manager':
          
       
        file = st.file_uploader('Upload a file')
        if file:
          try:
            df =pd.read_csv(file)
          except Exception as e:
            df =pd.read_excel(file) 
            
          df.loc[0:1100,'ASSIGNED'] = 'narmadha'
          df.loc[1100:,'ASSIGNED'] = 'shruthi'
          
          st.write(df)        
          
          st.button('Upload_TO_DB',on_click=upload_to_db,args=(df,))
 
      else:
          
          
          col1,col2 = st.columns(2)
          
          col3,col4 = st.columns(2)
         
          
          
          df = pd.read_sql(f''' select * from cbe.complaints where lower(assigned) = lower('{login_validate[0][0]}')''',engine)
          
          
          # st.write(df[ df['Status'] == 'Solved' ].count())
          # st.write(df[ df['Status'] == 'Solved' ]['Status'].count())
          
          
          col1.metric('Solved',df[ df['Status'] == 'Solved' ]['Status'].count())
          
          col2.metric('Closed',df[ df['Status'] == 'Closed' ]['Status'].count())
          
          col3.metric('Opened',df[ df['Status'] == 'Open' ]['Status'].count())
          
          col4.metric('Pending',df[ df['Status'] == 'Pending' ]['Status'].count())
          
          
          
          
          st.write(df)

          #st.write(df['Status'].unique())
          
          
          st.download_button('EXPORT_TO_CSV', df.to_csv(index=False),file_name = f'Complaints_{login_validate[0][0]}.csv',
mime='text/csv')


  else:
      st.error('Login Failed')
      st.info('please try again')
      st.warning('check credentials')
