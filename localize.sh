pybabel extract -F ./babel.cfg -o ./locale/messages.pot ./
pybabel update -l en_US -d ./locale -i ./locale/messages.pot
pybabel update -l hu -d ./locale -i ./locale/messages.pot
echo "Now do the translations and run compile afterwards: "
echo "pybabel compile -f -d ./locale"