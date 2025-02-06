import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

def extract_update_name(text):
    if "update" in text.lower():
        idx = text.lower().index("update")
        return text[:idx + len("update")]
    return text

def generate_traffic_plot_with_predefined_updates():
    # Create a row with 2 columns
    col1, col2 = st.columns([1, 7])

    # Column for the image (left)
    with col1:
        # Make sure to have an image at the specified path or pass a direct URL
        st.image("https://raw.githubusercontent.com/nurdigitalmarketing/previsione-del-traffico-futuro/9cdbf5d19d9132129474936c137bc8de1a67bd35/Nur-simbolo-1080x1080.png", width=80)

    # Column for the title and the text "by NUR® Digital Marketing" (center)
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
            
            if st.checkbox("Vuoi aggiungere altri aggiornamenti?"):
                new_update_date = st.text_input("Inserisci la data dell'update (formato '14 Sep 2023'):")
                new_update_name = st.text_input("Inserisci il nome dell'update fino alla parola 'update':")
                if new_update_date and new_update_name:
                    update_dates_list.append(new_update_date)
                    update_names_list.append(new_update_name)
            
            update_dates = [datetime.datetime.strptime(date, "%d %b %Y") for date in update_dates_list]
            dates = pd.to_datetime(data['Date'])
            
            plt.figure(figsize=(15,7))
            plt.plot(dates, data['Organic Traffic'], label='Utenti')

            y_position = data['Organic Traffic'].max() - (0.4 * data['Organic Traffic'].max())
            for date, update_name in zip(update_dates, update_names_list):
                # Check if the date is within the range of dataset dates
                if date >= dates.min() and date <= dates.max():
                    plt.axvline(date, linestyle='--', color='grey')  # Use a more visible color
                    plt.text(date, y_position, update_name, rotation=90, color='black', fontsize=9, 
                             ha='right', va='bottom', backgroundcolor='white')

            plt.title("Trend del traffico in relazione ai recenti Google Updates")
            plt.xlabel("Data")
            plt.ylabel("Utenti")
            plt.legend()
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            plt.tight_layout()
            
            st.pyplot(plt)

def get_predefined_updates():
    update_dates_list = [
        '19 Dec 2024', '12 Dec 2024', '11 Nov 2024', '15 Aug 2024', '20 Jun 2024', '5 Mar 2024', '8 Nov 2023', '2 Nov 2023', '5 Oct 2023', '14 Sep 2023', '22 Aug 2023', '12 Apr 2023', '15 Mar 2023', '21 Feb 2023',
        '14 Dec 2022', '5 Dec 2022', '19 Oct 2022', '20 Sep 2022', '12 Sep 2022',
        '25 Aug 2022', '27 Jul 2022', '25 May 2022', '23 Mar 2022', '22 Feb 2022', '1 Dec 2021',
        '17 Nov 2021', '3 Nov 2021', '26 Jul 2021', '1 Jul 2021', '28 Jun 2021', '23 Jun 2021',
        '15 Jun 2021', '2 Jun 2021', '8 Apr 2021'
    ]
    
    update_names_list = [
        extract_update_name(name) for name in [
            'Released the December 2024 spam update',
            'Released the December 2024 core update',
            'Released the November 2024 core update',
            'Released the August 2024 core update',
            'Released the June 2024 spam update',
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
    return update_dates_list, update_names_list

if __name__ == "__main__":
    generate_traffic_plot_with_predefined_updates()
