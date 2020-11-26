"""Home page shown when the user enters the application"""
import streamlit as st

import awesome_streamlit as ast


# pylint: disable=line-too-long
def write():
    """Used to write the page in the app.py file"""
    with st.spinner("Cargando ..."):
        ast.shared.components.title_awesome("")
        st.write(
            """
            Con SAM **Haz seguimiento de tu plan de desarrollo** en tiempo real y desde cualquier lugar.

Conoce como ha ido cambiando la destinación de los recursos del municipio, y el comportamiento de las principales áreas de interés:  Educación, Justicia y Seguridad, Salud y Medio Ambiente.

Conoce cuales son las principales peticiones o solicitudes de la ciudadanía, y cuáles son los temas principales que les interesa comentar en la plataforma Twitter en relación al municipio.

Municipio de Bello, Antioquia
Bello es un municipio de Colombia, su Alcaldía  es una Entidad territorial pública, perteneciente al Departamento de Antioquia. Forma parte de la denominada Área Metropolitana del Valle de Aburrá y está unido con la ciudad de Medellín.
Superficie: 149 km²
Población actual Total: 464,560 habitantes - Urbana: 458,173 habitantes
Para más información:   https://bello.gov.co/
La alcaldía tiene a su cargo la gestión y el uso efectivo de los recursos del municipio, así como la articulación con las entidades gubernamentales. Y a través del Plan de Desarrollo Municipal al igual que todos los municipios el País, materializa la estrategia, lineamientos, objetivos y acciones a desarrollar en el municipio durante un período de la alcaldía.
Actualmente, su administración se ha planteado las siguientes inquietudes,

- Cómo ha cambiado la distribución de los recursos en el municipio considerando el análisis histórico de los planes de desarrollo, con énfasis en los principales sectores: Educación, Justicia y Seguridad, Salud y Medio Ambiente?
- Análisis de los planes de desarrollo, y el cumplimiento de las metas en cada uno de los períodos, y ver la relación entre los indicadores Razón Eficiencia / Eficacia del plan de desarrollo y calificar el desempeño de la gestión del municipio.
- Cómo puedo conocer la percepción en tiempo real de la población que vive en Bello, Antioquia o a través de sus peticiones y solicitudes en las entidades municipales sobre el comportamiento de los sectores específicos como Educación, Salud, Justicia y Seguridad, y Medio Ambiente.



## La magia de SAM

Encuentras información de tus indicadores en un solo lugar…

Te puedes enterar de que están hablando tus ciudadanos en las redes..

Es una plataforma, escalable, y fácil de usar que te permite ver la información desde otra perspectiva, con un alto potencial de crecimiento.


    """
    
       )
       
        st.video('https://youtu.be/neUJOnoQENc')
