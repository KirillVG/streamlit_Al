# import module
import streamlit as st
import pandas as pd
import altair as alt

#@st.cache(suppress_st_warning=True)
def app():

    # Настройки среды
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #Путь к файлу-источнику
    full_dis = 'https://github.com/KirillVG/streamlit_Al/raw/main/alumina_from_factories.xlsx'

    def load_excel(data_link, sheet, col_name):
        dataset = pd.read_excel(data_link, sheet, index_col=False, usecols=col_name)
        return dataset

    def load_stantion():# Загрузка списка заводов
        full_data=load_excel(full_dis, 'page1', "b")#загрузка списка станций назначения
        df = pd.DataFrame(full_data,index=None, columns=None)
        val=df.drop_duplicates()
        return val   

    # Header
    st.title("Глинозем. Отгрузка с заводов ГД. 15.01.2022г.", anchor='dislocation')
    sb_factory=st.selectbox(label='Завод:',options=['Все','Завод_1','Завод_2','Завод_3','Завод_4'])
    st.write("______________________________________________________________________________________________")
    
    #Загружаем объемы
    if sb_factory == 'Все': 
        total_vol = load_excel(full_dis, 'page1', "a,c,d")
        total_vol=total_vol[(total_vol.date<='15.01.2022')]
        sum_vol_plan=total_vol['plan'].sum()
        sum_vol_fact=total_vol['fact'].sum()
        percent=sum_vol_fact/sum_vol_plan*100
    else:
        total_vol = load_excel(full_dis, 'page1', "a,b,c,d")
        total_vol=total_vol[(total_vol.factory==sb_factory) & (total_vol.date<='15.01.2022')]
        sum_vol_plan=total_vol['plan'].sum()
        sum_vol_fact=total_vol['fact'].sum()
        percent=sum_vol_fact/sum_vol_plan*100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("План с нач.мес.:", str(round(sum_vol_plan,0)) + " тн", "")
    col2.metric("Факт с нач.мес.:", str(round(sum_vol_fact,0)) + " тн", "")
    col3.metric("Выполнение:", str(round(percent,2)) + " %", "")
    
    st.write("______________________________________________________________________________________________")

    #Загружаем План/факт накопленным итогом по выбранному заводу
    if sb_factory == 'Все':  
        pf_vol = load_excel(full_dis, 'page1', "a,b,e,f")
        pf_vol=pf_vol.groupby(['date']).sum()
        pf_vol=pf_vol.reset_index()#сброс индексного поля возникающего при группировке
        pf_vol['date']=pf_vol['date'].dt.tz_localize(tz='Europe/Moscow')
        vagon = load_excel(full_dis, 'page4', "a,b,c")
    else:
        pf_vol = load_excel(full_dis, 'page1', "a,b,e,f")
        pf_vol=pf_vol[(pf_vol.factory==sb_factory)]
        pf_vol['date']=pf_vol['date'].dt.tz_localize(tz='Europe/Moscow')
        vagon = load_excel(full_dis, 'page3', "b,c,d,e")
        vagon = vagon[(vagon.factory==sb_factory)]
        vagon = vagon.reset_index()#сброс индексного поля возникающего при группировке
        
    col4, col5 = st.columns([3,1])
    col4.subheader("План/факт накопленным итогом с нач.мес., тн:")
    brush = alt.selection(type='interval', encodings=['x'])

    #Факт
    line_1 = alt.Chart(pf_vol).mark_line(size=5,color="red").encode(
    alt.X('date:T', title=None,scale=alt.Scale(nice={'interval': 'day', 'step': 1}),axis=alt.Axis(format="%d %m %y")),
    alt.Y('fact+:Q',title=None),tooltip=["fact+","date"]
    ).properties(width=1000,height=300)
    
    #План
    line_2 = alt.Chart(pf_vol).mark_area(size=3).encode(
    alt.X('date:T', title=None,scale=alt.Scale(nice={'interval': 'day', 'step': 1}),axis=alt.Axis(format="%d %m %y")),
    alt.Y('plan+:Q',title=None),tooltip=["plan+","date"]
    ).properties(width=1000,height=300)
    
    col4.altair_chart(line_2+line_1)
    
    if sb_factory == 'Все':
        col5.subheader("Вып. плана по заводам,%:")
        total = load_excel(full_dis, 'page2', "a,d")
        source = total
        bar_5 = alt.Chart(source).mark_bar().encode(
        alt.Y('factory', title=None),
        alt.X('total',title=None)).properties(width=300,height=300)
        
        text = bar_5.mark_text(dx=-15, color='red', align='center', baseline='middle').encode(
        text=alt.Text('total', format='.1f'))   
        
        d = {'col1': [percent], 'col2': ['Всего']}
        df = pd.DataFrame(data=d)
        line_3 = alt.Chart(df).mark_bar(size=5,color="red").encode(x='col1', y='col2')
        
        col5.altair_chart(bar_5+text+line_3)
    
    #Диаграмма структуры подвижного состава
    st.subheader("Структура подвижного состава, тн:")
    source = vagon
    #Факт
    bar_6 = alt.Chart(source).mark_bar(size=30,color="red").encode(
    alt.X('vagon', title=None),
    alt.Y('fact+:Q',title=None),tooltip=["fact+","vagon"]
    ).properties(width=500,height=300)
    
    #План
    bar_7 = alt.Chart(source).mark_bar(size=15).encode(
    alt.X('vagon', title=None),
    alt.Y('plan+',title=None),opacity=alt.value(1),tooltip=["plan+","vagon"]
    ).properties(width=500,height=300)
    
    st.altair_chart(bar_6+bar_7)
    
    st.write("______________________________________________________________________________________________")
    st.subheader("План/факт посуточно, тн:")

    #Загружаем План/факт посуточно по выбранному заводу
    if sb_factory == 'Все':  
        pf_vol = load_excel(full_dis, 'page1', "a,b,c,d")
        pf_vol=pf_vol.groupby(['date']).sum()
        pf_vol=pf_vol.reset_index()#сброс индексного поля возникающего при группировке
        pf_vol['date']=pf_vol['date'].dt.tz_localize(tz='Europe/Moscow')
    else:
        pf_vol = load_excel(full_dis, 'page1', "a,b,c,d")
        pf_vol=pf_vol[(pf_vol.factory==sb_factory)]
        pf_vol['date']=pf_vol['date'].dt.tz_localize(tz='Europe/Moscow')
        
        
    brush = alt.selection(type='interval', encodings=['x'])
    
    #Факт    
    bar_3 = alt.Chart(pf_vol).mark_bar(size=30,color="red").encode(
    alt.X('date:T', title=None,scale=alt.Scale(nice={'interval': 'day', 'step': 1}),axis=alt.Axis(format="%d %m %y")),
    alt.Y('fact:Q',title=None),tooltip=["fact","date"]
    ).properties(width=1450,height=300)
    
    #План
    bar_4 = alt.Chart(pf_vol).mark_bar(size=15).encode(
    alt.X('date:T', title=None,scale=alt.Scale(nice={'interval': 'day', 'step': 1}),axis=alt.Axis(format="%d %m %y")),
    alt.Y('plan:Q',title=None),opacity=alt.value(1),tooltip=["plan","date"]
    ).properties(width=1450,height=300)
    
    st.altair_chart(bar_3+bar_4)
    

