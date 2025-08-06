#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import os

class ChunkedHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/chunked':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Transfer-Encoding', 'chunked')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Emular exactamente la respuesta que recibes
            response_data = {
                "status": "0",
                "token": "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwZTkwMWUwZi0xMjM2LTRkMzktOGE4MC01ZmMzMDM2NWEyNzMiLCJpc3MiOiJnZGgiLCJzdWIiOiJIRV9BUElfMDExIiwiZXhwIjoxNzU0NDEwNzczLCJuYmYiOjE3NTQ0MTA3MTQsImlhdCI6MTc1NDQxMDcxNH0.wqTz5GqD0K9f5lxPo5yrwc_oBwnMK6Y_gUtNl-hCGZY",
                "correlation_id": "75ac8e21-131d-43be-8f80-2b4f3576e550"
            }
            
            response_json = json.dumps(response_data)
            
            # Enviar como un solo chunk (como tu servicio real)
            chunk_size_hex = f"{len(response_json):X}"
            self.wfile.write(f"{chunk_size_hex}\r\n".encode())
            self.wfile.write(response_json.encode())
            self.wfile.write(b"\r\n")
            self.wfile.flush()
            
            # Simular delay
            time.sleep(0.1)
            
            # Chunk final (0)
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
            
        elif self.path == '/chunked-multiple':
            # Versión con múltiples chunks para testing
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Transfer-Encoding', 'chunked')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response_data = {
                "status": "0",
                "token": "eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIwZTkwMWUwZi0xMjM2LTRkMzktOGE4MC01ZmMzMDM2NWEyNzMiLCJpc3MiOiJnZGgiLCJzdWIiOiJIRV9BUElfMDExIiwiZXhwIjoxNzU0NDEwNzczLCJuYmYiOjE3NTQ0MTA3MTQsImlhdCI6MTc1NDQxMDcxNH0.wqTz5GqD0K9f5lxPo5yrwc_oBwnMK6Y_gUtNl-hCGZY",
                "correlation_id": "75ac8e21-131d-43be-8f80-2b4f3576e550"
            }
            
            response_json = json.dumps(response_data)
            
            # Dividir en múltiples chunks
            chunk_size = 50
            chunks = [response_json[i:i+chunk_size] for i in range(0, len(response_json), chunk_size)]
            
            for chunk in chunks:
                chunk_size_hex = f"{len(chunk):X}"
                self.wfile.write(f"{chunk_size_hex}\r\n".encode())
                self.wfile.write(chunk.encode())
                self.wfile.write(b"\r\n")
                self.wfile.flush()
                
                time.sleep(0.2)  # Delay entre chunks
            
            # Chunk final
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
            
        elif self.path == '/chunked-incomplete':
            # Versión que simula respuesta incompleta
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Transfer-Encoding', 'chunked')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # Enviar solo parte de la respuesta
            partial_data = '{"status":"0","token":"eyJhbGciOiJIUzI1NiJ9'
            chunk_size_hex = f"{len(partial_data):X}"
            self.wfile.write(f"{chunk_size_hex}\r\n".encode())
            self.wfile.write(partial_data.encode())
            self.wfile.write(b"\r\n")
            self.wfile.flush()
            
            # No enviar el chunk final (simular conexión interrumpida)
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")

if __name__ == '__main__':
    # Railway usa la variable PORT
    port = int(os.environ.get('PORT', 8080))
    server = HTTPServer(('0.0.0.0', port), ChunkedHandler)
    print(f"Servidor chunked corriendo en puerto {port}")
    print("Endpoints disponibles:")
    print("  - /chunked (respuesta real)")
    print("  - /chunked-multiple (múltiples chunks)")
    print("  - /chunked-incomplete (respuesta incompleta)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido")
        server.server_close()