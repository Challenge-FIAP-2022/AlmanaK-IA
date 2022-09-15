# Documentação AlmanaK AI

## Integrantes do Grupo 
Nome do grupo: BEIJOZ
- Bianca Man Tchuin Chang Lee (RM: 89171)
- Danilo Zequim de Moura (RM: 89045)
- Eric Brianez Giannetti (RM: 87087)
- Matheus Pismel de Jeronymo (RM: 86931)
- Otavio de Magalhães Gomes (RM: 87680)
- Zack Lorenzzo Corrêa (RM: 87149)
<hr>
<br>

## Descrição do projeto
O projeto consiste na criação de um aplicativo mobile, onde os usuários podem consultar jogos presenciais para jogar no seu tempo de lazer. 
Com a pandemia, muitas crianças ficaram sem brincar com seus amigos, então o app poderá dar sugestões de brincadeiras! Mas não para por ai... 
a aplicação não se limita a crianças, podendo ser para adultos também. Podem ser selecionados itens ou categorias para trazer diferentes opções
de jogos na tela. Você pode consultar as regras do jogo, avaliar, comentar, entre outras funções.
<hr>
<br>

## Objetivo do Chatbot
Nessa etapa do projeto, estamos usando as funcionalidades de um chatbot para que o usuário possa realizar buscas personalizadas de jogos por meio de comandos de voz. Dessa forma, não há um fluxo da conversa, apenas o áudio do usuário obtendo como resposta um áudio de que a mensagem foi entendida e que os filtros serão aplicados. Junto com o áudio de resposta, um Json informando quais filtros devem ser aplicados.
<hr>
<br>

## Chatbot
Todos os arquivos de chatbot podem ser encontrados na pasta com o mesmo nome. Nela irá constar o Json com o <a href="/Chatbot/AlmanaK Watson Assistant.json">Watson Assistant</a>, json para os testes de endpoints realizados no <a href="/Chatbot/Insomnia_Request.json">Insominia</a> e o arquivo da arquitetura do endpoint feita em <a href="/Chatbot/Node Red AlmanaK.json">Nodered</a>.

Segue o link para o teste default do endpoint:

Método: GET

Link: https://almanak.mybluemix.net/chatbot/teste

Como resposta, é esperado um JSON conforme segue:

```json
{
	"text": "Ok, entendido, só um segundo enquanto ajusto os filtros. Se estiver tudo certo, basta clickar no botão buscar,  caso contrário pode enviar outro áudio pra mim.",
	"busca": {
		"sys-number": [
			"5",
			"1"
		],
		"Idade": [
			"maior de idade"
		],
		"Categorias": [
			"Cartas"
		],
		"Itens": [
			"Baralho"
		]
	}
}
```

<hr>
<br>

## Telegram

Para os demais testes e integração por voz, recomendamos que a conversa seja endereçada via telegram com o nosso chatbot de nome @AlmanaKFIAPbot ou acessando o link https://t.me/AlmanaKFIAPbot.
