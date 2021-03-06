from sympy import symbols, solve, Eq
import streamlit as st
from PIL import Image

Ti = symbols('x')

image = Image.open('images/greenhouses.jpeg')

st.image(image, caption=None)

st.header("Parte 2")
st.write(
    "[Link para achar qrad, qresp e qfot](https://docs.google.com/spreadsheets/d/1vZasm4fKt2AkOGR2y5VmaQlKSd5nDu_07daHEjmvXk0/edit#gid=1896904256)"
)

with st.expander("Temperatura interna (Ti)"):
    st.latex(r'''
        q_{\text{rad}} + q_{\text{resp}} = \pm (q_{\text{cond}} + q_{\text{pis}}) + q_{\text{sven}} + q_{\text{vla}} 
        + q_{\text{fot}} + q_{\text{rtc}}
    ''')

    st.latex(r'''
       q_{\text{rad}} + q_{\text{resp}} = \pm\Big(U A_{c} (T_{i} - T_{e}) + F P (T_{i}-T_{e})\Big) + \\ +\,\dot{\text{m}}\,c_{p}(T_{i} - T_{e}) + E\,FC\,q_{\text{rad}} 
        + q_{\text{fot}} + \tau_{pv}\tau_{\text{ri}}A\sigma(T_{i}^{4} - \epsilon T_{e}^{4}) 
    ''')

    st.latex(r'''
           q_{\text{rad}} + 0.003\cdot q_{\text{rad}} = \pm\Big(U A_{c} (T_{i} - T_{e}) + F P (T_{i}-T_{e})\Big) + \\ +\,\dot{\text{m}}\,c_{p}(T_{i} - T_{e}) + E\,FC\,q_{\text{rad}} 
            + 0.03\cdot q_{\text{rad}} + \tau_{pv}\tau_{\text{ri}}(C_{\text{piso}}\cdot L_{\text{piso}})\sigma(T_{i}^{4} - \epsilon T_{e}^{4}) 
        ''')

    col1, col2, col3 = st.columns(3)

    with col1:
        qrad = st.number_input("Taxa de transferência de calor por radiação (qrad, em W)", key="qrad", step=.01, value=42310.60, help="Hello")
    with col2:
        qresp = st.number_input("Taxa de transferência de calor devido a respiração (q_resp, em W)", key="qresp", step=.01, value=2952.31)
    with col3:
        qfot = st.number_input("Taxa de transferência de calor devido a fotossíntese (q_fot, em W)", key="qfot", step=.01, value=1269.048)

    with col1:
        U = st.number_input("Coeficiente global (U, em W/(m² · K))", key='U', step=.01, value=7.14)
        Ac = st.number_input("Ac", key='Ac', step=.01, value=771.00)
        F = st.number_input("Fator perimetral (F)", key='F', step=.01, value=1.40)
        transmitancia_do_piso_ou_veget = st.number_input("Transmitância de piso/vegetação (tau_pv, de 0 a 1)", step=.01, value=.85)
        comprimento_piso = st.number_input("Comprimento do piso (C_piso, em m)", step=.01, value=50.00)
    with col2:
        Te = st.number_input("Temperatura externa (T_e, em K)", key="te", step=.01, value=308.00)
        P = st.number_input("Perímetro (P, em m)", key="p", step=.01, value=33.00)
        E = st.number_input("E", key="eee", step=.01, value=0.80)
        transmitancia_na_reirrad = st.number_input("Transmitância na reirradiação (tau_ri, de 0 a 1)", step=.01, value=.80)
        largura_piso = st.number_input("Largura do piso (L_piso, em m)", step=.01, value=6.00)
    with col3:
        m_ponto = st.number_input("m_ponto", key="m_ponto", step=.01, value=4.21)
        Fc = st.number_input("Fc", key="fc", step=.01, value=0.214)
        emissividade_atmosfera = st.number_input("Emissividade atmosfera", key="Emissividade atmosfera", step=.01, value=0.83)
        cp = st.number_input("Calor específico (cp, em J/(kg · K)", key="cp", step=.01, value=1006.00)

    expr = Eq(- qrad - .1 * .03 * qrad + (U * Ac * (Ti - Te) + F * P * (Ti - Te)) + m_ponto * cp * (Ti - Te) + E * Fc * qrad
              + .03 * qrad + transmitancia_do_piso_ou_veget * transmitancia_na_reirrad * (comprimento_piso * largura_piso) *
              5.678 * 10 ** (-8) * (Ti ** 4 - emissividade_atmosfera * Te ** 4))

    sol = solve(expr, Ti)

    st.write("Temperatura interna obtida = {:.2f} °C (Obs: Comparar com temperaturas de conforto no verão e inverno.)"
             .format(sol[1] - 273.15))

