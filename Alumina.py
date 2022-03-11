# import module
import streamlit as st
import pandas as pd
import altair as alt

#@st.cache(suppress_st_warning=True)
def app():

    # Настройки среды
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #Путь к файлу-источнику
    full_dis = 'https://github.com/KirillVG/streamlit_Al/raw/main/alumina.xlsx'

    def load_excel(data_link, sheet, col_name):
        dataset = pd.read_excel(data_link, sheet, index_col=False, usecols=col_name)
        return dataset

    def load_stantion():# Загрузка списка заводов
        full_data=load_excel(full_dis, 'page_1', "a")#загрузка списка заводов
        df = pd.DataFrame(full_data,index=None, columns=None)
        val=df.drop_duplicates()
        return val   

    # Header
    st.title("Глинозем. Остатки на заводах и в пути. 15.01.2022г.", anchor='dislocation')
      
    #Факт
    total_vol = load_excel(full_dis, 'page_1', "a,b,c,d,e")
    
    #Факт остатков
    base = alt.Chart(total_vol).encode(alt.X('factory', title="Заводы"))
    bar_1=base.mark_bar(size=60, color="red").encode(alt.Y('volume:Q',title=None),opacity=alt.value(0.6),tooltip=["volume","factory"])
    bar_2=base.mark_bar(size=40).encode(alt.Y('way:Q',title=None),opacity=alt.value(1),tooltip=["way","factory"])
    #Норматив
    tick_1 = alt.Chart(total_vol).mark_tick(color='green',thickness=3,size=80).encode(alt.X('factory'), alt.Y('norm'))
    #Тех.минимум
    tick_2 = alt.Chart(total_vol).mark_tick(color='yellow',thickness=3,size=80).encode(alt.X('factory'), alt.Y('min'))
    #Подписи значений
    text = bar_1.mark_text(align='center',baseline='middle',dy=10,color="white").encode(text='volume:Q')
    st.altair_chart((bar_1+bar_2+tick_1+tick_2+text).properties(width=1300,height=300))
    
    sb_factory=st.selectbox(label='Выбрать завод для просмотра прогноза подхода:',options=['Завод_1','Завод_2','Завод_3','Завод_4'])
    st.write("______________________________________________________________________________________________")
    
    #Факт    
    f_vol = load_excel(full_dis, 'page_2', "a,b,c")
    f_vol=f_vol[(f_vol.destination==sb_factory)]
    f_vol['forecast']=f_vol['forecast'].dt.tz_localize(tz='Europe/Moscow')
    
    bar_3 = alt.Chart(f_vol).mark_bar(size=30).encode(
    alt.X('forecast:T', title=None,scale=alt.Scale(nice={'interval': 'day', 'step': 1}),axis=alt.Axis(format="%d %m %y")),
    alt.Y('volume:Q',title=None),tooltip=["volume","forecast"]
    ).properties(width=1450,height=300)
    st.altair_chart(bar_3)
    
    
    vol = load_excel(full_dis, 'page_2', "a,b,c,e")
    vol=vol[(vol.destination==sb_factory)]
    vol['forecast']=vol['forecast'].dt.tz_localize(tz='Europe/Moscow')
        
    ch=alt.Chart(vol).mark_bar(size=10).encode(
    alt.X('forecast:T', title=None),
    alt.Y('volume:Q', title=None),
    color='vagon:N',
    column='vagon:N')

    st.altair_chart(ch)
    
