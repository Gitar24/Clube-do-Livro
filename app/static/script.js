function listarlivros(livros) {
    const div = document.getElementById("lista-livros");
    if (!div) {
        return;
    }

    let html = "";
    for (const livro of livros) {
        html += `
            <div class="card">
                <div class="card-imagem">

                </div>
                <p>${livro.id}</p>
                <h3>${livro.titulo}</h3>
                <h4>${livro.autor}</h4>
                <span class="genero-lista">${livro.genero}</span>
                <span class="ano">${livro.ano_publicacao}</span>
                <span class="status">${livro.status}</span>
            </div>`;
    }
    div.innerHTML = html;
}

function listarlivrosrecomendados(recomendacoes) {
    const div = document.getElementById("lista-livros-recomendados");
    if (!div) {
        return;
    }

    let html = "";
    for (const livro of recomendacoes) {
        html += `
            <div class="card">
                <div class="card-imagem">

                </div>
                <p>${livro.id}</p>
                <h3>${livro.titulo}</h3>
                <h4>${livro.autor}</h4>
                <span class="genero-lista">${livro.genero}</span>
                <span class="ano">${livro.ano_publicacao}</span>
                <span class="status">${livro.status}</span>
            </div>`;
    }
    div.innerHTML = html;
}

const botaoCadastrar = document.getElementById("button_cadastrar");
if (botaoCadastrar) {
    botaoCadastrar.onclick = function() {
        const dados = {
            titulo: document.getElementById("titulo").value,
            autor: document.getElementById("autor").value,
            genero: document.getElementById("genero").value,
            ano_publicacao: document.getElementById("ano_publicacao").value
        };

        fetch("/livro", {
            method: "POST",
            headers: {"content-type": "application/json"},
            body: JSON.stringify(dados)
        })
        .then(function(retorno) {
            return retorno.json();
        })
        .then(function(resultado) {
            console.log(resultado);
            alert(resultado.mensagem || resultado.erro);
            if (resultado.mensagem) {
                document.getElementById("titulo").value = "";
                document.getElementById("autor").value = "";
                document.getElementById("genero").value = "";
                document.getElementById("ano_publicacao").value = "";
            }
        });
    };
}

const listaLivros = document.getElementById("lista-livros");
if (listaLivros) {
    fetch("/lista")
        .then(resultado => resultado.json())
        .then(livros => {
            listarlivros(livros);
        });
}

const botaoTodos = document.getElementById("todos");
if (botaoTodos) {
    botaoTodos.onclick = function() {
        fetch("/lista")
            .then(resultado => resultado.json())
            .then(livros => {
                listarlivros(livros);
            });
    };
}

const botaoLidos = document.getElementById("lidos");
if (botaoLidos) {
    botaoLidos.onclick = function() {
        fetch("/lidos")
            .then(resultado => resultado.json())
            .then(livros => {
                listarlivros(livros);
            });
    };
}

const botaoNaoLidos = document.getElementById("nao-lidos");
if (botaoNaoLidos) {
    botaoNaoLidos.onclick = function() {
        fetch("/nao_lidos")
            .then(resultado => resultado.json())
            .then(livros => {
                listarlivros(livros);
            });
    };
}

const botaoBuscar = document.getElementById("buscar");
if (botaoBuscar) {
    botaoBuscar.onclick = function(event) {
        event.preventDefault();
        const valor = document.getElementById("input_buscar").value;
        fetch(`/buscar?buscar=${valor}`)
            .then(resultado => resultado.json())
            .then(livros => {
                listarlivros(livros);
            });
    };
}

const listaRecomendados = document.getElementById("lista-livros-recomendados");
if (listaRecomendados) {
    fetch("/recomendacoes")
        .then(resultado => resultado.json())
        .then(recomendacoes => {
            listarlivrosrecomendados(recomendacoes);
        });
}

const botaoRegistrar = document.getElementById("button_registrar");
if (botaoRegistrar) {
    botaoRegistrar.onclick = function() {
        const dados = {
            livro_id: document.getElementById("livro_id").value,
            nota: document.getElementById("nota").value,
            comentario: document.getElementById("comentario").value,
            data_conclusao: document.getElementById("data_conclusao").value
        };

        fetch("/leituras", {
            method: "POST",
            headers: {"content-type": "application/json"},
            body: JSON.stringify(dados)
        })
        .then(function(retorno) {
            return retorno.json();
        })
        .then(function(resultado) {
            console.log(resultado);
            alert(resultado.mensagem || resultado.erro);
            if (resultado.mensagem) {
                document.getElementById("livro_id").value = "";
                document.getElementById("nota").value = "";
                document.getElementById("comentario").value = "";
                document.getElementById("data_conclusao").value = "";
            }
        });
    };
}
