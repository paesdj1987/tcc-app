# graficos.py

import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go  

def prepare_data():
    # Conectar ao banco de dados
    conn = sqlite3.connect('suap23.db')

    # Ler as tabelas necessárias
    AlunosSuperior = pd.read_sql_query("SELECT * FROM AlunosSuperior", conn)
    ComDeficiencia = pd.read_sql_query("SELECT * FROM ComDeficiencia", conn)
    EnsinoAnterior_Privado = pd.read_sql_query("SELECT * FROM EnsinoAnterior_Privado", conn)
    EnsinoAnterior_Publico = pd.read_sql_query("SELECT * FROM EnsinoAnterior_Publico", conn)
    DeficienciaAuditiva = pd.read_sql_query("SELECT * FROM DeficienciaAuditiva", conn)
    DeficienciaAuditiva_Surdo = pd.read_sql_query("SELECT * FROM DeficienciaAuditiva_Surdo", conn)
    DeficienciaFisica = pd.read_sql_query("SELECT * FROM DeficienciaFisica", conn)
    DeficienciaIntelectual = pd.read_sql_query("SELECT * FROM DeficienciaIntelectual", conn)
    DeficienciaVisual = pd.read_sql_query("SELECT * FROM DeficienciaVisual", conn)
    DeficienciaVisual_BaixaVisao = pd.read_sql_query("SELECT * FROM DeficienciaVisual_BaixaVisao", conn)
    DeficienciaVisual_Cegueira = pd.read_sql_query("SELECT * FROM DeficienciaVisual_Cegueira", conn)
    TEA = pd.read_sql_query("SELECT * FROM TEA", conn)
    CorRaca_Outra = pd.read_sql_query("SELECT * FROM CorRaca_Outra", conn)
    CorRaca_Parda = pd.read_sql_query("SELECT * FROM CorRaca_Parda", conn)
    CorRaca_Preta = pd.read_sql_query("SELECT * FROM CorRaca_Preta", conn)
    CorRaca_NaoDeclarado = pd.read_sql_query("SELECT * FROM CorRaca_NaoDeclarado", conn)
    CorRaca_Branca = pd.read_sql_query("SELECT * FROM CorRaca_Branca", conn)
    CorRaca_Amarela = pd.read_sql_query("SELECT * FROM CorRaca_Amarela", conn)
    CorRaca_Indigena = pd.read_sql_query("SELECT * FROM CorRaca_Indigena", conn)
    Periodo_Primeiro = pd.read_sql_query("SELECT * FROM Periodo_Primeiro", conn)
    Periodo_Segundo = pd.read_sql_query("SELECT * FROM Periodo_Segundo", conn)
    Periodo_Terceiro = pd.read_sql_query("SELECT * FROM Periodo_Terceiro", conn)
    Periodo_Quarto = pd.read_sql_query("SELECT * FROM Periodo_Quarto", conn)
    Periodo_Quinto = pd.read_sql_query("SELECT * FROM Periodo_Quinto", conn)
    Periodo_Sexto = pd.read_sql_query("SELECT * FROM Periodo_Sexto", conn)
    Periodo_Setimo = pd.read_sql_query("SELECT * FROM Periodo_Setimo", conn)
    Periodo_Oitavo = pd.read_sql_query("SELECT * FROM Periodo_Oitavo", conn)
    Periodo_Nono = pd.read_sql_query("SELECT * FROM Periodo_Nono", conn)
    Periodo_Decimo = pd.read_sql_query("SELECT * FROM Periodo_Decimo", conn)

    conn.close()

    # Selecionando apenas as colunas desejadas de ComDeficiencia
    ComDeficiencia_reduzida = ComDeficiencia[['Nome']]

    # Join entre as tabelas AlunosSuperior e ComDeficiencia = mescla_1
    mescla_1 = AlunosSuperior.merge(ComDeficiencia_reduzida, on='Nome', how='left', indicator=True)
    # Inserir a coluna 'Com Deficiencia?'
    mescla_1['Com Deficiencia?'] = mescla_1['_merge'].apply(lambda x: 'Sim' if x == 'both' else 'Não')
    # Remover a coluna auxiliar '_merge'
    mescla_1.drop(columns=['_merge'], inplace=True)

    # Tratando as tabelas EnsinoAnterior_Privado e EnsinoAnterior_Publico = mescla_2
    EnsinoAnterior_Privado['EnsinoAnterior'] = 'Privado'
    EnsinoAnterior_Publico['EnsinoAnterior'] = 'Publico'

    mescla_2_com_duplicadas = pd.concat([EnsinoAnterior_Privado, EnsinoAnterior_Publico], ignore_index=True)
    mescla_2 = mescla_2_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # Join entre as tabelas mescla_1 e mescla_2 = mescla_3
    mescla_3_com_duplicadas = mescla_1.merge(mescla_2[['Nome', 'EnsinoAnterior']], on='Nome', how='left')
    mescla_3 = mescla_3_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # Tratando a tabela DeficienciaAuditiva
    DeficienciaAuditiva['É Deficiente Auditivo?'] = 'Sim'

    # Join entre mescla_3 e DeficienciaAuditiva = mescla_4
    mescla_4_com_duplicadas = mescla_3.merge(DeficienciaAuditiva[['Nome', 'É Deficiente Auditivo?']], on='Nome', how='left')
    mescla_4 = mescla_4_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # Continue com o mesmo padrão para as demais tabelas de deficiência

    # DeficienciaAuditiva_Surdo
    DeficienciaAuditiva_Surdo['É Deficiente Auditivo e Surdo?'] = 'Sim'
    mescla_5_com_duplicadas = mescla_4.merge(DeficienciaAuditiva_Surdo[['Nome', 'É Deficiente Auditivo e Surdo?']], on='Nome', how='left')
    mescla_5 = mescla_5_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # DeficienciaFisica
    DeficienciaFisica['É Deficiente Fisico?'] = 'Sim'
    mescla_6_com_duplicadas = mescla_5.merge(DeficienciaFisica[['Nome', 'É Deficiente Fisico?']], on='Nome', how='left')
    mescla_6 = mescla_6_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # DeficienciaIntelectual
    DeficienciaIntelectual['É Deficiente Intelectual?'] = 'Sim'
    mescla_7_com_duplicadas = mescla_6.merge(DeficienciaIntelectual[['Nome', 'É Deficiente Intelectual?']], on='Nome', how='left')
    mescla_7 = mescla_7_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # DeficienciaVisual
    DeficienciaVisual['É Deficiente Visual?'] = 'Sim'
    mescla_8_com_duplicadas = mescla_7.merge(DeficienciaVisual[['Nome', 'É Deficiente Visual?']], on='Nome', how='left')
    mescla_8 = mescla_8_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # DeficienciaVisual_BaixaVisao
    DeficienciaVisual_BaixaVisao['É Deficiente Visual e tem Baixa Visao?'] = 'Sim'
    mescla_9_com_duplicadas = mescla_8.merge(DeficienciaVisual_BaixaVisao[['Nome', 'É Deficiente Visual e tem Baixa Visao?']], on='Nome', how='left')
    mescla_9 = mescla_9_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # DeficienciaVisual_Cegueira
    DeficienciaVisual_Cegueira['É Deficiente Visual e tem Cegueira?'] = 'Sim'
    mescla_10_com_duplicadas = mescla_9.merge(DeficienciaVisual_Cegueira[['Nome', 'É Deficiente Visual e tem Cegueira?']], on='Nome', how='left')
    mescla_10 = mescla_10_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # TEA
    TEA['É TEA?'] = 'Sim'
    mescla_11_com_duplicadas = mescla_10.merge(TEA[['Nome', 'É TEA?']], on='Nome', how='left')
    mescla_11 = mescla_11_com_duplicadas.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # Tratando as tabelas de Cor/Raca e fazendo o Join com mescla_11 = mescla_12
    def add_cor_raca(df, cor):
        df['Cor_Raca'] = cor
        return df

    CorRaca_Outra = add_cor_raca(CorRaca_Outra, 'Outra')
    CorRaca_Parda = add_cor_raca(CorRaca_Parda, 'Parda')
    CorRaca_Preta = add_cor_raca(CorRaca_Preta, 'Preta')
    CorRaca_NaoDeclarado = add_cor_raca(CorRaca_NaoDeclarado, 'NaoDeclarado')
    CorRaca_Branca = add_cor_raca(CorRaca_Branca, 'Branca')
    CorRaca_Amarela = add_cor_raca(CorRaca_Amarela, 'Amarela')
    CorRaca_Indigena = add_cor_raca(CorRaca_Indigena, 'Indigena')

    cor_raca_concatenado = pd.concat([CorRaca_Outra, CorRaca_Parda, CorRaca_Preta, CorRaca_NaoDeclarado, CorRaca_Branca, CorRaca_Amarela, CorRaca_Indigena], ignore_index=True)

    mescla_12 = mescla_11.merge(cor_raca_concatenado[['Nome', 'Cor_Raca']], on='Nome', how='left')
    mescla_12 = mescla_12.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # Tratando as tabelas de Período e fazendo o Join com mescla_12 = mescla_13
    def add_periodo(df, periodo):
        df['Periodo'] = periodo
        return df

    Periodo_Primeiro = add_periodo(Periodo_Primeiro, '1')
    Periodo_Segundo = add_periodo(Periodo_Segundo, '2')
    Periodo_Terceiro = add_periodo(Periodo_Terceiro, '3')
    Periodo_Quarto = add_periodo(Periodo_Quarto, '4')
    Periodo_Quinto = add_periodo(Periodo_Quinto, '5')
    Periodo_Sexto = add_periodo(Periodo_Sexto, '6')
    Periodo_Setimo = add_periodo(Periodo_Setimo, '7')
    Periodo_Oitavo = add_periodo(Periodo_Oitavo, '8')
    Periodo_Nono = add_periodo(Periodo_Nono, '9')
    Periodo_Decimo = add_periodo(Periodo_Decimo, '10')

    periodo_concatenado = pd.concat([Periodo_Primeiro, Periodo_Segundo, Periodo_Terceiro, Periodo_Quarto, Periodo_Quinto,
                                     Periodo_Sexto, Periodo_Setimo, Periodo_Oitavo, Periodo_Nono, Periodo_Decimo], ignore_index=True)

    mescla_13 = mescla_12.merge(periodo_concatenado[['Nome', 'Periodo']], on='Nome', how='left')
    mescla_13 = mescla_13.drop_duplicates(subset=['Nome', 'Curso', 'Situacao no Curso', 'Situacao no Ultimo Periodo'])

    # Inserindo a coluna "Semestre Ingresso" e tratando a coluna Curso
    mescla_13['Matricula'] = mescla_13['Matricula'].astype(str)
    mescla_13['Semestre Ingresso'] = mescla_13['Matricula'].str.slice(0, 5)
    # Reordenando as colunas
    colunas = mescla_13.columns.tolist()
    colunas.insert(0, colunas.pop(colunas.index('Semestre Ingresso')))
    mescla_13 = mescla_13[colunas]
    # Removendo prefixo numérico do nome do curso
    mescla_13['Curso'] = mescla_13['Curso'].str.replace(r'^\d+ - ', '', regex=True)
    mescla_13['Semestre Ingresso'] = mescla_13['Semestre Ingresso'].astype(int)
    # Removendo semestres indesejados
    mescla_13 = mescla_13[~mescla_13['Semestre Ingresso'].isin([20241, 2024, 20233])]

    # Tratando linhas com 'Cancelamento Compulsorio'
    duplicated_rows = mescla_13[mescla_13.duplicated(subset=['Nome', 'Curso'], keep=False)]
    cancelamento_compulsorio = duplicated_rows[duplicated_rows['Situacao no Ultimo Periodo'] == 'Cancelamento Compulsorio']
    indices_to_drop = cancelamento_compulsorio.index
    mescla_13 = mescla_13.drop(indices_to_drop)
    mescla_13.reset_index(drop=True, inplace=True)
    # Removendo '(Salvador)' da coluna Curso
    mescla_13['Curso'] = mescla_13['Curso'].str.replace(r' \(Salvador\)', '', regex=True)

    # O DataFrame final é mescla_13
    mescla_final = mescla_13.copy()

    return mescla_final

