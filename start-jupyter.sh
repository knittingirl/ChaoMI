#!/bin/bash
echo "=========================================="
echo "Starting Jupyter Notebook Server"
echo "=========================================="
echo ""
echo "✓ Access the notebook at: http://127.0.0.1:8888"
echo "  (Copy the token from the URL shown below)"
echo ""

jupyter notebook \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --ServerApp.custom_display_url="http://127.0.0.1:8888" \
    2>&1 | grep --line-buffered -v "file:///"
