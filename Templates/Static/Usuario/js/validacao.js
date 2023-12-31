// Função para aplicar a máscara de CPF
function aplicarMascaraCPF(cpf) {
    return cpf
        .replace(/\D/g, '') // Remove tudo que não é dígito
        .replace(/(\d{3})(\d)/, '$1.$2') // Coloca um ponto após o terceiro dígito
        .replace(/(\d{3})(\d)/, '$1.$2') // Coloca um ponto após os seis primeiros dígitos
        .replace(/(\d{3})(\d{1,2})/, '$1-$2') // Coloca um hífen após os nove primeiros dígitos
        .replace(/(-\d{2})\d+?$/, '$1'); // Permite apenas dois dígitos após o hífen
}
function aplicarMascaraData(valor) {
    return valor
        .replace(/\D/g, '') // Remove tudo que não é dígito
        .replace(/^(\d{2})(\d)/, '$1/$2') // Coloca uma barra após o dia
        .replace(/\/(\d{2})(\d)/, '/$1/$2'); // Coloca uma barra após o mês
}

// Função para validar o CPF
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, ''); // Remove tudo que não é dígito
    if (cpf.length !== 11) return false; // Verifica se tem 11 dígitos

    // Elimina CPFs invalidos conhecidos
    if (/^(.)\1+$/.test(cpf)) return false; // Regex que checa sequências como 111.111.111-11

    // Valida 1o digito
    let soma = 0;
    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.charAt(i - 1)) * (11 - i);
    }
    let resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(9))) return false;

    // Valida 2o digito
    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.charAt(i - 1)) * (12 - i);
    }
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(10))) return false;

    return true;
}

document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('formCadastro');
    var cpfInput = document.getElementById('cpf');
    var senhaInput = document.getElementById('password');
    var confirmSenhaInput = document.getElementById('confirm_password');
    var cpfError = document.querySelector('#cpf + span.error');
    var senhaError = document.querySelector('#confirm_password + span.error');
    var campos = form.querySelectorAll('input[required]');
    var dataNascimentoInput = document.getElementById('data_nascimento');

    dataNascimentoInput.addEventListener('input', function() {
        this.value = aplicarMascaraData(this.value);
    });
    
    // Aplicar a máscara ao CPF
    cpfInput.addEventListener('input', function() {
        this.value = aplicarMascaraCPF(this.value);
        cpfError.textContent = validarCPF(this.value) ? '' : 'CPF inválido';
    });

    // Verificar se as senhas coincidem
    confirmSenhaInput.addEventListener('input', function() {
        senhaError.textContent = senhaInput.value === this.value ? '' : 'As senhas não coincidem';
    });

    // Submissão do formulário
    form.addEventListener('submit', function(event) {
        let cpfValido = validarCPF(cpfInput.value);
        let senhasCoincidem = senhaInput.value === confirmSenhaInput.value;

        if (!cpfValido || !senhasCoincidem) {
            // Se o CPF não for válido ou as senhas não coincidirem, mostra os erros
            cpfError.textContent = cpfValido ? '' : 'CPF inválido';
            senhaError.textContent = senhasCoincidem ? '' : 'As senhas não coincidem';
            event.preventDefault(); // Impede a submissão do formulário
        }
        var formValido = true;

        campos.forEach(function(campo) {
            var errorSpan = campo.nextElementSibling;
            if (campo.type === 'text' && campo.value.trim() === '') {
                errorSpan.textContent = 'Este campo é obrigatório.';
                formValido = false;
            } else {
                errorSpan.textContent = '';
            }

            if (campo.id === 'cpf' && !validarCPF(campo.value)) {
                errorSpan.textContent = 'CPF inválido.';
                formValido = false;
            }

            // Verifica se a senha está preenchida
            if (senhaInput.value.trim() === '') {
                errorSpan = senhaInput.nextElementSibling;
                errorSpan.textContent = 'Este campo é obrigatório.';
                formValido = false;
            }

            // Verifica se a confirmação da senha está preenchida e se é igual à senha
            if (confirmSenhaInput.value.trim() === '') {
                errorSpan = confirmSenhaInput.nextElementSibling;
                errorSpan.textContent = 'Este campo é obrigatório.';
                formValido = false;
            } else if (senhaInput.value !== confirmSenhaInput.value) {
                errorSpan = confirmSenhaInput.nextElementSibling;
                errorSpan.textContent = 'As senhas não coincidem.';
                formValido = false;
            }

            if (campo.type === 'date' && !campo.valueAsDate) {
                errorSpan.textContent = 'Data inválida.';
                formValido = false;
            }
        });

        if (!formValido) {
            event.preventDefault();
        }
    });
});
