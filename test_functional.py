import pytest
from streamlit.testing.v1 import AppTest

def test_user_flow_add_training():
    """
    Prueba Funcional: Simula la interacción de un usuario real en la interfaz.
    Ingresa un texto de entrenamiento y verifica que la UI responda correctamente.
    """
    # 1. Inicializa el simulador de Streamlit apuntando a tu app principal
    at = AppTest.from_file("app.py")
    at.run()

    # 2. Simula al usuario escribiendo en el primer campo de texto que encuentre
    if at.text_input:
        at.text_input[0].input("Ayer corrí 30 minutos a paso ligero").run()
        
        # Verifica que la app no haya lanzado ninguna excepción/error visual
        assert not at.exception
        
    # 3. Simula la interacción con los botones si existen (ej: el cronómetro o registrar)
    if at.button:
        # Hace clic en el primer botón disponible y vuelve a renderizar la app
        at.button[0].click().run()
        assert not at.exception