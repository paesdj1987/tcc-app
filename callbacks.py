import dash
import os
from dash import dcc
from dash.dependencies import Input, Output, State
from graficos import (
    grafico_1, grafico_2, grafico_3, grafico_4, grafico_5,
    grafico_6, grafico_7, grafico_8, grafico_9, grafico_10
)

def register_callbacks(app):
    # 1. Callback para atualizar o gráfico com base na seleção do gráfico
    @app.callback(
        Output('grafico', 'figure'),
        [Input('grafico-selector', 'value')]
    )
    def render_graphs(grafico_selecionado):
        if grafico_selecionado == 1:
            return grafico_1()
        elif grafico_selecionado == 2:
            return grafico_2()
        elif grafico_selecionado == 3:
            return grafico_3()
        elif grafico_selecionado == 4:
            return grafico_4()
        elif grafico_selecionado == 5:
            return grafico_5()
        elif grafico_selecionado == 6:
            return grafico_6()
        elif grafico_selecionado == 7:
            return grafico_7()
        elif grafico_selecionado == 8:
            return grafico_8()
        elif grafico_selecionado == 9:
            return grafico_9()
        elif grafico_selecionado == 10:
            return grafico_10()
                

        # Se não houver gráfico correspondente
        return {}

    # 2. Callback para navegar entre os gráficos com os botões "Anterior" e "Próximo"
    @app.callback(
        Output('grafico-selector', 'value'),
        [Input('previous-button', 'n_clicks'),
         Input('next-button', 'n_clicks')],
        [State('grafico-selector', 'value')]
    )
    def update_graph(n_previous, n_next, current_value):
        if not n_previous and not n_next:
            return current_value

        ctx = dash.callback_context
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'previous-button':
            return max(current_value - 1, 1)
        elif button_id == 'next-button':
            return min(current_value + 1, 10)

        return current_value

    # 3. Callback para download do arquivo "mescla_final.xlsx"
    @app.callback(
        Output("download-excel-file", "data"),
        Input("excel-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_excel(n_clicks):
        file_path = os.path.join(os.getcwd(), "mescla_final.xlsx")
        return dcc.send_file(file_path)
