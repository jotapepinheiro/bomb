// ==UserScript==
// @name         Comprar Itens
// @namespace    https://cointofish.io
// @version      0.1
// @description  Comprar alimentados/itens
// @author       You
// @match        https://cointofish.io/*
// @icon         https://cointofish.io/favicon.ico
// @grant        GM_xmlhttpRequest
// @compatible chrome
// @compatible firefox
// @compatible opera
// @compatible safari
// @compatible edge
// @param {number} valor - Valor de compra
// ==/UserScript==

window.onload = function(){
    setTimeout( function(){
        var busca = document.querySelector("#searchmarketb");

        if(busca != null || busca != undefined) {
            comprarItens(4)
        }
    }, 30000);
};

async function comprarItens(valor) {

	window.document.querySelector("#searchmarketb").click();

    setTimeout(function() {
        var comidas = window.document.querySelector("#resultmarket").firstElementChild;
        var preco = comidas.querySelector(".pricefish").textContent.trim();

        if (parseInt(preco) == valor) {
            comidas.querySelector(".tokenimg").click();

            // Entre 300 ou 400, depende do tempo de carregamento da pagina
            setTimeout(function() {
                console.log('Comprado!');
                window.document.querySelector(".buyitemshopm").click();
            }, 400); // TEMPO DE ABERTURA DO MODAL

        } else {
            console.warn('Não Comprado!');
        }
	}, 600); // TEMPO DA ATUALIZACAO DA TELA

    await sleep(7000).then(() => { comprarItens(valor) });

 }

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
