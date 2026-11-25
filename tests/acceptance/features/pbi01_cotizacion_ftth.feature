Feature: Cotizacion FTTH (PBI-01)
  Como comercial de OptiFiber
  Quiero calcular cotizaciones confiables
  Para ofrecer precios correctos al cliente

  Scenario: Subtotal de una linea FTTH
    Given una cantidad de 2 y un precio unitario de 100.50
    When calculo el subtotal de la linea
    Then el subtotal es 201.00

  Scenario: Descuento por volumen desde S/ 1500
    Given un total sin descuento de 1600.00
    When calculo el descuento
    Then el descuento es 80.00

  Scenario: Sin descuento por debajo del umbral
    Given un total sin descuento de 1499.99
    When calculo el descuento
    Then el descuento es 0.00

  @critico
  Scenario: ★ Total del pedido con descuento
    Given las lineas 2 x 100.00 y 4 x 400.00
    When calculo el total del pedido
    Then el total del pedido es 1710.00

  Scenario: Total del pedido sin descuento
    Given las lineas 1 x 299.90 y 2 x 50.00
    When calculo el total del pedido
    Then el total del pedido es 399.90

  Scenario: Documento de cliente valido
    Given el documento "12345678"
    When normalizo el documento
    Then el documento normalizado es "12345678"

  @critico
  Scenario: ★ Documento de cliente invalido
    Given el documento "ABCD1234"
    When normalizo el documento
    Then el error de dominio menciona "digitos"

  @critico
  Scenario: ★ Stock insuficiente rechaza la venta
    Given una solicitud de 5 unidades con stock disponible de 2
    When valido el stock
    Then el error de dominio menciona "Stock insuficiente"
