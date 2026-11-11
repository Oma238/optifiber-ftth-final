import pytest

from src.presentacion.gui.utilidades import (
    MENSAJE_NUMERICO,
    convertir_decimal_positivo,
    convertir_entero_positivo,
)


def test_convertir_entero_positivo_valido():
    assert convertir_entero_positivo("5") == 5
    assert convertir_entero_positivo(10) == 10


def test_convertir_entero_positivo_invalido():
    with pytest.raises(ValueError, match=MENSAJE_NUMERICO):
        convertir_entero_positivo("abc")
    with pytest.raises(ValueError, match=MENSAJE_NUMERICO):
        convertir_entero_positivo("-4")
    with pytest.raises(ValueError, match=MENSAJE_NUMERICO):
        convertir_entero_positivo("0")


def test_convertir_decimal_positivo_valido():
    assert convertir_decimal_positivo("19.90") == 19.90
    assert convertir_decimal_positivo("19,90") == 19.90


def test_convertir_decimal_positivo_invalido():
    with pytest.raises(ValueError, match=MENSAJE_NUMERICO):
        convertir_decimal_positivo("letras")
    with pytest.raises(ValueError, match=MENSAJE_NUMERICO):
        convertir_decimal_positivo("-10.5")
