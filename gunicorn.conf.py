# # 서버 설정
# name = "advanced"
preload_app = True

# # 워커 설정
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 500
bind = ["0.0.0.0:8000"]

# # 타임아웃 설정
# timeout = 600
# graceful_timeout = 30

# # 요청 제한 설정
# limit_request_line = 2048
# limit_request_fields = 80
# limit_request_field_size = 4096

# # 성능 및 안정성 설정
# max_requests = 1000
# max_requests_jitter = 100
