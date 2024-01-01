document.addEventListener('DOMContentLoaded', function () {
    // Verificar o estado armazenado e ajustar a visibilidade
    var estadoLista = localStorage.getItem('listaAgendamentosVisivel');
    var lista = document.getElementById('listaAgendamentos');
    lista.style.display = estadoLista === 'true' ? 'block' : 'none';

        document.getElementById('toggleAgendamentos').addEventListener('click', function() {
            lista.style.display = lista.style.display === 'none' ? 'block' : 'none';
            // Armazenar o estado atual
            localStorage.setItem('listaAgendamentosVisivel', lista.style.display === 'block');
        });


        var estadoRealizarAgend = localStorage.getItem('realizarAgendamentosVisivel');
        var agendamento = document.getElementById('realizarAgendamento');
        agendamento.style.display = estadoRealizarAgend === 'true' ? 'block' : 'none';

            document.getElementById('toggleRealizarAgend').addEventListener('click', function() {
                agendamento.style.display = agendamento.style.display === 'none' ? 'block' : 'none';
                // Armazenar o estado atual
                localStorage.setItem('realizarAgendamentosVisivel', agendamento.style.display === 'block');
            });

    });
    
    