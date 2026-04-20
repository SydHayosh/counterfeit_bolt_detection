#Calls gitCheck.sh, checks for update on boot
./CBDS/counterfeit_bolt_detection/bootBehavior/gitCheck.sh
cd
cd CBDS
source .venv/bin/activate
./counterfeit_bolt_detection/frameworkOperator/userControls.py
