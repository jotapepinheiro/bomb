.PHONY: help
.DEFAULT_GOAL = help

## —— Docker 🐳  ———————————————————————————————————————————————————————————————
start-all: ## Iniciar todos os containers
	docker-compose up -d

down-all: ## Desligar todos os containers
	docker-compose down

commit-all: ## Salvar todos os containers
	docker commit bot_bomb bomb_bot_bomb:latest

bomb-shell: ## Acessar container bomb
	docker container exec -it bot_bomb bash

## —— SSH 🎶 ———————————————————————————————————————————————————————————————
init-bot: ## Enviar comando para bomb
	docker-compose exec bot_bomb sh -c "cd /home/ubuntu/Desktop/bomb \
	&& python3 index.py"

open-brave: ## Enviar comando para bomb
	docker-compose exec bot_bomb sh -c "brave-browser google.com"

## —— Outros 🛠️️ ———————————————————————————————————————————————————————————————

help: ## Lista de commandos
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m%-24s\033[0m %s\n", $$1, $$2}' \
	| sed -e 's/\[32m## /[33m/' && printf "\n"