# Preparando os dados uma vez ao importar o módulo
mescla_final = prepare_data()

# gráfico 1

import plotly.graph_objects as go

def grafico_1():
    # Preparar os dados
    df3 = pd.DataFrame(mescla_final)

    # Calcular a quantidade total de evasão por curso
    evasao_por_curso = df3[df3['Situacao no Curso'] == 'Evasao'].groupby('Curso').size().reset_index(name='Total Evasao')

    # Calcular a quantidade de alunos com deficiência por curso
    deficiencia_sim_por_curso = df3[df3['Com Deficiencia?'] == 'Sim'].groupby('Curso').size().reset_index(name='Total Com Deficiencia')

    # Mesclar os dados
    resultado5 = evasao_por_curso.merge(deficiencia_sim_por_curso, on='Curso')

    # Calcular o percentual de alunos com deficiência em relação ao total de evasão
    resultado5['Percentual Deficiencia (%)'] = (resultado5['Total Com Deficiencia'] / resultado5['Total Evasao']) * 100

    # Ordenar os cursos pelo percentual de deficiência
    resultado5 = resultado5.sort_values(by='Percentual Deficiencia (%)', ascending=True)

    # Criar o gráfico usando Plotly
    fig = go.Figure()

    # Adicionar as barras horizontais com hover de valor absoluto
    fig.add_trace(go.Bar(
        x=resultado5['Percentual Deficiencia (%)'],
        y=resultado5['Curso'],
        orientation='h',
        text=resultado5['Percentual Deficiencia (%)'].round(2).astype(str) + '%',
        textposition='outside',
        marker=dict(
            color=resultado5['Percentual Deficiencia (%)'],
            colorscale='Blues',
            line=dict(color='black', width=1)
        ),
        hovertemplate=
            "<b>Curso:</b> %{y}<br>" +
            "<b>Percentual Deficiência:</b> %{x:.2f}%<br>" +
            "<b>Total Evasões:</b> %{customdata[0]}<br>" +
            "<b>Total com Deficiência:</b> %{customdata[1]}",
        customdata=resultado5[['Total Evasao', 'Total Com Deficiencia']].values  # Passa os valores absolutos
    ))


    # Configurar o layout do gráfico
    fig.update_layout(
        title='Percentual de Deficiência em Relação à Evasão por Curso - 2023.2',
        xaxis_title='Percentual de Deficiência (%)',
        yaxis_title='Curso',
        template='plotly_white',
        title_font=dict(size=18, family='Arial'),
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        margin=dict(l=100, r=50, t=50, b=50)
    )

    return fig


