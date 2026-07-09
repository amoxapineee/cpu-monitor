.PHONY: run backend frontend stop

run: backend frontend

backend:
	uvicorn backend.main:app --reload --port 8000 &> /dev/null &
	@echo "Backend запущен на http://localhost:8000"
	@echo "API документация - http://localhost:8000/docs"

frontend:
	cd frontend && npm run dev &> /dev/null &
	@echo "Frontend запущен на http://localhost:5173"

stop:
	@echo "Остановка..."
	pkill -f uvicorn
	pkill -f vite
