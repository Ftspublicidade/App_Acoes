import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


def main():
    st.title("Analisando Ações - Fernanda Santos")
    st.image("dados.jpg")

    option = st.selectbox('Qual Empresa deseja analisar?', 
    ("Ibovespa","Via Varejo","Apple", "Petrobras"))

    if option == "Ibovespa":
        df = yf.Ticker("^BVSP").history(start= "2018-01-01")
        df = df.reset_index()
    elif option == "Via Varejo":
        df= yf.Ticker("VIIA3.SA").history(start= "2018-01-01")
        df = df.reset_index()
    elif option == "Apple":
        df = yf.Ticker("AAPL").history(start= "2018-01-01")
        df = df.reset_index()
    elif option == "Petrobras":
        df = yf.Ticker("PBR").history(start= "2018-01-01")
        df = df.reset_index()
    else:
        st.text("Seleção Inválida")

    st.text('Visualizando os Últimos registros do dataset...')
    slider = st.slider("Valores", 0,100)
    st.dataframe(df.tail(slider))

    # Análises

    st.header("Gráfico fechamento das ações")
    fig = px.line(df, x="Date", y="Close", title="Fechamento das ações", template="seaborn")
    st.plotly_chart(fig)

    # Dividendos
    dividendos = df.groupby(df["Date"].dt.year)["Dividends"].sum().reset_index()
    fig = px.line(dividendos, x="Date", y="Dividends", title="Dividendos Anuais ", 
    template="seaborn")
    st.write(fig)

    # Candlestick
    st.subheader("Gráfico de Candlestick, onde podemos analisar a oscilação entre a abertura e o fechamento, e se a ação fechou maior ou menor que o preço de abertura, para isso só analisar pela cor, os vermelhos fecharam com o preço menor do que o de abertura e os verdes fecharam com o preço maior do que o de abertura.")
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

    st.write(fig)

    csv = convert_df(df)
    st.download_button(
    label="Download dos dados em CSV",
    data=csv,
    file_name='large_df.csv',
    mime='text/csv',
)


if __name__ == '__main__':
    main()