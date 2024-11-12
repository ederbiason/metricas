import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Carregando os dados
data = pd.read_excel('tickets_TI_ficticios_varied_analistas.xlsx')

tipo_counts = data['Tipo'].value_counts()
st.title("Análise de Solicitações de TI")
st.subheader("Quantidade de Solicitações por Tipo")
fig, ax = plt.subplots()
tipo_counts.plot(kind='bar', ax=ax)
ax.set_xlabel("Tipo de Solicitação")
ax.set_ylabel("Quantidade")
ax.set_title("Quantidade de Solicitações por Tipo")
st.pyplot(fig)

urgencia_counts = data['Urgência'].value_counts()
st.subheader("Distribuição de Urgência das Solicitações")
fig, ax = plt.subplots()
ax.pie(urgencia_counts, labels=urgencia_counts.index, autopct='%1.1f%%', startangle=90)
ax.set_title("Distribuição de Urgência")
st.pyplot(fig)

# Contagem de status para solicitações e incidentes
status_counts = data['Status'].value_counts()

# Configuração do gráfico
st.subheader("Status das Solicitações e Incidentes")
fig, ax = plt.subplots()
status_counts.plot(kind='barh', color='salmon', ax=ax)  # 'barh' para barras horizontais
ax.set_xlabel("Quantidade")
ax.set_ylabel("Status")
ax.set_title("Status das Solicitações e Incidentes")
st.pyplot(fig)

data['Aberto em'] = pd.to_datetime(data['Aberto em'])
data['Mês/Ano'] = data['Aberto em'].dt.to_period('M')
mes_counts = data['Mês/Ano'].value_counts().sort_index()
st.subheader("Quantidade de Solicitações por Mês")
fig, ax = plt.subplots()
mes_counts.plot(kind='line', marker='o', ax=ax)
ax.set_xlabel("Mês/Ano")
ax.set_ylabel("Quantidade")
ax.set_title("Quantidade de Solicitações por Mês")
st.pyplot(fig)

# Processamento e criação de campos auxiliares
data['Aberto em'] = pd.to_datetime(data['Aberto em'])
data['Data de Fechamento'] = pd.to_datetime(data['Data de Fechamento'])
data['Mês/Ano'] = data['Aberto em'].dt.to_period('M')

# Remover registros sem data de fechamento para calcular tempo de resolução
data_fechadas = data.dropna(subset=['Data de Fechamento']).copy()
data_fechadas['Tempo de Resolução'] = (data_fechadas['Data de Fechamento'] - data_fechadas['Aberto em']).dt.days

# Gráfico 1: Tempo Médio de Resolução por Urgência
st.subheader("Tempo Médio de Resolução por Urgência")
urgencia_resolucao = data_fechadas.groupby('Urgência')['Tempo de Resolução'].mean()
fig1, ax1 = plt.subplots()
urgencia_resolucao.plot(kind='bar', color='skyblue', ax=ax1)
ax1.set_xlabel("Urgência")
ax1.set_ylabel("Tempo Médio de Resolução (dias)")
ax1.set_title("Tempo Médio de Resolução por Urgência")
st.pyplot(fig1)


st.title("Possíveis inconsistências")

data['Aberto em'] = pd.to_datetime(data['Aberto em'])
data['Data de Fechamento'] = pd.to_datetime(data['Data de Fechamento'])

# Problemas de Alocação ou Atribuição de recursos (profissionais) e até mesmo falha de comunicação 
st.subheader("Solicitações sem Analista Definido")
analista_na = data['Analista'].isna().sum()
analista_definido = len(data) - analista_na
fig1, ax1 = plt.subplots()
ax1.bar(['Definido', 'Não Definido'], [analista_definido, analista_na], color=['green', 'red'])
ax1.set_xlabel("Definição de Analista")
ax1.set_ylabel("Quantidade de Solicitações")
ax1.set_title("Distribuição de Solicitações por Definição de Analista")
st.pyplot(fig1)

# Isso pode indicar um problema de atraso na resolução ou priorização incorreta
#data_urgente_pendentes = data[(data['Urgência'] == 'Urgente') & (~data['Status'].isin(['Fechado', 'Em Progresso']))]
#percent_urgente_pendentes = (len(data_urgente_pendentes) / len(data[data['Urgência'] == 'Urgente'])) * 100
#fig1, ax1 = plt.subplots()
#ax1.bar(['Urgentes em Aberto ou\n em Progresso'], [percent_urgente_pendentes], color='orange')
#ax1.set_ylabel('Percentual (%)')
#ax1.set_title('Percentual de Serviços Urgentes Pendentes')
#ax1.set_ylim(0, 100)
#st.pyplot(fig1)

data_urgente_pendentes = data[(data['Urgência'] == 'Urgente') & (~data['Status'].isin(['Fechado', 'Em Progresso']))]
data_urgente_fechados = data[(data['Urgência'] == 'Urgente') & (data['Status'] == 'Fechado')]

# Percentuais de cada categoria
percent_urgente_pendentes = len(data_urgente_pendentes)
percent_urgente_fechados = len(data_urgente_fechados)
total_urgente = percent_urgente_pendentes + percent_urgente_fechados

# Calcular os percentuais relativos
sizes = [
    (percent_urgente_pendentes / total_urgente) * 100,
    (percent_urgente_fechados / total_urgente) * 100
]

labels = ['Urgentes Pendentes', 'Urgentes Fechados']
colors = ['orange', 'lightgreen']
explode = (0.1, 0)  # Destacar a primeira fatia (pendentes)

# Criar gráfico de pizza
fig1, ax1 = plt.subplots()
ax1.pie(
    sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
    explode=explode, shadow=True, wedgeprops={'edgecolor': 'black'}
)
ax1.set_title('Distribuição de Serviços Urgentes Pendentes vs Fechados')
ax1.axis('equal')  # Assegurar que o gráfico seja um círculo

# Mostrar o gráfico no Streamlit
st.pyplot(fig1)
