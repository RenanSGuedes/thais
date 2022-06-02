from sympy import symbols, solve, Eq
import streamlit as st

Ti = symbols('x')

col1, col2, col3 = st.columns(3)

with col1:
    qrad = st.number_input("qrad", key="qrad", value=42310.6)
with col2:
    qresp = st.number_input("qresp", key="qresp", value=2952.31)
with col3:
    qfot = st.number_input("qfot", key="qfot", value=1269.048)

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

st.write(sol[1] - 273)
