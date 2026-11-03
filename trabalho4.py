import unicodedata
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Passo 1 e 2 -> leitura e tratamento dos dados
df = pd.read_csv('Summer_olympic_Medals.csv')
df['Country_Name'] = df['Country_Name'].replace('United States', 'United States of America')
df = df[(df['Year'] >= 1992) & (df['Year'] <= 2020)].copy()
df['Total_Medals'] = df['Gold'] + df['Silver'] + df['Bronze']

# Tradução dos nomes dos países (o mapa continua usando o nome em inglês para localizar o país)
# Contém apenas os países/equipes presentes no arquivo entre 1992 e 2020 (em ordem alfabética).
traducao = {
    'Afghanistan': 'Afeganistão',
    'Algeria': 'Argélia',
    'Argentina': 'Argentina',
    'Armenia': 'Armênia',
    'Australia': 'Austrália',
    'Austria': 'Áustria',
    'Azerbaijan': 'Azerbaijão',
    'Bahamas': 'Bahamas',
    'Bahrain': 'Bahrein',
    'Barbados': 'Barbados',
    'Belarus': 'Bielorrússia',
    'Belgium': 'Bélgica',
    'Bermuda': 'Bermudas',
    'Botswana': 'Botsuana',
    'Brazil': 'Brasil',
    'Bulgaria': 'Bulgária',
    'Burkina Faso': 'Burkina Faso',
    'Burundi': 'Burundi',
    'Cameroon': 'Camarões',
    'Canada': 'Canadá',
    'Chile': 'Chile',
    'China': 'China',
    'Chinese Taipei': 'Taipé Chinês',
    'Colombia': 'Colômbia',
    'Costa Rica': 'Costa Rica',
    'Croatia': 'Croácia',
    'Cuba': 'Cuba',
    'Cyprus': 'Chipre',
    'Czech Republic': 'República Tcheca',
    'Czechoslovakia': 'Tchecoslováquia',
    'Denmark': 'Dinamarca',
    'Dominican Republic': 'República Dominicana',
    'Ecuador': 'Equador',
    'Egypt': 'Egito',
    'Eritrea': 'Eritreia',
    'Estonia': 'Estônia',
    'Ethiopia': 'Etiópia',
    'Fiji': 'Fiji',
    'Finland': 'Finlândia',
    'France': 'França',
    'Gabon': 'Gabão',
    'Georgia': 'Geórgia',
    'Germany': 'Alemanha',
    'Ghana': 'Gana',
    'Great Britain': 'Grã-Bretanha',
    'Greece': 'Grécia',
    'Grenada': 'Granada',
    'Guatemala': 'Guatemala',
    'Hong Kong': 'Hong Kong',
    'Hungary': 'Hungria',
    'Iceland': 'Islândia',
    'Independent Olympic Athletes': 'Atletas Olímpicos Independentes',
    'Independent Olympic Participants': 'Participantes Olímpicos Independentes',
    'India': 'Índia',
    'Indonesia': 'Indonésia',
    'Iran': 'Irã',
    'Ireland': 'Irlanda',
    'Israel': 'Israel',
    'Italy': 'Itália',
    'Ivory Coast': 'Costa do Marfim',
    'Jamaica': 'Jamaica',
    'Japan': 'Japão',
    'Jordan': 'Jordânia',
    'Kazakhstan': 'Cazaquistão',
    'Kenya': 'Quênia',
    'Kosovo': 'Kosovo',
    'Kuwait': 'Kuwait',
    'Kyrgyzstan': 'Quirguistão',
    'Latvia': 'Letônia',
    'Lithuania': 'Lituânia',
    'Macedonia': 'Macedônia do Norte',
    'Malaysia': 'Malásia',
    'Mauritius': 'Maurício',
    'Mexico': 'México',
    'Moldova': 'Moldávia',
    'Mongolia': 'Mongólia',
    'Montenegro': 'Montenegro',
    'Morocco': 'Marrocos',
    'Mozambique': 'Moçambique',
    'Namibia': 'Namíbia',
    'Netherlands': 'Países Baixos',
    'New Zealand': 'Nova Zelândia',
    'Niger': 'Níger',
    'Nigeria': 'Nigéria',
    'North Korea': 'Coreia do Norte',
    'North Macedonia': 'Macedônia do Norte',
    'Norway': 'Noruega',
    'Pakistan': 'Paquistão',
    'Panama': 'Panamá',
    'Paraguay': 'Paraguai',
    'Peru': 'Peru',
    'Philippines': 'Filipinas',
    'Poland': 'Polônia',
    'Portugal': 'Portugal',
    'Puerto Rico': 'Porto Rico',
    'Qatar': 'Catar',
    'ROC': 'Comitê Olímpico Russo',
    'Romania': 'Romênia',
    'Russia': 'Rússia',
    'Samoa': 'Samoa',
    'San Marino': 'San Marino',
    'Saudi Arabia': 'Arábia Saudita',
    'Serbia': 'Sérvia',
    'Serbia and Montenegro': 'Sérvia e Montenegro',
    'Singapore': 'Singapura',
    'Slovakia': 'Eslováquia',
    'Slovenia': 'Eslovênia',
    'South Africa': 'África do Sul',
    'South Korea': 'Coreia do Sul',
    'Spain': 'Espanha',
    'Sri Lanka': 'Sri Lanka',
    'Sudan': 'Sudão',
    'Suriname': 'Suriname',
    'Sweden': 'Suécia',
    'Switzerland': 'Suíça',
    'Syria': 'Síria',
    'Tajikistan': 'Tajiquistão',
    'Thailand': 'Tailândia',
    'Togo': 'Togo',
    'Tonga': 'Tonga',
    'Trinidad and Tobago': 'Trinidad e Tobago',
    'Tunisia': 'Tunísia',
    'Turkey': 'Turquia',
    'Turkmenistan': 'Turcomenistão',
    'Uganda': 'Uganda',
    'Ukraine': 'Ucrânia',
    'Unified Team': 'Equipe Unificada',
    'United Arab Emirates': 'Emirados Árabes Unidos',
    'United States': 'Estados Unidos',                  # usado na coluna Host_country (país sede)
    'United States of America': 'Estados Unidos',       # usado na coluna Country_Name
    'Uruguay': 'Uruguai',
    'Uzbekistan': 'Uzbequistão',
    'Venezuela': 'Venezuela',
    'Vietnam': 'Vietnã',
    'Yugoslavia': 'Iugoslávia',
    'Zambia': 'Zâmbia',
    'Zimbabwe': 'Zimbábue',
}

