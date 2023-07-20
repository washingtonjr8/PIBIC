import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go
from dash import callback_context

import numpy as np
import pandas as pd
import json
import dash_table
from dash_table.Format import Format, Group, Scheme, Symbol
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html, Input, Output, callback

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO], suppress_callback_exceptions=True)
########################################################## LV ######################################################################################################
df_states = pd.read_csv('C:/Users/washi/OneDrive/Área de Trabalho/PIBIC/df_states.csv', encoding='utf8', index_col=False, engine='python',on_bad_lines='skip', delimiter = ',')
df_importancia = pd.read_csv('C:/Users/washi/OneDrive/Área de Trabalho/PIBIC/df_importancia.csv', encoding='utf8', index_col=False, engine='python',on_bad_lines='skip', delimiter = ',')
brazil_states = json.load(open("C:/Users/washi/OneDrive/Área de Trabalho/PIBIC/brazil_geo.json", "r"))
year_op = []
for ano in df_states['Ano'].unique():
    year_op.append({'label': str(ano), 'value':ano})
label_drop = [
    {'label': 'Número de casos', 'value': 'Número de casos'},
    {'label': 'Óbitos', 'value': 'Óbitos'}
]
##################################################### FM ############################################################################################################
df_fm = pd.read_csv('C:/Users/washi/OneDrive/Área de Trabalho/PIBIC/arquivoFM.csv', encoding='utf8', index_col=False, engine='python',on_bad_lines='skip', delimiter = ',')
year_FM = []
for ano in df_fm['Ano'].unique():
    year_FM.append({'label': str(ano), 'value':ano})
label_drop = [
    {'label': 'Número de casos', 'value': 'Número de casos'},
    {'label': 'Óbitos', 'value': 'Óbitos'}
]

#####################################################################################################################################################################

# Layout da página inicial
app.layout = html.Div([
    html.H1(id = 'page-title'),
    html.Button('Leishmaniose Visceral', id='button-1', n_clicks=0),
    html.Button('Febre maculosa', id='button-2', n_clicks=0),
    dcc.Location(id='url', refresh=False),
    html.Div(id='redirect-div')
])

# Callback para atualizar a URL do navegador
@app.callback(Output('url', 'pathname'),
              Input('button-1', 'n_clicks'),
              Input('button-2', 'n_clicks'))
def update_url(page1_clicks, page2_clicks):
    ctx = callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == 'button-1':
        return '/page1'
    elif button_id == 'button-2':
        return '/page2'
    else:
        return ''

page_1_layout = html.Div([
    html.Div(# div para o modal
        dbc.Modal( # add o modal
        [
            dbc.ModalHeader("Aviso!", # add o texto do cabeçalho do modal
                    style = {'color': 'red'}), # alterando a cor to texto do cabeçalho do modal
            dbc.ModalBody( # adicionando o corpo do modal, que é um conjunto de elementos html
                    [
                        # add texto
                        html.Label("O mapa do Brasil pode demorar alguns segundos a mais para atualizar do que os demais gráficos em alguns navegadores."),
                        html.Br(), # adcionando um linha em branco
                        html.Label("Pedimos desculpas pelo incoveniente"), # adicionando mais texto
                        html.Label("\U0001F605") # adicionando um emoticon
                    ]
                ),
            dbc.ModalFooter( # add o footer
                dbc.Button( # add um botão para fechar o modal
                    "Ok!", # texto do botão
                    id = 'close-sm', # id do botão
                    className = "ml-auto", # dando uma classe de botão para o botão
                    )
                ),
            ],
            id = 'modal', # add uma ID ao modal
            is_open = True, # definindo que o modal vai estar aberto quando o usuario abrir o dashboard
            centered = True, # definindo que o modal vai estar centralizado
            style = {'textAlign': 'center'} # centralizando o texto do modal
        )
    ),
    html.Div([
        dbc.Row(
            dbc.Col(
                ), style = {'paddingTop': "20px", 'paddingBottom': "20px", 'color':'white'} # adicionado espaçamento para a linha
        ),
    ]),
    html.Div([
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(id = 'year', 
                            value = 2022,
                            options= year_op,
                            clearable = False, # permite remover o valor
                            style =  {'width': '50%'} # especifica que a largura do dropdown
                ), style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'}        
            ), 
        ),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(id = 'meu-dropdown', 
                            value = 'Número de casos',
                            options= label_drop,
                            clearable = False, # permite remover o valor
                            style =  {'width': '50%'} # especifica que a largura do dropdown
                ), style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'}
            ),
        ),
        dbc.Row(
            [
            dbc.Col( # Tabela
                html.Div(id = 'tabela'), # id da tabela do mapa
                width = 4, # número de colunas que a tabela irá ocupar
                align = 'center', # centralizando a tabela dentro das colunas
                style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'} # adicionando um espaçamento para não ficar tudo grudado
            ),
            dbc.Col( #mapa
                dcc.Graph(id = 'map_br'),
                width= 4,
                align = 'center',
                style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'} # adicionando um espaçamento para não ficar tudo grudado
            ),
            dbc.Col(
                dcc.Graph(id = 'graph_barras'),
                width = 3,
                align= 'center',
                style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'}
            ),
            ]
        ),
        dbc.Row( #Tabela importância
            dbc.Col(
                dcc.Graph(id = 'tabela_imp'), #id
                width= 4,
                align= 'center',
                style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'}
            ),
        ),    
    ])
])

