cat > install.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# 🚀 Auto Installer for VERA-CLI on Termux

echo "[*] Updating Termux..."
pkg update && pkg upgrade -y

echo "[*] Installing Python & Git..."
pkg install python git -y

echo "[*] Upgrading pip & build tools..."
python3 -m pip install --upgrade pip setuptools wheel

if [ ! -d "vera-cli" ]; then
    echo "[*] Cloning VERA CLI repo..."
    git clone https://github.com/VersaNexusIX/vera-cli.git
fi

cd vera-cli || exit
termux-setup-storage

echo "[*] Installing Python dependencies..."
pip3 install colorama
pip3 install beautifulsoup4
pip3 install yt-dlp
pip3 install requests
pip3 install lxml
pip3 install rich
pip3 install pillow

echo "[*] Installation complete! Run with: python3 cli.py"
EOF

chmod +x install.sh