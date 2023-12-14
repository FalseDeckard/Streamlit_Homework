import streamlit as st
import pandas as pd
import plotly as px

url = "https://raw.githubusercontent.com/FalseDeckard/Streamlit_Homework/main/clients.csv"
df = pd.read_csv(url, sep=";", index_col=0)

df['GENDER'] = df['GENDER'].replace({0: 'Мужчина', 1: 'Женщина'})
df['TARGET'] = df['TARGET'].replace({'Отклик не получен': 0, 'Отклик получен': 1})
df['SOCSTATUS_WORK_FL'] = df['SOCSTATUS_WORK_FL'].replace({0: 'Не работает', 1: 'Работает'})
df['SOCSTATUS_PENS_FL'] = df['SOCSTATUS_PENS_FL'].replace({0: 'Не пенсионер', 1: 'Пенсионер'})

df_num = df[['TARGET', 'AGE', 'CHILD_TOTAL', 'DEPENDANTS', 'PERSONAL_INCOME', 'LOAN_NUM_TOTAL', 'LOAN_NUM_CLOSED']]
df_no_targ_id = df.drop(["TARGET", "AGREEMENT_RK"], axis=1)
df_no_id = df.drop("AGREEMENT_RK", axis=1)

rus = {'GENDER': 'ПОЛ', 'AGE': 'ВОЗРАСТ', 'CHILD_TOTAL': 'КОЛ-ВО ДЕТЕЙ',
       'DEPENDANTS': 'КОЛ-ВО ИЖДИВЕНЦЕВ', 'PERSONAL_INCOME': 'ПЕРСОНАЛЬНЫЙ ДОХОД',
       'LOAN_NUM_TOTAL': 'КОЛ-ВО КРЕДИТОВ', 'LOAN_NUM_CLOSED': 'КОЛ-ВО ЗАКРЫТЫХ КРЕДИТОВ',
       'SOCSTATUS_WORK_FL': 'СОЦИАЛЬНЫЙ СТАТУС ОТНОСИТЕЛЬНО РАБОТЫ',
       'SOCSTATUS_PENS_FL': 'СОЦИАЛЬНЫЙ СТАТУС ОТНОСИТЕЛЬНО ПЕНСИИ',
       'AGREEMENT_RK': 'ID объекта', 'TARGET': 'ОТКЛИК НА МАРКЕТИНГОВУЮ КАМПАНИЮ'}


def on_rus(feature):
    return f'{feature} - {rus[feature]}'


def count_target(target_col):
    st.subheader('Распределение целевой переменной')
    fig = px.pie(df, names=target_col, title=f"Отклик клиента на маркетинговую кампанию банка {target_col}")
    st.plotly_chart(fig)

    st.write('Целевая переменная TARGET имеет дисбаланс в сторону отсутствия отклика (80%).')


def count_features(df):
    st.subheader('Распределение признаков')
    feature = st.selectbox("Выберите признак:", df.columns, format_func=on_rus, key='5')

    if feature == 'GENDER' or feature == 'SOCSTATUS_WORK_FL' or feature == 'SOCSTATUS_PENS_FL':
        fig = px.pie(df, names=feature, title=f"Распределение признака {feature}")
    else:
        fig = px.histogram(df, x=feature, nbins=30, title=f"Распределение признака {feature}")

    st.plotly_chart(fig)
    st.write('''
        - В датасете присутствуют два вещественных непрерывных признака: PERSONAL_INCOME и AGE;
        - Остальные признаки - категориальные, из них бинарные признаки: GENDER, SOCSTATUS_WORK_FL, SOCSTATUS_PENS_FL.
    ''')


def matrix(df):
    st.subheader('Матрица корреляции признаков')
    fig = px.imshow(df.corr(), title='Матрица корреляции признаков', labels=dict(x="Признаки", y="Признаки"))
    st.plotly_chart(fig)
    st.write('''
        - Наиболее скоррелированные пары признаков: LOAN_NUM_TOTAL - LOAN_NUM_CLOSED 
        и CHILD_TOTAL и DEPENDANTS;
        - Наименее скоррелированные пары признаков: LOAN_NUM_CLOSED - CHILD_TOTAL и LOAN_NUM_CLOSED - AGE;
        - Целевая переменная TARGET слабо коррелирует с признаками.
    ''')


def info(df):
    st.subheader('Числовые характеристики признаков')
    feature = st.selectbox("Выберите признак:", df.columns, format_func=on_rus, key='2')
    st.write(df[feature].describe())


