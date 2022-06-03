from sympy import symbols, solve, Eq
import streamlit as st

Ti = symbols('x')

st.header("Temperatura interna (Ti)")

st.latex(r'''
    q_{\text{rad}} + q_{\text{resp}} = \pm (q_{\text{cond}} + q_{\text{pis}}) + q_{\text{sven}} + q_{\text{vla}} 
    + q_{\text{fot}} + q_{\text{rtc}}
''')

st.latex(r'''
   q_{\text{rad}} + q_{\text{resp}} = \pm\Big(U A_{c} (T_{i} - T_{e}) + F P (T_{i}-T_{e})\Big) + \dot{\text{m}}c_{p}(T_{i} - T_{e}) + E\,FC\,q_{\text{rad}} 
    + q_{\text{fot}} + (T_{i}^{4} - \epsilon T_{e}^{4}) 
''')

col1, col2, col3 = st.columns(3)

with col1:
    qrad = st.number_input("qrad (W)", key="qrad", value=42310.6)
with col2:
    qresp = st.number_input("qresp (W)", key="qresp", value=2952.31)
with col3:
    qfot = st.number_input("qfot (W)", key="qfot", value=1269.048)

with col1:
    U = st.number_input("U", key='U', value=7.14)
    Ac = st.number_input("Ac", key='Ac', value=1)
    F = st.number_input("F", key='F', value=1.4)
with col2:
    Te = st.number_input("Te", key="te", value=308)
    P = st.number_input("P", key="p", value=33)
    E = st.number_input("E", key="eee", value=0.8)

with col3:
    m_ponto = st.number_input("m_ponto", key="m_ponto", value=4.21)
    Fc = st.number_input("Fc", key="fc", value=0.214)
    epsilon = st.number_input("epsilon", key="epsilon", value=0.83)
    cp = st.number_input("cp", key="cp", value=1006)

expr = Eq(- qrad - qresp + (U * Ac * (Ti - Te) + F * P * (Ti - Te)) + m_ponto * cp * (Ti - Te) + E * Fc * qrad + qfot + (
            Ti ** 4 - epsilon * Te ** 4))

sol = solve(expr, Ti)

st.write("Temperatura interna obtida = {:.2f} °C (Obs: Comparar com temperaturas de conforto no verão e inverno.)"
         .format(sol[1] - 273.15))

# Balanço de massa
# mp_ponto = ma_ponto * (wi - we)
# wi = mp_ponto/ma_ponto + we

st.header("Balanço de massa (wi)")

st.latex(r'''
    \dot{\text{m}}_{p} = \dot{\text{m}}_{v}
''')

st.latex(r'''
    \dot{\text{m}}_{p} = \dot{\text{m}}_{a}\,(\omega_{i} - \omega_{e})
''')

colA, colB, colC = st.columns(3)

with colA:
    mp_ponto = st.number_input("mp_ponto (kg/s)", key="mp_ponto", value=5)
with colB:
    ma_ponto = st.number_input("ma_ponto (kg/s)", key="ma_ponto", value=2)
with colC:
    we = st.number_input("we (%)", key="we", value=67)

wi = symbols("x")

expr = Eq(-mp_ponto + ma_ponto * (wi/100 - we/100))
sol = solve(expr, wi)

st.write("Umidade relativa interna obtida = {:.2f} % (Obs: Comparar com as umidades de conforto no verão e inverno.)"
         .format(sol[0]))

st.header("Parte 3")

st.latex(r'''
    \eta=\dfrac{T_{\text{BSE}} - (T_{\text{RE}} = T_{e})}{T_{\text{BSE}} - T_{\text{BUE}}}
''')

st.write("Para o we do exercício anterior, achar Tbse na carta.")