// ==UserScript==
// @name         Alimentar Peixe
// @namespace    https://cointofish.io
// @version      0.1
// @description  Caso não passe nenhum parâmetro, os peixes serão alimentados conforme a raridade
// @author       You
// @match        https://cointofish.io/*
// @icon         https://cointofish.io/favicon.ico
// @grant        GM_xmlhttpRequest
// @compatible chrome
// @compatible firefox
// @compatible opera
// @compatible safari
// @compatible edge
// @param {string|null} comida - pao, algas, abobora, maca
// ==/UserScript==

window.onload = function(){
    setTimeout( function(){
        var peixes = document.querySelector(".rowmodif");

        if(peixes != null || peixes != undefined) {
            alimentarPeixe()
        }
    }, 8000);
};

async function alimentarPeixe(comida) {
    var peixes = document.querySelector(".rowmodif");
    var proximo = peixes.firstElementChild;
    var comer = "";
    var sleepTime = 1500;

    let alimentos = {
        "maca": 1002,
        "pao": 1003,
        "alga": 1004,
        "abobora": 1025
    }

    let heroes = {
        "Common": alimentos.alga,
        "Uncommon": alimentos.alga,
        "Rare": alimentos.maca,
        "Super Rare": alimentos.pao,
        "Epic": alimentos.pao,
        "Legendary": alimentos.pao,
        "Unique": alimentos.pao
    }

    while(proximo) {
        var progress = proximo.querySelector(".progress-bar").style.getPropertyValue("width");

        if(parseInt(progress) == 0 || (parseInt(progress) > 0 && parseInt(progress) < 50)) {
            proximo.querySelector(".feedfish").click();
            await sleep(sleepTime);

            if(comida === undefined || comida === null) {
                var tabela = document.querySelector(".table-striped");
                var tipo = tabela.getElementsByTagName("td")[2].innerText;
                comer = heroes[tipo];
            } else {
                switch (comida) {
                    case "maca":
                        comer = alimentos.maca;
                        break;
                    case "pao":
                        comer = alimentos.pao;
                        break;
                    case "alga":
                        comer = alimentos.alga;
                        break;
                    case "abobora":
                        comer = alimentos.abobora;
                        break;
                }
            }
            await sleep(sleepTime);
            var alimento = document.querySelector("#avfoods");
            alimento.querySelector('option[value="' + comer + '"]').selected=true;
            await sleep(sleepTime);
            var event = new Event('change');
            alimento.dispatchEvent(event);
            await sleep(sleepTime);
            document.querySelector(".feednowfish").click();
            await sleep(sleepTime);
            document.querySelector(".btnclosemodal").click();
            await sleep(sleepTime).then((tipo) => {console.info(`${tipo} Alimentado!`)});
        }

        proximo = proximo.nextElementSibling;
    }

    // Alimenta o peixe a cada 10m
    var now = new Date
    await sleep(100).then(() => {console.warn(`Peixes alimentados às ${now.getHours()}:${now.getMinutes()}`)});
    await sleep(600000).then(() => { alimentarPeixe(comida) });
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}