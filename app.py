import streamlit as st 
import pandas as pd 
from datetime import datetime 
import matplotlib as pyplot
import sqlite3
import plotly.graph_objects as go


def main():
    ### Database Functions ###
    conn = sqlite3.connect('bot-data.db')
    c = conn.cursor()

    def create_table():
        c.execute('CREATE TABLE IF NOT EXISTS botelection(name TEXT,position TEXT,category TEXT,electdate DATE)')
        
    def add_vote(name,position,category,electdate):
        c.execute('INSERT INTO botelection(name,position,category,electdate) VALUES (?,?,?,?)',(name,position,category,electdate))
        conn.commit()

    def view_all_vote():
        c.execute('SELECT * FROM botelection')
        data = c.fetchall()
        return data

    def get_vote_by_position(position):
        c.execute('SELECT * FROM botelection WHERE position="{}"'.format(position))
        data = c.fetchall()
        return data

    def get_vote_by_name(author):
        c.execute('SELECT * FROM botelection WHERE name="{}"'.format(name))
        data = c.fetchall()
        return data

    def delete_vote(position):
        c.execute('DELETE FROM botelection WHERE position="{}"'.format(position))
        conn.commit()

### ---- End Database functions ---- ###

### ---- Layout ---- ###

    st.title('PBS 56th Annual Membership Meeting')
    menu = ["Board Execom Election", "Get Election Results"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Board Execom Election":
        st.header('BOT Execom Election')
        tophead = st.beta_container()
        chairman = st.beta_container()
        vice_chairman = st.beta_container()
        secretary = st.beta_container()
        member1 = st.beta_container()
        member2 = st.beta_container()
        results = st.beta_container()

        df = pd.read_csv('bot.csv')

        with tophead:
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

        with chairman:
            pres = df_new['FullName']
            pres = st.selectbox('Select New PBS President and Chairman:', pres)
            #ccn = df_new['Council'] #.iloc[0]
            
            council = df_new.query('FullName == @pres')
            chairman_council = council['Council'].iloc[0]
            #st.write(council)
            #st.write(chairman_council)

            #st.write(ccn)
            chair_title = "President & Chairman"

        with vice_chairman:
            ### Search for the selected Chairman name in previous selectbox ###
            pres_name = df_new.loc[df_new['FullName'] == pres]
            #st.write(name)

            ### Select values for Chairman and Council ###
            chr_council = pres_name['Council'].iloc[0]
            chr_name = pres_name['FullName'].iloc[0]
            #st.write(chr_council)
            #st.write(chr_name)

            ### Search and remove Name and Council from dataset and create new one ###
            vice_chair = df_new.query('FullName != @chr_name and Council != @chr_council')
            #dfsh = vice_chair.shape[0]
            #st.write(dfsh)
            vice_chair = vice_chair.reset_index(drop=True)
            #st.write(vice_chair)

            vice_chair_name = vice_chair['FullName']
            vpres = st.selectbox('Select New Vice-President and Vice-Chairman:', vice_chair_name)
            vchair_title = "Vice-President & Vice-Chairman"

        with secretary:
            ### Selected Vice-Chairman ###
            vice_chair = df_new.loc[df_new['FullName'] == vpres]

            vice_chair_name = vice_chair['FullName'].iloc[0]
            vice_chair_council = vice_chair['Council'].iloc[0]
            # st.write(vice_chair_name, vice_chair_council)

            ### Select Secretary ###
            secretary = df_new.query('FullName != @vice_chair_name and Council != @vice_chair_council and FullName !=@pres and Council != @chairman_council')
            #st.write(sec)
            secretary = secretary.reset_index(drop=True)
            #st.write(sec)

            secretary_name = secretary['FullName']
            secretary_council = secretary['Council']

            sec = st.selectbox('Select New Corporate Secretary:', secretary_name)
            sec_title = "Corporate Secretary"
            #st.write(secretary_name, secretary_council)

        with member1:
            ### Selected Vice-Chairman ###
            sec_name = df_new.loc[df_new['FullName'] == sec]

            sc_name = sec_name['FullName'].iloc[0]
            sc_council = sec_name['Council'].iloc[0]
            #st.write(sc_name, sc_council)

            # #st.write(vcn, vccn)
            df_member1 = df_new.query('FullName != @vice_chair_name and Council != @vice_chair_council '\
            + 'and FullName !=@pres and Council != @chairman_council and FullName != @sc_name and Council != @sc_council')
            # #df_mem1
            df_member1 = df_member1.reset_index(drop=True)

            member1_name = df_member1['FullName']
            # mem1cn = df_mem1['Council'].iloc[0]
            member1 = st.selectbox('Select New Member:', member1_name) # df_mem1)
            member1_title = "Member"

        with member2:
            df_member2 = df.copy()

            member1_name = df_member2.loc[df_member2['FullName'] == member1]
            #st.write(member1_name)
            mem1_name = member1_name['FullName'].iloc[0]
            mem1_council = member1_name['Council'].iloc[0]
            #st.write(mem1_name, mem1_council)

            # #st.write(vcn, vccn)
            df_member2 = df_new.query('FullName != @vice_chair_name '\
            + 'and FullName != @pres and FullName != @sc_name '\
            + 'and FullName != @mem1_name ')
            #df_member1
            #df_member1
            df_member2 = df_member2.reset_index(drop=True)

            member2_name = df_member2['FullName']
            # # mem1cn = df_mem1['Council'].iloc[0]
            member2 = st.selectbox('Select New Member:', member2_name) # df_mem1)
            member2_title = "Member"

            member2_name = df_member2.loc[df_member2['FullName'] == member2]
            mem2_name = member2_name['FullName'].iloc[0]
            mem2_council = member2_name['Council'].iloc[0]
            #st.write(member2_council)
        
        with results:
            res = st.beta_expander("SUMMARY & VOTE SUBMISSION")

            with res:
                col1,col2 = st.beta_columns(2)
                # Method 1
                col1.info("POSITIONS")
                col2.info("SELECTIONS")
                # Method 2
                with col1:
                    col1.write("**President & Chairman**")
                    col1.write("**Vice-President & Vice-Chairman**")
                    col1.write("**Corporate Secretary**")
                    col1.write("**Execom Member1**")
                    col1.write("**Execom Member2**")
                    #col1.text_input('Enter your number:','Number')
                    
                with col2:
                    col2.write(chr_name + ", " + chr_council)
                    col2.write(vice_chair_name + ", " + vice_chair_council)
                    col2.write(sc_name + ", " + sc_council)
                    col2.write(mem1_name + ", " + mem1_council)
                    col2.write(mem2_name + ", " + mem2_council)
                    #col2.write(' \n ')

                    if res.button("SUBMIT VOTE"):
                        create_table()
                        for x in range(0, 5):
                            if x == 0:
                                add_vote(chr_name,chair_title,chr_council,datetime.date(datetime.now()))
                            if x == 1:
                                add_vote(vice_chair_name,vchair_title,vice_chair_council,datetime.date(datetime.now()))
                            if x == 2:
                                add_vote(sc_name,sec_title,sc_council,datetime.date(datetime.now()))
                            if x == 3:
                                add_vote(mem1_name,member1_title,mem1_council,datetime.date(datetime.now()))
                            if x == 4:
                                add_vote(mem2_name,member2_title,mem2_council,datetime.date(datetime.now()))
                            
                        col1.success("Thank you for your vote. Please do not click the SUBMIT VOTE button again.")

    else:
        st.subheader("RESULTS OF EXECOM ELECTION")
        rows = view_all_vote()

        df_all = pd.DataFrame(rows, columns=['name','position','category','date'])

        #st.subheader('President & Chairman')
        chairman_result = df_all.loc[df_all['position'] == 'President & Chairman']
        name_chairman = chairman_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'}) #agg(['count'])
        name_chairman = name_chairman.set_index('name')
        xp_chairman = st.beta_expander('President & Chairman')
        with xp_chairman:
            st.write(name_chairman)
        #st.write(name_chairman)
        st.bar_chart(name_chairman['total'])

        #st.subheader('Vice-President & Vice-Chairman')
        vicechairman_result = df_all.loc[df_all['position'] == 'Vice-President & Vice-Chairman']
        name_vicechairman = vicechairman_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'})
        name_vicechairman = name_vicechairman.set_index('name')
        xp_vicechairman = st.beta_expander('Vice-President & Vice-Chairman')
        with xp_vicechairman:
            st.write(name_vicechairman)
        #st.write(name_vicechairman)
        st.bar_chart(name_vicechairman['total'])


        # st.subheader('Corporate Secretary')
        secretary_result = df_all.loc[df_all['position'] == 'Corporate Secretary']
        name_secretary = secretary_result.groupby('name')['position'].count().reset_index().rename(columns={'position':'total'})
        #name_secretary = secretary_result.value_counts(subset=['name'])
        name_secretary = name_secretary.set_index('name')
        xp_secretary = st.beta_expander('Corporate Secretary')
        with xp_secretary:
            st.write(name_secretary)
        #st.write(name_secretary)
        #st.bar_chart(name_secretary)
        st.bar_chart(name_secretary['total'])

        
        #st.subheader('Member')
        
        member1_result = df_all.loc[df_all['position'] == 'Member']
        name_member = member1_result.groupby(['name'])['position'].count().reset_index().rename(columns={'position':'total'})
        name_member = name_member.set_index('name')
        xp_member = st.beta_expander('Member')
        with xp_member:
            st.write(name_member)
        st.bar_chart(name_member['total'])

        tot = st.beta_expander("All Votes Here")
        with tot:
            st.write(df_all)



if __name__ == '__main__':
	main()
