Este script permite activar Comafi Token en otras aplicaciones de 2FA,
como Google Authenticator.
Ideal para el que ya tiene una app con varias cuentas de 2FA,
y no quiere tener que usar app otra solo para el token del Comafi.

Instrucciones
=============

1. En un cajero automático, seleccionar la opción
Claves > Generación de Claves > Comafi Token y seguir las instrucciones.
El cajero imprime un ticket con un código de asociación.
**Si ya estás usando la aplicación de Comafi Token,
dejará de funcionar.**
2. En la computadora, ejecutar `python3 activar-comafi.py` en una consola.
3. Ingresar el código de asociación.
**El código de asociación se puede usar una sola vez,
a partir de acá si algo sale mal no se puede volver a intentar,
ni ingresar el mismo código en la app oficial,
hay que obtener otro código en el cajero.**
4. Ingresar la clave numérica generada en el cajero.
5. Se muestra un código QR en la consola.
Escanearlo con una aplicación [TOTP](https://en.wikipedia.org/wiki/Time-based_One-time_Password_algorithm) compatible.
También se muestran datos para ingresar el token manualmente en la app.

Aplicaciones compatibles
========================

Los códigos de 2FA TOTP se suelen actualizar cada 30 segundos,
pero Comafi Token usa un período de 40 segundos.
Puede ser que algunas aplicaciones no lo soporten.

Estas apps fueron probadas y sé que funcionan:

**Google Authenticator para iOS**: Funciona con la URL o escaneando el código QR.
No funciona ingresando el seed a mano (no soporta cambiar el período).
El indicador de cuánto tiempo queda podría ser incorrecto.

**OTP Auth para iOS**: Funciona con la URL o el código QR.
Para ingreso manual: seleccionar Enter Credentials, ingresar la clave, guardar,
editar la cuenta recién agregada, y cambiar el Period a 40 segundos.

**Lastpass Authenticator**: Funciona con código QR. Creo que no soporta URL.
Para ingreso manual: ingresar la clave Base32, y cambiar el período a 40 segundos en Advanced Settings.

**Authy**: *No funciona.*

<!-- (TODO: agregar instrucciones de cómo probar si una app es compatible) -->
