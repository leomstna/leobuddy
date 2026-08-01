# 🧙 Mascote Virtual (estilo BonziBuddy / Clippy)

Assistente de tela com o seu OC, que reage ao que você está fazendo no PC.

## 1. Instalação

Requer **Windows** (a maioria das detecções usa APIs específicas do Windows)
e **Python 3.10+** instalado.

```bash
pip install -r requirements.txt
```

Isso já é o suficiente pro mascote funcionar. Tem também uma dependência
**opcional** (`winsdk`) que melhora a detecção de Spotify/streaming usando
a API de mídia nativa do Windows. Ela só tem instalação pré-compilada pra
algumas versões do Python — se você estiver numa versão muito nova (3.13,
3.14...) a instalação pode falhar pedindo Visual Studio. **Pode ignorar**,
o programa funciona normalmente sem ela (usa o método antigo de título da
janela como reserva). Se quiser tentar mesmo assim:

```bash
pip install -r requirements-opcional.txt
```

## 2. Coloque as imagens

Jogue **todos os seus PNGs** (exatamente com esses nomes) dentro da pasta `imagens/`:

```
mascote-virtual/
├── main.pyw
├── config.json          <- criado automaticamente
├── core/
└── imagens/              <- SUAS IMAGENS VÃO AQUI
    ├── STANDART.png
    ├── OLA.png
    ├── DANÇANDO.png
    ├── ... (todas as outras)
```

## 3. Rodar

Dê **dois cliques** em `main.pyw` (ou rode `pythonw main.pyw` pelo terminal
pra não abrir uma janela de console preta junto).

Clique com o **botão direito** no mascote pra abrir o menu (Configurações / Sair).
Clique e arraste com o **botão esquerdo** pra mover ele pela tela.

## 4. O que cada imagem representa

| Situação detectada                              | Imagem usada                              |
|--------------------------------------------------|--------------------------------------------|
| Parado / sem nada acontecendo (pose padrão)       | `STANDART.png`                              |
| Poses ociosas aleatórias (varia de tempos em tempos) | `MÃO NO BOLSO.png`, `MÃO NO BOLSO 2.png`, `BRAÇOS CRUZADO.png`, `SENTADO.png`, `SENTADO NO SOFA.png`, `PENSANDO.png` |
| Ao abrir o programa                               | `OLA.png` / `BRAÇOS ABERTOS.png`            |
| Ouvindo música no Spotify (fica "dançando", flip horizontal) | `DANÇANDO.png`                   |
| Assistindo filme/série (Netflix, Prime, YouTube, VLC...) | `PIPOCA.png`                         |
| Webcam ligada                                     | `CAMERA.png` / `CAMERA 2.png`               |
| Tirando print (Print Screen ou Win+Shift+S)       | `MÃO NA TELA.png`                           |
| Tempo de uso prolongado atingido                  | `RELOGIO GIGANTE.png`                       |
| App em tela cheia (jogo, apresentação) — mascote se afasta | `DE COSTAS.png`                    |
| Sugestão de pausa pro café                        | `CAFE ENORME.png` / `SENTADO CAFE.png`      |
| Usuário ausente por um tempo                      | `OLHANDO PRA BAIXO.png`                     |
| Trabalhando em documento/planilha                 | `PAPELADA.png` / `LENDO PAPEL.png`          |
| Lendo PDF/e-book                                  | `LENDO LIVRO.png` / `SENTADO LIVRO.png`     |
| Tarefa concluída / aprovação                      | `JOIA.png` / `JOIA APOIADO.png`             |
| Algo deu errado / confuso                         | `CONFUSO.png`                               |
| Abrindo a tela de configurações                   | `VARINHA.png`                               |
| Dando uma dica / chamando atenção                 | `APONTANDO.png` / `BRAÇOS PRO LADO.png`     |
| "Pensando" / processando algo                     | `PENSANDO.png`                              |

