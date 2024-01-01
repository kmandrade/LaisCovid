document.addEventListener('DOMContentLoaded', function () {
    
    var botaoRealizarAgendamento = document.getElementById('toggleRealizarAgend');
    var agendamento = document.getElementById('realizarAgendamento');

    botaoRealizarAgendamento.addEventListener('click', function() {
        var temAgendamentoAtivo = this.getAttribute('data-tem-agendamento-ativo') === 'true';
        if (temAgendamentoAtivo) {
            alert("Você já possui um agendamento ativo.");
        } else {
            agendamento.style.display = agendamento.style.display === 'none' ? 'block' : 'none';
            localStorage.setItem('realizarAgendamentosVisivel', agendamento.style.display === 'block');
        }
    });


    var estadoLista = localStorage.getItem('listaAgendamentosVisivel');
    var lista = document.getElementById('listaAgendamentos');
    lista.style.display = estadoLista === 'true' ? 'block' : 'none';

    document.getElementById('toggleAgendamentos').addEventListener('click', function() {
    lista.style.display = lista.style.display === 'none' ? 'block' : 'none';
    localStorage.setItem('listaAgendamentosVisivel', lista.style.display === 'block');
    });

});
    
    