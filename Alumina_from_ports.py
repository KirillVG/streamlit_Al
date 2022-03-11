# import module
import streamlit as st
import pandas as pd
import altair as alt

#@st.cache(suppress_st_warning=True)
def app():

    # Настройки среды
    st.set_option('deprecation.showPyplotGlobalUse', False)

    #Путь к файлу-источнику
    full_dis = 'https://github.com/KirillVG/streamlit_Al/raw/main/alumina_from_ports.xlsx'

    def load_excel(data_link, sheet, col_name):
        dataset = pd.read_excel(data_link, sheet, index_col=False, usecols=col_name)
        return dataset

    # Header
    st.title("Глинозем. Поступление и перевалка в портах. 15.01.2022г.", anchor='dislocation')
    sb_port=st.selectbox(label='Порт:',options=['Все','Порт_1','Порт_2','Порт_3','Порт_4'])
    st.write("______________________________________________________________________________________________")
    st.header("Поступление в порты")
        
     #Загружаем объемы
    if sb_port == 'Все': 
        #Факт
        total_vol_fct = load_excel(full_dis, 'page_1', "a,b,c,d,e")
        total_vol_fct=total_vol_fct[(total_vol_fct.date<='15.01.2022') & (total_vol_fct.mark=='fact')]
        sum_vol_fct=total_vol_fct['volume'].sum()
        total_vol_fct=total_vol_fct.groupby(['date']).sum()
        total_vol_fct=total_vol_fct.reset_index()#сброс индексного поля возникающего при группировке
        #План
        total_vol_pln = load_excel(full_dis, 'page_1', "a,b,c,d,e")
        total_vol_pln=total_vol_pln[(total_vol_pln.date>'15.01.2022') & (total_vol_pln.mark=='plan')]
        sum_vol_pln=total_vol_pln['volume'].sum()
        total_vol_pln=total_vol_pln.groupby(['date']).sum()
        total_vol_pln=total_vol_pln.reset_index()#сброс индексного поля возникающего при группировке
    else:
        #Факт
        total_vol_fct = load_excel(full_dis, 'page_1', "a,b,c,d,e")
        total_vol_fct=total_vol_fct[(total_vol_fct.port==sb_port) & (total_vol_fct.date<='15.01.2022') & (total_vol_fct.mark=='fact')]
        sum_vol_fct=total_vol_fct['volume'].sum()
        total_vol_fct=total_vol_fct.groupby(['date']).sum()
        total_vol_fct=total_vol_fct.reset_index()#сброс индексного поля возникающего при группировке
        #План
        total_vol_pln = load_excel(full_dis, 'page_1', "a,b,c,d,e")
        total_vol_pln=total_vol_pln[(total_vol_pln.port==sb_port) & (total_vol_pln.date>'15.01.2022') & (total_vol_pln.mark=='plan')]
        sum_vol_pln=total_vol_pln['volume'].sum()
        total_vol_pln=total_vol_pln.groupby(['date']).sum()
        total_vol_pln=total_vol_pln.reset_index()#сброс индексного поля возникающего при группировке
    
    col_1, col_2 = st.columns(2)
    with col_1:
        st.metric("Фактически поступило:", str(round(sum_vol_fct,0)) + " тн", "")
    
    with col_2:
        st.metric("Оставшийся план поступления:", str(round(sum_vol_pln,0)) + " тн", "")

    st.write("______________________________________________________________________________________________")
   
    source_fct = total_vol_fct
    source_pln = total_vol_pln
    st.write("План/Факт захода судов и объем поставленного накопленным итогом, тн")
    
    #Накопленный итог факт
    line_1=alt.Chart(source_fct).mark_area(color="green").transform_window(
        sort=[{'field': 'date'}],
        frame=[None, 0],
        cumulative='sum(volume)'
    ).encode(
        alt.X('date:T', title='дата прибытия судна',scale=alt.Scale(nice={'interval': 'day', 'step': 2})),
        alt.Y('cumulative:Q', title='объем накопл.итогом'),tooltip=["cumulative:Q","date"],opacity=alt.value(0.4)
    )
    #Посуточный факт
    bar_1 = alt.Chart(source_fct).mark_bar(size=30,color="red").encode(
    alt.X('date:T', title=None,scale=alt.Scale(nice={'interval': 'day', 'step': 2}),axis=alt.Axis(format="%d %m %y")),
    alt.Y('volume:Q',title=None),tooltip=["volume","date"]
    )
    #Подписи значений
    text_1 = bar_1.mark_text(align='center',baseline='middle',dy=-10,color="white").encode(text='volume:Q')
    #Посуточный план
    bar_2 = alt.Chart(source_pln).mark_bar(size=30).encode(
    alt.X('date:T', title=None,scale=alt.Scale(nice={'interval': 'day', 'step': 2}),axis=alt.Axis(format="%d %m %y")),
    alt.Y('volume:Q',title=None),tooltip=["volume","date"]
    )
    #Подписи значений
    text_2 = bar_2.mark_text(align='center',baseline='middle',dy=-10,color="white").encode(text='volume:Q')
   
    st.altair_chart((line_1+bar_1+text_1+bar_2+text_2).properties(width=1400,height=300))

    st.write("______________________________________________________________________________________________")
    
    #ПЕРЕВАЛКА Загружаем объемы
    st.header("Перевалка")
    if sb_port == 'Все': 
        total_vol = load_excel(full_dis, 'page_2', "a,c,d")
        total_vol=total_vol[(total_vol.date<='15.01.2022')]
        sum_vol_plan=total_vol['plan'].sum()
        sum_vol_fact=total_vol['fact'].sum()
        percent=sum_vol_fact/sum_vol_plan*100
    else:
        total_vol = load_excel(full_dis, 'page_2', "a,b,c,d")
        total_vol=total_vol[(total_vol.port==sb_port) & (total_vol.date<='15.01.2022')]
        sum_vol_plan=total_vol['plan'].sum()
        sum_vol_fact=total_vol['fact'].sum()
        percent=sum_vol_fact/sum_vol_plan*100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("План с нач.мес.:", str(round(sum_vol_plan,0)) + " тн", "")
    col2.metric("Факт с нач.мес.:", str(round(sum_vol_fact,0)) + " тн", "")
    col3.metric("Выполнение:", str(round(percent,2)) + " %", "")
    
    st.write("______________________________________________________________________________________________")

    #Загружаем План/факт накопленным итогом по выбранному заводу
    if sb_port == 'Все':  
        pf_vol = load_excel(full_dis, 'page_2', "a,b,e,f")
        pf_vol=pf_vol.groupby(['date']).sum()
        pf_vol=pf_vol.reset_index()#сброс индексного поля возникающего при группировке
        pf_vol['date']=pf_vol['date'].dt.tz_localize(tz='Europe/Moscow')
        vagon = load_excel(full_dis, 'page_5', "a,b,c")
    else:
        pf_vol = load_excel(full_dis, 'page_2', "a,b,e,f")
        pf_vol=pf_vol[(pf_vol.port==sb_port)]
        pf_vol['date']=pf_vol['date'].dt.tz_localize(tz='Europe/Moscow')
        vagon = load_excel(full_dis, 'page_4', "b,c,d,e")
        vagon = vagon[(vagon.port==sb_port)]
        vagon = vagon.reset_index()#сброс индексного поля возникающего при группировке
        
    col5, col6 = st.columns([3,1])
    col5.subheader("План/факт накопленным итогом с нач.мес., тн:")
    brush = alt.selection(type='interval', encodings=['x'])

    #Факт
    line_2 = alt.Chart(pf_vol).mark_line(size=5,color="red").encode(
    alt.X('date:T', title=None,scale=alt.Scale(nice={'interval': 'day', 'step': 2}),axis=alt.Axis(format="%d %m %y")),
    alt.Y('fact+:Q',title=None),tooltip=["fact+","date"]
    ).properties(width=1000,height=300)
    
    #План
    line_3 = alt.Chart(pf_vol).mark_area(size=3).encode(
    alt.X('date:T', title=None,scale=alt.Scale(nice={'interval': 'day', 'step': 2}),axis=alt.Axis(format="%d %m %y")),
    alt.Y('plan+:Q',title=None),tooltip=["plan+","date"]
    ).properties(width=1000,height=300)
    
    col5.altair_chart(line_3+line_2)
    
    if sb_port == 'Все':
        col6.subheader("Вып. плана по портам,%:")
        total = load_excel(full_dis, 'page_3', "a,d")
        source = total
        bar_5 = alt.Chart(source).mark_bar().encode(
        alt.Y('port', title=None),
        alt.X('total',title=None)).properties(width=300,height=300)
        
        text = bar_5.mark_text(dx=-15, color='white', align='center', baseline='middle').encode(
        text=alt.Text('total', format='.1f'))   
        
        d = {'col1': [percent], 'col2': ['Всего']}
        df = pd.DataFrame(data=d)
        line_3 = alt.Chart(df).mark_bar(size=5,color="red").encode(x='col1', y='col2')
        
        col6.altair_chart(bar_5+text+line_3)
    
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
    if sb_port == 'Все':  
        pf_vol = load_excel(full_dis, 'page_2', "a,b,c,d")
        pf_vol=pf_vol.groupby(['date']).sum()
        pf_vol=pf_vol.reset_index()#сброс индексного поля возникающего при группировке
        pf_vol['date']=pf_vol['date'].dt.tz_localize(tz='Europe/Moscow')
    else:
        pf_vol = load_excel(full_dis, 'page_2', "a,b,c,d")
        pf_vol=pf_vol[(pf_vol.port==sb_port)]
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
