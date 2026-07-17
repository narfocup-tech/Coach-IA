import os
import re
import ollama  

class CoachAI:
    def __init__(self, username, sport):
        self.username = username.strip()
        self.sport = sport.strip().lower()
        self.streak_points = 0
        self.level = "Amateur"
        
        # Inicializamos habilidades específicas según el deporte
        self.skills = self._inicializar_habilidades()

    def _inicializar_habilidades(self):
        """Define habilidades específicas para los deportes más comunes."""
        deporte = self.sport
        
        if "basquet" in deporte or "basketball" in deporte or "baloncesto" in deporte:
            return {"Dribbling (Manejo)": 0, "Shooting (Tiro)": 0, "Defense (Defensa)": 0, "Físico": 0}
        elif "futbol" in deporte or "soccer" in deporte:
            return {"Control y Pase": 0, "Remate (Tiro)": 0, "Gambeta (Regate)": 0, "Físico": 0}
        elif "calistenia" in deporte or "gym" in deporte or "funcional" in deporte:
            return {"Fuerza Empuje": 0, "Fuerza Tirón": 0, "Resistencia": 0, "Movilidad": 0}
        elif "boxeo" in deporte or "mma" in deporte:
            return {"Técnica (Golpes)": 0, "Footwork (Paso)": 0, "Sparring": 0, "Físico": 0}
        else:
            # Deportes genéricos o no listados
            return {"Técnica": 0, "Táctica": 0, "Físico": 0, "Mental": 0}

    def detectar_habilidad_entrenada(self, texto_usuario):
        """Analiza el texto del usuario para identificar qué habilidad quiere entrenar."""
        texto = texto_usuario.lower()
        
        # Recorremos cada habilidad asignada al usuario
        for skill in self.skills.keys():
            # Limpiamos el nombre de la habilidad para usarlo como palabra clave de búsqueda
            # Ej: "Dribbling (Manejo)" -> buscamos "dribbling" o "manejo"
            palabras_clave = re.findall(r'[a-zA-Záéíóúüñ]+', skill.lower())
            for palabra in palabras_clave:
                if len(palabra) > 3 and palabra in texto:
                    return skill
                    
        # Palabras clave genéricas si no hubo coincidencia exacta directa
        if "tiro" in texto or "shoot" in texto or "lanzamiento" in texto:
            for k in self.skills.keys():
                if "tiro" in k.lower() or "shoot" in k.lower(): return k
        if "dribbling" in texto or "pique" in texto or "manejo" in texto or "regate" in texto or "gambeta" in texto:
            for k in self.skills.keys():
                if "dribbling" in k.lower() or "regate" in k.lower() or "gambeta" in k.lower(): return k

        # Si no detecta nada específico, cae por defecto en "Físico" si existe
        for k in self.skills.keys():
            if "físico" in k.lower() or "fisico" in k.lower():
                return k
        return list(self.skills.keys())[0]

    def registrar_entrenamiento(self, minutos, habilidad=None):
        if minutos <= 0:
            raise ValueError("Los minutos deben ser mayores a cero.")
        
        puntos_ganados = 10 + (minutos // 5)
        self.streak_points += puntos_ganados
        
        # Subimos la habilidad específica (máximo 100 puntos por habilidad)
        if habilidad and habilidad in self.skills:
            self.skills[habilidad] = min(100, self.skills[habilidad] + puntos_ganados)
        
        # Lógica de nivel general basada en los puntos totales
        if self.streak_points >= 100:
            self.level = "Pro"
        elif self.streak_points >= 50:
            self.level = "Semi-Pro"
        else:
            self.level = "Amateur"
            
        return puntos_ganados

    def generar_rutina_ia(self, estado_usuario):
        """Llama al modelo local de Ollama para armar la rutina real."""
        habilidad = self.detectar_habilidad_entrenada(estado_usuario)
        
        prompt = (
            f"Sos un entrenador personal experto en {self.sport}. "
            f"El cliente se llama {self.username} y quiere una rutina para mejorar específicamente su **{habilidad}**. "
            f"Esto es lo que te dice el cliente sobre su estado físico actual y limitaciones: '{estado_usuario}'.\n\n"
            f"Armale una rutina corta y estructurada paso a paso. Sé muy claro y amigable."
        )
        
        try:
            # Usamos el cliente local de Ollama (asegurate de tener el modelo descargado en tu PC)
            response = ollama.chat(
                model="llama3",  # Cambialo por "gemma2", "mistral", etc., si usás otro modelo en Ollama
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        except Exception as e:
            # Fallback amigable si Ollama está apagado o no responde
            return (
                f"⚠️ *(Nota: No pudimos conectar con tu Ollama local, ejecutando rutina básica)*\n\n"
                f"💪 **COACH AI ({self.sport.upper()}):** ¡Entendido {self.username}! Vamos a trabajar específicamente tu **{habilidad}**.\n\n"
                f"1. **Calentamiento (3 min):** Movilidad articular general enfocada en tu tren inferior.\n"
                f"2. **Bloque Principal ({habilidad}):** Ejercicios técnicos controlados para mejorar tu {habilidad}.\n"
                f"3. **Vuelta a la calma (2 min):** Estiramientos suaves y respiración profunda."
            )