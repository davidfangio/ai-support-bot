const formulario = document.getElementById("chat-form");
const campoMensagem = document.getElementById("mensagem");
const areaChat = document.getElementById("chat");
let conversationId = null;

function adicionarMensagem(remetente, mensagem) {
    const elemento = document.createElement("div");

    elemento.classList.add("mensagem");

    if (remetente === "Você") {
        elemento.classList.add("mensagem-usuario");
    } else {
        elemento.classList.add("mensagem-robbie");
    }

    elemento.innerHTML = DOMPurify.sanitize(marked.parse(mensagem));

    areaChat.appendChild(elemento);
    areaChat.scrollTop = areaChat.scrollHeight;
}

formulario.addEventListener("submit", async function(evento) {
    evento.preventDefault();

    const mensagem = campoMensagem.value;

    const botao = formulario.querySelector("button");
    botao.disabled = true;

    adicionarMensagem("Você", mensagem);

    campoMensagem.value = "";

    const indicador = document.createElement("div");
indicador.classList.add("mensagem", "mensagem-robbie", "indicador-digitando");
indicador.textContent = "Robbie está digitando...";

areaChat.appendChild(indicador);
areaChat.scrollTop = areaChat.scrollHeight;

    try {
    const resposta = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            mensagem: mensagem,
            conversation_id: conversationId
        })
    });

    const dados = await resposta.json();

    indicador.remove();

    if (!resposta.ok) {
        throw new Error(dados.resposta || "Erro ao enviar mensagem.");
    }

    conversationId = dados.conversation_id;

    adicionarMensagem("Robbie", dados.resposta);

} catch (erro) {
    indicador.remove();

    adicionarMensagem(
        "Robbie",
        "Não foi possível enviar sua mensagem. Tente novamente em alguns instantes."
    );

} finally {
    botao.disabled = false;
}
});