# gráfico 2

def grafico_2():
    # Preparar os dados
    df4 = pd.DataFrame(mescla_final)

    # Filtrar por 'Evasao' na "Situacao no Curso"
    df_evasao2 = df4[df4['Situacao no Curso'] == 'Evasao']

    # Agrupar por 'Curso' e contar evasões por 'Periodo'
    resultado6 = df_evasao2.groupby(['Curso', 'Periodo']).size().unstack(fill_value=0)

    # Adicionar coluna com o total de evasões por curso
    resultado6['Total Evasoes'] = resultado6.sum(axis=1)

    # Redefinir o índice para que 'Curso' apareça como coluna na visualização
    resultado6 = resultado6.reset_index()

    # Garantir que todos os períodos estão presentes como colunas
    periodos = [str(i) for i in range(1, 11)]
    resultado6 = resultado6.reindex(columns=['Curso'] + periodos + ['Total Evasoes'], fill_value=0)

    # Renomear colunas dos períodos para 'Periodo 1', etc.
    resultado6.columns = ['Curso'] + [f'Periodo {i}' for i in range(1, 11)] + ['Total Evasoes']

    # Transformar o DataFrame para formato longo
    resultado6_melted = resultado6.melt(
        id_vars=['Curso'],
        value_vars=[f'Periodo {i}' for i in range(1, 11)],
        var_name='Período',
        value_name='Quantidade'
    )

    # Criar o gráfico de barras empilhadas horizontais usando Plotly
    fig = go.Figure()

    # Garantir a ordem dos períodos
    periodos = [f'Periodo {i}' for i in range(1, 11)]

    # Adicionar barras para cada período
    for periodo in periodos:
        dados_periodo = resultado6_melted[resultado6_melted['Período'] == periodo]
        fig.add_trace(go.Bar(
            y=dados_periodo['Curso'],
            x=dados_periodo['Quantidade'],
            name=periodo,
            orientation='h',
            text=dados_periodo['Quantidade'],
            textposition='inside',
            hovertemplate=(
                "<b>Curso:</b> %{y}<br>" +
                "<b>Período:</b> " + periodo + "<br>" +
                "<b>Evasões:</b> %{x} alunos<extra></extra>"
            ),
            marker=dict(line=dict(width=0.5, color='black'))
        ))

    # Configurar o layout do gráfico
    fig.update_layout(
        title='Número de Evasões por Período e Curso - 2023.2',
        xaxis_title='Número de Evasões',
        yaxis_title='Curso',
        barmode='stack',
        template='plotly_white',
        title_font=dict(size=18, family='Arial'),
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        legend=dict(
            title='Período',
            title_font=dict(size=12),
            font=dict(size=12),
            orientation='h',
            x=0.5,
            xanchor='center',
            y=-0.2,
            traceorder='normal'  # Mantém a ordem dos períodos
        ),
        margin=dict(l=100, r=50, t=50, b=100)
    )

    return fig


