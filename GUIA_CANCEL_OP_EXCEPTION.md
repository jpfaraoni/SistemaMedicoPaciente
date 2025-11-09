# Guia de Uso da CancelOpException

## 📋 Resumo

A `CancelOpException` deve ser usada para interceptar quando o usuário cancela uma operação (clica em "Cancelar" ou fecha a janela).

## 🎯 Onde a Exceção DEVE ser LEVANTADA

### 1. **Nas Telas (limite/) - Métodos de Interface**

#### `tela_pacientes.py`
- ✅ **`exibe_lista_pacientes()`** (linha 132-133, 140-141)
  - Quando: Usuário clica em "Cancelar", "Fechar" ou fecha a janela
  - Quando: Usuário clica em "Confirmar" sem selecionar nenhum paciente
  
- ✅ **`pega_novos_dados_paciente()`** (linha 76-77)
  - Quando: Usuário clica em "Cancelar" ou fecha a janela
  
- ✅ **`seleciona_paciente()`** (linha 98-99)
  - Quando: Usuário clica em "Cancelar" ou fecha a janela

#### `tela_consulta.py`
- ✅ **`exibe_lista_consulta()`** (linha 127-128)
  - Quando: Usuário clica em "Cancelar", "Fechar" ou fecha a janela

#### `tela_medicos.py` (se existir)
- ✅ Métodos similares devem levantar a exceção quando o usuário cancela

## 🛡️ Onde a Exceção DEVE ser CAPTURADA

### 1. **Nos Controladores (controle/) - Métodos de Negócio**

#### `controlador_pacientes.py`

- ✅ **`atualizar_paciente()`** (linha 99-100)
  - **IMPORTANTE**: Verificar se `cpf is None` ANTES de chamar `pega_novos_dados_paciente()`
  - Captura a exceção de `pega_novos_dados_paciente()` se o usuário cancelar a edição
  
- ✅ **`remover_paciente()`** (linha 122-123)
  - **IMPORTANTE**: Verificar se `cpf is None` ANTES de tentar remover
  - Captura a exceção se o usuário cancelar a seleção
  
- ✅ **`listar_pacientes()`** (linha 133-134)
  - Captura a exceção de `exibe_lista_pacientes()` e retorna `None`
  - **CRÍTICO**: Deve retornar `None` explicitamente, não apenas fazer `pass`

- ✅ **`adicionar_paciente()`** (linha 52-53)
  - Captura a exceção de `pega_dados_paciente()` se o usuário cancelar

#### `controlador_consulta.py`

- ✅ **`adicionar_consultas()`** (deve ter)
  - Captura a exceção se o usuário cancelar em qualquer etapa
  
- ✅ **`atualizar_consulta()`** (deve ter)
  - Captura a exceção se o usuário cancelar em qualquer etapa
  
- ✅ **`remover_consulta()`** (deve ter)
  - Captura a exceção se o usuário cancelar a seleção

#### `controlador_medicos.py`

- ✅ Métodos similares devem capturar a exceção

## ⚠️ Padrão de Uso Correto

### ❌ **ERRADO - Não verifica None antes de continuar**
```python
def atualizar_paciente(self):
    try:
        cpf = self.listar_pacientes(selecionar=True)
        # PROBLEMA: Se cpf for None, continua executando!
        paciente = self.busca_paciente(cpf)
        novos_dados = self.pega_novos_dados_paciente()  # Executa mesmo se cancelou!
    except CancelOpException:
        pass
```

### ✅ **CORRETO - Verifica None antes de continuar**
```python
def atualizar_paciente(self):
    try:
        cpf = self.listar_pacientes(selecionar=True)
        
        # Verifica se o usuário cancelou ANTES de continuar
        if cpf is None:
            return  # Retorna silenciosamente
        
        paciente = self.busca_paciente(cpf)
        novos_dados = self.pega_novos_dados_paciente()  # Só executa se não cancelou
    except CancelOpException:
        pass  # Captura se cancelar na segunda tela
```

## 🔄 Fluxo Correto

1. **Tela levanta exceção** → `raise CancelOpException()`
2. **Controlador captura** → `except CancelOpException: return None`
3. **Método que chama verifica** → `if cpf is None: return`
4. **Operação não continua** → Usuário cancelou com sucesso

## 📝 Checklist de Implementação

- [x] Telas levantam `CancelOpException` quando usuário cancela
- [x] `listar_pacientes()` retorna `None` quando captura a exceção
- [x] `atualizar_paciente()` verifica `if cpf is None` antes de continuar
- [x] `remover_paciente()` verifica `if cpf is None` antes de continuar
- [x] Métodos capturam `CancelOpException` no final do try/except
- [x] `exibe_lista_pacientes()` trata "Fechar" como cancelamento
- [x] `exibe_lista_pacientes()` verifica se algo foi selecionado

## 🎯 Regra de Ouro

**SEMPRE verifique se o retorno é `None` ANTES de continuar a operação quando o método pode retornar `None` devido a cancelamento!**

