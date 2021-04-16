import streamlit as st 
import pandas as pd 
from datetime import datetime 
import matplotlib as pyplot
import sqlite3
import plotly.graph_objects as go
import base64

def main():

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    def remote_css(url):
        st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

    def icon(icon_name):
        st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

    local_css("style.css")
    #remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

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

    def get_table():
        c.execute('SELECT count(*) FROM botelection')
        data = c.fetchall()
        return data
    

### ---- End Database functions ---- ###

### ---- Layout ---- ###

    st.title('PBS 56th Annual Membership Meeting')
    menu = ["Board Execom Election", "Get Election Results"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    create_table()
    tophead = st.beta_container()
    chairman = st.beta_container()
    vice_chairman = st.beta_container()
    secretary = st.beta_container()
    member1 = st.beta_container()
    member2 = st.beta_container()
    results = st.beta_container()

    if choice == "Board Execom Election":

        df = pd.read_csv('bot.csv')
        
        with tophead:
            st.header(f"**BOT Executive Committee Election**")
            name = df['FullName']
            x = df.shape[0]
            st.write('\n')

            nominees = st.beta_expander("Names of Nominees / Total Count = " + str(x))
            nominees.write(df)
            st.markdown("""
                    \n \n \n
            """)
            st.write('\n')

            df_new = df.copy()
            count = get_table()

        ##### ----------------------------------------- President & Chairman ------------------------------------ #####
        with chairman:     #### PRESIDENT AND CHAIRMAN  ####
            agree = st.checkbox("Vote for President & Chairman")
            if agree:
                local_css("style.css")
                chair_FullName = df_new['FullName']
                chair_Council = df_new['Council']
                chair_FullName_Council = chair_FullName + ' , ' + chair_Council
                chair = st.selectbox('Select President and Chairman:', chair_FullName_Council)
                chair = chair.split(" , ")

                chair_title = "President & Chairman"
                col1,col2 = st.beta_columns(2)
                with col1:
                    chair_button = col1.button("  SUBMIT  ")
                    if chair_button:
                        add_vote(chair[0],chair_title,chair[1],datetime.date(datetime.now()))
                        col2.success(f"Vote successful.")
                with col2:
                    st.write()

                winner, win_shape = get_tie("President & Chairman")   ###   Get  ###
                #st.write(win_shape)
                if win_shape > 1:
                    tie_for_chairman = st.beta_expander('Break Tie Vote here.')
                    with tie_for_chairman:
                        #placeholder = st.empty()
                        #if st.checkbox(f"There is a tie for President & Chairman"):
                        #st.error(f"Tie breaker for President & Chairman.")
                        # tie_winner = df.new()
                        # for i in range(win_shape):
                        #     win1[i]= winner['name'].iloc[i]
                        win1 = winner['name'].iloc[0]
                        win2 = winner['name'].iloc[1]
                        win3 = winner['name'].iloc[3]
                        win4 = winner['name'].iloc[4]

                        tie_chairman = df_new.query('FullName == @win1 or FullName == @win2 or FullName == @win3 or FullName == @win4')
                        tie_chairman = tie_chairman.reset_index(drop=True)
                        tie_FullName = tie_chairman['FullName']
                        tie_Council = tie_chairman['Council']
                        tie_FullName_Council = tie_FullName + ' , ' + tie_Council
                        chair = st.selectbox('Tie breaker for President & Chairman:', tie_FullName_Council)
                        chair = chair.split(" , ")

                        chair_title = "President & Chairman"
                        col1,col2 = st.beta_columns(2)
                        with col1:
                            chair_button = col1.button("Submit Vote to Break Tie.") 
                            if chair_button:
                                add_vote(chair[0],chair_title,chair[1],datetime.date(datetime.now()))
                                col2.success(f"Vote successful.")
                        with col2:
                            st.write()
                            #col2.warning(f"Select nominee then click **Submit Vote** once.")
        
            st.markdown("""
                ---
                \n
                \n
            """)
        ##### ----------------------------------------- Vice President & Vice-Chairman ------------------------------------ #####
        with vice_chairman:
            agree = st.checkbox("Vote for Vice-President & Vice-Chairman")
            if agree:
                winner_pres, win_shape_pres = get_tie("President & Chairman")
                if win_shape_pres > 1:
                    st.error(f"Tie breaker for President & Chairman not yet resolved.")
                else:
                    chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
                    chairman_council = chairman_info['Council'].iloc[0]  # Council

                    ### Search and remove Name and Council from dataset and create new one ###
                    vice_chair = df_new.query('Council != @chairman_council')
                    vice_chair = vice_chair.reset_index(drop=True)
                    vice_chair_FullName = vice_chair['FullName']
                    vice_chair_Council = vice_chair['Council']
                    vice_chair_FullName_Council = vice_chair_FullName + ' , ' + vice_chair_Council
                    vice_chair = st.selectbox('Select Vice-President and Vice-Chairman:', vice_chair_FullName_Council)
                    vice_chair = vice_chair.split(" , ")

                    vice_chair_title = "Vice-President & Vice-Chairman"
                    col1,col2 = st.beta_columns(2)
                    with col1:
                        vice_chair_button = col1.button("  SUBMIT  ")
                        if vice_chair_button:
                            add_vote(vice_chair[0],vice_chair_title,vice_chair[1],datetime.date(datetime.now()))
                            col2.success(f"Vote successful.")
                    with col2:
                        st.write()

                    winner, win_shape = get_tie("Vice-President & Vice-Chairman")
                    #st.write(win_shape)
                    if win_shape > 1:
                        tie_for_vice_chairman = st.beta_expander('Break Tie Vote here.')
                        with tie_for_vice_chairman:
                            win1 = winner['name'].iloc[0]
                            win2 = winner['name'].iloc[1]
                            win3 = winner['name'].iloc[2]
                            win4 = winner['name'].iloc[3]
                            # for i in range(win_shape):
                            #     win[i] = winner['name'].iloc[i]

                            tie_vice_chairman = df_new.query('FullName == @win1 or FullName == @win2 or FullName == @win3 or FullName == @win4')
                            tie_vice_chairman = tie_vice_chairman.reset_index(drop=True)
                            tie_FullName = tie_vice_chairman['FullName']
                            tie_Council = tie_vice_chairman['Council']
                            tie_FullName_Council = tie_FullName + ' , ' + tie_Council
                            vice_chair = st.selectbox('Tie breaker for Vice-President & Vice-Chairman:', tie_FullName_Council)
                            vice_chair = vice_chair.split(" , ")

                            vice_chair_title = "Vice-President & Vice-Chairman"
                            col1,col2 = st.beta_columns(2)
                            with col1:
                                chair_button = col1.button("Submit Vote to Break Tie") 
                                if chair_button:
                                    add_vote(vice_chair[0],vice_chair_title,vice_chair[1],datetime.date(datetime.now()))
                                    col2.success(f"Vote successful.")
                            with col2:
                                st.write()
            st.markdown("""
                ---
                \n
                \n
            """)
        ##### ----------------------------------------- Corporate Secretary ------------------------------------ #####
        with secretary:
            agree = st.checkbox("Vote for Corporate Secretary")
            if agree:
                ### TEST IF PENDING TIE IS NOT YET RESOLVED in Vice-President & Vice-Chairman ###
                winner_vc, win_shape_vc = get_tie("Vice-President & Vice-Chairman")
                if win_shape_vc > 1:
                    st.error(f"Tie breaker for Vice-President & Vice-Chairman not yet resolved.")
                else:
                    ### Get values for Chairman and Council ###
                    chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
                    chairman_council = chairman_info['Council'].iloc[0]

                    ## Get Winner for Vice-President & Vice-Chairman ###
                    vice_chairman_election_result, vice_chairman_name, vice_chairman_info, hvchair = elected("Vice-President & Vice-Chairman")
                    vice_chairman_council = vice_chairman_info['Council'].iloc[0]

                    ## Search and remove Name and Council from dataset and create new one ###
                    secretary = df_new.query('Council != @vice_chairman_council and Council != @chairman_council')
                    secretary = secretary.reset_index(drop=True)
                    secretary_FullName = secretary['FullName']
                    secretary_Council = secretary['Council']
                    secretary_FullName_Council = secretary_FullName + ' , ' + secretary_Council
                    secretary = st.selectbox('Select Corporate Secretary:', secretary_FullName_Council)
                    secretary = secretary.split(" , ")

                    secretary_title = "Corporate Secretary"
                    col1,col2 = st.beta_columns(2)
                    with col1:
                        secretary_button = col1.button("   SUBMIT    ")
                        if secretary_button:
                            add_vote(secretary[0],secretary_title,secretary[1],datetime.date(datetime.now()))
                            col2.success(f"Vote successful.")
                    with col2:
                        st.write()

                winner, win_shape = get_tie("Corporate Secretary")
                if win_shape > 1:
                    tie_for_secretary = st.beta_expander('Break Tie Vote here.')
                    with tie_for_secretary:
                        win1 = winner['name'].iloc[0]
                        win2 = winner['name'].iloc[1]
                        #win3 = winner['name'].iloc[2]
                        #win4 = winner['name'].iloc[3]

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
                            secretary_button = col1.button("  SUBMIT   ")
                            if secretary_button:
                                add_vote(secretary[0],secretary_title,secretary[1],datetime.date(datetime.now()))
                                col2.success(f"Vote successful.")
                        with col2:
                            st.write()
            st.markdown("""
                ---
                \n
                \n
            """)

        ##### ----------------------------------------- Member 1 ------------------------------------ #####
        with member1:
            agree = st.checkbox("Vote for Member 1")
            if agree:
                ###  TEST IF PENDING TIE IN SECRETARY IS NOT YET RESOLVED  ###
                winner, win_shape = get_tie("Corporate Secretary")
                if win_shape > 1:
                   st.error(f"Tie breaker for Corporate Secretary not yet resolved.")
                else:
                    ### Get values for Chairman and Council ###
                    chairman_election_result, chairman_name, chairman_info, hchair = elected("President & Chairman")
                    chairman_council = chairman_info['Council'].iloc[0]

                    ### Get Winner for Vice-President & Vice-Chairman ###
                    vice_chairman_election_result, vice_chairman_name, vice_chairman_info, hvchair = elected("Vice-President & Vice-Chairman")
                    vice_chairman_council = vice_chairman_info['Council'].iloc[0]

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
                        member1_button = col1.button("   SUBMIT   ")
                        if member1_button:
                            add_vote(member1[0],member1_title,member1[1],datetime.date(datetime.now()))
                            col2.success(f"Vote successful.")
                    with col2:
                        st.write()
                
                winner, win_shape = get_tie("Member1")
                if win_shape > 1:
                    tie_for_member1 = st.beta_expander('Break Tie Vote here.')
                    with tie_for_member1:
                        win1 = winner['name'].iloc[0]
                        win2 = winner['name'].iloc[1]
                        #win3 = winner['name'].iloc[2]
                        #win4 = winner['name'].iloc[3]

                        tie_member1 = df_new.query('FullName == @win1 or FullName == @win2')
                        tie_member1 = tie_member1.reset_index(drop=True)
                        tie_FullName = tie_member1['FullName']
                        tie_Council = tie_member1['Council']
                        tie_FullName_Council = tie_FullName + ' , ' + tie_Council
                        member1 = st.selectbox('Tie breaker for Member1:', tie_FullName_Council)
                        member1 = member1.split(" , ")

                        secretary_title = "Member1"
                        col1,col2 = st.beta_columns(2)
                        with col1:
                            member1_button = col1.button("  SUBMIT   ")
                            if member1_button:
                                add_vote(member1[0],member1_title,member1[1],datetime.date(datetime.now()))
                                col2.success(f"Vote successful.")
                        with col2:
                            st.write()

            st.markdown("""
                ---
                \n
                \n
            """)

        ##### ----------------------------------------- Member 2 ------------------------------------ ##### HERERHERERHERERHE
        with member2:
            agree = st.checkbox("Vote for Member 2")
            if agree:
                winner_mem1, win_shape_mem1 = get_tie("Member1")
                if win_shape_mem1 > 1:
                    st.error(f"Tie breaker for Member 1 not yet resolved.")
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
                        member2_button = col1.button("  SUBMIT ")
                        if member2_button:
                            add_vote(member2[0],member2_title,member2[1],datetime.date(datetime.now()))
                            col2.success(f"Vote successful.")
                    with col2:
                        st.write()
                
                winner, win_shape = get_tie("Member2")
                if win_shape > 1:
                    tie_for_member2 = st.beta_expander('Break Tie Vote here.')
                    with tie_for_member2:
                        win1 = winner['name'].iloc[0]
                        win2 = winner['name'].iloc[1]
                        #win3 = winner['name'].iloc[2]
                        #win4 = winner['name'].iloc[3]

                        tie_member2 = df_new.query('FullName == @win1 or FullName == @win2') # or FullName == @win3 or FullName == @win4')
                        tie_member2 = tie_member2.reset_index(drop=True)
                        tie_FullName = tie_member2['FullName']
                        tie_Council = tie_member2['Council']
                        tie_FullName_Council = tie_FullName + ' , ' + tie_Council
                        member2 = st.selectbox('Tie breaker for Member 2:', tie_FullName_Council)
                        member2 = member2.split(" , ")

                        member2_title = "Member2"
                        col1,col2 = st.beta_columns(2)
                        with col1:
                            member2_button = col1.button("  SUBMIT  ")
                            if member2_button:
                                add_vote(member2[0],member2_title,member2[1],datetime.date(datetime.now()))
                                col2.success(f"Vote successful.")
                        with col2:
                            st.write()
            
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
        name_chairman = chairman_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'Total'}) #agg(['count'])
        name_chairman = name_chairman.set_index('name')
        chair_sum_total = name_chairman['Total'].sum()

        ### Get Highest Vote PRESIDENT & CHAIRMAN ###
        highest = name_chairman['Total'].max()
        winner = name_chairman[name_chairman['Total'] == highest]
        winner_shape = winner.shape[0]

        st.table(name_chairman.sort_values(by='Total', ascending=False))
        #st.markdown(filedownload(chairman_result), unsafe_allow_html=True)
        st.write(f"**Total Voter(s): **" + str(chair_sum_total))

        ########## VICE-PRESIDENT & VICE-CHAIRMAN ###########
        st.subheader('Vice-President & Vice-Chairman Top Vote')
        vice_chairman_result = df_all.loc[df_all['position'] == 'Vice-President & Vice-Chairman']
        name_vice_chairman = vice_chairman_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'Total'}) #agg(['count'])
        name_vice_chairman = name_vice_chairman.set_index('name')
        vcsum_total = name_vice_chairman['Total'].sum()

        ### Get Highest Vote VICE-PRESIDENT & VICE-CHAIRMAN ###
        highest_vice_chairman = name_vice_chairman['Total'].max()
        winner_vice_chairman = name_vice_chairman[name_vice_chairman['Total'] == highest_vice_chairman]
        #vice_shape = winner.shape[0]

        st.table(name_vice_chairman.sort_values(by='Total', ascending=False))
        st.write(f"**Total Voter(s): **" + str(vcsum_total))
        #st.write(winner_vice_chairman)

        ########## SECRETARY ###########
        st.subheader('Corporate Secretary Top Vote')
        secretary_result = df_all.loc[df_all['position'] == 'Corporate Secretary']
        name_secretary = secretary_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'Total'}) #agg(['count'])
        name_secretary = name_secretary.set_index('name')
        secsum_total = name_secretary['Total'].sum()

        ### Get Highest Vote ###
        highest_secretary = name_secretary['Total'].max()
        winner_secretary = name_secretary[name_secretary['Total'] == highest_secretary]
        #vice_shape = winner.shape[0]

        st.table(name_secretary.sort_values(by='Total', ascending=False))
        st.write(f"**Total Voter(s): **" + str(secsum_total))
        #st.write(winner_secretary)

        ########## MEMBER1 ###########
        st.subheader('Member 1 Top Vote')
        member1_result = df_all.loc[df_all['position'] == 'Member1']
        name_member1 = member1_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'Total'}) #agg(['count'])
        name_member1 = name_member1.set_index('name')
        mem1sum_total = name_member1['Total'].sum()

        ### Get Highest Vote ###
        highest_member1 = name_member1['Total'].max()
        winner_member1 = name_member1[name_member1['Total'] == highest_member1]
        #vice_shape = winner.shape[0]

        st.table(name_member1.sort_values(by='Total', ascending=False))
        st.write(f"**Total Voter(s): **" + str(mem1sum_total))
        #st.write(winner_member1)

        ########## MEMBER 2 ###########
        st.subheader('Member 2 Top Vote')
        member2_result = df_all.loc[df_all['position'] == 'Member2']
        name_member2 = member2_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'Total'}) #agg(['count'])
        name_member2 = name_member2.set_index('name')
        mem2sum_total = name_member2['Total'].sum()
        ### Get Highest Vote ###
        highest_member2 = name_member2['Total'].max()
        winner_member2 = name_member2[name_member2['Total'] == highest_member2]
        #vice_shape = winner.shape[0]
        
        st.table(name_member2.sort_values(by='Total', ascending=False))
        st.write(f"**Total Voter(s): **" + str(mem2sum_total))

        tot = st.beta_expander("All Votes Here")
        with tot:
            st.table(df_all)

            def filedownload(df):
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
                href = f'<a href="data:file/csv;base64,{b64}" download="election-result.csv">Download Results</a>'
                return href

            st.markdown(filedownload(df_all), unsafe_allow_html=True)




if __name__ == '__main__':
	main()
