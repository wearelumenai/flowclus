set -e
echo "Running the data simulation service on port 8080"
python -m flowsim --host 0.0.0.0 --port 8080&
echo "Running the data visualization service on port 32211"
python -m oc --host 0.0.0.0 --port 32211 --simport 8080
