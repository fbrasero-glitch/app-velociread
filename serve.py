import http.server
import socketserver
import socket
import os

PORT = 8000

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No necesita conectarse realmente
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silenciar los logs de peticiones estáticas para mantener limpia la consola
        pass

    def end_headers(self):
        # Desactivar cache para desarrollo y facilitar recargas de código
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

local_ip = get_local_ip()
url = f"http://{local_ip}:{PORT}"

print("=" * 60)
print("             VELOCIREAD - SERVIDOR LOCAL")
print("=" * 60)
print(" El servidor esta activo.")
print(" Para abrir la app en tu iPhone:")
print(" 1. Conecta tu iPhone a la MISMA RED WI-FI que esta PC.")
print(" 2. Abre Safari en tu iPhone e ingresa la siguiente URL:")
print(f"\n      {url}\n")
print(f" En tu PC tambien puedes abrir: http://localhost:{PORT}")
print("=" * 60)
print(" Deja esta ventana abierta mientras uses la app.")
print(" Presiona Ctrl+C para detener el servidor.")
print("=" * 60)

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
