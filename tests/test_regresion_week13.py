"""Pruebas de regresion de la semana 13, responsable Julio Diaz.

Cubren escenarios que aun no estaban en la suite: devolucion de stock en una
venta con varias lineas, cantidades incorrectas desde repositorio y desde la
interfaz, busquedas sin resultados y prevencion de operaciones con datos
invalidos o incompletos.
"""

from unittest.mock import Mock

import pytest
from sqlalchemy import func, select

from src.dominio.servicios import ErrorDominio
from src.infraestructura.modelos import (
    CategoriaModel,
    ClienteModel,
    DetallePedidoModel,
    PedidoModel,
    ProductoModel,
)
from src.infraestructura.repositorios import (
    CatalogoRepositorio,
    ClienteRepositorio,
    PedidoRepositorio,
)
from src.presentacion.gui.pantallas.catalogo import ModalProducto
from src.presentacion.gui.pantallas.clientes import ModalClienteNuevo
from src.presentacion.gui.pantallas.pedidos import PantallaPedidos


@pytest.fixture
def datos_regresion(db_session):
    """Datos minimos: dos productos, una categoria y un cliente de prueba."""
    categoria = CategoriaModel(nombre="Fibra Optica")
    fibra = ProductoModel(
        sku="FIB-013",
        nombre="Cable drop de prueba",
        precio=100.0,
        stock=4,
        categoria=categoria,
    )
    accesorio = ProductoModel(
        sku="ACC-013",
        nombre="Conector de prueba",
        precio=20.0,
        stock=6,
        categoria=categoria,
    )
    cliente = ClienteModel(nombre="Cliente Regresion", documento="22222222")
    db_session.add_all([categoria, fibra, accesorio, cliente])
    db_session.commit()
    return {
        "categoria": categoria,
        "fibra": fibra,
        "accesorio": accesorio,
        "cliente": cliente,
    }


def _modal_cliente(db_session, nombre: str, documento: str) -> ModalClienteNuevo:
    """Arma el modal real sin Tk y conecta el repositorio real."""
    modal = ModalClienteNuevo.__new__(ModalClienteNuevo)
    modal.nombre = Mock(valor=Mock(return_value=nombre))
    modal.documento = Mock(valor=Mock(return_value=documento))
    modal.telefono = Mock(valor=Mock(return_value=""))
    modal.email = Mock(valor=Mock(return_value=""))
    modal.direccion = Mock(valor=Mock(return_value=""))
    modal.app = Mock()
    modal.app.clientes = ClienteRepositorio(db_session)
    modal.al_guardar = Mock()
    modal.cerrar = Mock()
    modal.limpiar_error = Mock()
    modal.mostrar_error = Mock()
    return modal


def _modal_producto(db_session, precio: str, stock: str, sku="QA-013") -> ModalProducto:
    """Arma el modal real sin Tk y conecta el catalogo real."""
    categorias = CatalogoRepositorio(db_session).listar_categorias()
    modal = ModalProducto.__new__(ModalProducto)
    modal.app = Mock()
    modal.app.catalogo = CatalogoRepositorio(db_session)
    modal.al_guardar = Mock()
    modal.cerrar = Mock()
    modal.limpiar_error = Mock()
    modal.mostrar_error = Mock()
    modal.categorias = categorias
    modal.sku = Mock(valor=Mock(return_value=sku))
    modal.nombre = Mock(valor=Mock(return_value="Producto QA"))
    modal.precio = Mock(valor=Mock(return_value=precio))
    modal.stock = Mock(valor=Mock(return_value=stock))
    modal.categoria = Mock(valor=Mock(return_value=categorias[0].nombre))
    modal.etiquetas = Mock(valor=Mock(return_value=""))
    modal.descripcion = Mock(get=Mock(return_value=""))
    return modal


# ---------------------------------------------------------------------------
# 1. Recuperacion del stock al cancelar una venta
# ---------------------------------------------------------------------------
def test_cancelar_venta_con_varias_lineas_devuelve_stock_y_permite_reutilizarlo(
    db_session, datos_regresion
):
    repo = PedidoRepositorio(db_session)
    pedido = repo.crear_pedido("22222222", [("FIB-013", 2), ("ACC-013", 3)])

    assert datos_regresion["fibra"].stock == 2
    assert datos_regresion["accesorio"].stock == 3

    repo.cambiar_estado(pedido.id, "CANCELADO")
    db_session.expire_all()

    assert datos_regresion["fibra"].stock == 4
    assert datos_regresion["accesorio"].stock == 6

    nuevo = repo.crear_pedido("22222222", [("FIB-013", 4), ("ACC-013", 6)])

    assert nuevo.id != pedido.id
    assert datos_regresion["fibra"].stock == 0
    assert datos_regresion["accesorio"].stock == 0


# ---------------------------------------------------------------------------
# 2. Validacion de cantidades incorrectas
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("cantidad", [0, -1])
def test_crear_pedido_rechaza_cantidad_no_positiva(db_session, datos_regresion, cantidad):
    repo = PedidoRepositorio(db_session)

    with pytest.raises(ErrorDominio, match="mayor que cero"):
        repo.crear_pedido("22222222", [("FIB-013", cantidad)])

    assert db_session.scalar(select(func.count(PedidoModel.id))) == 0
    assert db_session.scalar(select(func.count(DetallePedidoModel.id))) == 0
    db_session.expire_all()
    assert datos_regresion["fibra"].stock == 4


