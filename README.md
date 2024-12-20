# Reto Multiagentes

## Ejecución

  El comando principal de ejecución es el siguiente:
  `python Main.py BinPacking --ListaCSV Prod7.csv --Confianza 7.43 --VRackC 122:46:160 --VRackR 80.01:208.03:213.61 --VRackS 182.9:195.5:60.96 --salidaCSV volCalculado.csv`
  Tiene las variables en el parser:

  - ListaCsv: La lista de productos proporcionada por el socio formador. Para este programa se tiene que usar una versión modificada de los datos ya que los ajustamos para que los cálculos fueran más precisos. Por esta razón se tiene que usar el csv `Prod7.csv` Ademas de que este csv no incluye la harina ni el aceite que no se almacenan en racks.
  - Confianza: Es el márgen de error.
  - VRackC: Son las medidas de los racks que se usarán para guardar ingredientes congelados.
  - VRackR: Son las medidas de los racks que se usarán para guardar ingredientes refrigerados.
  - VRackS: Son las medidas de los racks que se usarán para guardar ingredientes secos.
  - salidaCSV: Es el nombre del archivo csv donde se guardaran los productos, su cantidad en cada rack y el rack en el que están localizados.

    Usando BinPacking se pueden obtener los siguientes acomodos de los 3 racks de ingredientes secos obtenidos:
    <p align="center">
      <img src="imagenesREADME/Figure_1_BinPacking.png" width="30%">
      <img src="imagenesREADME/Figure_2_BinPacking.png" width="30%">
      <img src="imagenesREADME/Figure_3_BinPacking.png" width="30%">
    </p>

  El comando de la simulación es el siguiente: `python Main.py Simulacion` Este comando ejecuta la simulación usando multiagentes que se mueven a cada nodo (rack).
  Vista Aerea de la simulación
  ![Vista Aerea](imagenesREADME/simulation_screenshot.png)

  El comando secundario para obtener el volumen de los ingredientes congelados es `python VolumenCongelados.py`.
  
## Conformación del Equipo

**Integrantes del equipo**  

- Esteban Leal Menéndez - Colíder y desarrollador  
  - **Fortalezas:** Soy una persona entusiasta que aprende rápido. Me gusta retarme y descubrir talentos nuevos. Trabajo bien en equipo y soy líder cuando se necesita.
  - **Áreas de oportunidad:** Puedo llegar a procrastinar tareas lo cual me puede llegar a generar estrés y disminuir mi eficiencia y eficacia.
  - **Expectativas del bloque:** Espero fortalecer el trabajo en equipo, fortalecer la comunicación y el análisis espacial.

- Daniel Arteaga Mercado - Líder  
  - **Fortalezas:** Soy una persona responsable y comprometida con los objetivos planteados, me desenvuelvo de manera adecuada al trabajar colaborativamente y siempre trato de aportar ideas innovadoras/creativas.
  - **Áreas de oportunidad:** A veces no comunico asertivamente mis ideas y me cuesta asignar tiempos específicos para la realización de tarea.
  - **Expectativas del bloque:** Espero poder trabajar de manera fluida y eficiente junto con el socio formador para poder lograr, como equipo, un producto final con calidad en el que apliquemos los conocimientos adquiridos en la materia y al mismo tiempo aporte valor a la empresa del socio.  

- Stephanie Ortega Espinosa - Coordinadora y diseñadora
  - **Fortalezas:** Me considero una persona enfocada, atenta a los detalles, líder y buena coordinadora.
  - **Áreas de oportunidad:** Creo que puedo mejorar en mi compromiso respecto al esfuerzo requerido en cada tarea.
  - **Expectativas del bloque:** Espero desarrollar y reforzar ciertas áreas enfocadas a las matemáticas.

- Gabriel Ponce Peña - Desarrollador
  - **Fortalezas:** Cuento con habilidades en diversas tecnologías de programación, como Java, JavaScript, React, Node y Python, entre otras. Además, tengo sólidas habilidades blandas esenciales para el desarrollo diario.
  - **Áreas de oportunidad:** Reconozco que tengo una oportunidad de mejora en cuanto a la procrastinación, ya que tiendo a esperar hasta el último momento en algunos proyectos.
  - **Expectativas del bloque:** Espero reforzar los distintos conocimientos que sean relevantes para mi carrera profesional, de la misma manera que han sido reforzado a lo largo de la universidad

