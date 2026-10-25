 LoL Worlds Analytics: Pre-Match Betting Simulator (ETL & C# Blazor)

📌 Descripción del Proyecto

Este proyecto es una arquitectura de software de grado empresarial diseñada para calcular la Esperanza Matemática (EV+) en cuotas de apuestas deportivas de League of Legends (específicamente calibrado para el Mundial / Worlds).

A diferencia de los simuladores comunes, este sistema utiliza un ecosistema completo que extrae estadísticas crudas (Oracle's Elixir), las limpia y audita mediante un pipeline ETL en Python, y las almacena en una base de datos relacional para alimentar un frontend analítico en C# Blazor.

⚙️ Arquitectura y Flujo de Datos (Fase 1.0)

El proyecto se divide en tres capas principales:

Pipeline ETL Automatizado (Python & Pandas):

Extrae datos masivos de torneos profesionales en formato CSV.

Aplica un filtro estricto de liga (league == 'WLDs') para blindar la base de datos contra errores de tipeo de parches (ej. falsos 16.2) y aislar exclusivamente el meta actual.

Reestructura los datos: separa el rendimiento colectivo del equipo y lo inyecta a nivel de jugador individual.

Bóveda de Datos Relacional (SQL Server):

Actúa como el motor estadístico histórico.

Posee un "Escudo Antiduplicados" mediante llaves compuestas que rechaza automáticamente partidas ya registradas, optimizando el rendimiento de lectura.

Frontend Analítico Pre-Match (C# Blazor):

Interfaz de usuario interactiva para simular escenarios de Draft.

Implementa un Algoritmo de Doble Factor: cruza el Winrate actual del campeón en el parche del Mundial con el desempeño histórico individual del jugador profesional (KDA, objetivos).

Genera líneas de riesgo por colores para identificar cuotas de valor frente a casas de apuestas (ej. Betano).

🚀 Cómo funciona el Algoritmo (Gestión de Riesgo)

El sistema está diseñado estrictamente como un Pre-Match Predictor. No opera en vivo. Su mayor precisión matemática ocurre al finalizar la fase de Draft, evaluando las "Win Conditions" antes de que los jugadores abandonen la base. Se utiliza bajo estrictas reglas de gestión de Bankroll (riesgo de 2% a 5% por jugada) para capitalizar los errores algorítmicos (cuotas mal puestas) de las casas de apuestas a largo plazo.

🔮 Roadmap (Fase 2.0 - Próximamente)

Integración con IA Generativa (Llama 3 Local): Implementación de un motor cualitativo para analizar las composiciones de Early Game vs Late Game, aportando contexto táctico que la matemática pura no puede predecir por sí sola.