> Quer mudar algum mapeamento? Edite `core/constants.py` — é só um dicionário
> Python, dá pra trocar as imagens, mensagens e prioridades de cada evento.

## 5. Configurações disponíveis (menu ⚙️)

**Aba Geral**
- Minutos de uso contínuo até soltar o alerta do relógio gigante
- Minutos de inatividade que resetam esse contador
- Mascote sempre por cima de todos os apps
- Iniciar automaticamente com o Windows
- Mostrar ou não o balão de fala

**Aba Detecção** — liga/desliga cada sensor individualmente:
- Spotify, Streaming, Print Screen, Webcam, Uso prolongado, Tela cheia

**Aba Aparência**
- Escala/tamanho do mascote
- Intervalo entre poses ociosas
- Chance de soltar frases aleatórias

## 6. Como funcionam as detecções (por trás dos panos)

- **Spotify**: olha o título da janela do processo `Spotify.exe`. Quando
  toca música, o título vira `"Música - Artista"`; quando pausado, fica só
  `"Spotify"`. É uma heurística simples, sem precisar da API oficial.
- **Streaming**: varre os títulos de todas as janelas abertas procurando por
  palavras-chave (Netflix, Prime Video, HBO Max, YouTube, VLC, etc).
- **Webcam**: lê o registro do Windows (`CapabilityAccessManager`), que
  guarda se algum app está usando a câmera agora.
- **Print Screen**: um listener de teclado global escuta a tecla
  `Print Screen` e o atalho `Win+Shift+S`.
- **Tempo de uso**: usa `GetLastInputInfo` do Windows pra saber há quanto
  tempo o mouse/teclado não é usado, e soma o tempo "ativo" da sessão.
- **Tela cheia**: compara o tamanho da janela em foco com o tamanho da tela.

Tudo isso roda numa thread separada a cada alguns segundos (configurável),
então não trava a animação do mascote.

## 7. Se algo não estiver funcionando

Clique com o botão direito no mascote (ou no ícone da bandeja) e escolha
**"🔍 Testar detectores"**. Isso mostra na hora o que cada sensor está
enxergando (se a biblioteca tá instalada, se achou uma sessão de mídia
tocando, se a webcam foi detectada, etc.), e também salva esse relatório
em `mascote_log.txt`, na mesma pasta do `main.pyw`.

Como o `.pyw` roda sem janela de console, **qualquer erro agora vai parar
nesse `mascote_log.txt`** — se algo parecer travado ou não detectar nada,
esse arquivo é o primeiro lugar pra olhar.

Problemas corrigidos numa rodada recente:
- **Transparência com "buracos" no cabelo/roupa escura**: a chave de
  transparência era preta, que colide com partes escuras do personagem.
  Agora usa um magenta (`#FE01FE`) que não aparece na arte.
- **Escala inconsistente entre poses**: as imagens agora são redimensionadas
  pela ALTURA (todas ficam do mesmo tamanho de personagem), em vez de um
  multiplicador aplicado sobre o tamanho original de cada PNG.
- **Borrado / tamanho errado em telas com escala do Windows >100%**: faltava
  ativar DPI awareness antes de criar a janela; sem isso o Windows "estica"
  a janela inteira feito bitmap.
- **Spotify não detectado**: versões recentes do Spotify nem sempre colocam
  "Música - Artista" no título da janela. Agora a detecção usa primeiro a
  API de mídia do Windows (SMTC — a mesma que alimenta os botões de mídia
  do teclado), com o método antigo de título como reserva.

## 8. Ideias pra expandir depois
- Detectar Discord em chamada de voz (ícone de headset ativo)
- Detectar quando está compilando/rodando código (VS Code + terminal aberto)
- Sistema de "humor" que muda a personalidade do mascote ao longo do dia
- Falar as mensagens em voz alta (`pyttsx3`)
- Deixar escolher entre vários OCs/skins diferentes