# grafico 3

def grafico_3():
    # Preparar os dados
    df = pd.DataFrame(mescla_final)

    # Filtrar por 'Evasao' na "Situacao no Curso"
    df_evasao3 = df[df['Situacao no Curso'] == 'Evasao']

    # Agrupar por 'Semestre Ingresso' e contar evasões por 'Periodo'
    resultado7 = df_evasao3.groupby(['Semestre Ingresso', 'Periodo']).size().unstack(fill_value=0)

    # Adicionar coluna com o total de evasões por Semestre
    resultado7['Total Evasoes'] = resultado7.sum(axis=1)

    # Redefinir o índice para que 'Semestre Ingresso' apareça
    resultado7 = resultado7.reset_index()

    # Garantir que todos os períodos de 1 a 10 estão presentes como colunas
    periodos = [str(i) for i in range(1, 11)]
    resultado7 = resultado7.reindex(columns=['Semestre Ingresso'] + periodos + ['Total Evasoes'], fill_value=0)

    # Renomear colunas dos períodos para 'Periodo 1', etc.
    resultado7.columns = ['Semestre Ingresso'] + [f'Periodo {i}' for i in range(1, 11)] + ['Total Evasoes']

    # Adicionar coluna de percentual sobre a coluna "Total Evasoes"
    resultado7['Percentual Evasoes'] = (resultado7['Total Evasoes'] / resultado7['Total Evasoes'].sum()) * 100
    resultado7['Percentual Evasoes'] = resultado7['Percentual Evasoes'].round(2)

    # Preparar os dados para o gráfico
    semestres = resultado7['Semestre Ingresso'].astype(str)
    evasoes = resultado7['Total Evasoes']
    percentuais = resultado7['Percentual Evasoes']

    # Criar o gráfico de barras horizontais usando Plotly
    fig = go.Figure()

    fig.add_trace(go.Bar(
    y=semestres,
    x=evasoes,
    orientation='h',
    text=percentuais.apply(lambda x: f"{x:.2f}%"),
    textposition='outside',
    marker=dict(color='lightblue', line=dict(color='black', width=1)),
    hovertemplate=
        "<b>Semestre de Ingresso:</b> %{y}<br>" +
        "<b>Total de Evasões:</b> %{x}<br>" +
        "<b>Percentual de Evasões:</b> %{customdata:.2f}%",
    customdata=percentuais  # Passa os percentuais de evasão como dados adicionais
    ))


    # Configurar o layout do gráfico
    fig.update_layout(
        title='Total de Evasões por Semestre de Ingresso - 2023.2',
        xaxis_title='Total de Evasões',
        yaxis_title='Semestre de Ingresso',
        template='plotly_white',
        title_font=dict(size=18, family='Arial'),
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        margin=dict(l=100, r=50, t=50, b=50),
        plot_bgcolor='#F5F5F5',
        paper_bgcolor='white'
    )

    return fig