- Ángel Rogelio Cruz Ibarra - Analista  
  - **Fortalezas:** Me considero una persona creativa, proactiva y con habilidades para resolver problemas de manera efectiva.
  - **Áreas de oportunidad:** Quiero mejorar en la gestión del tiempo y en la planificación de tareas para ser más eficiente.
  - **Expectativas del bloque:** Espero adquirir conocimientos prácticos sobre la logística y la gestión de inventarios en un entorno real.

**Expectativas del equipo**  

- ¿Qué esperan lograr como equipo al finalizar el bloque?
  - Como equipo, esperamos finalizar el bloque con una solución eficiente que optimice el espacio de almacenamiento y la logística de distribución en Ponte Pizza, logrando una reducción de tiempos y costos en las entregas a sucursales. Además, buscamos fortalecer nuestras habilidades técnicas y de trabajo colaborativo, así como generar resultados cuantificables que demuestren la efectividad de nuestro sistema. Al concluir, aspiramos a entregar una documentación completa que sirva como base para futuras mejoras y optimizaciones en los procesos de la empresa.
- Listado de metas específicas del equipo para este proyecto.
    1. Optimizar la distribución y el uso del espacio en el almacén.
    2. Reducir los tiempos de preparación y entrega a las sucursales.
    3. Desarrollar un sistema de simulación eficiente para modelar escenarios de logística.
    4. Implementar métricas que midan la eficiencia del flujo de trabajo en el almacén.
    5. Crear documentación completa y detallada del sistema y los resultados obtenidos.
    6. Fortalecer habilidades de colaboración y comunicación en equipo.
    7. Generar un análisis de resultados que sirva para futuras optimizaciones del almacén.
- Compromisos individuales y colectivos para alcanzar los objetivos.
  - Individuales
    - Esteban Leal Menéndez - Colíder y desarrollador: Me comprometo a ser proactivo en el aprendizaje y a liderar en momentos clave, mientras manejo mi tiempo para evitar la procrastinación.
    - Daniel Arteaga Mercado - Líder: Me comprometo a comunicar mis ideas de manera más asertiva y a establecer tiempos claros para las tareas, fomentando un trabajo colaborativo eficiente.
    - Stephanie Ortega Espinosa - Coordinadora y diseñadora: Me comprometo a coordinar eficazmente al equipo, asegurando el cumplimiento de las tareas y a esforzarme más en cada actividad para mejorar mis resultados.
    - Gabriel Ponce Peña - Desarrollador: Me comprometo a utilizar mis habilidades de programación de manera efectiva y a gestionar mejor mi tiempo para evitar la procrastinación en los proyectos.
    - Ángel Rogelio Cruz Ibarra - Analista: Me comprometo a planificar mis tareas de manera más eficiente y a contribuir con soluciones creativas en el equipo, mejorando mi gestión del tiempo.
  - Colectivos
    - Colaboración activa: Trabajar juntos y compartir ideas.
    - Responsabilidad compartida: Cumplir con los plazos y revisar el progreso.
    - Comunicación efectiva: Mantener canales abiertos para resolver problemas.
    - Evaluación continua: Revisar procesos y ajustar estrategias regularmente.

## Descripción del Reto a Desarrollar

El reto propuesto por el socio formador “Ponte Pizza” es rediseñar un espacio, el cual actualmente se utiliza como “bodega”, con el fin de que este sirva como espacio de almacenaje de materia prima para la preparación de las pizzas, en este se colocarán refrigeradores, estanterías y congeladores. Desde este espacio que se encuentra en la parte trasera del local central de “Ponte Pizza”, también se pretende distribuir a las demás sucursales de la ciudad, ya que actualmente el proveedor reparte sucursal por sucursal la materia prima, esto generará que se optimicen las rutas de entrega, se reduzca el tiempo de espera de las sucursales y se disminuyan los costos logísticos. Nosotros como ingenieros en sistemas computacionales modelaremos el espacio tridimensional y el movimiento del personal dentro de este espacio como agentes informáticos inteligentes para que se pueda simular diferentes escenarios de trabajo, optimizar la distribución de los productos, reducir el tiempo de preparación de pedidos y mejorar la eficiencia general del almacén.

## Diagrama de agentes involucrados

![Diagrama de Clases](imagenesREADME/Diagrama_Clases_Ponte_Pizza.png)

## Diagrama de Protocolos de Interacción

![Diagrama de Protocolos](imagenesREADME/Diagrama_Protocolos_Interaccion_Ponte_Pizza.png)