# Se algum nome não estiver na lista, continua em inglês
df['Pais'] = df['Country_Name'].map(traducao).fillna(df['Country_Name'])
df['Sede'] = df['Host_country'].map(traducao).fillna(df['Host_country'])

# Nomes das colunas que aparecem nos gráficos
rotulos = {'Pais': 'Países', 'Country_Name': 'Países', 'Total_Medals': 'Total de medalhas',
           'Gold': 'Ouro', 'Silver': 'Prata', 'Bronze': 'Bronze', 'Year': 'Ano'}

# Passo 7 -> opções dos filtros
colunas = {'Ouro': 'Gold', 'Prata': 'Silver', 'Bronze': 'Bronze', 'Todos': 'Total_Medals'}
cores = {'Ouro': 'gold', 'Prata': 'silver', 'Bronze': '#cd7f32', 'Todos': 'steelblue'}

df_anos = df[['Year', 'Sede']].drop_duplicates().sort_values('Year')
opcoes_ano = [{'label': 'Todos os anos', 'value': 'Todos'}]
for i, linha in df_anos.iterrows():
    opcoes_ano.append({'label': str(linha['Year']) + ' - ' + linha['Sede'], 'value': int(linha['Year'])})

# Ordem alfabética ignorando os acentos (para "África do Sul" ficar no início)
opcoes_pais = sorted(df['Pais'].unique(), key=lambda p: unicodedata.normalize('NFD', p))