def test_carrito_no_supera_el_stock_disponible(datos_regresion):
    pantalla = PantallaPedidos.__new__(PantallaPedidos)
    pantalla.app = Mock()
    pantalla._por_sku = {"FIB-013": datos_regresion["fibra"]}
    pantalla.carrito = {"FIB-013": 4}
    pantalla._render_productos = Mock()
    pantalla._render_resumen = Mock()

    pantalla._cambiar_cantidad("FIB-013", 1)

    assert pantalla.carrito["FIB-013"] == 4
    pantalla.app.notificar.assert_called_once_with("Stock insuficiente de FIB-013.", "alerta")
    pantalla._render_productos.assert_not_called()
    pantalla._render_resumen.assert_not_called()


# ---------------------------------------------------------------------------
# 3. Busqueda de registros inexistentes
# ---------------------------------------------------------------------------
def test_buscar_registros_inexistentes_devuelve_none(db_session, datos_regresion):
    assert ClienteRepositorio(db_session).buscar_por_documento("99999999") is None
    assert CatalogoRepositorio(db_session).buscar_por_sku("NO-EXISTE") is None
    assert PedidoRepositorio(db_session).obtener(9999) is None


@pytest.mark.parametrize(
    ("documento", "sku", "mensaje"),
    [
        ("99999999", "FIB-013", "No existe un cliente"),
        ("22222222", "NO-EXISTE", "No existe un producto"),
    ],
)
def test_crear_pedido_rechaza_cliente_o_producto_inexistente(
    db_session, datos_regresion, documento, sku, mensaje
):
    with pytest.raises(ErrorDominio, match=mensaje):
        PedidoRepositorio(db_session).crear_pedido(documento, [(sku, 1)])

    assert db_session.scalar(select(func.count(PedidoModel.id))) == 0
    db_session.expire_all()
    assert datos_regresion["fibra"].stock == 4


# ---------------------------------------------------------------------------
# 4. Prevencion de operaciones con datos invalidos
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("documento", ["123", "1234567A", "123456789"])
def test_cliente_con_documento_invalido_no_se_guarda(db_session, documento):
    modal = _modal_cliente(db_session, "Cliente Invalido", documento)

    modal._guardar()

    assert db_session.scalar(select(func.count(ClienteModel.id))) == 0
    modal.mostrar_error.assert_called_once()
    modal.app.notificar.assert_called_once()
    modal.cerrar.assert_not_called()


@pytest.mark.parametrize(("precio", "stock"), [("abc", "1"), ("10", "abc")])
def test_producto_con_valor_no_numerico_no_se_guarda(db_session, datos_regresion, precio, stock):
    modal = _modal_producto(db_session, precio, stock)

    modal._guardar()

    assert db_session.scalar(select(func.count(ProductoModel.id))) == 2
    modal.mostrar_error.assert_called_once_with(
        "El precio y el stock deben ser numeros validos."
    )
    modal.cerrar.assert_not_called()


def test_pedido_con_sku_repetido_no_se_guarda(db_session, datos_regresion):
    repo = PedidoRepositorio(db_session)

    with pytest.raises(ErrorDominio, match="esta repetido"):
        repo.crear_pedido("22222222", [("FIB-013", 1), ("fib-013", 1)])

    assert db_session.scalar(select(func.count(PedidoModel.id))) == 0
    db_session.expire_all()
    assert datos_regresion["fibra"].stock == 4


def test_cambiar_estado_invalido_no_modifica_el_pedido(db_session, datos_regresion):
    repo = PedidoRepositorio(db_session)
    pedido = repo.crear_pedido("22222222", [("FIB-013", 1)])

    with pytest.raises(ErrorDominio, match="Estado de pedido no valido"):
        repo.cambiar_estado(pedido.id, "REVISION")

    assert repo.obtener(pedido.id).estado == "PENDIENTE"
    assert datos_regresion["fibra"].stock == 3


# ---------------------------------------------------------------------------
# 5. Validacion de campos obligatorios
# ---------------------------------------------------------------------------
def test_producto_sin_sku_no_se_guarda_desde_el_modal(db_session, datos_regresion):
    modal = _modal_producto(db_session, "10", "1", sku="  ")

    modal._guardar()

    assert db_session.scalar(select(func.count(ProductoModel.id))) == 2
    modal.mostrar_error.assert_called_once()
    modal.cerrar.assert_not_called()


@pytest.mark.parametrize(("sku", "nombre"), [("", "Producto"), ("QA-014", "")])
def test_crear_producto_requiere_sku_y_nombre(db_session, datos_regresion, sku, nombre):
    catalogo = CatalogoRepositorio(db_session)

    with pytest.raises(ErrorDominio, match="obligatorios"):
        catalogo.crear_producto(
            sku=sku,
            nombre=nombre,
            precio=10.0,
            stock=1,
            categoria_id=datos_regresion["categoria"].id,
        )

    assert db_session.scalar(select(func.count(ProductoModel.id))) == 2


def test_categoria_sin_nombre_no_se_guarda(db_session):
    with pytest.raises(ErrorDominio, match="obligatorio"):
        CatalogoRepositorio(db_session).crear_categoria("   ")

    assert db_session.scalar(select(func.count(CategoriaModel.id))) == 0
