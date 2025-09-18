// 1. Configuração do Cliente Supabase
// Vá em "Project Settings" > "API" no seu painel Supabase para encontrar essas informações.
const SUPABASE_URL = 'https://rprwkinapuwsdpiifrdl.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwcndraW5hcHV3c2RwaWlmcmRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgyMDQ4NjAsImV4cCI6MjA3Mzc4MDg2MH0.enGl5j313BI8cMxe6soGhViHd6667z8usxtJXPR2F9k';

const supabase = supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// 2. Elemento da Tabela
const projectListTbody = document.getElementById('project-list');

/**
 * Função para carregar os projetos do Supabase e renderizar na tabela.
 */
async function carregarProjetos() {
    // Limpa a tabela e mostra mensagem de carregamento
    projectListTbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Carregando projetos...</td></tr>';

    const { data: projetos, error } = await supabase
        .from('projetos')
        .select('*')
        .order('created_at', { ascending: true }); // Ordena pelos mais antigos primeiro

    if (error) {
        console.error('Erro ao buscar projetos:', error);
        projectListTbody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: red;">Erro ao carregar projetos.</td></tr>';
        return;
    }

    // Limpa a tabela novamente antes de adicionar os novos dados
    projectListTbody.innerHTML = '';

    if (projetos.length === 0) {
        projectListTbody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Nenhum projeto encontrado.</td></tr>';
        return;
    }

    // 3. Cria uma linha (<tr>) para cada projeto
    projetos.forEach(projeto => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${projeto.nome}</td>
            
            <td>
                <textarea onblur="atualizarCampo(${projeto.id}, 'situacao', this.value)">${projeto.situacao || ''}</textarea>
            </td>

            <td>
                <input type="text" value="${projeto.prazo || ''}" onblur="atualizarCampo(${projeto.id}, 'prazo', this.value)" />
            </td>

            <td>
                <select onchange="atualizarCampo(${projeto.id}, 'prioridade', this.value)">
                    <option value="Alta Prioridade" ${projeto.prioridade === 'Alta Prioridade' ? 'selected' : ''}>Alta Prioridade</option>
                    <option value="Média Prioridade" ${projeto.prioridade === 'Média Prioridade' ? 'selected' : ''}>Média Prioridade</option>
                    <option value="Baixa Prioridade" ${projeto.prioridade === 'Baixa Prioridade' ? 'selected' : ''}>Baixa Prioridade</option>
                    <option value="" ${!projeto.prioridade ? 'selected' : ''}>N/A</option>
                </select>
            </td>
        `;
        projectListTbody.appendChild(tr);
    });
}

/**
 * Função para atualizar um campo específico de um projeto no Supabase.
 * @param {number} id - O ID do projeto a ser atualizado.
 * @param {string} coluna - O nome da coluna a ser atualizada ('situacao', 'prazo', 'prioridade').
 * @param {string} valor - O novo valor para a coluna.
 */
async function atualizarCampo(id, coluna, valor) {
    console.log(`Atualizando projeto ${id}, coluna ${coluna} para: "${valor}"`);

    const { error } = await supabase
        .from('projetos')
        .update({ [coluna]: valor }) // Usamos [coluna] para definir a chave do objeto dinamicamente
        .eq('id', id);

    if (error) {
        console.error('Erro ao atualizar o projeto:', error);
        alert('Falha ao salvar a alteração. Verifique o console para mais detalhes.');
    } else {
        console.log('Projeto atualizado com sucesso!');
        // Poderíamos adicionar um feedback visual aqui, como um brilho verde na célula.
    }
}

// 4. Carrega os projetos assim que a página estiver pronta
document.addEventListener('DOMContentLoaded', carregarProjetos);
