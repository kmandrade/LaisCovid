document.addEventListener('DOMContentLoaded', function () {
    
    var botaoRealizarAgendamento = document.getElementById('toggleRealizarAgend');
    var agendamento = document.getElementById('realizarAgendamento');

    botaoRealizarAgendamento.addEventListener('click', function() {
        agendamento.style.display = agendamento.style.display === 'none' ? 'block' : 'none';
        localStorage.setItem('realizarAgendamentosVisivel', agendamento.style.display === 'block');
    });

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
    
});
    
    