######################################################### CALLBACKS DA PAGINA 1 ####################################################################

#AVISO

@app.callback(Output('modal', 'is_open'),
              [Input('close-sm', 'n_clicks'),],
              [State('modal', 'is_open')])
def close_modal(n, is_open):
    if n:
        return not is_open
    return is_open

#GRAFICO DE AUXILIO DO DIAG. LV

@app.callback(Output('tabela_imp', 'figure'),
              [Input('year','value'), Input('meu-dropdown', 'value')])
def update_graph_brazil(selected_year, value):
        
        df_imp = df_importancia
        df_imp = df_imp.sort_values(by='Valor', ascending=False)
    
        fig = px.bar(df_imp, # data frame com os dados
            x = 'Variáveis', # coluna para os dados do eixo x
            y = 'Valor', # coluna para os dados do eixo y
            barmode = 'group', # setando que o gráfico é do tipo group
            color = 'Variáveis', 
            template= 'none',
            )
    
        fig.update_yaxes(
            showticklabels=True, 
        )
        fig.update_traces(
        width=0.5,     #define a largura das barras para 0,5
        marker=dict(line=dict(width=1, color='Black'))   # adiciona uma linha preta ao redor de cada barra. Você pode ajustar a largura e a cor da linha de acordo com suas preferências.
        )
        fig.update_layout(
        width=550,
        height=600,
        title="Importância dos Recursos Para o Auxílio do Diagnóstico da LV",
        xaxis_title= None,
        yaxis_title="Importância Relativa",
        showlegend = False,
        margin=dict(l=150)   #aumenta a margem esquerda do gráfico em 150 pixels
        )
        return fig

#TABELA


@app.callback(Output('tabela', 'children'),
            [Input('year', 'value')])
def update_table_map(selected_year,):
    df_ano = df_states[df_states['Ano'] == selected_year] # filtrando o data frame com o selected_year
    df_ano = df_ano.drop(['Ano'], axis = 1)
    df_ano = df_ano.reset_index(drop=True)
    df_ano.sort_values(by='Estado', inplace=True, ascending=True) # ordenando os dados
    df_ano.reset_index(inplace=True, drop=True) # resetando o indice

    return [dash_table.DataTable
    (data=df_ano.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df_ano.columns],
    fixed_rows={'headers': True}, # fixando o cabeçalho para que a barra de rolamento não esconda o cabeçalho
    style_table={'height': '400px', 'overflowY': 'auto'}, # adicionando uma barra de rolamento, e fixando o tamanho da tabela em 400px
    style_header={'textAlign': 'center', 'color':'black'}, # centralizando o texto do cabeçalho
    style_cell={'textAlign': 'center', 'font-size': '14px'}, # centralizando o texto das céluas e alterando o tamanho da fonte
    style_data = {
        'color': 'black',
        'backgroundColor': 'white'
    },
    style_data_conditional=[ # este parametro altera a cor da célula quando o usuário clica na célula
                                        {
                                            "if": {"state": "selected"},
                                            "backgroundColor": "rgba(205, 205, 205, 0.3)",
                                            "border": "inherit !important",
                                        }]
    )]
                

#MAPA

@app.callback(Output('map_br','figure'),
             [Input('year','value'), Input('meu-dropdown','value')])
