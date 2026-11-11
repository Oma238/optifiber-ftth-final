"""Pruebas de validacion del formulario de alta de clientes."""

from unittest.mock import Mock

from src.presentacion.gui.pantallas.clientes import ModalClienteNuevo

MENSAJE_OBLIGATORIOS = "Por favor complete los campos obligatorios (Nombre y Documento)"


def _modal(nombre: str, documento: str) -> ModalClienteNuevo:
    """Construye el modal sin inicializar Tk para probar solo la logica."""
    modal = ModalClienteNuevo.__new__(ModalClienteNuevo)
    modal.nombre = Mock(valor=Mock(return_value=nombre))
    modal.documento = Mock(valor=Mock(return_value=documento))
    modal.telefono = Mock(valor=Mock(return_value=""))
    modal.email = Mock(valor=Mock(return_value=""))
    modal.direccion = Mock(valor=Mock(return_value=""))
    modal.app = Mock()
    modal.al_guardar = Mock()
    modal.cerrar = Mock()
    modal.limpiar_error = Mock()
    modal.mostrar_error = Mock()
    return modal


def test_campos_vacios_no_invoca_al_repositorio():
    modal = _modal("   ", "  ")

    modal._guardar()

    modal.app.clientes.crear.assert_not_called()
    modal.mostrar_error.assert_called_once_with(MENSAJE_OBLIGATORIOS)
    modal.app.notificar.assert_called_once_with(MENSAJE_OBLIGATORIOS, "alerta")
    modal.cerrar.assert_not_called()


def test_cliente_valido_se_registra_y_confirma():
    modal = _modal("Ana Quispe", "12345678")

    modal._guardar()

    modal.app.clientes.crear.assert_called_once_with(
        nombre="Ana Quispe",
        documento="12345678",
        telefono="",
        email="",
        direccion="",
    )
    modal.app.notificar.assert_called_once_with("Cliente registrado exitosamente")
    modal.al_guardar.assert_called_once_with()
    modal.cerrar.assert_called_once_with()
