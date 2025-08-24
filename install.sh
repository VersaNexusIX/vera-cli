cat > install.sh <<'EOF'
#!/data/data/com.termux/files/usr/bin/bash
# 🚀 Auto Installer for VERA-CLI on Termux

echo "[*] Updating Termux..."
pkg update && pkg upgrade -y

echo "[*] Installing Python & Git..."
pkg install python git -y

echo "[*] Upgrading pip & build tools..."
python3 -m pip install --upgrade pip setuptools wheel

# Clone repo kalau belum ada
if [ ! -d "vera-cli" ]; then
    echo "[*] Cloning VERA CLI repo..."
    git clone https://github.com/VersaNexusIX/vera-cli.git
fi

cd vera-cli || exit
termux-setup-storage

cat > requirements.txt <<REQ
beautifulsoup4
pillow
pyfiglet
colorama
requests
yt-dlp
lxml
rich
REQ

echo "[*] Installing Python dependencies..."
pip3 install -r requirements.txt

echo "[*] Installation complete! Run with: python3 cli.py"
EOF

chmod +x install.sh