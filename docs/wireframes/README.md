# Wireframes — OptiFiber FTTH

Mapeo de las 5 pantallas a los atributos declarados en `src/infraestructura/modelos.py`.

| Pantalla | Atributos utilizados |
| --- | --- |
| Dashboard | `PedidoModel.id`, `PedidoModel.fecha`, `PedidoModel.estado`, `PedidoModel.total`, `DetallePedidoModel.subtotal` |
| Clientes | `ClienteModel.id`, `ClienteModel.nombre`, `ClienteModel.documento`, `ClienteModel.telefono`, `ClienteModel.email`, `ClienteModel.direccion`, `ClienteModel.creado_en` |
| Catálogo | `ProductoModel.sku`, `ProductoModel.nombre`, `ProductoModel.precio`, `ProductoModel.stock`, `ProductoModel.activo`, `CategoriaModel.nombre`, `EtiquetaModel.nombre`, `producto_etiqueta` |
| Pedidos | `PedidoModel.estado`, `PedidoModel.total`, `PedidoModel.cliente_id`, `DetallePedidoModel.producto_id`, `DetallePedidoModel.cantidad`, `DetallePedidoModel.precio_unitario`, `DetallePedidoModel.subtotal`, `ClienteModel.documento`, `ProductoModel.sku` |
| Reportes | `PedidoModel.fecha`, `PedidoModel.total`, `DetallePedidoModel.cantidad`, `DetallePedidoModel.subtotal`, `ProductoModel.categoria_id`, `ProductoModel.nombre` |
