import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

def extract_update_name(text):
    if "update" in text.lower():
        idx = text.lower().index("update")
        return text[:idx + len("update")]
    return text

def generate_traffic_plot_with_predefined_updates():
    col1, col2 = st.columns([1, 7])

    with col1:
        st.image("https://raw.githubusercontent.com/nurdigitalmarketing/previsione-del-traffico-futuro/9cdbf5d19d9132129474936c137bc8de1a67bd35/Nur-simbolo-1080x1080.png", width=80)

    with col2:
        st.title('Tendenza del Traffico Attuale')
        st.markdown('###### by [NUR® Digital Marketing](https://www.nur.it)')

        with st.expander("Come Funziona"):
            st.markdown("""
            Per utilizzare questa applicazione, segui questi passi:

            1. Vai su **Ahrefs - Site Explorer**.
            2. Seleziona **Panoramica**, poi **Ricerca Organica**.
            3. Imposta il periodo di tempo a **1 anno (o 2 se disponibili)** e la granularità a **Giornaliera**.
            4. Clicca su **Esporta** per scaricare i dati.
            5. Apri il file esportato e rimuovi le prime righe, mantenendo solo i dati relativi al numero di utenti.
            6. Rinomina la colonna A in "Date" e la colonna B in "Organic Traffic", e salva il file in formato `.csv`.
            """)

        with st.expander("Note Importanti"):
            st.markdown("""
            - All'interno dello script, è presente un elenco degli update core di Google dal 2022 ad oggi.
            - È consigliabile verificare regolarmente se ci sono stati nuovi aggiornamenti visitando [Google Search Central](https://status.search.google.com/products/rGHU1u87FJnkP6W2GwMi/history) e aggiornare di conseguenza l'elenco degli update nell'applicazione.
            """)

        st.markdown("---")
        uploaded_file = st.file_uploader("Carica il file CSV dei dati di traffico", type="csv")
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            update_dates_list, update_names_list = get_predefined_updates()
            update_dates = [datetime.datetime.strptime(date, "%d %b %Y") for date in update_dates_list]
            dates = pd.to_datetime(data['Date'])
            data['Date'] = dates
            
            fig = px.line(data, x='Date', y='Organic Traffic', title='Andamento del traffico da tutte le fonti di acquisizione', labels={'Date': 'Data', 'Organic Traffic': 'Utenti'})
            
            for date, name in zip(update_dates, update_names_list):
                if date >= dates.min() and date <= dates.max():
                    fig.add_vline(x=date, line_dash="dash", line_color="grey", annotation_text=name, annotation_position="top left")

            fig.update_layout(xaxis=dict(tickformat="%d %b %Y"), hovermode="x")
            fig.update_traces(mode="lines+markers")
            st.plotly_chart(fig, use_container_width=True)

def get_predefined_updates():
    # Elenco degli update core di Google
    return [
        '5 Mar 2024', '8 Nov 2023', '2 Nov 2023', '5 Oct 2023', '14 Sep 2023', '22 Aug 2023', '12 Apr 2023', '15 Mar 2023', '21 Feb 2023',
        '14 Dec 2022', '5 Dec 2022', '19 Oct 2022', '20 Sep 2022', '12 Sep 2022',
        '25 Aug 2022', '27 Jul 2022', '25 May 2022', '23 Mar 2022', '22 Feb 2022', '1 Dec 2021',
        '17 Nov 2021', '3 Nov 2021', '26 Jul 2021', '1 Jul 2021', '28 Jun 2021', '23 Jun 2021',
        '15 Jun 2021', '2 Jun 2021', '8 Apr 2021'
    ], [
        extract_update_name(name) for name in [
            'Released the March 2024 core update',
            'Released the November 2023 reviews update',
            'Released the November 2023 core update',
            'Released the October 2023 core update',
            'Released the September 2023 helpful content update',
            'Released the August 2023 core update',
            'Released the April 2023 reviews update',
            'Released the March 2023 core update',
            'Released the February 2023 product reviews update',
            'Released the December 2022 link spam update',
            'Released the December 2022 helpful content update',
            'Released the October 2022 spam update',
            'Released the September 2022 product reviews update',
            'Released the September 2022 core update',
            'Released the August 2022 helpful content update',
            'Released the July 2022 product reviews update',
            'Released the May 2022 core update',
            'Released the March 2022 product reviews update',
            'Released the page experience update for desktop',
            'Released the December 2021 product reviews update',
            'Released the November 2021 core update',
            'Released the November 2021 spam update',
            'Released the July 2021 link spam update',
            'Released the July 2021 core update',
            'Released the first part of the June 2021 spam update',
            'Released the second part of the June 2021 spam update',
            'Released the page experience update for mobile',
            'Released the June 2021 core update',
            'Released the April 2021 product reviews update'
        ]
    ]

if __name__ == "__main__":
    generate_traffic_plot_with_predefined_updates()
