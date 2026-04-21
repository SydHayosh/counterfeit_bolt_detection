
#Calls gitCheck.sh, checks for update on boot

#chmod -R 777 .
#cd CBDS/bootBehavior/

#./gitCheck.sh

#After gitCheck.sh, opens userControls.py
cd
cd CBDS

source .venv/bin/activate
cd
cd CBDS
python -m frameworkOperator.userControls 

echo "Boot succesful"