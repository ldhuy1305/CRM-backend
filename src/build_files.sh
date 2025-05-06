pip3 install --upgrade pip --no-input
pip3 install -r requirements.txt
python3.12 manage.py collectstatic --noinput

if [ ! -d "static" ]; then
    echo "Error: Directory 'static' was not created."
    exit 1
fi