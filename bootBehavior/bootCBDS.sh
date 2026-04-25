

chmod +x ~/CBDS/bootBehavior/bootCBDS.sh
#!/bin/bash
# Load user environment
#source ~/.bashrc 2>/dev/null || source ~/.bash_profile 2>/dev/null

# Navigate and activate venv
cd ~/CBDS || { echo "CBDS directory not found"; exit 1; }
. .venv/bin/activate

# Run the program
#cd ~/CBDS
#/home/jacks-engineering/CBDS/.venv/bin/python -m frameworkOperator.userControls
#echo "Boot successful"