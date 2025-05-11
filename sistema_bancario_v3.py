from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero # número da conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        saldo_excedido = valor > saldo #
        
        if saldo_excedido:
            print(f"\nSaldo insuficiente para a operação. Saldo atual: R$ {saldo}")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso")            
            return True

        else:
            print("Valor informado inválido para a operação.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            # hora = datetime.now()
            # extrato += f"{hora.strftime(mascara_ptbr)} - Depósito:      R$ {valor:.2f}\n" # Registra extrato
            print("Depósito realizado com sucesso!")

        else:
            print("Valor informado inválido para a operação.")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_saque = 500, saques_diarios = 3):
        super().__init__(numero, cliente)

        self._limite_saque = limite_saque
        self._saques_diarios = saques_diarios

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        limite_excedido = valor > self._limite_saque
        saques_excedidos = numero_saques >= self._saques_diarios

        if limite_excedido:
            print(f"\nLimite de saque excedido para a operação. (Limite atual: R$ {self._limite_saque:.2f})")

        elif saques_excedidos:
            print(f"\nLimite de saques diários ({self._saques_diarios}) excedidos.")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência: {self.agencia}
            Conta: {self.numero}
            Titular: {self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )
    
    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower():
                yield transacao

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)

        if sucesso:
            conta.historico.adicionar_transacao(self)

def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nCliente já cadastrado com este CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento: ")
    endereco = input("Informe o endereço: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("\nCliente cadastrado.")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada!")

def consulta_saldo(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print(f"\tSaldo: \t\tR$ {conta.saldo:.2f}")

def listar_contas(contas):
    for conta in contas:
        print(f"\n{conta}")

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    
    if not conta:
        return
    
    print("\n***************** EXTRATO *****************")
    extrato = ""
    transacoes = conta.historico.transacoes

    extrato = ""
    tem_transacao = False
    
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}\n"
    
    if not tem_transacao:
        extrato = "Não foram realizadas transações\n"
    
    print(extrato)
    print(f"\nSaldo: \t\tR$ {conta.saldo:.2f}\n*******************************************")

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do saque: "))
    
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta cadastrada.")
        return
    
    # tentar inserir seleção de conta
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do depósito: "))
    
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def menu():
    menu = """
    Olá!
    Informe o serviço desejado entre as opções:

        1 - Cadastrar cliente
        2 - Cadastrar conta
        3 - Listar contas
        4 - Consultar Saldo
        5 - Extrato
        6 - Saque
        7 - Depósito
        
        0 - Sair

    => """
    
    return int(input(menu))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == 1: # Cadastrar cliente
            cadastrar_cliente(clientes)
                    
        elif opcao == 2: # Cadastrar conta
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == 3: # Listar contas
            listar_contas(contas)
        
        elif opcao == 4: # Consultar saldo
            consulta_saldo(clientes)
                    
        elif opcao == 5: # Consultar extrato
            exibir_extrato(clientes)
        
        elif opcao == 6: # Sacar
            sacar(clientes)
        
        elif opcao == 7: # Depositar
            depositar(clientes)
                    
        elif opcao == 0: # Sair
            print("Obrigado por usar nossos serviços!")
            break

        else:
            print("Opção invalida!\nPor favor insira uma opção válida.")

main()