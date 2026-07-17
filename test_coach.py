import unittest
from coach import CoachAI

class TestCoachAI(unittest.TestCase):

    def setUp(self):
        """Se ejecuta antes de cada test. Inicializa un usuario de prueba."""
        # Usamos los nombres de deportes en minúsculas para asegurar la coincidencia exacta
        self.coach_basquet = CoachAI(username="Franco", sport="basquet")
        self.coach_futbol = CoachAI(username="Messi", sport="futbol")

    def test_inicializacion_habilidades_basquet(self):
        """Valida que un jugador de básquet tenga las habilidades correspondientes en cero."""
        habilidades = self.coach_basquet.skills
        self.assertIn("Dribbling (Manejo)", habilidades)
        self.assertIn("Shooting (Tiro)", habilidades)
        self.assertEqual(habilidades["Dribbling (Manejo)"], 0)

    def test_inicializacion_habilidades_futbol(self):
        """Valida que un jugador de fútbol tenga sus habilidades específicas."""
        habilidades = self.coach_futbol.skills
        self.assertIn("Gambeta (Regate)", habilidades)
        self.assertIn("Remate (Tiro)", habilidades)
        self.assertEqual(habilidades["Gambeta (Regate)"], 0)

    def test_detectar_habilidad_dribbling(self):
        """Prueba que el detector asocie palabras clave a la habilidad de Dribbling."""
        texto = "Quiero practicar mi pique y un poco de dribbling hoy"
        habilidad_detectada = self.coach_basquet.detectar_habilidad_entrenada(texto)
        self.assertEqual(habilidad_detectada, "Dribbling (Manejo)")

    def test_detectar_habilidad_defecto(self):
        """Prueba que si no se especifica habilidad, asigne 'Físico' o la primera por defecto."""
        texto = "Quiero entrenar suave hoy, no sé qué hacer"
        habilidad_detectada = self.coach_basquet.detectar_habilidad_entrenada(texto)
        self.assertEqual(habilidad_detectada, "Físico")

    def test_registro_entrenamiento_puntos_y_nivel(self):
        """Verifica que sumar minutos aumente los puntos de constancia y cambie el nivel."""
        # Un entrenamiento de 20 minutos debería dar: 10 + (20 // 5) = 14 puntos.
        puntos_ganados = self.coach_basquet.registrar_entrenamiento(20, "Dribbling (Manejo)")
        
        self.assertEqual(puntos_ganados, 14)
        self.assertEqual(self.coach_basquet.streak_points, 14)
        self.assertEqual(self.coach_basquet.skills["Dribbling (Manejo)"], 14)
        self.assertEqual(self.coach_basquet.level, "Amateur")

    def test_subir_de_nivel_pro(self):
        """Verifica que el usuario suba a nivel PRO al superar los 100 puntos."""
        # Registramos entrenamientos largos para acumular más de 100 puntos
        self.coach_basquet.registrar_entrenamiento(100) # 10 + 20 = 30 pts
        self.coach_basquet.registrar_entrenamiento(150) # 10 + 30 = 40 pts
        self.coach_basquet.registrar_entrenamiento(150) # 10 + 30 = 40 pts (Total: 110 pts)
        
        self.assertEqual(self.coach_basquet.level, "Pro")

    def test_registro_minutos_invalidos(self):
        """Verifica que el sistema lance un error si se ingresan minutos negativos o cero."""
        with self.assertRaises(ValueError):
            self.coach_basquet.registrar_entrenamiento(-5)

if __name__ == "__main__":
    unittest.main()