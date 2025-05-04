# gunicorn_conf.py
bind = "0.0.0.0:5001"
workers = 1
worker_class = "gevent" 
accesslog = "-"  # Log a stdout (importante para Docker)
errorlog = "-"   # Log a stdout
loglevel = "info"
capture_output = True  # Captura los prints/logs de Flask
timeout = 120
keepalive = 5