def update_map_brazil(selected_year, value):
    
    if value == 'Número de casos':
        df_ano = df_states[df_states['Ano'] == selected_year] # novo df com os dados de apenas 1 estado por vez
        fig = px.choropleth_mapbox(
                            df_ano, locations = "Sigla", geojson = brazil_states,
                            color= 'N_CASOS', color_continuous_scale = 'Purples', 
                            center= {'lat':-16.95, 'lon':-47.78}, animation_frame = 'Ano',
                            zoom = 4, range_color = [0, df_ano['N_CASOS'].max()],
                            opacity = 1.0, hover_data= {"Estado": True, "N_CASOS":True})
    
        fig.layout.update(
            paper_bgcolor = 'white',
            autosize = True,
            margin = go.Margin(l=0, r=0, t=0, b=0),
            showlegend = False,
            mapbox_style= "carto-positron" #"carto-darkmatter"
    )
    if value == 'Óbitos':
        df_ano = df_states[df_states['Ano'] == selected_year] # novo df com os dados de apenas 1 estado por vez
        fig = px.choropleth_mapbox(
                            df_ano, locations = "Sigla", geojson = brazil_states,
                            color= 'Óbitos', color_continuous_scale = 'Purples', 
                            center= {'lat':-16.95, 'lon':-47.78}, animation_frame = 'Ano',
                            zoom = 4, range_color = [0, df_ano['Óbitos'].max()],
                            opacity = 1.0, hover_data= {"Estado": True, "Óbitos":True})
    
        fig.layout.update(
            paper_bgcolor = 'white',
            autosize = True,
            margin = go.Margin(l=0, r=0, t=0, b=0),
            showlegend = False,
            mapbox_style= "carto-positron" #"carto-darkmatter"
    )
    return fig
       

#GRÁFICO DE BARRAS

@app.callback(Output('graph_barras', 'figure'),
              [Input('year','value'), Input('meu-dropdown', 'value')])
def update_graph_brazil(selected_year, value):

    if value == 'Número de casos':
        df_graph = df_states[df_states['Ano'] == selected_year]
        df_graph = df_graph.sort_values(by='N_CASOS', ascending=True)
        #criando mapa
        fig = px.bar(df_graph, # data frame com os dados
            x = 'N_CASOS', # coluna para os dados do eixo x
            y = 'Sigla', # coluna para os dados do eixo y
            barmode = 'group', # setando que o gráfico é do tipo group
            color = 'Estado', 
            hover_data = {'N_CASOS': True, 'Estado': True, 'Sigla': False}, # Removendo o Mes para que não fique repetido no título do hover e no conteúdo do hover
            template= 'none',
            )
    
        fig.update_yaxes(
            showticklabels=True, 
        )
        fig.update_traces(
        width=0.5,     #define a largura das barras para 0,5
        marker=dict(line=dict(width=1, color='Black'))   # adiciona uma linha preta ao redor de cada barra. Você pode ajustar a largura e a cor da linha de acordo com suas preferências.
        )
        fig.update_layout(
        width=500,
        height=600,
        xaxis_title='Número de Casos',
        yaxis_title= None,
        showlegend = False,
        margin=dict(l=150)   #aumenta a margem esquerda do gráfico em 150 pixels
        )
    if value == 'Óbitos':
        df_graph = df_states[df_states['Ano'] == selected_year]
        df_graph = df_graph.sort_values(by='Óbitos', ascending=True)
        #criando mapa
        fig = px.bar(df_graph, # data frame com os dados
            x = 'Óbitos', # coluna para os dados do eixo x
            y = 'Sigla', # coluna para os dados do eixo y
            barmode = 'group', # setando que o gráfico é do tipo group
            color = 'Estado', 
            hover_data = {'Óbitos': True, 'Estado': True, 'Sigla': False}, # Removendo o Mes para que não fique repetido no título do hover e no conteúdo do hover
            template= 'none',
            )
    
        fig.update_yaxes(
            showticklabels=True, 
        )
        fig.update_traces(
        width=0.5,     #define a largura das barras para 0,5
        marker=dict(line=dict(width=1, color='Black'))   # adiciona uma linha preta ao redor de cada barra. Você pode ajustar a largura e a cor da linha de acordo com suas preferências.
        )
        fig.update_layout(
        width=500,
        height=600,
        xaxis_title='Quantidade de Óbitos',
        yaxis_title= None,
        showlegend = False,
        margin=dict(l=150)   #aumenta a margem esquerda do gráfico em 150 pixels
        )
    

    return fig

####################################################################### PÁGINA 2 E SEUS CALLBACKS ###############################################################################


