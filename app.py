import streamlit as st 
import pandas as pd 
from datetime import datetime 
import matplotlib as pyplot
import sqlite3
import plotly.graph_objects as go

def main():
    ### Database Functions ###
    #conn = sqlite3.connect('bot-data.db')
    conn = sqlite3.connect('bot-data-14Apr.db')
    c = conn.cursor()

    def create_table():
        c.execute('CREATE TABLE IF NOT EXISTS botelection(name TEXT,position TEXT,category TEXT, electdate DATE)')

    def add_vote(name,position,category,electdate):
        c.execute('INSERT INTO botelection(name,position,category,electdate) VALUES (?,?,?,?)',(name,position,category,electdate))
        conn.commit()
    
    def view_all_vote():
        c.execute('SELECT * FROM botelection')
        data = c.fetchall()
        return data
    
    def elected(position):
        rows = view_all_vote()
        df_all = pd.DataFrame(rows, columns=['name','position','category','date'])

        #chairman_result = df_all.loc[df_all['position'] == 'President & Chairman']
        winner_result = df_all.loc[df_all['position'] == position ]
        name_of_elected = winner_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])
        #name_chairman = name_chairman.set_index('name')

        ### get highest vote
        highest = name_of_elected['total'].max()
        winner = name_of_elected[name_of_elected['total'] == highest]
        winner_shape = winner.shape[0]

        ### Name of Elected Board member
        elected_name = winner['name'].to_string(index=False)
        #st.write(winner_name)

        ### Get information of Elected Boardmember: FullName, LastName, FirstName, Council, Type  ###
        elected_info = df.query('FullName == @elected_name')
        #st.write(chairman_winner)

        return name_of_elected, elected_name, elected_info, winner_shape

    def get_tie(position):
        rows = view_all_vote()
        df_all = pd.DataFrame(rows, columns=['name','position','category','date'])

        chairman_result = df_all.loc[df_all['position'] == position ]
        name_chairman = chairman_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])
        #name_chairman = name_chairman.set_index('name')

        ### Get Highest Vote ###
        highest = name_chairman['total'].max()
        winner = name_chairman[name_chairman['total'] == highest]
        winner_shape = winner.shape[0]

        return winner, winner_shape

### ---- End Database functions ---- ###