# grafico 4

import plotly.graph_objects as go
import numpy as np

def grafico_4():
    # Passo 1: Preparar os dados
    total_alunos = mescla_final.groupby(['Curso', 'Cor_Raca']).size().reset_index(name='Total')
    evasao_alunos = mescla_final[mescla_final['Situacao no Curso'] == 'Evasao']
    evasao_counts = evasao_alunos.groupby(['Curso', 'Cor_Raca']).size().reset_index(name='Evasao')
    resultado = pd.merge(total_alunos, evasao_counts, on=['Curso', 'Cor_Raca'], how='left')
    resultado['Evasao'] = resultado['Evasao'].fillna(0).astype(int)

    # Pivotar os dados
    categorias_cor_raca = ['Amarela', 'Branca', 'Indigena', 'NaoDeclarado', 'Outra', 'Parda', 'Preta']
    pivot_percent = resultado.pivot_table(index='Curso', columns='Cor_Raca', values='Evasao', aggfunc='sum').fillna(0)
    pivot_total = resultado.pivot_table(index='Curso', columns='Cor_Raca', values='Total', aggfunc='sum').fillna(0)
    percentuais = (pivot_percent / pivot_total).fillna(0) * 100

    # Ajustar os índices e colunas
    percentuais = percentuais.reindex(columns=categorias_cor_raca).fillna(0)
    pivot_percent = pivot_percent.reindex(columns=categorias_cor_raca).fillna(0)

    # Posições no eixo X
    cursos = percentuais.index.tolist()

    # Paleta de cores
    colors = px.colors.qualitative.Set3

    # Inicializar gráfico
    fig = go.Figure()

    # Acumulador para barras empilhadas
    bottom_values = np.zeros(len(cursos))

    # Criar as barras empilhadas
    for i, cor in enumerate(categorias_cor_raca):
        percent_values = percentuais[cor].values
        evasao_values = pivot_percent[cor].values

        fig.add_trace(go.Bar(
            x=cursos,
            y=percent_values,
            name=cor,
            text=[f"{p:.1f}% ({int(e)})" for p, e in zip(percent_values, evasao_values)],
            textposition="inside",
            marker=dict(color=colors[i % len(colors)]),
            hoverinfo="x+y+text"
        ))

    # Configurar layout do gráfico
    fig.update_layout(
        title='Percentual de Evasão por Cor/Raça em Cada Curso - 2023.2',
        xaxis_title='Curso',
        yaxis_title='Percentual de Evasão (%)',
        barmode='stack',
        template='plotly_white',
        title_font=dict(size=18, family='Arial'),
        xaxis=dict(title_font=dict(size=14), tickangle=45, tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12), range=[0, 210]),
        legend=dict(
            title='Cor/Raça',
            title_font=dict(size=14),
            font=dict(size=12),
            orientation="v",  # Orientação vertical
            x=1.02,  # Posição horizontal fora do gráfico
            y=1,  # Posição vertical no topo
            xanchor="left",
            yanchor="top"
        ),
        margin=dict(l=50, r=150, t=50, b=100)  # Espaço extra à direita para acomodar a legenda
    )

    return fig


# grafico 5

import plotly.graph_objects as go
import numpy as np

