import streamlit as st
import pandas as pd

import numpy as np
import yfinance as yf
import mplfinance as mpl

import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

import numpy as np
import yfinance as yf
#import mplfinance as mpl

#import plotly.express as px
import plotly.graph_objects as go
#import seaborn as sns
import matplotlib.pyplot as plt

import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from xgboost import XGBRegressor

plt.switch_backend('TkAgg')

st.set_page_config(layout='wide', page_title='Prever Preço Ação', page_icon='🧠')

st.write('Pagina para montar um sistema de predict dos preços de ações 🧠')

stock_list = ['TSLA','AAPL','VALE3.SA','PETR3.SA','WEGE3.SA','GOOG','ITUB4.SA','ALLD3.SA','CASH3.SA','BRAP4.SA']
metrica_rmse = 0
mensagem = "" 

headCol1, headCol2 = st.columns(2)

with headCol1:
    
    papel_select = st.selectbox('**Selecione abaixo o papel que deseja realizar um teste de Predict do preço:** ', stock_list)
    
    btn_predict = st.button('Realizar Predição', use_container_width=True)
    
    dados_papel_base = yf.download(papel_select, start='2023-01-01', interval='1d', rounding=True)
    dados_papel_predict = yf.download(papel_select, start='2022-01-01', interval='1d', rounding=True)
    dados_papel_predict.drop(['Adj Close'], axis = 1, inplace=True)
    dados_papel_predict['Close_Tomorrow'] = dados_papel_predict['Close'].shift(-1)
    dados_papel_predict.dropna(inplace=True)
    
    if btn_predict:
        
        # Dividir os dados em treinamento e teste
        train_size = int(0.8 * len(dados_papel_predict))
        train_data = dados_papel_predict[:train_size]
        test_data = dados_papel_predict[train_size:]

        # Selecionar as características (features) relevantes
        features = ['Open', 'High', 'Low', 'Close', 'Volume']
        target = 'Close_Tomorrow'

        X_train = train_data[features]
        y_train = train_data[target]
        X_test = test_data[features]
        y_test = test_data[target]

        # Treinar o modelo XGBoost
        model = XGBRegressor(max_depth=1, learning_rate = 0.09)
        model.fit(X_train, y_train)

        # Fazer previsões
        y_pred = model.predict(X_test)

        # Avaliar o desempenho do modelo após o treinamento
        metrica_rmse = np.sqrt(mean_squared_error(y_test, y_pred, squared=False))
        
        ## Código para realizar a predição para o fechamento do próximo dia de pregão

        #pego a última linha de pregão registrada ou algum outro ultimo resultado
        ultimo_fechamento = dados_papel_base.iloc[[-1]]
        ultimo_fechamento_list = [ultimo_fechamento[feature] for feature in features]

        # Fazer a previsão para o próximo fechamento
        predict_prox_fechamento = model.predict(np.array(ultimo_fechamento_list).reshape(1, -1))
        previsao_prox_fech = predict_prox_fechamento
        print(previsao_prox_fech)
        
        #mostrar o valor previsto
        mensagem = "Previsão para o próximo fechamento:**{:.2f}**".format(predict_prox_fechamento[0])

ultimo_fechamento = dados_papel_base['Close'].iloc[-1]

with headCol2:
    st.write("**Dados e Resultados:** ")
    st.write("Último fechamento: **{}**".format(ultimo_fechamento))
    st.write("Métrica RMSE (Desempenho do algoritmo na previsão): **{:.2f}**".format(metrica_rmse))
    st.write(mensagem)
    st.write("**Observações:**")
    
st.markdown("""
        <p style="text-align: justify">        
        A predição realizada acima é baseada no algoritmo XGBoost usado na forma de regressão, 
        a métrica RSME(Root Mean Squared Error - Raiz quadrada do erro-médio) foi a forma utilizada
        para indicar a performance do algoritmo de acordo com o papel selecionado, resumindo o uso 
        dessa métrica: quanto menor for o valor indica que o treinamento do algoritmo com os dados históricos
        do papel foi melhor desenvolvido, o que pode levar a uma previsão do próximo fechamento mais precisa.
        
        The prediction performed above is based on the XGBoost algorithm used 
        in the form of regression, the RSME (Root Mean Squared Error) metric was used 
        to indicate the algorithm's performance according to the selected paper, 
        summarizing the use of this metric: the lower the value indicates that the algorithm's
        training with the paper's historical data was better developed, which can lead to a more 
        accurate prediction of the next close.

        </p>
    """,unsafe_allow_html=True)
    
st.write('**Gráfico da Ação para visualizar as últimas cotações: (Gráfico Diário)** ')
figura = go.Figure(data=[go.Candlestick(
        name='Candles',
        x=dados_papel_base.index,
        open=dados_papel_base['Open'],
        high=dados_papel_base['High'],
        low=dados_papel_base['Low'],
        close=dados_papel_base['Close'] ) ])

figura.update_layout(xaxis_rangeslider_visible=False, autosize=True, width=1100, height=650)
st.plotly_chart(figura, theme="streamlit", use_container_width=True)


st.markdown("""
        <p style="text-align: justify">
            <b> Observações Importantes:</b>
            Para este teste de predict foi utilizado o algoritmo XGBoost no modelo de Regressor(regressão), utilizando
            dados históricos de uma ação no formato OHLC(open,high,low e close), foi realizado pequenas adaptações
            na estrutura do data frame para realizar a previsão do próximo fechamento.
        </p>

        <p style="text-align: justify">
            <b> Lembrando que este exemplo é meramente de cunho voltado para aprendizado, não é feita nenhuma recomendação 
            de compra ou venda de ativos, os ativos utilizados na lista foram adicionados aleatoriamente para representar
            uma mera lista de ações brasileiras e americanas a fim de testar a eficiência do algoritmo.</b>
        </p>
        
        <p style="text-align: justify">
            <b> Important observations: </b> 
            For this prediction test, the XGBoost algorithm was used in the Regression model, 
            using historical data of a stock in the OHLC format (open, high, low, and close), 
            minor adaptations were made to the structure of the data frame to predict the next close.
        </p>

        <p style="text-align: justify">
            <b> Remember that this example is purely for learning purposes. 
            No recommendation is made to buy or sell assets. The assets used in the list 
            were added randomly to represent a mere list of Brazilian and American stocks 
            to test the efficiency of the algorithm. </b>
        </p>
        
        """,unsafe_allow_html=True)
>>>>>>> a02234b (projetoFinance)
