import streamlit as st


st.title('Tabela')
st.dataframe(
    st.session_state['df'],
    hide_index=True,
    use_container_width=True,
    column_config={
        'Order Date': st.column_config.DateColumn(label='Data do Pedido'),
        'Profit': st.column_config.NumberColumn(label='Lucro', format='R$ %.2f')
    }
)