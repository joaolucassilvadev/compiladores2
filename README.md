# Compiladores2

Este repositório implementa um tradutor de arquivos `.vm` para `.asm` como parte do projeto Nand2Tetris. O tradutor converte códigos da linguagem de máquina virtual (VM) para códigos em Assembly do Hack Computer.

## Estrutura do Repositório

O repositório está organizado nas seguintes pastas:

- **07/** e **08/**: Contêm arquivos `.vm` que serão traduzidos para `.asm`. Também possuem arquivos `.txt` (scripts para o CPUEmulator) e `.cmp` (gabaritos para comparação com os arquivos `.out` gerados pelo CPUEmulator).
- **nand2tetris-tools/**: Contém ferramentas do Nand2Tetris, incluindo o CPUEmulator, que será utilizado para testar e comparar arquivos `.asm` com arquivos `.cmp` através dos arquivos `.out`.
- **.src/**: Contém os códigos Python responsáveis pela tradução dos arquivos `.vm` para `.asm`.

## Como Utilizar o Tradutor

Para executar a tradução de um arquivo `.vm` para `.asm`, siga as instruções abaixo.

### No Windows
1. Abra um terminal e navegue até a pasta `.src`:
   ```sh
   cd caminho/para/.src
   ```
2. Execute o seguinte comando, substituindo `caminho_do_arquivo.vm` pelo caminho do arquivo `.vm` desejado:
   ```sh
   python VMTranslator.py "caminho_do_arquivo.vm"
   ```

### No Linux
1. Abra um terminal e navegue até a pasta `.src`:
   ```sh
   cd caminho/para/.src
   ```
2. Execute o seguinte comando:
   ```sh
   python3 VMTranslator.py "caminho_do_arquivo.vm"
   ```

## Explicação dos Arquivos Python

O tradutor está implementado nos seguintes arquivos Python:

- **VMTranslator.py**: Gerencia a leitura do arquivo `.vm`, instancia o `Parser` para analisar os comandos e utiliza o `CodeWriter` para gerar a saída em Assembly.
- **Parser.py**: Responsável por analisar os comandos do arquivo `.vm`, separando-os em `command`, `arg1` e `arg2`.
- **CodeWriter.py**: Converte os comandos analisados em Assembly Hack, gerando a saída correspondente no arquivo `.asm`.

## Testes

Para testar a tradução:
1. Traduza um arquivo `.vm` para `.asm` seguindo as instruções acima.
2. Utilize o CPUEmulator (disponível na pasta `nand2tetris-tools/`) para comparar o arquivo `.asm` gerado com o `.cmp` correspondente.

## Observação

Este repositório faz parte do projeto Nand2Tetris e pode ser expandido para suportar mais comandos e funcionalidades no futuro.
