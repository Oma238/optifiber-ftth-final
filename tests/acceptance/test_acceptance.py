"""Escenarios de aceptacion ATDD para PBI-01 y PBI-02."""

from pytest_bdd import given, parsers, scenarios, then, when
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.dominio.servicios import (
    ErrorDominio,
    calcular_descuento,
    calcular_subtotal,
    calcular_total_pedido,
    validar_documento,
    validar_stock,
)
from src.infraestructura.modelos import (
    Base,
    CategoriaModel,
    ClienteModel,
    DetallePedidoModel,
    EtiquetaModel,
    PedidoModel,
    ProductoModel,
)

scenarios("features/pbi01_cotizacion_ftth.feature")
scenarios("features/pbi02_persistencia_orm.feature")


# --- PBI-01: cotizacion FTTH -------------------------------------------------


@given(
    parsers.parse("una cantidad de {cantidad:d} y un precio unitario de {precio:f}"),
    target_fixture="ctx",
)
def linea_a_cotizar(cantidad, precio):
    return {"cantidad": cantidad, "precio": precio}


@given(parsers.parse("un total sin descuento de {total:f}"), target_fixture="ctx")
def total_sin_descuento(total):
    return {"total": total}


@given(parsers.parse("las lineas {c1:d} x {p1:f} y {c2:d} x {p2:f}"), target_fixture="ctx")
def lineas_del_pedido(c1, p1, c2, p2):
    return {"lineas": [(c1, p1), (c2, p2)]}


@given(parsers.parse('el documento "{documento}"'), target_fixture="ctx")
def documento_cliente(documento):
    return {"documento": documento}


@given(
    parsers.parse("una solicitud de {cantidad:d} unidades con stock disponible de {stock:d}"),
    target_fixture="ctx",
)
def solicitud_con_stock(cantidad, stock):
    return {"cantidad": cantidad, "stock": stock}


@when("calculo el subtotal de la linea")
def calcular_subtotal_linea(ctx):
    ctx["resultado"] = calcular_subtotal(ctx["cantidad"], ctx["precio"])


@when("calculo el descuento")
def calcular_descuento_total(ctx):
    ctx["resultado"] = calcular_descuento(ctx["total"])


@when("calculo el total del pedido")
def calcular_total(ctx):
    ctx["resultado"] = calcular_total_pedido(ctx["lineas"])


@when("normalizo el documento")
def normalizar_documento(ctx):
    ctx["error"] = None
    try:
        ctx["resultado"] = validar_documento(ctx["documento"])
    except ErrorDominio as exc:
        ctx["error"] = exc


@when("valido el stock")
def validar_stock_solicitud(ctx):
    ctx["error"] = None
    try:
        validar_stock(ctx["cantidad"], ctx["stock"])
    except ErrorDominio as exc:
        ctx["error"] = exc


@then(parsers.parse("el subtotal es {esperado:f}"))
def verificar_subtotal(ctx, esperado):
    assert ctx["resultado"] == esperado


@then(parsers.parse("el descuento es {esperado:f}"))
def verificar_descuento(ctx, esperado):
    assert ctx["resultado"] == esperado


@then(parsers.parse("el total del pedido es {esperado:f}"))
def verificar_total(ctx, esperado):
    assert ctx["resultado"] == esperado


@then(parsers.parse('el documento normalizado es "{esperado}"'))
def verificar_documento(ctx, esperado):
    assert ctx["error"] is None
    assert ctx["resultado"] == esperado


@then(parsers.parse('el error de dominio menciona "{texto}"'))
def verificar_error_dominio(ctx, texto):
    assert ctx["error"] is not None
    assert texto in str(ctx["error"])


# --- PBI-02: persistencia ORM ------------------------------------------------


@given("una base de datos en memoria", target_fixture="ctx")
def base_en_memoria():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield {"engine": engine, "session": session}
    engine.dispose()