page_2_layout = html.Div([
    html.Div(# div para o modal
        dbc.Modal( # add o modal
        [
            dbc.ModalHeader("Aviso!", # add o texto do cabeçalho do modal
                    style = {'color': 'red'}), # alterando a cor to texto do cabeçalho do modal
            dbc.ModalBody( # adicionando o corpo do modal, que é um conjunto de elementos html
                    [
                        # add texto
                        html.Label("O mapa do Brasil pode demorar alguns segundos a mais para atualizar do que os demais gráficos em alguns navegadores."),
                        html.Br(), # adcionando um linha em branco
                        html.Label("Pedimos desculpas pelo incoveniente"), # adicionando mais texto
                        html.Label("\U0001F605") # adicionando um emoticon
                    ]
                ),
            dbc.ModalFooter( # add o footer
                dbc.Button( # add um botão para fechar o modal
                    "Ok!", # texto do botão
                    id = 'fechar-sm', # id do botão
                    className = "ml-auto", # dando uma classe de botão para o botão
                    )
                ),
            ],
            id = 'modal-2', # add uma ID ao modal
            is_open = True, # definindo que o modal vai estar aberto quando o usuario abrir o dashboard
            centered = True, # definindo que o modal vai estar centralizado
            style = {'textAlign': 'center'} # centralizando o texto do modal
        )
    ),
    html.Div([
        dbc.Row(
            dbc.Col(
                ),style = {'paddingTop': "20px", 'paddingBottom': "20px", 'color':'white'} # adicionado espaçamento para a linha
        ),
    ]),
    html.Div([
            dbc.Col(
                dcc.Dropdown(id = 'year-2', 
                            value = 2020,
                            options= year_FM,
                            clearable = False, # permite remover o valor
                            style =  {'width': '50%'} # especifica que a largura do dropdown
            ), style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'}        
        ), 
            dbc.Col(
                dcc.Dropdown(id = 'meu-dropdown-2', 
                            value = 'Número de casos',
                            options= label_drop,
                            clearable = False, # permite remover o valor
                            style =  {'width': '50%'} # especifica que a largura do dropdown
            ), style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'}
        ),
        dbc.Row(
            [
            dbc.Col( # Tabela
                html.Div(id = 'tabela-2'), # id da tabela do mapa
                width = 4, # número de colunas que a tabela irá ocupar
                align = 'center', # centralizando a tabela dentro das colunas
                style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'} # adicionando um espaçamento para não ficar tudo grudado
            ),
            dbc.Col( #mapa
                dcc.Graph(id = 'map_br-2'),
                width= 4,
                align = 'center',
                style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'} # adicionando um espaçamento para não ficar tudo grudado
            ),
            dbc.Col(
                dcc.Graph(id = 'graph_barras-2'),
                width = 3,
                align= 'center',
                style = {'display': 'inline-block', 'paddingLeft': '2%', 'paddingRight': '2%'}
            ),
            ]
        ),    
    ])
])

#AVISO

@app.callback(Output('modal-2', 'is_open'),
              [Input('fechar-sm', 'n_clicks'),],
              [State('modal-2', 'is_open')])
def close_modal(n, is_open):
    if n:
        return not is_open
    return is_open

#TABELA


@app.callback(Output('tabela-2', 'children'),
            [Input('year-2', 'value')])
def update_table_map(selected_year,):
    df_ano = df_fm[df_fm['Ano'] == selected_year] # filtrando o data frame com o selected_year
    df_ano = df_ano.drop(['Ano'], axis = 1)
    df_ano = df_ano.reset_index(drop=True)
    df_ano.sort_values(by='Estado', inplace=True, ascending=True) # ordenando os dados
    df_ano.reset_index(inplace=True, drop=True) # resetando o indice

    return [dash_table.DataTable
    (data=df_ano.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df_ano.columns],
    fixed_rows={'headers': True}, # fixando o cabeçalho para que a barra de rolamento não esconda o cabeçalho
    style_table={'height': '400px', 'overflowY': 'auto'}, # adicionando uma barra de rolamento, e fixando o tamanho da tabela em 400px
    style_header={'textAlign': 'center', 'color':'black'}, # centralizando o texto do cabeçalho
    style_cell={'textAlign': 'center', 'font-size': '14px'}, # centralizando o texto das céluas e alterando o tamanho da fonte
    style_data = {
        'color': 'black',
        'backgroundColor': 'white'
    },
    style_data_conditional=[ # este parametro altera a cor da célula quando o usuário clica na célula
                                        {
                                            "if": {"state": "selected"},
                                            "backgroundColor": "rgba(205, 205, 205, 0.3)",
                                            "border": "inherit !important",
                                        }]
    )]
                

#MAPA

@app.callback(Output('map_br-2','figure'),
             [Input('year-2','value'), Input('meu-dropdown-2','value')])
