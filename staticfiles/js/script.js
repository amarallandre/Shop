let carrinho = [];
let produtosDisponiveis = [];


function exibirProdutos(produtos) {
  const produtosContainer = document.querySelector(".produtos-container");
  produtosContainer.innerHTML = "";

  produtos.forEach((produto) => {
    const produtoElement = document.createElement("div");
    produtoElement.classList.add("produto");

    produtoElement.innerHTML = `
    <h3>${produto.nome}</h3>
    <p>${produto.descricao}</p>
    <p>Preço: R$ ${produto.preco}</p>
    <button class="adicionar-carrinho" data-produto-id="${produto.id}">
      Adicionar ao Carrinho
    </button>
    <button class="remover-produto" data-produto-id="${produto.id}">
      Remover Produto
    </button>
  `;

    produtosContainer.appendChild(produtoElement);
  });


  adicionarOuvintes();
}


function adicionarOuvintes() {
  const produtosDisponiveis = document.querySelectorAll(
    ".adicionar-carrinho"
  );

  produtosDisponiveis.forEach((botao) => {
    botao.addEventListener("click", function () {
      const produtoId = this.getAttribute("data-produto-id");
      adicionarAoCarrinho(produtoId);
    });
  });
}


function adicionarAoCarrinho(produtoId) {
  const produto = encontrarProdutoPorId(produtoId);

  if (produto) {
    const itemNoCarrinho = carrinho.find(
      (item) => item.produtoId === produtoId
    );

    if (itemNoCarrinho) {
      itemNoCarrinho.quantidade++;
    } else {
      carrinho.push({
        produtoId: produtoId,
        nome: produto.nome,
        preco: parseFloat(produto.preco),
        quantidade: 1,
      });
    }

    atualizarCarrinho();
  }
}


function atualizarCarrinho() {
  const carrinhoLista = document.getElementById("carrinho-lista");
  carrinhoLista.innerHTML = "";

  carrinho.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.nome} - Quantidade: ${
      item.quantidade
    } - Subtotal: R$ ${item.preco * item.quantidade}`;
    carrinhoLista.appendChild(li);
  });
}


function encontrarProdutoPorId(produtoId) {
  return produtosDisponiveis.find((produto) => produto.id == produtoId);
}


function obterProdutosDisponiveis() {
  $.ajax({
    url: "/produtos_disponiveis/",
    method: "GET",
    dataType: "json",
    success: function (data) {

      produtosDisponiveis = data;
      exibirProdutos(data);
    },
    error: function (error) {
      console.error("Erro ao obter produtos disponíveis:", error);
    },
    success: function (data) {
      produtosDisponiveis = data;
      exibirProdutos(data);
    },
  });
}

const botoesRemoverProduto = document.querySelectorAll(".remover-produto");
botoesRemoverProduto.forEach((botao) => {
  botao.addEventListener("click", function () {
    const produtoId = this.closest(".produto").getAttribute("data-produto-id");
    removerProduto(produtoId);
  });
});

function removerProduto(produtoId) {
  fetch(`/Remover_produto/${produtoId}/`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": obterCSRFToken(),
    },
  })
    .then((response) => {
      if (response.ok) {

        const elementoRemover = document.querySelector(`[data-produto-id="${produtoId}"]`);
        if (elementoRemover) {
          elementoRemover.remove();
        }
      } else {
        console.error("Erro ao remover produto:", response.statusText);
      }
    })
    .catch((error) => {
      console.error("Erro ao remover produto:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {

  obterProdutosDisponiveis();




  const btnLimparCarrinho = document.getElementById("limpar-carrinho");
  btnLimparCarrinho.addEventListener("click", function () {
    limparCarrinho();
  });



  function limparCarrinho() {
    carrinho = [];
    atualizarCarrinho();
  }

  function atualizarCarrinho() {
    const carrinhoLista = document.getElementById("carrinho-lista");
    carrinhoLista.innerHTML = "";

    carrinho.forEach((item) => {
      const li = document.createElement("li");
      li.textContent = `${item.nome} - Quantidade: ${item.quantidade} - Subtotal: R$ ${item.preco * item.quantidade}`;
      carrinhoLista.appendChild(li);
    });
  }

  const btnFinalizarCompra = document.getElementById("finalizar-compra");
  btnFinalizarCompra.addEventListener("click", function () {
    finalizarCompra();
  });

  function finalizarCompra() {
    const itensDoCarrinho = carrinho.map((item) => ({
      produto_id: item.produtoId,
      quantidade: item.quantidade,
      preco_unitario: item.preco,
    }));

    if (itensDoCarrinho.length > 0) {
      fetch("/historico/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": obterCSRFToken(),
        },
        body: JSON.stringify({
          itens_do_carrinho: itensDoCarrinho,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          alert(data.mensagem);
          window.location.href = "/historico/";
        })
        .catch((error) => {
          console.error("Erro ao finalizar compra:", error);
        });
    } else {
      console.error(
        "Erro: Carrinho vazio. Adicione itens ao carrinho antes de finalizar a compra."
      );
    }
  }

  function obterCSRFToken() {
    const cookieValue = document.cookie
      .split("; ")
      .find((row) => row.startsWith("csrftoken="))
      .split("=")[1];
    return cookieValue;
  }

  let proximoNumeroCompra = 1;

  function obterProximoNumeroDaCompra() {

    const numeroDaCompra = proximoNumeroCompra;
    proximoNumeroCompra++;

    return null;
  }
});