# Balanço de massa
# mp_ponto = ma_ponto * (wi - we)
# wi = mp_ponto/ma_ponto + we


with st.expander("Balanço de massa (wi)"):

    st.latex(r'''
        \dot{\text{m}}_{p} = \dot{\text{m}}_{v}
    ''')

    st.latex(r'''
        \dot{\text{m}}_{p} = \dot{\text{m}}_{a}\,(\omega_{i} - \omega_{e})
    ''')

    colA, colB, colC = st.columns(3)

    with colA:
        mp_ponto = st.number_input("mp_ponto (Evapotranspiração da planta) (kg/s)", key="mp_ponto", step=.01, value=4.05)
    with colB:
        ma_ponto = st.number_input("ma_ponto (kg/s)", key="ma_ponto", step=.01, value=27.00)
    with colC:
        we = st.number_input("we (Umidade relativa externa INV/VER) (%)", key="we", step=.01, value=68.00)

    wi = symbols("x")

    expr = Eq(-mp_ponto + ma_ponto * (wi / 100 - we / 100))
    sol = solve(expr, wi)

    st.write("Umidade relativa interna obtida = {:.2f} % (Obs: Comparar com as umidades de conforto no verão e "
             "inverno.) "
             .format(sol[0]))

st.header("Parte 3")

