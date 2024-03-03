# ------------------- Importar modulos -------------------
from metodos_numericos_dcb_fi.utilidades.configuracion import maxIteraciones, text
from metodos_numericos_dcb_fi.utilidades.leerEntrada import funcion
# ------------------- Importar bibliotecas -------------------
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from time import sleep
from IPython.display import clear_output
import sympy as sp
from sympy.abc import x

# ------------------- Funciones -------------------       
def graficarBiseccion(f:funcion, x_i:float, x_s:float, tolerancia:float, animacion:bool=True)->go.Figure:
    # Crear la figura
    fig = go.Figure()
    # Crear la curva de la función
    x = np.linspace(x_i-0.5, x_s+0.5, int(abs(x_s-x_i)*15))
    try:
        y = [f.f(i) for i in x]
    except:
        raise ValueError(f'{text["Errores"]["funcion_no_continua"].replace("{1}", x_i).replace("{2}", x_s)}')
    y_min = min(y)
    y_max = max(y)
    fig.add_trace(go.Scatter(x=x, y=y, name=f'f(x)={f.f_text}', mode='lines', line=dict(color='blue', width=2), showlegend=True))
    fig.update_layout(title=f'Método de bisección para f(x)={f.f_text}<br>x_i={round(x_i, 3)}, x_s={round(x_s,3)} y tolerancia={tolerancia}', xaxis_title='x', yaxis_title='f(x)', title_x=0.5)
    fig.show()
    # Aplicar el método de bisección y graficar
    i = 1
    while i <= maxIteraciones:
        x_m = (x_i + x_s)/2
        fig.add_trace(go.Scatter(x=[x_i, x_i], y=[y_min, y_max], mode='lines', line=dict(color='red', width=1, dash='dash'), showlegend=True, name=f'Limite inferior iteracion {i}: {round(x_i,2)}'))
        fig.add_trace(go.Scatter(x=[x_s, x_s], y=[y_min, y_max], mode='lines', line=dict(color='red', width=1, dash='dash'), showlegend=True, name=f'Limite superior iteracion {i}: {round(x_s,2)}'))
        if f.f(x_m) == 0: # si la raíz es exacta
            fig.add_trace(go.Scatter(x=[x_m], y=[0], mode='markers', marker=dict(color='red', size=10, symbol='diamond-open'), showlegend=True, name=f'Raíz exacta: {round(x_m,5)}'))
            break
        if abs(f.f(x_m)) < tolerancia: # si la raíz es aproximada
            fig.add_trace(go.Scatter(x=[x_m], y=[0], mode='markers', marker=dict(color='red', size=10, symbol='diamond-open'), showlegend=True, name=f'Raíz aproximada: {round(x_m,5)}'))
            break
        fig.add_trace(go.Scatter(x=[x_m], y=[0], mode='markers', marker=dict(color='red', size=5), showlegend=True, name=f'Raíz aproximada iteracion {i}: {round(x_m,2)}'))
        if animacion:
            sleep(1.5)
            clear_output(wait=True)
            fig.show()
        fig.data[-1].marker.color = 'orange'
        fig.data[-2].line.color = 'grey'
        fig.data[-3].line.color = 'grey'
        if f.f(x_i)*f.f(x_m) < 0:
            x_s = x_m
        else:
            x_i = x_m
        i += 1
    
    clear_output(wait=True)
    fig.show()
    return fig

def graficarNR(f:funcion, x_0:float, tolerancia:float, animacion:bool=True)->go.Figure:
    # Crear la figura
    fig = go.Figure()
    # Crear la curva de la función
    x_ = np.linspace(x_0-0.5, x_0+0.5, int(abs(x_0+1)*15))
    try:
        y = [f.f(i) for i in x_]
    except:
        raise ValueError(f'{text["Errores"]["funcion_no_continua_2"].replace("{1}", f.f_text)}')
    fig.add_trace(go.Scatter(x=x_, y=y, name=f'f(x)={f.f_text}', mode='lines', line=dict(color='blue', width=2), showlegend=True))
    fig.update_layout(title=f'Método de Newton-Raphson para f(x)={f.f_text}<br>x_0={round(x_0, 3)} y tolerancia={tolerancia}', xaxis_title='x', yaxis_title='f(x)', title_x=0.5)
    # Aplicar el método de Newton-Raphson y graficar
    i = 1
    df = sp.diff(f.f_text, x) # Derivar la función
    df = sp.lambdify(x, df, 'numpy')
    x_anterior = x_0
    fig.add_trace(go.Scatter(x=[x_anterior], y=[0], mode='markers', marker=dict(color='red', size=5), showlegend=True, name=f'x_0: {round(x_anterior,2)}'))
    fig.show()
    fig.data[-1].marker.color = 'orange'
    while i <= maxIteraciones:
        x_nueva = x_anterior - (f.f(x_anterior)/df(x_anterior))
        if x_nueva < x_.min():
            x_ = np.linspace(x_nueva-0.5, x_0+0.5, int(abs(x_0+1-x_nueva)*15))
            try:
                y = [f.f(i) for i in x_]
            except:
                raise ValueError(f'{text["Errores"]["funcion_no_continua_2"].replace("{1}", f.f_text)}')
            fig.data[0].x = tuple(x_)
            fig.data[0].y = tuple(y)
        fig.add_trace(go.Scatter(x=[x_nueva, x_anterior], y=[0, f.f(x_anterior)], mode='lines', line=dict(color='red', width=1, dash='dash'), showlegend=True, name=f'df({round(x_anterior, 2)})'))
        fig.add_trace(go.Scatter(x=[x_anterior, x_anterior], y=[0,f.f(x_anterior)], mode='lines', line=dict(color='red', width=1, dash='dash'), showlegend=False))
        if abs(f.f(x_nueva)) == 0:
            fig.add_trace(go.Scatter(x=[x_nueva], y=[0], mode='markers', marker=dict(color='red', size=10, symbol='diamond-open'), showlegend=True, name=f'Raíz exacta: {round(x_nueva,5)}'))
            break
        if abs(f.f(x_nueva)) < tolerancia:
            fig.add_trace(go.Scatter(x=[x_nueva], y=[0], mode='markers', marker=dict(color='red', size=10, symbol='diamond-open'), showlegend=True, name=f'Raíz aproximada: {round(x_nueva,5)}'))
            break
        fig.add_trace(go.Scatter(x=[x_nueva], y=[0], mode='markers', marker=dict(color='red', size=5), showlegend=True, name=f'Raíz aproximada iteracion {i}: {round(x_nueva,2)}'))
        if animacion:
            sleep(1.5)
            clear_output(wait=True)
            fig.show()
        fig.data[-1].marker.color = 'orange'
        fig.data[-2].line.color = 'gray'
        fig.data[-3].line.color = 'gray'
        x_anterior = x_nueva
        i += 1

    clear_output(wait=True)
    fig.show()
    