### ---- Layout ---- ###

    st.title('PBS 56th Annual Membership Meeting')
    menu = ["Board Execom Election", "Get Election Results"]

    choice = st.sidebar.selectbox("Menu", menu)
    
    create_table()

    if choice == "Board Execom Election":
        st.header(f"**BOT Execom Election**")
        st.markdown('''
            ---
        ''')
        tophead = st.beta_container()
        chairman = st.beta_container()
        vice_chairman = st.beta_container()
        secretary = st.beta_container()
        member1 = st.beta_container()
        member2 = st.beta_container()
        results = st.beta_container()

        df = pd.read_csv('bot.csv')
      
        df_new = df.copy()

    #### PRESIDENT ####
        agree = st.checkbox("Proceed to President & Chairman")
        if agree:
            chair_FullName = df_new['FullName']
            chair_Council = df_new['Council']
            chair_FullName_Council = chair_FullName + ' , ' + chair_Council
            chair = st.selectbox('Select New PBS President and Chairman:', chair_FullName_Council)
            chair = chair.split(" , ")

            chair_title = "President & Chairman"
            col1,col2 = st.beta_columns(2)
            with col1:
                chair_button = col1.button("VOTE for President & Chairman")
                if chair_button:
                    add_vote(chair[0],chair_title,chair[1],datetime.date(datetime.now()))
                    col1.success(f"Vote successful.")
            with col2:
                col2.warning(f"Select nominee then click **Submit Vote** once.")

        st.markdown("""
            ---
            \n
            \n
        """)

    #### VICE PRESIDENT  ####

        agree = st.checkbox("Proceed to Vice-President & Vice-Chairman")
        if agree:
            #st.checkbox("Great", value = True)

            ### Get Winner for President & Chairman ###
            ### BREAK TIE IF EVER THERE IS/ARE ###
            winner, win_shape = get_tie("President & Chairman")
            if win_shape > 1:
                st.error(f"Tie breaker for President & Chairman.")
                # tie_winner = df.new()
                win1 = winner['name'].iloc[0]
                win2 = winner['name'].iloc[1]
                tie_chairman = df_new.query('FullName == @win1 or FullName == @win2')
                tie_chairman = tie_chairman.reset_index(drop=True)
                tie_FullName = tie_chairman['FullName']
                tie_Council = tie_chairman['Council']
                tie_FullName_Council = tie_FullName + ' , ' + tie_Council
                chair = st.selectbox('Tie breaker for President & Chairman:', tie_FullName_Council)
                chair = chair.split(" , ")

                chair_title = "President & Chairman"
                col1,col2 = st.beta_columns(2)
                with col1:
                    chair_button = col1.button("Tie Breaker VOTE for President & Chairman")
                    if chair_button:
                        add_vote(chair[0],chair_title,chair[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")
            else:
                ### Get Winner for President & Chairman ###
                chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
                chairman_council = chairman_info['Council'].iloc[0]  # Council

                ### Search and remove Name and Council from dataset and create new one ###
                vice_chair = df_new.query('Council != @chairman_council')
                vice_chair = vice_chair.reset_index(drop=True)
                vice_chair_FullName = vice_chair['FullName']
                vice_chair_Council = vice_chair['Council']
                vice_chair_FullName_Council = vice_chair_FullName + ' , ' + vice_chair_Council
                vice_chair = st.selectbox('Select New PBS Vice-President and Vice-Chairman:', vice_chair_FullName_Council)
                vice_chair = vice_chair.split(" , ")

                vice_chair_title = "Vice-President & Vice-Chairman"
                col1,col2 = st.beta_columns(2)
                with col1:
                    vice_chair_button = col1.button("VOTE for Vice-President & Vice-Chairman")
                    if vice_chair_button:
                        add_vote(vice_chair[0],vice_chair_title,vice_chair[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")

        st.markdown("""
            ---
            \n
            \n
        """)

    #### SECRETARY  ####
        agree = st.checkbox("Proceed to Corporate Secretary")
        if agree:
            ### Get values for Chairman and Council ###
            chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
            chairman_council = chairman_info['Council'].iloc[0]

            ## Get Winner for Vice-President & Vice-Chairman ###
            ## BREAK TIE HERE  ####
            winner, win_shape = get_tie("Vice-President & Vice-Chairman")
            #st.write(winner, win_shape)
            if win_shape > 1:
                st.error(f"Tie breaker for Vice-President & Vice-Chairman.")
                # tie_winner = df.new()
                win1 = winner['name'].iloc[0]
                win2 = winner['name'].iloc[1]
                tie_vice_chairman = df_new.query('FullName == @win1 or FullName == @win2')
                tie_vice_chairman = tie_vice_chairman.reset_index(drop=True)
                tie_FullName = tie_vice_chairman['FullName']
                tie_Council = tie_vice_chairman['Council']
                tie_FullName_Council = tie_FullName + ' , ' + tie_Council
                tie_winners = st.selectbox('Tie breaker for Vice-President & Vice-Chairman.:', tie_FullName_Council)
                tie_winners = tie_winners.split(" , ")

                vice_chair_title = "Vice-President & Vice-Chairman"
                col1,col2 = st.beta_columns(2)
                with col1:
                    vice_chair_button = col1.button("Tie Breaker VOTE for Vice-President & Vice-Chairman")
                    if vice_chair_button:
                        add_vote(vice_chair[0],vice_chair_title,vice_chair[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")
            else:
                vice_chairman_election_result, vice_chairman_name, vice_chairman_info, hvchair = elected("Vice-President & Vice-Chairman")
                vice_chairman_council = vice_chairman_info['Council'].iloc[0]

                ## Search and remove Name and Council from dataset and create new one ###
                secretary = df_new.query('Council != @vice_chairman_council and Council != @chairman_council')
                secretary = secretary.reset_index(drop=True)
                secretary_FullName = secretary['FullName']
                secretary_Council = secretary['Council']
                secretary_FullName_Council = secretary_FullName + ' , ' + secretary_Council
                secretary = st.selectbox('Select New Corporate Secretary:', secretary_FullName_Council)
                secretary = secretary.split(" , ")

                secretary_title = "Corporate Secretary"
                col1,col2 = st.beta_columns(2)
                with col1:
                    secretary_button = col1.button("VOTE for Corporate Secretary")
                    if secretary_button:
                        add_vote(secretary[0],secretary_title,secretary[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")

        st.markdown("""
            ---
            \n
            \n
        """)

    #### MEMBER 1
        agree = st.checkbox("Proceed to Member 1")
        if agree:
            ### Get values for Chairman and Council ###
            chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
            chairman_council = chairman_info['Council'].iloc[0]

            ### Get Winner for Vice-President & Vice-Chairman ###
            vice_chairman_election_result, vice_chairman_name, vice_chairman_info, hvchair = elected("Vice-President & Vice-Chairman")
            vice_chairman_council = vice_chairman_info['Council'].iloc[0]

            winner, win_shape = get_tie("Corporate Secretary")
            if win_shape > 1:
                st.error(f"Tie breaker for Corporate Secretary.")
                # tie_winner = df.new()
                win1 = winner['name'].iloc[0]
                win2 = winner['name'].iloc[1]
                tie_secretary = df_new.query('FullName == @win1 or FullName == @win2')
                tie_secretary = tie_secretary.reset_index(drop=True)
                tie_FullName = tie_secretary['FullName']
                tie_Council = tie_secretary['Council']
                tie_FullName_Council = tie_FullName + ' , ' + tie_Council
                secretary = st.selectbox('Tie breaker for Corporate Secretary:', tie_FullName_Council)
                secretary = secretary.split(" , ")

                secretary_title = "Corporate Secretary"
                col1,col2 = st.beta_columns(2)
                with col1:
                    secretary_button = col1.button("VOTE for Corporate Secretary")
                    if secretary_button:
                        add_vote(secretary[0],secretary_title,secretary[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")

            else:
                 ### Get Winner Member 1 ###
                secretary_election_result, secretary_name, secretary_info, shape_sec = elected("Corporate Secretary")
                secretary_council = secretary_info['Council'].iloc[0]

                ### Search and remove Name and Council from dataset and create new one ###
                member1 = df_new.query('Council != @vice_chairman_council and Council != @chairman_council and Council != @secretary_council')
                member1 = member1.reset_index(drop=True)
                member1_FullName = member1['FullName']
                member1_Council = member1['Council']
                member1_FullName_Council = member1_FullName + ' , ' + member1_Council
                member1 = st.selectbox('Select Member One:', member1_FullName_Council)
                member1 = member1.split(" , ")

                member1_title = "Member1"
                col1,col2 = st.beta_columns(2)
                with col1:
                    member1_button = col1.button("VOTE for Member 1")
                    if member1_button:
                        add_vote(member1[0],member1_title,member1[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")
            
        st.markdown("""
            ---
            \n
            \n
        """)

    #### MEMBER 2
        agree = st.checkbox("Proceed to Member 2")
        if agree:
            
            ### Get Winner Member 1 ###
            winner, win_shape = get_tie("Member1")
            if win_shape > 1:
                st.error(f"Tie breaker for Member 1.")
                # tie_winner = df.new()
                win1 = winner['name'].iloc[0]
                win2 = winner['name'].iloc[1]
                tie_member1 = df_new.query('FullName == @win1 or FullName == @win2')
                tie_member1 = tie_member1.reset_index(drop=True)
                tie_FullName = tie_member1['FullName']
                tie_Council = tie_member1['Council']
                tie_FullName_Council = tie_FullName + ' , ' + tie_Council
                member1 = st.selectbox('Tie breaker for Member 1:', tie_FullName_Council)
                member1 = member1.split(" , ")

                member1_title = "Member1"
                col1,col2 = st.beta_columns(2)
                with col1:
                    secretary_button = col1.button("VOTE for Member 1")
                    if secretary_button:
                        add_vote(member1[0],member1_title,member1[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")

            else:

                ### Get values for Chairman and Council ###
                chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
                chairman_council = chairman_info['Council'].iloc[0]
                #st.write(chairman_name)

                ### Get Winner for Vice-President & Vice-Chairman ###
                vice_chairman_election_result, vice_chairman_name, vice_chairman_info, hvchair = elected("Vice-President & Vice-Chairman")
                vice_chairman_council = vice_chairman_info['Council'].iloc[0]
                #st.write(vice_chairman_name)

                secretary_election_result, secretary_name, secretary_info, shape_sec = elected("Corporate Secretary")
                secretary_council = secretary_info['Council'].iloc[0]
                #st.write(secretary_name)

                ### Get Winner Member 1 ###
                member1_election_result, member1_name, member1_info, shape_member1 = elected("Member1")
                member1_council = member1_info['Council'].iloc[0]
                #st.write(member1_name)

                ### Search and remove Name and Council from dataset and create new one ###
                member2 = df_new.query('FullName != @chairman_name and FullName != @vice_chairman_name and FullName != @secretary_name and FullName != @member1_name')
                member2 = member2.reset_index(drop=True)
                member2_FullName = member2['FullName']
                member2_Council = member2['Council']
                member2_FullName_Council = member2_FullName + ' , ' + member2_Council
                member2 = st.selectbox('Select Member 2:', member2_FullName_Council)
                member2 = member2.split(" , ")

                member2_title = "Member2"
                col1,col2 = st.beta_columns(2)
                with col1:
                    member1_button = col1.button("VOTE for Member 2")
                    if member1_button:
                        add_vote(member1[0],member1_title,member1[1],datetime.date(datetime.now()))
                        col1.success(f"Vote successful.")
                with col2:
                    col2.warning(f"Select nominee then click **Submit Vote** once.")
            
        st.markdown("""
            ---
            \n
            \n
        """)
    
    else:
        st.subheader("BOT ELECTION RESULTS")

        rows = view_all_vote()
        df_all = pd.DataFrame(rows, columns=['name','position','category','date'])

        st.subheader('President & Chairman Top Vote')
        chairman_result = df_all.loc[df_all['position'] == 'President & Chairman']
        name_chairman = chairman_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])
        #name_chairman = name_chairman.set_index('name')

        ### Get Highest Vote PRESIDENT & CHAIRMAN ###
        highest = name_chairman['total'].max()
        winner = name_chairman[name_chairman['total'] == highest]
        winner_shape = winner.shape[0]

        st.write(winner)

        ########## VICE-PRESIDENT & VICE-CHAIRMAN ###########
        st.subheader('Vice-President & Vice-Chairman Top Vote')
        vice_chairman_result = df_all.loc[df_all['position'] == 'Vice-President & Vice-Chairman']
        name_vice_chairman = vice_chairman_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])

        ### Get Highest Vote VICE-PRESIDENT & VICE-CHAIRMAN ###
        highest_vice_chairman = name_vice_chairman['total'].max()
        winner_vice_chairman = name_vice_chairman[name_vice_chairman['total'] == highest_vice_chairman]
        #vice_shape = winner.shape[0]

        st.write(winner_vice_chairman)

        ########## SECRETARY ###########
        st.subheader('Corporate Secretary Top Vote')
        secretary_result = df_all.loc[df_all['position'] == 'Corporate Secretary']
        name_secretary = secretary_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])

        ### Get Highest Vote ###
        highest_secretary = name_secretary['total'].max()
        winner_secretary = name_secretary[name_secretary['total'] == highest_secretary]
        #vice_shape = winner.shape[0]

        st.write(winner_secretary)

        ########## MEMBER1 ###########
        st.subheader('Member 1 Top Vote')
        member1_result = df_all.loc[df_all['position'] == 'Member1']
        name_member1 = member1_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])

        ### Get Highest Vote ###
        highest_member1 = name_member1['total'].max()
        winner_member1 = name_member1[name_member1['total'] == highest_member1]
        #vice_shape = winner.shape[0]

        st.write(winner_member1)

        ########## MEMBER 2 ###########
        st.subheader('Member 2 Top Vote')
        member2_result = df_all.loc[df_all['position'] == 'Member2']
        name_member2 = member2_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])

        ### Get Highest Vote ###
        highest_member2 = name_member2['total'].max()
        winner_member2 = name_member2[name_member2['total'] == highest_member2]
        #vice_shape = winner.shape[0]

        st.write(winner_member2)

if __name__ == '__main__':
	main()
