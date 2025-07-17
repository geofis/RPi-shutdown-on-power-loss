#!/bin/bash

SCRIPT_NAME="shutdown_on_power_loss.py"
SERVICE_NAME="shutdown-power-loss.service"
CONF_NAME="shutdown_on_power_loss.conf"

SCRIPT_DEST="/usr/local/bin/$SCRIPT_NAME"
SERVICE_DEST="/etc/systemd/system/$SERVICE_NAME"
CONF_DEST="/etc/$CONF_NAME"

echo "🛑 Deteniendo servicio..."
sudo systemctl stop "$SERVICE_NAME"

echo "❌ Deshabilitando servicio..."
sudo systemctl disable "$SERVICE_NAME"

echo "➖ Eliminando archivos..."
[ -f "$SCRIPT_DEST" ] && sudo rm "$SCRIPT_DEST" && echo "✔️ Eliminado $SCRIPT_DEST"
[ -f "$CONF_DEST" ] && sudo rm "$CONF_DEST" && echo "✔️ Eliminado $CONF_DEST"
[ -f "$SERVICE_DEST" ] && sudo rm "$SERVICE_DEST" && echo "✔️ Eliminado $SERVICE_DEST"

echo "🔄 Recargando systemd..."
sudo systemctl daemon-reload

echo "✅ Desinstalación completada."

