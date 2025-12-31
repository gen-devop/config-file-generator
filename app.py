from flask import Flask, render_template, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    device_type = request.form.get('device_type')
    config_lines = []
    if device_type == 'switch':
        hostname = request.form.get('hostname', 'switch')
        vlan = request.form.get('vlan', '10')
        config_lines.append(f'sysname {hostname}')
        config_lines.append(f'vlan {vlan}')
    elif device_type == 'router':
        hostname = request.form.get('hostname', 'router')
        interface = request.form.get('interface', 'GigabitEthernet0/0/0')
        ip_address = request.form.get('ip_address', '192.168.0.1 255.255.255.0')
        config_lines.append(f'sysname {hostname}')
        config_lines.append(f'interface {interface}')
        config_lines.append(f' ip address {ip_address}')
    else:
        config_lines.append('# Unsupported device type')

    config_text = '\n'.join(config_lines) + '\n'

    if 'download' in request.form:
        return Response(
            config_text,
            mimetype='text/plain',
            headers={'Content-Disposition': 'attachment; filename=config.cfg'}
        )

    return render_template('config.html', config=config_text)

if __name__ == '__main__':
    app.run(debug=True)