with st.expander("Eficiência"):
    st.write(
        "[Achar TBSU a partir da TBSE, UR e Altitude](http://www.agais.com/toolbox/psicrometria3.php)"
    )

    st.latex(r'''
        \eta=\dfrac{T_{\text{BSE}} - (T_{\text{resfriamento}} = T_{e})}{T_{\text{BSE}} - T_{\text{BUE}}}
    ''')

    st.write(
        "Para o we do exercício anterior, achar TBSE na carta"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        tbse = st.number_input("Tbse (°C)", key="tbse", step=.01, value=30.40)
    with col2:
        tbue = st.number_input("Tbue (°C)", key="tbue", step=.01, value=22.20)
    with col3:
        eficiencia = st.number_input("Eficiência (%)", key="eficiencia", step=.01, value=85.00)

    tre = tbse - (eficiencia / 100) * (tbse - tbue)

    st.write("Temperatura = {:.2f}°C".format(tre))

# Achar m_ponto

with st.expander("Fluxo mássico"):
    col1, col2 = st.columns(2)

    with col1:
        st.latex(r'''
            F_{\text{elev}} = \dfrac{101325}{BP}
        ''')
        st.latex(r'''
            F_{\text{temp}} = \dfrac{\text{3.89}}{\Delta{T}}
        ''')
        st.latex(r'''
            F_{\text{cv}} = F_{\text{elev}}\,F_{\text{luz}}\,F_{\text{temp}}
        ''')
    with col2:
        st.latex(r'''
            F_{\text{luz}} = \dfrac{\text{Intensidade de luz}}{53819.55}
        ''')
        st.latex(r'''
            F_{\text{vel}} = \dfrac{\text{5.52}}{\sqrt{{\text{comprimento}_{\text{estufa}}}}}
        ''')

    st.write("Verificar qual é maior entre Fcv e Fvel")

    st.latex(r'''
        \dot{V} (\text{m³/s}) = \text{comprimento}\times\text{largura}_\text{estufa}\times0.04064\times(F_{\text{cv}}\,||\,F_{\text{vel}})
    ''')

    colA, colB, colC = st.columns(3)

    with colA:
        bp = st.number_input("Pressão barométrica (Pa)", step=.01, value=93997.00)
        intensidade_luz = st.number_input("Intensidade de luz (lux)", step=.01, value=150710.00)
    with colB:
        delta_T = st.number_input("Delta T (chute, Thais considerou = 1)", step=.01, value=3.89)
    with colC:
        largura_da_estufa = st.number_input("Largura da estufa (m) (cal/g°C)", step=.01, value=10.00)
        densidade_ar = st.number_input("Densidade do ar (1.07 kg/m³)", step=.01, value=1.05)

    # Verificar qual é maior (Fcv e Fvel)
    # Novo v_ponto = comprimento *largura_da_estufa * 0.04064 * (Fcv || Fvel)

    # ma_ponto = v_ponto * rho (depende de T)

    felev = 101325/bp
    fluz = intensidade_luz/53819.55
    ftemp = 3.89/delta_T
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

    st.write("Fluxo volumétrico obtido = {:.2f} (m³/s)".format(v_ponto))
    st.write("Fluxo mássico obtido = {:.2f} (kg/s)".format(m_ponto_x))

with st.expander("Novo Ti"):
    st.latex(r'''
       q_{\text{rad}} + 0.003\cdot q_{\text{rad}} = \pm\Big(U A_{c} (T_{i} - T_{e}) + F P (T_{i}-T_{e})\Big) + \\ +\,\dot{\text{m}}\,c_{p}(T_{i} - T_{\text{resfriamento}}) + E\,FC\,q_{\text{rad}} 
        + 0.03\cdot q_{\text{rad}} +\\
        +\,\tau_{pv}\tau_{\text{ri}}(C_{\text{piso}}\cdot L_{\text{piso}})\sigma(T_{i}^{4} - \epsilon T_{e}^{4}) 
    ''')

    colX, colY, colZ = st.columns(3)

    with colX:
        m_ponto = st.number_input("m_ponto (kg/s)", step=.01, value=m_ponto_x)
        qrad = st.number_input("qrad (W)", step=.01, value=322000.00)
    with colY:
        Te = st.number_input("Temperatura externa (T_e, em K)", step=.01, value=30.40 + 273.15)
    with colZ:
        T_resfriamento = st.number_input("Temperatura de resfriamento (T_resfriamento, em K)", step=.01, value=tre + 273.15)

    expr = Eq(- qrad - .1 * .03 * qrad + (U * Ac * (Ti - Te) + F * P * (Ti - Te)) + m_ponto * cp * (Ti - T_resfriamento) + E * Fc * qrad
              + .03 * qrad + transmitancia_do_piso_ou_veget * transmitancia_na_reirrad * (comprimento_piso * largura_piso) *
              5.678 * 10 ** (-8) * (Ti ** 4 - emissividade_atmosfera * Te ** 4))

    sol = solve(expr, Ti)

    st.write("Nova temperatura interna obtida = {:.2f} °C (Obs: Comparar com temperaturas de conforto no verão e inverno.)"
             .format(sol[1] - 273.15))

with st.expander("Balanço de massa (wi)"):

    st.latex(r'''
        \dot{\text{m}}_{p} = \dot{\text{m}}_{v}
    ''')

    st.latex(r'''
        \dot{\text{m}}_{p} = \dot{\text{m}}_{a}\,(\omega_{i} - \omega_{e})
    ''')

    colA, colB, colC = st.columns(3)

    with colA:
        mp_ponto = st.number_input("mp_ponto (Evapotranspiração da planta) (kg/s)", key="mp_ponto_2", step=.01, value=4.05)
    with colB:
        ma_ponto = st.number_input("ma_ponto (kg/s)", key="ma_ponto_2", step=.01, value=27.00)
    with colC:
        we = st.number_input("we (Umidade relativa externa) (%)", key="we_2", step=.01, value=68.00)

    wi = symbols("x")

    expr = Eq(-mp_ponto + ma_ponto * (wi / 100 - we / 100))
    sol = solve(expr, wi)

    st.write("Umidade relativa interna obtida = {:.2f} % (Obs: Comparar com as umidades de conforto no verão e "
             "inverno.) "
             .format(sol[0]))
