import streamlit as st

import pandas as pd

import numpy as np
import yfinance as yf

import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt

import datetime
from datetime import date, timedelta

plt.switch_backend('TkAgg')

def main():
    st.set_page_config(layout='wide')
    
    #calculando a tendência do papel escolhido e montando o mecânismo de compra e venda
    def tendencia():
        condicao_alta = (dados_papel['Close'] > dados_papel['MM1Simples']) & (dados_papel['Close'] > dados_papel['MM2Simples'])
        condicao_baixa = (dados_papel['Close'] < dados_papel['MM1Simples']) & (dados_papel['Close'] < dados_papel['MM2Simples'])
        
        dados_papel['Tendencia'] = np.where(condicao_alta,'Alta',np.where(condicao_baixa,'Baixa','Indefinida'))

    def btnCompra():
        
            # Cria botões para sim e não
                if st.sidebar.button("Sim"):
                    st.sidebar.write("Você clicou em 'Sim'!")
            # Coloque aqui a lógica ou ação a ser executada quando o usuário clicar em 'Sim'
                elif st.sidebar.button("Não"):
                    st.sidebar.write("Você clicou em 'Não'!")
            # Coloque aqui a lógica ou ação a ser executada quando o usuário clicar em 'Não'
    
    stock_list = ['TSLA','AAPL','VALE3.SA','PETR3.SA','WEGE3.SA','GOOG','ITUB4.SA','ALLD3.SA','CASH3.SA','BRAP4.SA']
    time_frames = ['Diário - 1d', '5 Dias - 5d','Semanal - 1wk','Mês - 1mo']
    lista_medias_principais = [0,5,8,9,10,15,19,20,30,35,50,60,80]
    
    hedcol1, hedcol2 = st.columns(2)
    
    with hedcol1:
        selecao_papel = st.selectbox('**Selecione abaixo o papel que deseja visualizar:** ', stock_list)
        papel_select = selecao_papel
        
        data_hoje = date.today()
        data_default = data_hoje - timedelta(days=10)
        data_start = st.date_input('**Selecione uma data início para plotagem do gráfico:** ', format='YYYY-MM-DD', value=data_default)
        
        select_mm2 = st.selectbox('**Selecione o periodo da segunda média simples que deseja inserir no gráfico:** ',lista_medias_principais)
        
    with hedcol2:
        periodo_grafico = str(st.selectbox('**Selecione um dos prazos para plotagem do gráfico:** ', time_frames))
        aux = periodo_grafico
        
        select_mm1 = st.selectbox('**Selecione o periodo da primeira média simples que deseja inserir no gráfico:** ',lista_medias_principais)
    
    intervalo_graph = aux.split('-')
    intervalo_final = intervalo_graph[1].strip()
    
    dados_papel = yf.download(papel_select, start=data_start, interval=intervalo_final)

    dados_papel.drop(['Adj Close'], axis=1, inplace=True)

    #criando uma média(mma) de 20 e 50 simples
    dados_papel['MM1Simples'] = dados_papel['Close'].rolling(window=select_mm1).mean()
    dados_papel['MM2Simples'] = dados_papel['Close'].rolling(window=select_mm2).mean()
    
    tendencia()
    
    col1, col2 = st.columns([1,1])
    st.title('Grafico da ação: {}'.format(papel_select))
    st.subheader('Gráfico de Candlesticks')
    
    with col1:
            
        # Coluna da esquerda com botões
        st.sidebar.title('Opções para o papel')
        botao1_compra = st.sidebar.button('Compra', use_container_width=True)
        st.write('') #espaço dos botões
        botao2_venda = st.sidebar.button('Venda', use_container_width=True)
        st.write('') #espaço 
        st.sidebar.subheader('Informações do papel:')
        st.sidebar.markdown(f"**Atual tendência do papel é possívelmente de:** {dados_papel['Tendencia'].iloc[-1]} ")
        
    with col2:
        
        
        figura = go.Figure(data=[go.Candlestick(
        name='Candles',
        x=dados_papel.index,
        open=dados_papel['Open'],
        high=dados_papel['High'],
        low=dados_papel['Low'],
        close=dados_papel['Close'] ), go.Scatter(x=dados_papel.index, y=dados_papel['MM1Simples'], line=dict(color='blue', width=2), name='Média movel de: {}'.format(select_mm1)),
                                      go.Scatter(x=dados_papel.index, y=dados_papel['MM2Simples'], line=dict(color='Orange', width=2), name='Média movel de: {}'.format(select_mm2)) ])

    figura.update_layout(xaxis_rangeslider_visible=False, autosize=True, width=1100, height=650)
    st.plotly_chart(figura, theme="streamlit", use_container_width=True)
    
    st.markdown(
        """
        **Observações:**
        A descrição de tendência do papel localizada no menu lateral é calculada de acordo com 
        as médias escolhidas pelo usuário, sendo estas as principais médias móveis utilizadas no mercado.
        Sendo mais recomendado acompanhar as flutuações do ativo nos prazos Diário, Semanal ou mensal,
        devido a volatilidade que o mercado pode provocar e impactar nas médias. E aconselhável trabalhar
        com uma média mais curta("rápida") e uma mais longa.
        
        **Observations:**
        The trend description of the paper located in the side menu is calculated according to the 
        averages chosen by the user, these being the main moving averages used in the market.
        It is more recommended to follow the fluctuations of the asset in the Daily, Weekly, or Monthly timeframes,
        due to the volatility that the market can cause and impact the averages. It is advisable to work
        with a shorter average ("fast") and a longer one.  
        """
    )      

if __name__ == '__main__':
    main()