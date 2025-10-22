# Xiu - Removedor de Silêncio 🤫

![GitHub repo size](https://img.shields.io/github/repo-size/athuuum/xiu?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/athuuum/xiu?style=flat-square)

`Xiu` é uma aplicação de desktop (Windows) construída em Python e CustomTkinter. Ela fornece uma interface gráfica simples para remover partes silenciosas de arquivos de mídia (áudio ou vídeo) usando o poder do **FFmpeg**.

A aplicação permite o processamento em lote, ajuste fino da detecção de silêncio e conversão de formato opcional.

[Imagem: Screenshot da interface principal do Xiu]

---

## ✨ Funcionalidades

* **Interface Gráfica Moderna:** Construída com CustomTkinter, com suporte a temas (Claro, Escuro e Padrão do Sistema).
* **Processamento em Lote:** Selecione e processe múltiplos arquivos de áudio ou vídeo de uma só vez.
* **Ajuste de Silêncio (Duração):** Defina a duração mínima (em segundos) que um segmento deve ter para ser considerado "silêncio" e ser removido.
* **Ajuste de Silêncio (Nível):** Defina o nível de volume (em dB) abaixo do qual o áudio é considerado silêncio.
* **Conversão de Formato:** Opção de manter o formato original (padrão) ou converter a saída para `.mp3`, `.wav`, `.m4a` ou `.flac`.
* **Persistência:** Suas configurações de tema, duração e nível de dB são salvas automaticamente em um arquivo `config.json` para a próxima vez que usar o app.

---

## ⚠️ Dependências

Este programa possui duas categorias de dependências: as bibliotecas Python e uma ferramenta externa essencial (FFmpeg).

### 1. Dependências do Python

O programa utiliza as seguintes bibliotecas Python:

* `customtkinter`
* `tkfontawesome`
* `CTkMessagebox`
* `CTkMenuBar`

Você pode instalá-las usando o pip:

bash`
pip install customtkinter tkfontawesome CTkMessagebox CTkMenuBar `

### 2. Dependência Externa: FFmpeg (Obrigatório)

O `Xiu` **não** processa o áudio diretamente. Ele atua como uma interface gráfica que executa comandos do **FFmpeg** em segundo plano. Portanto, o FFmpeg é **essencial** para que o programa funcione.

#### Onde Baixar o FFmpeg?

Você deve baixar o FFmpeg separadamente, pois ele não está incluído neste repositório.

1.  **Site Oficial:** [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2.  **Recomendação para Windows:** O site oficial linka para builds otimizadas. Recomendamos as builds do **Gyan.dev**:
    * Acesse: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
    * Baixe a versão `essentials` (arquivo `.zip`).

#### Onde Colocar o FFmpeg?

Este programa foi codificado para procurar o FFmpeg em um caminho muito específico relativo a ele mesmo.

Após baixar e descompactar o arquivo `.zip` do FFmpeg, você **DEVE** seguir esta estrutura de pastas:

1.  Na pasta onde você salvou o script `xiu.py` (ou onde o executável `.exe` está), crie uma pasta chamada `ffmpeg`.
2.  Entre na pasta `ffmpeg` que você acabou de criar.
3.  Copie o conteúdo da pasta que você baixou (que inclui as pastas `bin`, `doc`, etc.) para dentro desta pasta `ffmpeg`.

O programa procura especificamente pelo caminho: `.\ffmpeg\bin\ffmpeg.exe`. Se este arquivo não for encontrado, o programa exibirá uma mensagem de erro ao tentar processar qualquer mídia.

---

## 🚀 Instalação e Uso

1.  **Clone ou Baixe este Repositório:**
    ```bash
    git clone [https://github.com/athuuum/xiu.git](https://github.com/athuuum/xiu.git)
    cd xiu
    ```

2.  **Instale as Dependências Python:**
    ```bash
    pip install -r requirements.txt 
    ```
    *(Nota: Se um `requirements.txt` não estiver disponível, use o comando da seção de dependências acima).*

3.  **Baixe e Configure o FFmpeg:**
    * Siga as instruções detalhadas na seção "Dependência Externa: FFmpeg (Obrigatório)" acima.

4.  **Execute o Programa:**
    ```bash
    python xiu.py
    ```
    *(Assumindo que o arquivo principal se chama `xiu.py`)*

---

## ⚙️ Como Usar a Interface

1.  **Selecionar Arquivos:** Clique no botão "Selecionar arquivos" para adicionar um ou mais arquivos de mídia (áudio ou vídeo) à lista.
2.  **Duração (segundos):** Arraste o slider para definir o tempo mínimo de silêncio a ser cortado. (Ex: `0.5s` remove silêncios de meio segundo ou mais).
3.  **Nível de Silêncio (dB):** Arraste o slider para definir o limiar de volume. Valores mais baixos (ex: `-50dB`) são mais sensíveis e detectarão silêncios mais sutis. Valores mais altos (ex: `-20dB`) só removerão silêncio quase absoluto.
4.  **Formato de Saída:**
    * **Manter Original:** Tenta salvar no mesmo formato do arquivo de entrada.
    * **Atenção (Vídeos):** Se você selecionar "Manter Original" para um arquivo de *vídeo* (`.mp4`, `.mkv`, etc.), o programa extrairá o áudio e o salvará como `.mp3`.
    * **Outros Formatos:** Você pode forçar a conversão para `.mp3`, `.wav`, `.m4a` ou `.flac`.
5.  **Remover Silêncio:** Clique no botão principal. Uma janela de "Processando" aparecerá.
6.  **Saída:** Os novos arquivos serão salvos na **mesma pasta** dos arquivos originais, prefixados com `xiu_` (ex: `audio.mp3` se torna `xiu_audio.mp3`).



