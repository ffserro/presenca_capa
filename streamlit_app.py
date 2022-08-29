import streamlit as st
import pandas as pd 
import pyrebase
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from datetime import datetime
st.set_page_config(page_title='Presença', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="centered", menu_items=None)

firebase = pyrebase.initialize_app(st.secrets.CONFIG_KEY)
db = firebase.database()


df = pd.read_csv('./CAPA.csv')
presentes = []

gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_default_column(maintainColumnOrder=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
gb.configure_auto_height(True)
gb.configure_column("NOME", 'Oficial Aluno')



gb.configure_side_bar()

gb.configure_selection('multiple')
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)


gb.configure_grid_options(domLayout='normal')
gridOptions = gb.build()



st.write('# Presença CApA')
st.write('Por favor, selecione o nome dos oficiais que já se encontram no CIANB e clique no botão abaixo para dar presença.')
grid_response = AgGrid(
    df, 
    gridOptions=gridOptions,
    fit_columns_on_grid_load = True,
    data_return_mode='FILTERED', 
    update_mode='GRID_CHANGED',
    theme='streamlit'    
    )

st.write(grid_response['selected_rows'])

enviar = st.button('Presente!')
if enviar:
    for nome in grid_response['selected_rows']:
        presentes.append(nome['NOME'])
        pass

st.write(presentes)



'''
ids = [i['id'] for i in grid_response['selected_rows']]
for i in ([list(db.child('itens').order_by_child('id').equal_to(x).get().val().keys())[0] for x in ids]):
    db.child('itens').child(i).update({'situacao':'Em trânsito', 'data_envio':datetime.now().strftime("%d/%m/%Y")})
'''