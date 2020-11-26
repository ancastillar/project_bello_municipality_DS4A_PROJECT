"""Main module for the streamlit app"""
import streamlit as st

import awesome_streamlit as ast
import src.pages.about
import src.pages.gallery.index
import src.pages.home
import src.pages.resources
import src.pages.vision
import src.pages.pqrs


ast.core.services.other.set_logging_format()

PAGES = {
    "Inicio": src.pages.home,
    "Estadisticas Generales": src.pages.resources,
    "Analisis detallado alcaldia de Bello": src.pages.vision,
    "Percepción ciudadania en twitter": src.pages.about,
    "Percepción ciudadania en PQRSD": src.pages.pqrs,
}


def main():
    """Main function of the App"""
    st.sidebar.title("Menu Principal")
    selection = st.sidebar.radio("Ir a", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Cargando {selection} ..."):
        ast.shared.components.write_page(page)
    st.sidebar.title("Problema Principal")
    st.sidebar.info(
        "Como entidad territorial - La Alcaldía es la encargada de **administrar los recursos de cada municipio**; y velar por que estos recursos sean utilizados de manera efectiva, para generar bienestar a sus habitantes, así como la articulación con las entidades gubernamentales."
    )
    st.sidebar.title("Sobre Nosotros")
    st.sidebar.info(
        """
        Somos un grupo interdisciplinario de profesionales pertenecientes a la cohorte 2020 del programa Data Science for All. Nuestro propósito es aplicar la ciencia de datos junto con el conocimiento de nuestras carreras para buscar soluciones a problemas  presentes en la administración de recursos públicos, especialmente a nivel territorial. Para el diseño de la interfaz nos basamos en el desarrollo open source de Marc Skov Madsen, mas información aqui:
        [datamodelsanalytics.com](https://datamodelsanalytics.com).
"""
    )


if __name__ == "__main__":
    main()
