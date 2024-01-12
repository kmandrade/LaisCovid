document.addEventListener('DOMContentLoaded', function () {
    

    var estadoLista = localStorage.getItem('listaAgendamentosVisivel');
    var lista = document.getElementById('listaAgendamentos');
    lista.style.display = estadoLista === 'true' ? 'block' : 'none';

    document.getElementById('toggleAgendamentos').addEventListener('click', function() {
    lista.style.display = lista.style.display === 'none' ? 'block' : 'none';
    localStorage.setItem('listaAgendamentosVisivel', lista.style.display === 'block');
    });

    
    document.getElementById('inputBuscaEstabelecimento').addEventListener('input', function(e) {
        var textoBusca = e.target.value.toLowerCase();
        var dropdown = document.getElementById('dropdownEstabelecimento');
        var opcoes = dropdown.options;
        var encontrado = false;

        for (var i = 1; i < opcoes.length; i++) {
            var estabelecimento = opcoes[i].getAttribute('data-nome').toLowerCase();
            
            if (estabelecimento.includes(textoBusca)) {
                opcoes[i].style.display = '';
                if (!encontrado) {
                    dropdown.value = opcoes[i].value; 
                    encontrado = true;
                }
            } else {
                opcoes[i].style.display = 'none';
            }
        }

        if (!encontrado) {
            dropdown.value = ''; 
        }
    });
    var dropdownEstabelecimento = document.getElementById('dropdownEstabelecimento');
    var spanVagasDisponiveis = document.getElementById('vagasDisponiveis');

    dropdownEstabelecimento.addEventListener('change', function() {
        var estabelecimentoId = this.value;
        if (estabelecimentoId) {
            fetch(`/agendamento/verificar-vagas/${estabelecimentoId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro ao buscar vagas');
                    }
                    return response.json();
                })
                .then(data => {
                    spanVagasDisponiveis.textContent = `Vagas disponíveis: ${data.vagas_disponiveis}`;
                })
                .catch(error => {
                    console.error('Erro na requisição AJAX:', error);
                    spanVagasDisponiveis.textContent = 'Erro ao buscar vagas';
                });
        } else {
            spanVagasDisponiveis.textContent = 'Vagas disponíveis: ';
        }
    });
    
});
    
    