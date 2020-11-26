# DS4A project
Present historical information of the development plan of the municipality of Bello - Antioquia to facilitate the vision, and support the management of its administration.

## Installation
Install libraries necessary for the project
```
pip install -r requirements.txt
pip install -r requirements2.txt
```

## Run
Run this command to start the app. 
```bash
streamlit run app.py
```


## Architecture 🚀
The architecture is based on AWS, the services used are:
1. EC2 -> In which the main algorithms are housed.
2. S3 Bucket -> The SIEE file uploaded by the municipalities is stored.
3. Lambda -> Allows you to host the application that consumes the Twitter API.
4. RDS -> A database is used in Postgress.

_These instructions will allow you to know which services are used to deploy the entire application._

Check **Deployment** to know how to deploy the project.

<div align="center">
       <img src="images/Diagrama.png?raw=true" width="400px"</img> 
</div>



### Project Layout 

As our application grows we would refactor our app.py file into multiple folders and files.

```bash
.
├── app.py
├── terridata_process.py
├── listener_twitter.py
├── class_PQRS.py
├── emotionals.py
├── main_twitter.py
├── database_process.py
├── graficar.py
├── Preprocess.py
├── Preprocess.py
├── model
|   └── model
|       └── my_model_emtion.h5
├── EmoLex
|   └── EmoLex
|       ├── anger.txt
|       ├── anticipation.txt
|       ├── disgust.txt
|       ├── fear.txt
|       ├── joy.txt
|       ├── negative.txt
|       ├── positive.txt
|       ├── sadness.txt
|       ├── surprise.txt
|       └── trust.txt
└── src
|   └── pages 
|       ├── pqrs.py
|       ├── home.py
|       ├── resources.py
|       ├── vision.py
|       └── about.py
└── Data
    └── Data 
        ├── consolidado_general_con_sectores_modelos.csv
        ├── consolidado_general_con_sectores.csv
        └── consolidado_para_percepcion.csv

```

## Despliegue 📦

Run this command to deploy the app. 
```
docker build -t ds4a 
docker-compose up -d
```

## Twitter 🖥
Here are some examples of twitter in the security area. The Tweet is in the native language of the country where it was implemented, Colombia.
------
1. RT @EmpresarioVox: El Gobierno oculta que estamos totalmente a la deriva. Hace meses saltó la alarma en la Seguridad Social porque el gasto…
2. RT @laurxweird: "conocí a esta belleza cuando estaba protegiendo a un hombre sin hogar de ser acosado por alguien de seguridad"
Esta es mi…
3. RT @CIDH: Por último, la #CIDH reitera al Estado las recomendaciones formuladas durante su reciente visita in loco, especialmente la de lle…
4. RT @GNB_Sucre: #OperaciónGarraOriental2020 
Nuestros efectivos trabajan de manera articulada con cuerpos policiales para velar por tu segur…
5. RT @Lautafym: La pandemia de las fuerzas de seguridad del mundo tiene mucho más tiempo de vigencia que cualquier otra. Es más difícil de cu…
6. RT @diario24horas: El presidente Andrés Manuel López Obrador elogió el trabajo realizado por titular de la Secretaría de Seguridad y Protec…
7. RT @lqmhr: Tenemos un Canciller que no habla inglés. Es como tener, no sé, una antropóloga como Ministra de Seguridad.
Espero no leer vuestros tweets hablando sobre las medidas de seguridad cuando sois los primeros que no las cumplís máquinas
8. RT @Millerrojas19: @RicardoMolanoV1 @qmoncaleano @MdeFrancisco12 @fdbedout @MeDicenWally Comparto. Totalmente
En Colombia alcanzan un cargo…
9. RT @lvillavicenciom: autoridad civil, es que sus miembros son formados ideológicamente bajo los estertores de la doctrina de la seguridad n…


--------

## Built with 🛠️
_Mention the tools you used to create your project_

* [Streamlit](https://github.com/MarcSkovMadsen/awesome-streamlit) - The best Framework to develop apps
* [Plotly](https://plotly.com/) - Graphs
* [ROME](https://rometools.github.io/rome/) - Usado para generar RSS


## Video 📖
[![ScreenShot](images/port.png?raw=true)](https://www.youtube.com/watch?v=neUJOnoQENc)

## Versions 📌
We use [SemVer](http://semver.org/) for versioning. For all available versions, see what[tags in this repository](https://github.com/tu/proyecto/tags).

## Authors ✒️
* **Andres Felipe Velasquez** - *Member DS4a* - [afvrsystems](https://github.com/afvrsystems)
* **Laura Lopez** - *Member DS4a* - [Lauravlopez](https://github.com/Lauravlopez)
* **Natalia Castilla Reyes** - *Member DS4a* - [ancastillar](https://github.com/ancastillar)
* **Olga Angulo** - *Member DS4a* - [Olucya](https://github.com/Olucya)
* **Jhon Rodriguez** - *Member DS4a* - [Lauravlopez](https://github.com/Lauravlopez)
* **Migue Jurado** - *Member DS4a* - [Miguel Jurado](https://github.com/migeruj)
* **Adonai Vera** - *Member DS4a* - [AdonaiVera](https://github.com/AdonaiVera)

You can also look at the list of all [contributors](https://github.com/AdonaiVera/Bello/contributors) who have participated in this project. 

## License 📄

This project is under the License, see the file [LICENSE.md](LICENSE.md) more details.

## Expressions of Gratitude🎁

* Tell others about this project 📢
* Give thanks publicly 🤓.


---
