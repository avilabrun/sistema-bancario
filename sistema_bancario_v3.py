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
        self._numero = numero
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

        self.limite_saque = limite_saque
        self.saques_diarios = saques_diarios

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        limite_excedido = valor > self.limite_saque
        saques_exedidos = numero_saques >= self.saques_diarios

        if limite_excedido:
            print(f"\nLimite de saque excedido para a operação. (Limite atual: R$ {self.limite_saque:.2f})")

        elif saques_exedidos:
            print(f"\nLimite de saques diários ({self.saques_diarios}) excedidos.")

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
                "valor": transacao.valor
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    pass

class Saque(Transacao):
    pass