import streamlit as st
import pandas as pd 
import pyrebase
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from datetime import datetime, timedelta, timezone
agora = datetime.now().astimezone(timezone(timedelta(hours=-3)))

st.set_page_config(page_title='Presença', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="centered", menu_items=None)

firebase = pyrebase.initialize_app(st.secrets.CONFIG_KEY)
db = firebase.database()

nomes = pd.read_csv('./CAPA.csv')

df = pd.DataFrame()
for i in nomes.NOME:
    if agora.strftime('%Y-%m-%d') not in db.child('presenca').child(i).get().val().keys() or db.child('presenca').child(i).child(agora.strftime('%Y-%m-%d')).get().val() == False:
	    df = pd.concat([df, pd.DataFrame({'NOME':[i]})],ignore_index=True)


gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_default_column(maintainColumnOrder=True, value=True, editable=False)
gb.configure_auto_height(True)
gb.configure_column("NOME", 'Oficial Aluno')



gb.configure_side_bar()

gb.configure_selection('multiple')
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)


gridOptions = gb.build()


st.write('# Presença CApA - {}'.format(agora.strftime('%d/%m/%Y')))

kpi1, kpi2 = st.columns(2)

kpi1.metric(
    label='Presentes',
    value=len(nomes) - len(df)
)

kpi2.metric(
    label='Ausentes',
    value=len(df)
)

st.write('Por favor, selecione o nome dos oficiais que já se encontram no CIANB e clique no botão abaixo para dar presença.')

if len(df) != 0:
    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions,
        fit_columns_on_grid_load = True,
        data_return_mode='FILTERED', 
        update_mode='GRID_CHANGED',
        theme='streamlit'    
        )


    enviar = st.button('Presente!')
    if enviar:
        for nome in grid_response['selected_rows']:
            db.child('presenca').child(nome['NOME']).update({agora.strftime('%Y-%m-%d'):agora.strftime('%H:%M:%S')})
        st.experimental_rerun()
else:
    st.title('Todos a bordo!')
    final = pd.DataFrame()
    for i in nomes.NOME:
        st.write(db.child('presenca').child(i).child(agora.strftime('%Y-%m-%d')).get().val())
        final = pd.concat([final, pd.DataFrame({ i : [db.child('presenca').child(i).child(agora.strftime('%Y-%m-%d')).get().val()] })]), ignore_index=True)
    st.dataframe(final)