def grafico_5():
    # Preparar os dados
    df_evasao6 = mescla_final[mescla_final['Situacao no Curso'] == 'Evasao']
    resultado10 = df_evasao6.groupby(['Curso', 'Sexo']).size().unstack(fill_value=0)

    totais_df = mescla_final.groupby(['Curso', 'Sexo']).size().unstack(fill_value=0).fillna(0)
    totais_df.rename(columns={'F': 'Total_Feminino', 'M': 'Total_Masculino'}, inplace=True)

    resultado10.reset_index(inplace=True)
    resultado10 = resultado10.merge(totais_df, on='Curso', how='left')

    resultado10['Percentual_Feminino'] = (resultado10['F'] / resultado10['Total_Feminino']) * 100
    resultado10['Percentual_Masculino'] = (resultado10['M'] / resultado10['Total_Masculino']) * 100

    resultado10.rename(columns={'F': 'Evasao_Feminino', 'M': 'Evasao_Masculino'}, inplace=True)
    resultado10['Total_Evasao'] = resultado10['Evasao_Feminino'] + resultado10['Evasao_Masculino']

    # Configurar os dados para o gráfico
    cursos = resultado10['Curso']
    evasao_feminino = resultado10['Evasao_Feminino']
    percentual_feminino = resultado10['Percentual_Feminino']
    evasao_masculino = resultado10['Evasao_Masculino']
    percentual_masculino = resultado10['Percentual_Masculino']

    # Criar o gráfico de barras empilhadas com Plotly
    fig = go.Figure()

    # Adicionar as barras Feminino
    fig.add_trace(go.Bar(
        x=cursos,
        y=evasao_feminino,
        name='Feminino',
        marker_color='#ff9999',
        text=[f"{int(e)} ({p:.2f}%)" for e, p in zip(evasao_feminino, percentual_feminino)],
        textposition='auto'  # Ajusta a posição automaticamente dentro das barras
    ))

    # Adicionar as barras Masculino empilhadas
    fig.add_trace(go.Bar(
        x=cursos,
        y=evasao_masculino,
        name='Masculino',
        marker_color='#99c2ff',
        text=[f"{int(e)} ({p:.2f}%)" for e, p in zip(evasao_masculino, percentual_masculino)],
        textposition='auto'  # Ajusta a posição automaticamente dentro das barras
    ))

    # Configurar layout do gráfico
    fig.update_layout(
        title='Evasões por Curso e Sexo - 2023.2',
        xaxis_title='Curso',
        yaxis_title='Número de Evasões',
        barmode='stack',
        template='plotly_white',
        title_font=dict(size=18, family='Arial'),
        xaxis=dict(title_font=dict(size=14), tickangle=45, tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        legend=dict(title='Sexo', font=dict(size=12)),
        margin=dict(l=50, r=50, t=50, b=100)
    )

    return fig


# grafico 6

import plotly.graph_objects as go

def grafico_6():
    # Preparar os dados
    df_evasao7 = mescla_final[mescla_final['Situacao no Curso'] == 'Evasao']
    resultado11 = df_evasao7.groupby(['Curso', 'EnsinoAnterior']).size().unstack(fill_value=0)

    totais_df = mescla_final.groupby(['Curso', 'EnsinoAnterior']).size().unstack(fill_value=0).fillna(0)
    totais_df.rename(columns={'Publico': 'Total_Publico', 'Privado': 'Total_Privado'}, inplace=True)

    resultado11.reset_index(inplace=True)
    resultado11 = resultado11.merge(totais_df, on='Curso', how='left')

    resultado11['Percentual_Privado'] = (resultado11['Privado'] / resultado11['Total_Privado']) * 100
    resultado11['Percentual_Publico'] = (resultado11['Publico'] / resultado11['Total_Publico']) * 100

    resultado11.rename(columns={'Privado': 'Evasao_Privado', 'Publico': 'Evasao_Publico'}, inplace=True)

    # Configurar os dados para o gráfico
    cursos = resultado11['Curso']
    evasao_privado = resultado11['Evasao_Privado']
    percentual_privado = resultado11['Percentual_Privado']
    evasao_publico = resultado11['Evasao_Publico']
    percentual_publico = resultado11['Percentual_Publico']

    # Criar o gráfico de barras empilhadas com Plotly
    fig = go.Figure()

    # Adicionar as barras Privado
    fig.add_trace(go.Bar(
        x=cursos,
        y=evasao_privado,
        name='Privado',
        marker_color='#77dd77',
        text=[f"{int(e)} ({p:.2f}%)" for e, p in zip(evasao_privado, percentual_privado)],
        textposition='inside'
    ))

    # Adicionar as barras Público empilhadas
    fig.add_trace(go.Bar(
        x=cursos,
        y=evasao_publico,
        name='Publico',
        marker_color='#ffdd57',
        text=[f"{int(e)} ({p:.2f}%)" for e, p in zip(evasao_publico, percentual_publico)],
        textposition='inside'
    ))

    # Configurar layout do gráfico
    fig.update_layout(
        title='Evasões por Curso e Ensino Anterior - 2023.2',
        xaxis_title='Curso',
        yaxis_title='Número de Evasões',
        barmode='stack',
        template='plotly_white',
        title_font=dict(size=18, family='Arial'),
        xaxis=dict(title_font=dict(size=14), tickangle=45, tickfont=dict(size=12)),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        legend=dict(title='Ensino Anterior', font=dict(size=12)),
        margin=dict(l=50, r=50, t=50, b=100)
    )

    return fig


# grafico 7

def grafico_7():
    # Preparar os dados
    df12 = pd.DataFrame(mescla_final)
    df_evasao8 = df12[df12['Situacao no Curso'] == 'Evasao']

    deficiencias = [
        'É Deficiente Auditivo?',
        'É Deficiente Auditivo e Surdo?',
        'É Deficiente Fisico?',
        'É Deficiente Intelectual?',
        'É Deficiente Visual?',
        'É Deficiente Visual e tem Baixa Visao?',
        'É Deficiente Visual e tem Cegueira?',
        'É TEA?'
    ]

    resultados = []
    total_evasoes = len(df_evasao8)
    for deficiencia in deficiencias:
        qtd_evasoes = df_evasao8[deficiencia].value_counts().get('Sim', 0)
        percentual_evasoes = (qtd_evasoes / total_evasoes) * 100
        resultados.append([deficiencia, qtd_evasoes, percentual_evasoes])

    resultado12 = pd.DataFrame(resultados, columns=['Deficiencia', 'Qtd Evasoes', '% Evasoes'])

    # Configurar cores baseadas no percentual
    percentual_evasoes = resultado12['% Evasoes']
    cmap = px.colors.sequential.Blues
    colors = [cmap[int((pct / percentual_evasoes.max()) * (len(cmap) - 1))] for pct in percentual_evasoes]

    # Criar o gráfico de barras horizontais com Plotly
    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=resultado12['Deficiencia'],
        x=percentual_evasoes,
        orientation='h',
        text=[f"{int(qtd)} ({pct:.2f}%)" for qtd, pct in zip(resultado12['Qtd Evasoes'], percentual_evasoes)],
        textposition='inside',
        marker=dict(color=colors, line=dict(color='black', width=1))
    ))

    # Configurar layout do gráfico
    fig.update_layout(
        title='Distribuição de Evasões por Tipo de Deficiência - 2023.2',
        xaxis_title='Percentual de Evasões',
        yaxis_title='Tipo de Deficiência',
        template='plotly_white',
        title_font=dict(size=18, family='Arial'),
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12), tickformat=".2f%"),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        margin=dict(l=50, r=50, t=50, b=100)
    )

    return fig


