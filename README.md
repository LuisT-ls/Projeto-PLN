# Tradutor Multilíngue

![Tradutor Multilíngue](https://img.shields.io/badge/Tradutor-Multil%C3%ADngue-blue)  
![Python Version](https://img.shields.io/badge/Python-3.7%2B-green)  
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

## Descrição

O **Tradutor Multilíngue** é uma aplicação desktop em Python com interface gráfica desenvolvida com `Tkinter`. Ele utiliza as bibliotecas `googletrans`, `TextBlob` e `langdetect` para traduzir textos entre vários idiomas, detectar automaticamente o idioma de entrada e realizar análise de sentimento e subjetividade. Além disso, permite a tradução de arquivos de texto e mantém um histórico das traduções realizadas.

## Funcionalidades

- **Tradução Automática**: Tradução de textos em tempo real para vários idiomas.
- **Detecção Automática de Idioma**: Identifica o idioma do texto automaticamente.
- **Análise de Texto**: Realiza análise de sentimentos (polaridade) e subjetividade.
- **Histórico de Traduções**: Armazena as últimas 100 traduções realizadas.
- **Importação e Tradução de Arquivos**: Traduza arquivos `.txt` e salve os resultados.
- **Interface Intuitiva**: Interface amigável criada com `Tkinter`.
- **Copiar Tradução**: Copie o texto traduzido para a área de transferência.

## Tecnologias Utilizadas

- **Python 3.7+**
- **Tkinter**: Interface gráfica.
- **googletrans**: API de tradução do Google.
- **langdetect**: Detecção de idiomas.
- **TextBlob**: Análise de sentimento e subjetividade.
- **pyperclip**: Manipulação da área de transferência.
- **JSON**: Armazenamento de histórico.
- **Datetime**: Registro de data e hora.

## Pré-requisitos

Certifique-se de ter o Python 3.7 ou superior instalado. Instale as dependências com o comando abaixo:

```bash
pip install googletrans==4.0.0-rc1 langdetect textblob pyperclip
```

## Como Usar

1. Clone o repositório:

   ```bash
   git clone https://github.com/LuisT-ls/Projeto-PLN.git
   ```

2. Navegue até o diretório do projeto:

   ```bash
   cd Projeto-PLN
   ```

3. Execute o script principal:

   ```bash
   python translator_gui.py
   ```

4. Interaja com a interface gráfica para:
   - Inserir texto para tradução.
   - Selecionar idiomas de origem e destino.
   - Realizar análise de texto.
   - Importar arquivos de texto para tradução.

## Estrutura do Projeto

```
Projeto-PLN/
│
├── translator_gui.py           # Código principal da aplicação
├── translation_history.json    # Arquivo de histórico de traduções (gerado automaticamente)
└── README.md                   # Documentação do projeto
```

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. Faça um fork do projeto.
2. Crie uma nova branch: `git checkout -b minha-nova-feature`.
3. Faça suas alterações e commit: `git commit -m 'Adicionando nova funcionalidade'`.
4. Envie suas alterações: `git push origin minha-nova-feature`.
5. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.

---

**Autor:** _Luís Antonio Souza Teixeira_  
**Contato:** _luishg213@gmail.com_

---

**Nota:** Este projeto foi criado para fins educacionais e demonstração de habilidades em Python, Tkinter e Processamento de Linguagem Natural (PLN).