# gunicorn_conf.py
bind = "0.0.0.0:5002"
workers = 1
worker_class = "gevent" 
accesslog = "-"  # Log a stdout (importante para Docker)
errorlog = "-"   # Log a stdout
loglevel = "info"
capture_output = True  # Captura los prints/logs de Flask
timeout = 300
keepalive = 5