def diagram_feature(df):
    st.subheader('Попарные распределения признаков')
    feature_1 = st.selectbox("Выберите первый признак:", df.columns, format_func=on_rus, key='7')
    feature_2 = st.selectbox("Выберите второй признак:", df.columns, format_func=on_rus, key='8')

    fig = px.scatter(df, x=feature_1, y=feature_2, title=f"Диаграмма рассеяния для пары {feature_1} - {feature_2}")
    st.plotly_chart(fig)
    st.write('''
        - Некоторые признаки имеют отрицательную линейную зависимость - CHILD_TOTAL/PERSONAL_INCOME 
        и CHILD_TOTAL И LOAN_NUM_TOTAL;
        - Некоторые связаны напрямую и потому показывают положительную линейную зависимость - CHILD_TOTAL/DEPENDANTS ;
        - Какие-то не имеют четкой зависимости: AGE/LOAN_NUM_TOTAL.
    ''')




def diagram_with_target(df):
    st.subheader('Распределение целевой переменной в зависимости от признаков')
    feature = st.selectbox("Выберите признак:", df.columns, format_func=on_rus, key='6')

    if feature == 'PERSONAL_INCOME' or feature == 'AGE':
        fig = px.histogram(df, x=feature, color='TARGET', nbins=30, title=f"Распределение целевой переменной TARGET относительно {feature}")
    else:
        fig = px.bar(df, x=feature, color='TARGET', title=f"Распределение целевой переменной TARGET относительно {feature}")

    st.plotly_chart(fig)
    st.write('''
        - Можно сказать, что с уменьшением дискретных значений для категориальных признаков 
        наблюдается увеличение вероятности отклика или отсутствия отклика;
        - Чем меньше PERSONAL_INCOME, тем больше даты по таким клиентам;
        - Для AGE высокие показатели по отклику/отсутствию отклика приходятся с 22 лет до 40 лет - основная целевая аудитория.
    ''')
       
def boxplot_feature(df):
    st.subheader('Ящики с усами для выбранных признаков')
    feature_1 = st.selectbox("Выберите первый признак:", df.columns, format_func=on_rus, key='10')
    feature_2 = st.selectbox("Выберите второй признак:", df.columns, format_func=on_rus, key='11')

    fig = px.box(df, x=feature_1, y=feature_2, title=f"Ящики с усами для пары {feature_1} - {feature_2}")
    st.plotly_chart(fig)

if __name__ == "__main__":
    st.title('EDA предобработанных данных клиентов банка')
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader('Исследуем признаки и их взаимосвязь с целевой переменной, '
                 'числовые характеристики признаков, корреляцию признаков и т.д.')
    st.write('Исходные данные - база данных с информацией о клиентах банка и их персональных данных, '
             'таких как пол, количество детей и т.д.')
    st.info(''' Таблица с данными состоит из:
    - AGREEMENT_RK — уникальный идентификатор объекта в выборке;
    - TARGET — целевая переменная: отклик на маркетинговую кампанию (1 — отклик был зарегистрирован, 0 — отклика не было);
    - AGE — возраст клиента;
    - SOCSTATUS_WORK_FL — социальный статус клиента относительно работы (1 — работает, 0 — не работает);
    - SOCSTATUS_PENS_FL — социальный статус клиента относительно пенсии (1 — пенсионер, 0 — не пенсионер);
    - GENDER — пол клиента (1 — мужчина, 0 — женщина);
    - CHILD_TOTAL — количество детей клиента;
    - DEPENDANTS — количество иждивенцев клиента;
    - PERSONAL_INCOME — личный доход клиента (в рублях);
    - LOAN_NUM_TOTAL — количество ссуд клиента;
    - LOAN_NUM_CLOSED — количество погашенных ссуд клиента.
                    ''')
       
    st.markdown("<br><br>", unsafe_allow_html=True)
    count_features(df_no_targ_id)

    st.markdown("<br><br>", unsafe_allow_html=True)
    info(df_no_id)

    st.markdown("<br><br>", unsafe_allow_html=True)
    count_target("TARGET")   
       
    st.markdown("<br><br>", unsafe_allow_html=True)
    diagram_feature(df_no_targ_id)

    st.markdown("<br><br>", unsafe_allow_html=True)
    diagram_with_target(df_no_id)

    st.markdown("<br><br>", unsafe_allow_html=True)
    matrix(df_num)
       
    st.markdown("<br><br>", unsafe_allow_html=True)
    boxplot_feature(df)
