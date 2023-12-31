
document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.getElementById('formCadastro');
    const cpfInput = document.getElementById('cpf');
    const nomeCompletoInput = document.getElementById('nome_completo');
    const dataNascimentoInput = document.getElementById('data_nascimento');
    const senhaInput = document.getElementById('password');
    const confirmSenhaInput = document.getElementById('confirm_password');

    // Função para validar o formato do CPF
    function validarCPF(cpf) {
        return cpf.match(/^\d{3}\.\d{3}\.\d{3}-\d{2}$/);
    }

    // Máscara para CPF
    cpfInput.addEventListener('input', () => {
        cpfInput.value = cpfInput.value
            .replace(/\D/g, '')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d)/, '$1.$2')
            .replace(/(\d{3})(\d{1,2})/, '$1-$2')
            .replace(/(-\d{2})\d+?$/, '$1');
        cpfInput.nextElementSibling.style.display = validarCPF(cpfInput.value) ? 'none' : 'block';
    });

    // Máscara para Data de Nascimento
    dataNascimentoInput.addEventListener('input', () => {
        dataNascimentoInput.value = dataNascimentoInput.value
            .replace(/\D/g, '')
            .replace(/(\d{2})(\d)/, '$1/$2')
            .replace(/(\d{2})(\d)/, '$1/$2');
    });

    form.addEventListener('submit', (e) => {
        let valid = true;

        // Validar CPF
        if (!validarCPF(cpfInput.value)) {
            valid = false;
            cpfInput.nextElementSibling.style.display = 'block';
        } else {
            cpfInput.nextElementSibling.style.display = 'none';
        }

        // Validar Nome Completo
        if (!nomeCompletoInput.value.trim()) {
            valid = false;
            nomeCompletoInput.nextElementSibling.style.display = 'block';
        } else {
            nomeCompletoInput.nextElementSibling.style.display = 'none';
        }

        // Validar Data de Nascimento
        if (!dataNascimentoInput.value.match(/^\d{2}\/\d{2}\/\d{4}$/)) {
            valid = false;
            dataNascimentoInput.nextElementSibling.style.display = 'block';
        } else {
            dataNascimentoInput.nextElementSibling.style.display = 'none';
        }

        // Validar Senha
        if (!senhaInput.value.trim()) {
            valid = false;
            senhaInput.nextElementSibling.style.display = 'block';
        } else {
            senhaInput.nextElementSibling.style.display = 'none';
        }

        // Validar Confirmação de Senha
        if (senhaInput.value !== confirmSenhaInput.value) {
            valid = false;
            confirmSenhaInput.nextElementSibling.style.display = 'block';
        } else {
            confirmSenhaInput.nextElementSibling.style.display = 'none';
        }

        // Se algum campo obrigatório não estiver válido, previne o envio do formulário
        if (!valid) {
            e.preventDefault();
        }
    });
});