@given(parsers.parse('un cliente con DNI "{documento}" y un producto con SKU "{sku}"'))
def cliente_y_producto(ctx, documento, sku):
    cliente = ClienteModel(nombre="Cliente FTTH", documento=documento)
    producto = ProductoModel(
        sku=sku,
        nombre="ONT GPON",
        precio=89.90,
        stock=10,
        categoria=CategoriaModel(nombre="Fibra"),
    )
    ctx["session"].add_all([cliente, producto])
    ctx["session"].commit()
    ctx["cliente"] = cliente
    ctx["producto"] = producto


@given(parsers.parse('una categoria "{nombre}" con etiquetas "{e1}" y "{e2}"'))
def categoria_con_etiquetas(ctx, nombre, e1, e2):
    categoria = CategoriaModel(nombre=nombre)
    etiquetas = [EtiquetaModel(nombre=e1), EtiquetaModel(nombre=e2)]
    ctx["session"].add_all([categoria, *etiquetas])
    ctx["session"].commit()
    ctx["categoria"] = categoria
    ctx["etiquetas"] = etiquetas


@given(parsers.parse('una categoria "{nombre}"'))
def categoria_simple(ctx, nombre):
    categoria = CategoriaModel(nombre=nombre)
    ctx["session"].add(categoria)
    ctx["session"].commit()
    ctx["categoria"] = categoria


@when(parsers.parse("guardo un pedido con {cantidad:d} unidades a {precio:f}"))
def guardar_pedido(ctx, cantidad, precio):
    subtotal = calcular_subtotal(cantidad, precio)
    detalle = DetallePedidoModel(
        producto=ctx["producto"],
        cantidad=cantidad,
        precio_unitario=precio,
        subtotal=subtotal,
    )
    pedido = PedidoModel(cliente=ctx["cliente"], total=subtotal)
    pedido.detalles.append(detalle)
    ctx["session"].add(pedido)
    ctx["session"].commit()
    ctx["pedido_id"] = pedido.id
    ctx["detalle_id"] = detalle.id


@when(parsers.parse('guardo el producto "{nombre}" con SKU "{sku}" y precio {precio:f}'))
def guardar_producto(ctx, nombre, sku, precio):
    producto = ProductoModel(
        sku=sku,
        nombre=nombre,
        precio=precio,
        stock=5,
        categoria=ctx["categoria"],
        etiquetas=ctx["etiquetas"],
    )
    ctx["session"].add(producto)
    ctx["session"].commit()
    ctx["producto_id"] = producto.id


@when("intento guardar un producto con precio negativo")
def guardar_producto_invalido(ctx):
    ctx["error"] = None
    try:
        ctx["session"].add(
            ProductoModel(
                sku="INVALIDO",
                nombre="Producto invalido",
                precio=-1.0,
                categoria=ctx["categoria"],
            )
        )
        ctx["session"].commit()
    except IntegrityError as exc:
        ctx["session"].rollback()
        ctx["error"] = exc


@then(parsers.parse("el pedido se recupera con total {esperado:f}"))
def verificar_pedido_guardado(ctx, esperado):
    pedido = ctx["session"].get(PedidoModel, ctx["pedido_id"])
    assert pedido is not None
    assert pedido.total == esperado
    assert len(pedido.detalles) == 1


@then("al eliminar el cliente se eliminan sus pedidos y detalles")
def verificar_cascada(ctx):
    session = ctx["session"]
    session.delete(ctx["cliente"])
    session.commit()
    assert session.get(PedidoModel, ctx["pedido_id"]) is None
    assert session.get(DetallePedidoModel, ctx["detalle_id"]) is None


@then(parsers.parse("el producto se recupera con su categoria y {cantidad:d} etiquetas"))
def verificar_producto_guardado(ctx, cantidad):
    producto = ctx["session"].get(ProductoModel, ctx["producto_id"])
    assert producto is not None
    assert producto.categoria.nombre == "Fibra"
    assert len(producto.etiquetas) == cantidad


@then("la base de datos rechaza el producto por una restriccion de integridad")
def verificar_restriccion(ctx):
    assert ctx["error"] is not None
