Feature: Persistencia ORM (PBI-02)
  Como operador de OptiFiber
  Quiero que los datos se guarden con integridad
  Para recuperar clientes, catalogo y pedidos sin perdidas

  @critico
  Scenario: ★ Cliente, pedido y detalle se guardan en cascada
    Given una base de datos en memoria
    And un cliente con DNI "12345678" y un producto con SKU "ONT-GPON"
    When guardo un pedido con 2 unidades a 89.90
    Then el pedido se recupera con total 179.80
    And al eliminar el cliente se eliminan sus pedidos y detalles

  Scenario: Producto con categoria y etiquetas N a M
    Given una base de datos en memoria
    And una categoria "Fibra" con etiquetas "hogar" y "empresa"
    When guardo el producto "ONT GPON" con SKU "ONT-01" y precio 89.90
    Then el producto se recupera con su categoria y 2 etiquetas

  Scenario: Restricciones de integridad protegen el catalogo
    Given una base de datos en memoria
    And una categoria "Fibra"
    When intento guardar un producto con precio negativo
    Then la base de datos rechaza el producto por una restriccion de integridad