# Passo 8 -> dashboard
app = Dash(__name__)
server = app.server   # necessário para o Render

# Fundo da página inteira (#668B8B) e remoção da margem branca padrão do navegador
app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body { margin: 0; background-color: #668B8B; }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
        <script>
        // Zoom do mapa: nunca fica menor que o tamanho padrão (escala 1); só aumenta os desenhos
        (function () {
            function ligar() {
                var caixa = document.getElementById('map');
                if (!caixa) { setTimeout(ligar, 300); return; }
                if (caixa.dataset.zoomFixo) { return; }
                caixa.dataset.zoomFixo = '1';
                caixa.addEventListener('wheel', function (e) {
                    var gd = caixa.getElementsByClassName('js-plotly-plot')[0];
                    if (!gd || !window.Plotly) { return; }
                    var geo = (gd.layout && gd.layout.geo) || {};
                    var atual = (geo.projection && geo.projection.scale) || 1;
                    var dy = Math.max(-100, Math.min(100, e.deltaY));
                    if (atual <= 1 && dy > 0) { return; }   // já no tamanho padrão: a página rola normalmente
                    e.preventDefault();
                    e.stopPropagation();
                    var nova = Math.min(12, Math.max(1, atual * Math.exp(-dy * 0.002)));
                    if (nova === atual) { return; }
                    var mudancas = {'geo.projection.scale': nova, 'dragmode': nova > 1 ? 'pan' : false};
                    if (nova <= 1) { mudancas['geo.center.lon'] = 0; mudancas['geo.center.lat'] = 0; }
                    window.Plotly.relayout(gd, mudancas);
                }, {capture: true, passive: false});
            }
            ligar();
        })();
        </script>
    </body>
</html>'''

# Estilos (tudo empilhado, centralizado e do mesmo tamanho)
estilo_titulo = {'textAlign': 'center', 'backgroundColor': '#1f3a5f', 'color': 'white',
                 'padding': '20px', 'borderRadius': '8px', 'marginBottom': '20px'}
estilo_filtro_medalha = {'textAlign': 'center', 'margin': '10px auto'}
estilo_filtro = {'textAlign': 'left', 'margin': '10px auto'}      # texto à esquerda, alinhado com o gráfico
estilo_texto_filtro = {'display': 'block', 'marginBottom': '8px'}  # espaço entre o texto e a seleção
estilo_grafico = {'height': '500px', 'width': '100%'}
estilo_caixa = {'height': '500px', 'width': '100%', 'overflow': 'hidden'}   # moldura do mapa (tamanho fixo)

app.layout = html.Div([
    html.H1('Quadro de Medalhas Olímpicas (1992 a 2020)', style=estilo_titulo),

    # Filtro de medalha (mapa, área e barras)
    html.Div([
        html.Label('Tipo de medalha:', style=estilo_texto_filtro),
        dcc.RadioItems(id='filtro-medalha', options=['Ouro', 'Prata', 'Bronze', 'Todos'], value='Todos',
                       inline=True,
                       labelStyle={'display': 'inline-block', 'marginRight': '30px'},
                       inputStyle={'marginRight': '6px'})
    ], style=estilo_filtro_medalha),

    # Mapa: a moldura tem sempre o mesmo tamanho, mas o conteúdo permite zoom (roda do mouse) e arrastar
    html.Div([
        dcc.Graph(id='map', style=estilo_grafico,
                  config={'scrollZoom': True, 'displaylogo': False,
                          'modeBarButtonsToRemove': ['select2d', 'lasso2d']})
    ], style=estilo_caixa),

    dcc.Graph(id='area-chart', style=estilo_grafico),

    # Filtro de ano (barras)
    html.Div([
        html.Label('Ano olímpico (País sede):', style=estilo_texto_filtro),
        dcc.Dropdown(id='filtro-ano', options=opcoes_ano, value='Todos', clearable=False)
    ], style=estilo_filtro),

    dcc.Graph(id='bar-chart', style=estilo_grafico),

    # Filtro de país (pizza)
    html.Div([
        html.Label('País:', style=estilo_texto_filtro),
        dcc.Dropdown(id='filtro-pais', options=opcoes_pais, value='Estados Unidos', clearable=False)
    ], style=estilo_filtro),

    dcc.Graph(id='pie-chart', style=estilo_grafico)

], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '900px', 'margin': '0 auto', 'padding': '30px',
          'textAlign': 'center'})


# Mapa (filtro de medalha)
@app.callback(Output('map', 'figure'), Input('filtro-medalha', 'value'))
def atualiza_mapa(medalha):
    coluna = colunas[medalha]
    df_country_medals = df.groupby(['Country_Name', 'Pais'])[coluna].sum().reset_index()

    map_fig = px.choropleth(df_country_medals,
                        locations='Country_Name',
                        locationmode='country names',
                        color=coluna,
                        hover_name='Pais',
                        hover_data={'Country_Name': False},
                        labels=rotulos,
                        color_continuous_scale=px.colors.sequential.YlOrRd,
                        title='Medalhas (' + medalha + ') de 1992 a 2020')
    map_fig.update_layout(dragmode=False)   # no tamanho padrão o mapa fica parado
    # Sem moldura própria: a única caixa visível é a branca, que tem tamanho fixo.
    # O zoom só mexe no conteúdo (os países) dentro dela.
    map_fig.update_geos(showframe=False, bgcolor='white')
    return map_fig


# Área (filtro de medalha)
@app.callback(Output('area-chart', 'figure'), Input('filtro-medalha', 'value'))
def atualiza_area(medalha):
    coluna = colunas[medalha]
    top_countries = df.groupby('Pais')[coluna].sum().nlargest(10).index

    df_countries = df.groupby(['Pais', 'Year'])[coluna].sum().reset_index()
    df_top_10_countries = df_countries[df_countries['Pais'].isin(top_countries)]

    area_fig = px.area(df_top_10_countries,
                       x="Year",
                       y=coluna,
                       color="Pais",
                       labels=rotulos,
                       title='Top 10 Países por medalhas (' + medalha + ') de 1992 a 2020')
    return area_fig


# Barras (filtro de medalha + filtro de ano)
@app.callback(Output('bar-chart', 'figure'),
              Input('filtro-medalha', 'value'),
              Input('filtro-ano', 'value'))
def atualiza_barra(medalha, ano):
    coluna = colunas[medalha]

    if ano == 'Todos':
        df_ano = df
        texto_ano = '1992 a 2020'
    else:
        df_ano = df[df['Year'] == ano]
        texto_ano = str(ano)

    df_top_countries = df_ano.groupby('Pais')[coluna].sum().nlargest(10).reset_index()

    bar_fig = px.bar(df_top_countries,
                     x='Pais',
                     y=coluna,
                     labels=rotulos,
                     color_discrete_sequence=[cores[medalha]],
                     title='Top 10 Países com mais medalhas (' + medalha + ') - ' + texto_ano)
    return bar_fig


# Pizza (filtro de país)
@app.callback(Output('pie-chart', 'figure'), Input('filtro-pais', 'value'))
def atualiza_pizza(pais):
    df_pais = df[df['Pais'] == pais]

    df_pizza = pd.DataFrame({
        'Medalha': ['Ouro', 'Prata', 'Bronze'],
        'Total': [df_pais['Gold'].sum(), df_pais['Silver'].sum(), df_pais['Bronze'].sum()]
    })

    pie_fig = px.pie(df_pizza,
                     names='Medalha',
                     values='Total',
                     color='Medalha',
                     color_discrete_map={'Ouro': 'gold', 'Prata': 'silver', 'Bronze': '#cd7f32'},
                     title='Total de medalhas de ' + pais + ' de 1992 a 2020')
    return pie_fig


# Execute o aplicativo
if __name__ == '__main__':
    app.run(debug=False)
