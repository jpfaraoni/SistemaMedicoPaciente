# Sistema Médico - Gerenciamento de Médicos

## 📋 Funcionalidades Implementadas

### 🏥 Entidade Medico
- **Atributos**: CRM, nome, especialidade, expediente_inicial, expediente_final, sala
- **Getters e Setters**: Para todos os atributos com validação de tipos
- **Método estático**: `popular_medicos()` para criar médicos iniciais

### 🗄️ DAO MedicoDAO
- **Herda de DAO**: Usa o padrão DAO abstrato
- **Métodos**: add, update, get, remove com validações
- **Persistência**: Salva em `medicos.pkl`

### 🎛️ ControladorMedicos
- **Não segue MVC**: Interface de linha de comando para facilitar uso
- **Métodos principais**:
  - `adicionar_medico()` - Cadastra novo médico
  - `atualizar_medico()` - Atualiza dados do médico
  - `remover_medico()` - Remove médico do sistema
  - `listar_medicos()` - Lista todos os médicos
  - `listar_medicos_por_especialidade()` - Filtra por especialidade
  - `listar_medicos_por_sala()` - Filtra por sala
  - `verificar_disponibilidade_medico()` - Verifica horário de expediente
  - `busca_medico()` - Busca médico por CRM

## 🚀 Como Usar

### 1. Inicializar Sistema
```bash
python inicializar_sistema.py
```
Este script cria:
- 13 salas (4 andares)
- 10 médicos com diferentes especialidades

### 2. Executar Sistema Principal
```bash
python main.py
```

### 3. Menu Principal
- **Opção 1**: Gerenciar Pacientes
- **Opção 2**: Gerenciar Médicos ← **NOVO!**
- **Opção 3**: Gerenciar Consultas
- **Opção 0**: Finalizar Sistema

### 4. Menu Médicos
- **Opção 1**: Adicionar Médico
- **Opção 2**: Atualizar Médico
- **Opção 3**: Remover Médico
- **Opção 4**: Listar Médicos
- **Opção 5**: Listar por Especialidade
- **Opção 6**: Listar por Sala
- **Opção 7**: Popular Médicos Iniciais
- **Opção 0**: Voltar

## 👨‍⚕️ Médicos Criados Automaticamente

| CRM | Nome | Especialidade | Sala | Expediente |
|-----|------|---------------|------|------------|
| 12345 | Dr. João Silva | Cardiologia | 101 | 08:00-17:00 |
| 12346 | Dra. Maria Santos | Pediatria | 102 | 07:00-16:00 |
| 12347 | Dr. Pedro Costa | Ortopedia | 103 | 09:00-18:00 |
| 12348 | Dra. Ana Oliveira | Dermatologia | 201 | 08:30-17:30 |
| 12349 | Dr. Carlos Lima | Neurologia | 202 | 07:30-16:30 |
| 12350 | Dra. Fernanda Rocha | Ginecologia | 203 | 08:00-17:00 |
| 12351 | Dr. Roberto Alves | Urologia | 204 | 09:00-18:00 |
| 12352 | Dra. Juliana Ferreira | Psiquiatria | 301 | 08:30-17:30 |
| 12353 | Dr. Marcos Pereira | Cirurgia Geral | 302 | 07:00-16:00 |
| 12354 | Dra. Patricia Souza | Oftalmologia | 303 | 08:00-17:00 |

## 🔗 Integração com Consultas

O `ControladorMedicos` está totalmente integrado com o sistema de consultas:

- **`listar_medicos(selecionar=True)`**: Usado em `adicionar_consultas()`
- **`busca_medico(crm)`**: Usado para buscar médico por CRM
- **`verificar_disponibilidade_medico()`**: Verifica se médico está em expediente
- **Sala do médico**: Automaticamente atribuída à consulta

## 📁 Arquivos Criados/Modificados

### Novos Arquivos:
- `entidades/medico.py` - Entidade Médico
- `DAO/medico_dao.py` - DAO para médicos
- `controle/controlador_medicos.py` - Controlador completo
- `exceptions/medico_nao_encontrado_exception.py` - Exception
- `popular_medicos.py` - Script para popular médicos
- `inicializar_sistema.py` - Script de inicialização completo

### Arquivos Modificados:
- `controle/controlador_sistema.py` - Adicionado controlador de médicos
- `limite/tela_sistema.py` - Atualizado menu principal
- `controle/controlador_consulta.py` - Integração com médicos

## ✅ Funcionalidades Testadas

- ✅ Criação de médicos
- ✅ Listagem de médicos
- ✅ Busca por CRM
- ✅ Filtros por especialidade e sala
- ✅ Verificação de disponibilidade
- ✅ Integração com sistema de consultas
- ✅ Persistência em arquivo pickle
- ✅ Menu interativo completo

O sistema está pronto para uso! 🎉
