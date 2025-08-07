# Parking Service API

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-darkgreen.svg)
![Django REST Framework](https://img.shields.io/badge/DRF-3.16-red.svg)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Test Coverage](https://img.shields.io/badge/Coverage-97%25-brightgreen.svg)](https://github.com/actions)
[![CI](https://github.com/CFBruna/parking_service/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/CFBruna/parking_service/actions)

**Status do Projeto:** ✅ Versão 1.0 (Completo) ✅

Uma API RESTful robusta para gerenciamento de um serviço de estacionamento, construída com Django e Django REST Framework. O projeto foi totalmente containerizado com Docker e segue as melhores práticas de desenvolvimento, incluindo testes automatizados com alta cobertura, linting e formatação de código.

## Principais Funcionalidades

* **Gestão de Clientes (`/customers`):** CRUD completo para o cadastro de clientes.
* **Gestão de Veículos (`/vehicles`):** CRUD para veículos, associando-os a clientes.
* **Tipos de Veículos (`/vehicles/type`):** Gerenciamento de categorias de veículos (ex: Carro, Moto).
* **Controle de Estacionamento:**
    * **Vagas (`/parking/spots`):** Gerenciamento das vagas de estacionamento.
    * **Registros (`/parking/records`):** Sistema para registrar a entrada e saída de veículos, com atualização automática do status de ocupação da vaga.
* **Autenticação:** Sistema de autenticação baseado em JWT para proteger os endpoints da API.
* **Admin Otimizado:** Interface de administração customizada com uma funcionalidade inteligente de auto-preenchimento de dados de veículos para agilizar o fluxo de trabalho.

## Decisão de Arquitetura: Geração de Dados de Veículos

Um requisito comum em sistemas de estacionamento é o preenchimento automático de informações do veículo (marca, modelo, cor) a partir da placa. No entanto, não existem APIs públicas, gratuitas e legais no Brasil para este fim. Soluções baseadas em *web scraping* de portais governamentais foram descartadas por serem instáveis, violarem termos de serviço e apresentarem riscos relacionados à LGPD.

Como solução pragmática e profissional, foi implementado um endpoint (`/api/v1/vehicles/get-by-plate/`) que atua como um provedor de dados simulado:

1.  Quando uma placa **nova** é informada, o sistema utiliza a biblioteca **Faker** para gerar dados fictícios de marca, modelo e cor.
2.  Esses dados são salvos no banco de dados.
3.  Em consultas futuras para a mesma placa, os dados consistentes salvos anteriormente são retornados.

Essa abordagem demonstra a capacidade de contornar limitações do mundo real, garantindo uma experiência de usuário fluida e permitindo que o sistema funcione de forma completa e independente, sem depender de serviços externos.

## Tech Stack & Ferramentas

O projeto foi construído com foco em qualidade, manutenibilidade e práticas modernas de desenvolvimento.

* **Backend:** Django, Django REST Framework
* **Banco de Dados:** PostgreSQL
* **Containerização:** Docker, Docker Compose
* **Gerenciamento de Dependências:** `pip` e `pip-tools` (`pip-compile`)
* **Testes:** `pytest`, `pytest-django`, `pytest-cov` (com **97% de cobertura**)
* **Qualidade de Código:** `Ruff` para linting e formatação, `pre-commit` para automação de checks de qualidade.
* **Autenticação:** `djangorestframework-simplejwt` para JWT.
* **Documentação da API:** `drf-spectacular` para geração automática de schemas OpenAPI 3.

## Como Rodar o Projeto Localmente

O projeto é totalmente containerizado, então tudo que você precisa é do Docker e do Docker Compose.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Configure as variáveis de ambiente:**
    Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`.
    ```bash
    cp .env.example .env
    ```
    *O arquivo `.env` já vem com valores padrão para o ambiente de desenvolvimento. Você pode alterá-los se necessário.*

3.  **Suba os contêineres:**
    ```bash
    docker-compose up --build
    ```
    O comando `--build` é importante na primeira vez para construir a imagem Docker.

4.  **Acesse a aplicação:**
    * **API:** `http://127.0.0.1:8000/api/v1/`
    * **Admin:** `http://127.0.0.1:8000/` (Crie um superusuário primeiro)

5.  **(Opcional) Crie um superusuário para o Admin:**
    Em um novo terminal, com os contêineres rodando, execute:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

## Executando os Testes

A suíte de testes automatizados é fundamental para garantir a qualidade e a estabilidade do projeto.

1.  **Para rodar todos os testes:**
    Com os contêineres rodando, execute o seguinte comando:
    ```bash
    docker-compose exec web pytest
    ```

2.  **Para rodar os testes e ver o relatório de cobertura no terminal:**
    ```bash
    docker-compose exec web pytest --cov
    ```

3.  **Para gerar um relatório de cobertura HTML detalhado:**
    ```bash
    docker-compose exec web pytest --cov --cov-report=html
    ```
    Abra o arquivo `htmlcov/index.html` no seu navegador para explorar o relatório.