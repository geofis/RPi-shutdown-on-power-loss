#!/bin/bash

SCRIPT_NAME="shutdown_on_power_loss.py"
SERVICE_NAME="shutdown-power-loss.service"
CONF_NAME="shutdown_on_power_loss.conf"

SCRIPT_DEST="/usr/local/bin/$SCRIPT_NAME"
SERVICE_DEST="/etc/systemd/system/$SERVICE_NAME"
CONF_DEST="/etc/$CONF_NAME"

echo "⏳ ¿Cuántos segundos debe esperar antes de apagar tras pérdida de energía externa?"
read -p "Tiempo de espera en segundos (por defecto 600): " USER_TIMEOUT
USER_TIMEOUT=${USER_TIMEOUT:-600}

echo "📌 ¿Qué número de GPIO quieres usar para detectar pérdida de energía externa?"
read -p "Número de GPIO (por defecto 26): " USER_GPIO
USER_GPIO=${USER_GPIO:-26}

echo "📁 Copiando script al sistema..."
sudo cp "$SCRIPT_NAME" "$SCRIPT_DEST"
sudo chmod +x "$SCRIPT_DEST"

echo "📁 Copiando archivo de configuración..."
#echo "USER_TIMEOUT=$USER_TIMEOUT" | sudo tee "$CONF_DEST" > /dev/null
echo -e "USER_TIMEOUT=$USER_TIMEOUT\nGPIO_PIN=$USER_GPIO" | sudo tee "$CONF_DEST" > /dev/null

echo "📁 Copiando servicio systemd..."
sudo cp "$SERVICE_NAME" "$SERVICE_DEST"

echo "🔄 Recargando systemd..."
sudo systemctl daemon-reload

echo "✅ Habilitando y reiniciando servicio..."
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl restart "$SERVICE_NAME"

echo "📋 Estado del servicio:"
sudo systemctl status "$SERVICE_NAME" --no-pager