def update_map_brazil(selected_year, value):
    
    if value == 'Número de casos':
        df_ano = df_fm[df_fm['Ano'] == selected_year] # novo df com os dados de apenas 1 estado por vez
        fig = px.choropleth_mapbox(
                            df_ano, locations = "Sigla", geojson = brazil_states,
                            color= 'N_CASOS', color_continuous_scale = 'Purples', 
                            center= {'lat':-16.95, 'lon':-47.78}, animation_frame = 'Ano',
                            zoom = 4, range_color = [0, df_ano['N_CASOS'].max()],
                            opacity = 1.0, hover_data= {"Estado": True, "N_CASOS":True})
    
        fig.layout.update(
            paper_bgcolor = 'white',
            autosize = True,
            margin = go.Margin(l=0, r=0, t=0, b=0),
            showlegend = False,
            mapbox_style= "carto-positron" #"carto-darkmatter"
    )
    if value == 'Óbitos':
        df_ano = df_fm[df_fm['Ano'] == selected_year] # novo df com os dados de apenas 1 estado por vez
        fig = px.choropleth_mapbox(
                            df_ano, locations = "Sigla", geojson = brazil_states,
                            color= 'Óbitos', color_continuous_scale = 'Purples', 
                            center= {'lat':-16.95, 'lon':-47.78}, animation_frame = 'Ano',
                            zoom = 4, range_color = [0, df_ano['Óbitos'].max()],
                            opacity = 1.0, hover_data= {"Estado": True, "Óbitos":True})
    
        fig.layout.update(
            paper_bgcolor = 'white',
            autosize = True,
            margin = go.Margin(l=0, r=0, t=0, b=0),
            showlegend = False,
            mapbox_style= "carto-positron" #"carto-darkmatter"
    )
    return fig
       

#GRÁFICO DE BARRAS

@app.callback(Output('graph_barras-2', 'figure'),
              [Input('year-2','value'), Input('meu-dropdown-2', 'value')])
def update_graph_brazil(selected_year, value):

    if value == 'Número de casos':
        df_graph = df_fm[df_fm['Ano'] == selected_year]
        df_graph = df_graph.sort_values(by='N_CASOS', ascending=True)
        #criando mapa
        fig = px.bar(df_graph, # data frame com os dados
            x = 'N_CASOS', # coluna para os dados do eixo x
            y = 'Sigla', # coluna para os dados do eixo y
            barmode = 'group', # setando que o gráfico é do tipo group
            color = 'Estado', 
            hover_data = {'N_CASOS': True, 'Estado': True, 'Sigla': False}, # Removendo o Mes para que não fique repetido no título do hover e no conteúdo do hover
            template= 'none',
            )
    
        fig.update_yaxes(
            showticklabels=True, 
        )
        fig.update_traces(
        width=0.5,     #define a largura das barras para 0,5
        marker=dict(line=dict(width=1, color='Black'))   # adiciona uma linha preta ao redor de cada barra. Você pode ajustar a largura e a cor da linha de acordo com suas preferências.
        )
        fig.update_layout(
        width=500,
        height=600,
        xaxis_title='Número de casos',
        yaxis_title= None,
        showlegend = False,
        margin=dict(l=150)   #aumenta a margem esquerda do gráfico em 150 pixels
        )
    if value == 'Óbitos':
        df_graph = df_fm[df_fm['Ano'] == selected_year]
        df_graph = df_graph.sort_values(by='Óbitos', ascending=True)
        #criando mapa
        fig = px.bar(df_graph, # data frame com os dados
            x = 'Óbitos', # coluna para os dados do eixo x
            y = 'Sigla', # coluna para os dados do eixo y
            barmode = 'group', # setando que o gráfico é do tipo group
            color = 'Estado', 
            hover_data = {'Óbitos': True, 'Estado': True, 'Sigla': False}, # Removendo o Mes para que não fique repetido no título do hover e no conteúdo do hover
            template= 'none',
            )
    
        fig.update_yaxes(
            showticklabels=True, 
        )
        fig.update_traces(
        width=0.5,     #define a largura das barras para 0,5
        marker=dict(line=dict(width=1, color='Black'))   # adiciona uma linha preta ao redor de cada barra. Você pode ajustar a largura e a cor da linha de acordo com suas preferências.
        )
        fig.update_layout(
        width=500,
        height=600,
        xaxis_title='Quantidade de Óbitos',
        yaxis_title= None,
        showlegend = False,
        margin=dict(l=150)   #aumenta a margem esquerda do gráfico em 150 pixels
        )
    

    return fig


# Callback para exibir a página correspondente
@app.callback([Output('redirect-div', 'children'),
              Output('page-title', 'children')],
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page_1_layout, 'Leishmaniose Visceral'
    if pathname == '/page2':
        return page_2_layout, 'Febre Maculosa'
    else:
        return None, "Doenças Negligenciadas"
    



if __name__ == '__main__':
    app.run_server(debug=True)