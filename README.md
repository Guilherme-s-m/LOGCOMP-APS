# Projeto: Linguagem de Programação para Street Fighter

Bem-vindo ao projeto de criação de uma linguagem de programação dedicada a programar as ações de personagens em partidas de Street Fighter! Este projeto tem como objetivo fornecer uma ferramenta inovadora para os entusiastas de jogos de luta, permitindo que eles programem e personalizem as ações dos personagens de maneira programática.

## Visão Geral
Este projeto envolve o desenvolvimento de uma linguagem de programação simples e eficaz que permitirá aos usuários definir os movimentos e estratégias de um personagem de Street Fighter em um ambiente de batalha simulado. A linguagem será projetada para ser acessível tanto para iniciantes quanto para programadores experientes, com uma sintaxe clara e funcionalidades poderosas.

### Funcionalidades
*Sintaxe Intuitiva*: A linguagem terá uma sintaxe fácil de entender, permitindo que os usuários escrevam scripts para controlar os personagens sem a necessidade de aprender uma linguagem de programação complexa.

*Controle Total do Personagem*: Os usuários poderão definir movimentos, combinações de golpes, defesas e estratégias avançadas para seus personagens.

### Como utilizar
A linguagem utiliza um sistema de tempo, em que cada ação realizada pelo seu pesonagem leva 1 segundo para ser executada. Seguindo esse pensamento, a linguagem segue um fluxo de loop, em que ela toda está envolta em um loop até o tempo acabar ou a vida de um dos personagens zerar.
Variáveis disponíveis:
 - char_a_life
 - char_b_life
 - char_a_action
 - char_b_action

As variáveis relacionadas à ação do personagem são as ações que foram definidas na iteração anterior.

### Contexto 
Algumas variáveis da partida já estão definidas:
 - Tempo Máximo: A partida dura 5 minutos (300 segundos)
 - Vida dos Personagens: Cada personagem na partida tem 100 de vida
 - Dano dos Ataques: todos os ataques dão um dano fixo em 5

Em um primeiro momento, a linguagem está baseada nos personagens padrão "personagem a" e "personagem b" que tem os mesmos Status e não possuem habilidades especiais e combos, sendo estes pontos futuros de evolução. Outra mudança que pode acontecer em um segundo momento seria a adição de uma variável de posição e uma análise do range das habilidades.

Os resultados demonstrarão o vencedor da partida, o tempo de vitória, e a vida do vencedor. Se a partida não estiver finalizada ao fim do tempo, vence quem estiver com mais vida, mas se ambos estiverem com a vida igual, ocorre empate. Em caso de empate, será mostrado a vida de ambos os personagens (que deve ser igual).