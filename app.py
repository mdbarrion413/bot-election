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
        vicechairman = st.beta_container()
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
            df_pres = df_new['FullName'] # + ' ' + df_vp['First Name']
            pres = st.selectbox('Select New PBS President and Chairman:', df_pres)
            ccn = df_new['Council'].iloc[0]
            chair_title = "President & Chairman"

        with vicechairman:
            ### Search for the selected Chairman name in previous selectbox ###
            name = df_new.loc[df_new['FullName'] == pres]

            ### Select valuse fo Name and Council ###
            cn = name['Council'].iloc[0]
            nm = name['FullName'].iloc[0]

            ### Search and remove Name and Council from dataset and create new one ###
            df_vc = df_new.query('FullName != @nm and Council != @cn')
            dfsh = df_vc.shape[0]
            df_vc = df_vc.reset_index(drop=True)

            df_vpres = df_vc['FullName'] # + ' ' + df_vp['First Name']
            vpres = st.selectbox('Select New Vice-President and Vice-Chairman:', df_vpres)
            vchair_title = "Vice-President & Vice-Chairman"

        with secretary:
            ### Selected Vice-Chairman ###
            name_vc = df_vc.loc[df_vc['FullName']==vpres]

            vcn = name_vc['FullName'].iloc[0]
            vccn = name_vc['Council'].iloc[0]

            #st.write(vcn, vccn)
            df_sec = df_vc.query('FullName != @vcn and Council != @vccn')
            #df_sec
            df_sec = df_sec.reset_index(drop=True)

            df_nsec = df_sec['FullName']# + ' ' + df_vp['First Name']
            scn = df_sec['Council'].iloc[0]
            sec = st.selectbox('Select New Corporate Secretary:', df_nsec)
            sec_title = "Corporate Secretary"

        with member1:
            ### Selected Vice-Chairman ###
            name_sec = df_sec.loc[df_sec['FullName']==sec]

            scfn = name_sec['FullName'].iloc[0]
            sccn = name_sec['Council'].iloc[0]

            #st.write(vcn, vccn)
            df_mem1 = df_sec.query('FullName != @scfn and Council != @sccn')
            #df_sec
            df_mem1 = df_mem1.reset_index(drop=True)

            mem1nm = df_mem1['FullName'] # + ' ' + df_vp['First Name']
            mem1cn = df_mem1['Council'].iloc[0]
            mem1 = st.selectbox('Select 1 New Member:', df_mem1)
            mem1_title = "Member"

        with member2:
            mem2_title = "Member"
            df_mem2 = df_new.query('FullName != @pres and FullName != @vpres and FullName != @sec and FullName != @mem1')
            df_mem2 = df_mem2.reset_index(drop=True)
            mem2nm = df_mem2['FullName'] # + ' ' + df_vp['First Name']
            mem2cn = df_mem2['Council'].iloc[0]
            mem2 = st.selectbox('Select 1 New Member:', df_mem2)

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
                    
                with col2:
                    col2.write(pres + ", " + cn)
                    col2.write(vpres + ", " + vccn)
                    col2.write(sec + ", " + scn)
                    col2.write(mem1 + ", " + mem1cn)
                    col2.write(mem2 + ", " + mem2cn)
                    col2.write(' \n ')
                    if res.button("SUBMIT VOTE"):
                        create_table()
                        for x in range(0, 5):
                            if x == 0:
                                add_vote(pres,chair_title,cn,datetime.date(datetime.now()))
                            if x == 1:
                                add_vote(vpres,vchair_title,vccn,datetime.date(datetime.now()))
                            if x == 2:
                                add_vote(sec,sec_title,scn,datetime.date(datetime.now()))
                            if x == 3:
                                add_vote(mem1,mem1_title,mem1cn,datetime.date(datetime.now()))
                            if x == 4:
                                add_vote(mem2,mem2_title,mem2cn,datetime.date(datetime.now()))
                            
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