# Gráfico 8

def grafico_8():
    # Criar DataFrame com base no mescla_final
    df13 = pd.DataFrame(mescla_final)

    # Converter colunas de deficiência para valores binários
    columns_to_convert = [
        'É Deficiente Auditivo?', 'É Deficiente Auditivo e Surdo?', 'É Deficiente Fisico?',
        'É Deficiente Intelectual?', 'É Deficiente Visual?', 'É Deficiente Visual e tem Baixa Visao?',
        'É Deficiente Visual e tem Cegueira?', 'É TEA?'
    ]

    for column in columns_to_convert:
        df13[column] = df13[column].apply(lambda x: 1 if x == 'Sim' else 0)

    # Filtrar apenas as linhas com 'Situacao no Curso' = 'Evasao'
    df_evasao9 = df13[df13['Situacao no Curso'] == 'Evasao']

    # Agrupar por 'EnsinoAnterior' e calcular somatório
    resultado13 = df_evasao9.groupby('EnsinoAnterior').agg(
        {
            'É Deficiente Auditivo?': 'sum',
            'É Deficiente Auditivo e Surdo?': 'sum',
            'É Deficiente Fisico?': 'sum',
            'É Deficiente Intelectual?': 'sum',
            'É Deficiente Visual?': 'sum',
            'É Deficiente Visual e tem Baixa Visao?': 'sum',
            'É Deficiente Visual e tem Cegueira?': 'sum',
            'É TEA?': 'sum'
        }
    )

    # Renomear colunas
    column_rename = {
        'É Deficiente Auditivo?': 'Def_Auditivo',
        'É Deficiente Auditivo e Surdo?': 'Def_Auditivo_Surdo',
        'É Deficiente Fisico?': 'Def_Fisico',
        'É Deficiente Intelectual?': 'Def_Intelectual',
        'É Deficiente Visual?': 'Def_Visual',
        'É Deficiente Visual e tem Baixa Visao?': 'Def_Visual_Baixa_Visao',
        'É Deficiente Visual e tem Cegueira?': 'Def_Visual_Cegueira',
        'É TEA?': 'TEA'
    }

    resultado13 = resultado13.rename(columns=column_rename).reset_index()

    # Transformar o DataFrame para formato longo
    df_long = resultado13.melt(id_vars='EnsinoAnterior',
                               value_vars=['Def_Auditivo', 'Def_Auditivo_Surdo', 'Def_Fisico', 'Def_Intelectual',
                                           'Def_Visual', 'Def_Visual_Baixa_Visao', 'Def_Visual_Cegueira', 'TEA'],
                               var_name='Tipo_Deficiencia',
                               value_name='Quantidade')

    # Adicionar coluna para diferenciar "Público" e "Privado"
    df_long['Padrão'] = df_long['EnsinoAnterior'].apply(lambda x: 'Privado' if x == 'Privado' else 'Público')

    # Criar o gráfico de barras agrupadas
    fig = go.Figure()

    # Definir cores para cada tipo de deficiência
    cores = {
        'Def_Auditivo': 'royalblue',
        'Def_Auditivo_Surdo': 'lightblue',
        'Def_Fisico': 'orange',
        'Def_Intelectual': 'green',
        'Def_Visual': 'red',
        'Def_Visual_Baixa_Visao': 'purple',
        'Def_Visual_Cegueira': 'pink',
        'TEA': 'cyan'
    }

    # Adicionar barras para cada tipo de deficiência
    for deficiencia in df_long['Tipo_Deficiencia'].unique():
        df_def = df_long[df_long['Tipo_Deficiencia'] == deficiencia]
        fig.add_trace(go.Bar(
            x=df_def['EnsinoAnterior'],
            y=df_def['Quantidade'],
            name=deficiencia,
            marker_pattern_shape=df_def['Padrão'].apply(lambda x: "/" if x == "Privado" else "."),
            marker_color=cores[deficiencia],
            text=df_def['Quantidade'],
            textposition='outside'
        ))

    # Atualizar o layout do gráfico
    fig.update_layout(
    title=dict(
        text='Quantidade de Alunos por Curso e Tipo de Ensino - 2023.2',
        font=dict(size=18, family='Arial')
    ),
    xaxis=dict(
        title="Curso",
        title_font=dict(size=14),  
        tickangle=45,
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title="Quantidade de Alunos",
        title_font=dict(size=14),  
        tickfont=dict(size=12)
    ),
    template='plotly_white',
    barmode='group',
    legend=dict(title="Tipo de Ensino", font=dict(size=12)),
    margin=dict(l=50, r=50, t=50, b=100)
)


    return fig



