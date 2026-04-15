echo "Checking onchipCBDS branch for updates..."
cd
cd CBDS

git clone -b onchipCBDS https://github.com/SydHayosh/counterfeit_bolt_detection.git
echo "Checking libraries for updates..."

ts=$(date +%s)
sudo apt-get update &> /var/run/update-repositories-on-bootup-output-${ts}.log

echo "CBDS Online"
