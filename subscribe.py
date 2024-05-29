import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import random
import threading
from paho.mqtt import client as mqtt_client
import base64

# MQTT setup
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'subscribe-{random.randint(0, 100)}'

# Global variables to store sensor data
sensor_data = {
    "temperature": 0.0,
    "humidity": 0.0,
    "distance": 0.0,
    "gas_state": "No Data",
    "image": ""
}

# MQTT client setup
def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        try:
            payload = msg.payload.decode()
            # Extract sensor data from the message
            data_parts = payload.split(", ")
            for part in data_parts:
                key, value = part.split(": ")
                key = key.lower().strip()
                value = value.strip()
                if key in sensor_data:
                    if key in ["temperature", "humidity", "distance"]:
                        sensor_data[key] = float(value.replace("C", "").replace("%", "").replace("cm", ""))
                    elif key == "image":
                        sensor_data[key] = value
                    else:
                        sensor_data[key] = value
        except Exception as e:
            print(f"Error processing message: {e}")

    client.subscribe(topic)
    client.on_message = on_message

def mqtt_thread():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

# Start MQTT in a separate thread
thread = threading.Thread(target=mqtt_thread)
thread.daemon = True
thread.start()

# Dash app setup
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("Sensor Dashboard"), className="text-center my-3")),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Temperature"),
            dbc.CardBody(html.H2(id="temperature-display", className="card-title"))
        ], className="text-center"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Humidity"),
            dbc.CardBody(html.H2(id="humidity-display", className="card-title"))
        ], className="text-center"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Distance"),
            dbc.CardBody(html.H2(id="distance-display", className="card-title"))
        ], className="text-center"), width=3),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Gas State"),
            dbc.CardBody(html.H2(id="gas-state-display", className="card-title"))
        ], className="text-center"), width=3),
    ]),
    dbc.Row(dbc.Col(html.Img(id="image-display", style={"width": "100%"}), className="text-center my-3")),
    dbc.Row(dbc.Col(dbc.Alert(id="alert-display", is_open=False, duration=4000), className="text-center my-3")),
    dcc.Interval(id="update-interval", interval=100, n_intervals=0)  # Update every second
])

@app.callback(
    Output("temperature-display", "children"),
    Output("humidity-display", "children"),
    Output("distance-display", "children"),
    Output("gas-state-display", "children"),
    Output("image-display", "src"),
    Output("alert-display", "children"),
    Output("alert-display", "is_open"),
    Input("update-interval", "n_intervals")
)
def update_display(n):
    try:
        image_src = f"data:image/jpeg;base64,{sensor_data['image']}"
        
        # Default values for alert
        alert_messages = []
        is_alert_open = False
        
        # Check conditions for alerts
        if sensor_data["temperature"] > 25:
            alert_messages.append("Warning: High Temperature!")
        if sensor_data["humidity"] > 70:
            alert_messages.append("Warning: High Humidity!")
        if sensor_data["distance"] < 10:
            alert_messages.append("Warning: Object Nearing!")
        if sensor_data["gas_state"] == "Detected":
            alert_messages.append("Warning: Gas Detected!")
        
        if alert_messages:
            is_alert_open = True
        
        return (
            f"{sensor_data['temperature']:.1f} °C",
            f"{sensor_data['humidity']:.1f} %",
            f"{sensor_data['distance']:.2f} cm",
            sensor_data["gas_state"],
            image_src,
            " ".join(alert_messages),
            is_alert_open
        )
    except Exception as e:
        print(f"Error in callback: {e}")
        # Return the last known good values
        image_src = f"data:image/jpeg;base64,{sensor_data['image']}"
        return (
            f"{sensor_data['temperature']:.1f} °C",
            f"{sensor_data['humidity']:.1f} %",
            f"{sensor_data['distance']:.2f} cm",
            sensor_data["gas_state"],
            image_src,
            "Error occurred, displaying last known values.",
            True
        )

if __name__ == '__main__':
    app.run_server(debug=True)