# gráfico 9

def grafico_9():
    # Preparar os dados
    df15 = pd.DataFrame(mescla_final)
    df_evasao10 = df15[df15['Situacao no Curso'] == 'Evasao']

    # Contar o total de evasões por 'Cor_Raca'
    total_evasao_por_cor_raca = df_evasao10.groupby('Cor_Raca').size().reset_index(name='Total Evasao')

    # Contar o total de evasões com deficiência e sem deficiência por 'Cor_Raca'
    deficiencia_counts = df_evasao10.groupby(['Cor_Raca', 'Com Deficiencia?']).size().unstack(fill_value=0).reset_index()
    deficiencia_counts.columns = ['Cor_Raca', 'Sem Deficiencia', 'Com Deficiencia']

    # Mesclar os contadores com o total de evasão
    resultado15 = total_evasao_por_cor_raca.merge(deficiencia_counts, on='Cor_Raca', how='left')
    resultado15['Percentual Deficiencia (%)'] = (resultado15['Com Deficiencia'] / resultado15['Total Evasao']) * 100

    # Organizar os dados para o gráfico
    data_melted = resultado15.melt(
        id_vars='Cor_Raca',
        value_vars=['Sem Deficiencia', 'Com Deficiencia'],
        var_name='Com Deficiencia?',
        value_name='Quantidade'
    )

    # Cores para as barras
    cores = {'Sem Deficiencia': '#1f77b4', 'Com Deficiencia': '#d62728'}

    # Criar o gráfico com Plotly
    fig = go.Figure()

    # Adicionar barras para "Sem Deficiencia" e "Com Deficiencia"
    for categoria in data_melted['Com Deficiencia?'].unique():
        subset = data_melted[data_melted['Com Deficiencia?'] == categoria]
        fig.add_trace(go.Bar(
            x=subset['Cor_Raca'],
            y=subset['Quantidade'],
            name=categoria,
            marker_color=cores[categoria],
            text=subset['Quantidade'],
            textposition='outside'
        ))

    # Configurar layout do gráfico
    fig.update_layout(
        title='Evasões por Cor/Raça e Deficiência - 2023.2',
        xaxis_title='Cor/Raça',
        yaxis_title='Quantidade de Evasões',
        barmode='group',
        template='plotly_white',
        title_font=dict(size=18, family='Arial'),
        xaxis=dict(title_font=dict(size=14), tickfont=dict(size=12), tickangle=45),
        yaxis=dict(title_font=dict(size=14), tickfont=dict(size=12)),
        legend=dict(title='Com Deficiência?', font=dict(size=12)),
        margin=dict(l=50, r=50, t=50, b=100)
    )

    return fig


# Gráfico 10


def grafico_10():
    # Preparar os dados
    df14 = pd.DataFrame(mescla_final)

    evasao_por_ensino = df14[df14['Situacao no Curso'] == 'Evasao'].groupby('EnsinoAnterior').size().reset_index(name='Total Evasao')
    deficiencia_sim_por_ensino = df14[df14['Com Deficiencia?'] == 'Sim'].groupby('EnsinoAnterior').size().reset_index(name='Total Com Deficiencia')

    resultado14 = evasao_por_ensino.merge(deficiencia_sim_por_ensino, on='EnsinoAnterior', how='left')
    resultado14['Total Com Deficiencia'] = resultado14['Total Com Deficiencia'].fillna(0)
    resultado14['(%)Percentual Deficiencia'] = (resultado14['Total Com Deficiencia'] / resultado14['Total Evasao']) * 100

    # Dados para o gráfico
    labels = resultado14['EnsinoAnterior']
    values = resultado14['Total Com Deficiencia']

    # Criar o gráfico de pizza com Plotly
    fig = go.Figure()

    fig.add_trace(go.Pie(
        labels=labels,
        values=values,
        hole=0.3,  # Criar um gráfico de rosca
        textinfo='label+percent',
        textfont=dict(size=14),
        marker=dict(
            colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'],
            line=dict(color='white', width=2)
        ),
        pull=[0.1 if i == 0 else 0 for i in range(len(labels))]  # Destaque no primeiro segmento
    ))

    # Configurar layout do gráfico
    fig.update_layout(
        title='Distribuição de Evasão por Ensino Anterior - 2023.2',
        title_font=dict(size=18, family='Arial'),
        showlegend=True,
        legend_title='Ensino Anterior',
        legend=dict(font=dict(size=12)),
        margin=dict(l=50, r=50, t=50, b=50)
    )

    return fig













