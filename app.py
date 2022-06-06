from sympy import symbols, solve, Eq
import streamlit as st

Ti = symbols('x')

st.header("Temperatura interna (Ti)")

st.latex(r'''
    q_{\text{rad}} + q_{\text{resp}} = \pm (q_{\text{cond}} + q_{\text{pis}}) + q_{\text{sven}} + q_{\text{vla}} 
    + q_{\text{fot}} + q_{\text{rtc}}
''')

st.latex(r'''
   q_{\text{rad}} + q_{\text{resp}} = \pm\Big(U A_{c} (T_{i} - T_{e}) + F P (T_{i}-T_{e})\Big) + \\ +\,\dot{\text{m}}\,c_{p}(T_{i} - T_{e}) + E\,FC\,q_{\text{rad}} 
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
    transmitancia_do_piso_ou_veget = st.number_input("Transmitância de piso/vegetação", value=.85)
    comprimento_piso = st.number_input("Comprimento do piso", value=10)
with col2:
    Te = st.number_input("Te", key="te", value=308)
    P = st.number_input("P", key="p", value=33)
    E = st.number_input("E", key="eee", value=0.8)
    transmitancia_na_reirrad = st.number_input("Transmitância na reirradiação", value=.8)
    largura_piso = st.number_input("Largura do piso", value=6)
with col3:
    m_ponto = st.number_input("m_ponto", key="m_ponto", value=4.21)
    Fc = st.number_input("Fc", key="fc", value=0.214)
    emissividade_atmosfera = st.number_input("Emissividade atmosfera", key="Emissividade atmosfera", value=0.83)
    cp = st.number_input("cp", key="cp", value=1006)

expr = Eq(- qrad - .1 * .03 * qrad + (U * Ac * (Ti - Te) + F * P * (Ti - Te)) + m_ponto * cp * (Ti - Te) + E * Fc * qrad
          + .03 * qrad + transmitancia_do_piso_ou_veget * transmitancia_na_reirrad * (comprimento_piso * largura_piso) *
          5.678 * 10 ** (-8) * (Ti ** 4 - emissividade_atmosfera * Te ** 4))

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

expr = Eq(-mp_ponto + ma_ponto * (wi / 100 - we / 100))
sol = solve(expr, wi)

st.write("Umidade relativa interna obtida = {:.2f} % (Obs: Comparar com as umidades de conforto no verão e inverno.)"
         .format(sol[0]))

st.header("Parte 3")

st.latex(r'''
    \eta=\dfrac{T_{\text{BSE}} - (T_{\text{RE}} = T_{e})}{T_{\text{BSE}} - T_{\text{BUE}}}
''')

st.write("Para o we do exercício anterior, achar Tbse na carta.")

col1, col2, col3 = st.columns(3)

with col1:
    tbse = st.number_input("Tbse (°C)", key="tbse", value=34)
with col2:
    tbue = st.number_input("Tbue (°C)", key="tbue", value=28)
with col3:
    tre = st.number_input("Tre (°C)", key="tre", value=29)

eficiencia = (tbse - tre) / (tbse - tbue)

st.write("Eficiência obtida = {:.2f}%".format(eficiencia * 100))

# Achar m_ponto

st.subheader("Cálculo de mp")

col1, col2 = st.columns(2)

with col1:
    st.latex(r'''
        F_{\text{elev}} = \dfrac{101325}{BP}
    ''')
    st.latex(r'''
        F_{\text{temp}} = \dfrac{\text{3.89}}{T_{\text{externa do ar}} - T_{\text{RE}}}
    ''')
    st.latex(r'''
        F_{\text{cv}} = F_{\text{elev}}\,F_{\text{luz}}\,F_{\text{temp}}
    ''')
with col2:
    st.latex(r'''
        F_{\text{luz}} = \dfrac{\text{Intensidade de luz}}{53819.55}
    ''')
    st.latex(r'''
        F_{\text{temp}} = \dfrac{\text{5.52}}{\sqrt{{\text{largura}_{\text{estufa}}}}}
    ''')

st.write("Verificar qual é maior entre Fcv e Fvel")

st.latex(r'''
    \dot{V} = \text{comprimento}\times\text{largura}_\text{estufa}\times0.04064\times(F_{\text{cv}}\,||\,F_{\text{vel}})
''')

colA, colB, colC = st.columns(3)

with colA:
    bp = st.number_input("Pressão barométrica (Pa)", value=101700)
    intensidade_luz = st.number_input("Intensidade de luz (lux)", value=150000)
with colB:
    t_externa_do_ar = st.number_input("Temperatura externa do ar (°C)", value=35)
    tre = st.number_input("Tre (Temperatura de resfriamento)", value=tre)
with colC:
    largura_da_estufa = st.number_input("Largura da estufa (face menor)", value=10)
    densidade_ar = st.number_input("Densidade do ar (1.07 kg/m³)", value=1.07)

# Verificar qual é maior (Fcv e Fvel)
# Novo v_ponto = comprimento *largura_da_estufa * 0.04064 * (Fcv || Fvel)

# ma_ponto = v_ponto * rho (depende de T)

felev = 101325/bp
fluz = intensidade_luz/53819.55
ftemp = 3.89/(t_externa_do_ar - tre)
fvel = 5.52/largura_da_estufa**.5
fcv = felev * fluz * ftemp

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Felev = {:.3f}".format(felev))
    st.write("Fluz = {:.3f}".format(fluz))
with col2:
    st.write("Ftemp = {:.3f}".format(ftemp))
    st.write("Fvel = {:.3f}".format(fvel))
with col3:
    st.write("Fcv = {:.3f}".format(fcv))

if fcv > fvel:
    maior = fcv
else:
    maior = fvel

v_ponto = comprimento_piso * largura_da_estufa * .04064 * maior
m_ponto_x = v_ponto * densidade_ar

st.write("Fluxo mássico obtido {:.2f} kg/s".format(m_ponto_x))

st.subheader("Novo Ti")

colX, colY = st.columns(2)

with colX:
    m_ponto = st.number_input("m_ponto", value=m_ponto_x)
with colY:
    Te = st.number_input("Te", value=t_externa_do_ar + 273)

expr = Eq(- qrad - .1 * .03 * qrad + (U * Ac * (Ti - Te) + F * P * (Ti - Te)) + m_ponto * cp * (Ti - Te) + E * Fc * qrad
          + .03 * qrad + transmitancia_do_piso_ou_veget * transmitancia_na_reirrad * (comprimento_piso * largura_piso) *
          5.678 * 10 ** (-8) * (Ti ** 4 - emissividade_atmosfera * Te ** 4))

sol = solve(expr, Ti)

st.write("Nova temperatura interna obtida = {:.2f} °C (Obs: Comparar com temperaturas de conforto no verão e inverno.)"
         .format(sol[1] - 273.15))
