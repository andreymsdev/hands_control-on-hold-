# Hand-Control System

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.x-red?style=for-the-badge&logo=googles-fuchsia)
![OS](https://img.shields.io/badge/OS-Linux%20(Arch)-yellowgreen?style=for-the-badge&logo=linux)

---

## Objetivo

O **Hand-Control System** é um projeto de **Interação Humano-Computador (HCI)** que utiliza **Visão Computacional** e **Machine Learning** para traduzir gestos da mão em comandos de controle do sistema operacional. O objetivo é proporcionar uma forma alternativa, ergonômica e **hands-free** (sem contato) de gerenciar funções básicas do PC.

O sistema rastreia as mãos em tempo real através da webcam, identifica a posição e o estado dos 21 *landmarks* (pontos de referência) de cada mão, e executa ações do sistema com base em gestos predefinidos.

---

## Objetivo

Permitir a interação sem contato com o computador, traduzindo movimentos e posições da mão em comandos do sistema (como aumentar/diminuir volume, suspender, ou controlar brilho da tela), promovendo uma forma alternativa e ergonômica de controle.

---

## Funcionalidades e Gestos Mapeados

O sistema reconhece e executa as seguintes ações no sistema operacional Linux:

| Gesto (Mão Única) | Critério de Detecção | Função Acionada |
| :--- | :--- | :--- |
| **Mão Aberta** | Todos os cinco dedos levantados (Polegar, Indicador, Médio, Anelar, Mindinho). | Suspender o PC (`systemctl suspend`). |
| **Dedo Indicador** | Apenas o Indicador levantado. | Aumentar Volume. |
| **Dedo Médio** | Apenas o Médio levantado. | Diminuir Volume. |
| **Dedo Polegar** | Apenas o Polegar levantado. | Diminuir Brilho da Tela. |
| **Polegar + Indicador** | Polegar e Indicador levantados (sinal de "L"). | Aumentar Brilho da Tela. |

---

## Tecnologias 

| Categoria | Tecnologia | Uso no Projeto |
| :--- | :--- | :--- |
| **Visão Computacional** | **MediaPipe Hands** | Modelo de ML para rastreamento de 21 *landmarks* 3D da mão. |
| **Processamento de Imagem** | **OpenCV (`cv2`)** | Captura de vídeo, pré-processamento de *frames* (espelhamento) e exibição da interface gráfica. |
| **Controle de Áudio** | **`pulsectl`** | Interface de baixo nível para controlar o volume do PulseAudio no Linux. |
| **Controle de Sistema** | **`os.system` / `brightnessctl`** | Execução de comandos de sistema (suspender, controlar brilho). |
| **Ambiente** | **Python 3.11+ (pyenv)** | Linguagem de programação e gerenciamento de versão via Pyenv. |

---

## Instalação 

Este projeto requer um ambiente Python específico devido a incompatibilidades históricas do **MediaPipe** com as versões mais recentes (como Python 3.13 no Arch Linux). Recomenda-se o uso do **`pyenv`** para gerenciar a versão correta do Python.

### Pré-requisitos

1.  **Instalar Dependências de Sistema:**
    ```bash
    sudo pacman -S bazel gtk3 # bazel e gtk3 são necessários para compilação/display
    ```
2.  **Instalar pyenv** (se ainda não tiver).

### 1. Configurar o Ambiente Virtual

Crie um novo ambiente virtual usando uma versão compatível do Python (3.11 é a mais estável para MediaPipe):

```bash
pyenv install 3.11
pyenv virtualenv 3.11 hands_env
pyenv activate hands_env
