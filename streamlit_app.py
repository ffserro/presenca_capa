import streamlit as st
import pandas as pd 
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from datetime import datetime
st.set_page_config(page_title='Presença', page_icon='https://www.marinha.mil.br/sites/default/files/favicon-logomarca-mb.ico', layout="centered", menu_items=None)


#query = db.child('itens').get().val().values()

df = pd.read_csv('ffserro/presenca_capa/CAPA.csv')

st.dataframe(df)

#Infer basic colDefs from dataframe types
gb = GridOptionsBuilder.from_dataframe(df[['data_cadastro', 'pi', 'nome', 'descricao', 'preco_unitario', 'quantidade', 'uf', 'lvad', 'situacao', 'origem']])

#customize gridOptions
gb.configure_default_column(maintainColumnOrder=True, groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
gb.configure_auto_height(True)
gb.configure_pagination()
gb.configure_column("data_cadastro", 'Data', type=["dateColumnFilter","customDateTimeFormat"], custom_format_string='dd-MM-yyyy', pivot=True)
gb.configure_column("pi", 'PI')
gb.configure_column("nome", 'Nome do item')
gb.configure_column("descricao",'Descrição')
gb.configure_column("lvad", 'LVAD')
gb.configure_column("preco_unitario", 'Preço Unitário', type=["customCurrencyFormat"], custom_currency_symbol="R$", aggFunc='sum')
gb.configure_column("quantidade", 'Quantidade', type=["numericColumn"], aggFunc='max')
gb.configure_column("situacao", 'Situação')
gb.configure_column("uf", 'UF')
gb.configure_column("origem",'Origem')


gb.configure_side_bar()

gb.configure_selection('multiple')
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren=True, groupSelectsFiltered=True)

gb.configure_pagination(paginationAutoPageSize=True)

gb.configure_grid_options(domLayout='normal')
gridOptions = gb.build()



st.write('# Envio dos itens cadastrados')
grid_response = AgGrid(
    df, 
    gridOptions=gridOptions,
    fit_columns_on_grid_load = True,
    data_return_mode='FILTERED', 
    update_mode='GRID_CHANGED',
    allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
    theme='streamlit'    
    )

enviar = st.button('Enviar itens selecionados para o DepSMRJ')
if enviar:
    ids = [i['id'] for i in grid_response['selected_rows']]
    for i in ([list(db.child('itens').order_by_child('id').equal_to(x).get().val().keys())[0] for x in ids]):
        db.child('itens').child(i).update({'situacao':'Em trânsito', 'data_envio':datetime.now().strftime("%d/%m/%Y")})
