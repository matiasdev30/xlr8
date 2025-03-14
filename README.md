# XLR8

XLR8 é um projeto desenvolvido para 

## Estrutura do Projeto

A estrutura do projeto está organizada da seguinte forma:

```
XLR8/
├── .venv/          # Ambiente virtual (ignorado pelo Git)
├── recordings/     # Diretório para gravações
├── results/        # Diretório para saídas/resultados
├── src/            # Código-fonte do projeto
├── requirements.txt # Dependências do projeto
└── .gitignore      # Arquivos ignorados pelo Git
```

## Como Baixar e Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/matiasdev30/xlr8.git
   cd xlr8
   ```
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows, use .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Baixe os modelos necessários (detalhes abaixo) e salve-os na pasta `models/`.
4. Execute o programa:
   ```bash
   python src/main.py  # Ajuste conforme o nome do seu arquivo principal
   ```

## Modelos Necessários

Para que o projeto funcione corretamente, é necessário baixar os seguintes modelos do Hugging Face:

📢 **Transcrição de áudio**: Usei o modelo [mariana-coelho-9/whisper-small-pt](https://huggingface.co/mariana-coelho-9/whisper-small-pt) para converter fala em português para texto com alta precisão.

💬 **Chat e geração de respostas**: O modelo [DeepSeek-Coder-V2-Lite-Instruct-4bit-mlx](https://huggingface.co/DeepSeek-Coder-V2-Lite-Instruct-4bit-mlx) foi a escolha para processar e responder às interações de forma inteligente.

🌍 **Tradução de texto**: Implementei [Helsinki-NLP/opus-mt-tc-big-en-pt](https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-pt) e [facebook/mbart-large-50-many-to-many-mmt](https://huggingface.co/facebook/mbart-large-50-many-to-many-mmt) para suportar traduções fluidas entre inglês, português e outras línguas.

Após o download, salve os arquivos na pasta `models/` dentro do projeto.

## Contribuição

Sinta-se à vontade para contribuir! Para isso, siga os seguintes passos:

1. Faça um fork do repositório.
2. Crie uma branch para a sua feature: `git checkout -b minha-feature`
3. Faça commit das suas alterações: `git commit -m 'Minha nova feature'`
4. Envie para o repositório remoto: `git push origin minha-feature`
5. Abra um Pull Request.

## Autor

- **Matias Dev** - [GitHub](https://github.com/matiasdev30)

