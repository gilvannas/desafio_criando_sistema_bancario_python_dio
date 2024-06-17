from abc import ABC, ABCMeta, abstractclassmethod, abstractproperty
from datetime import datetime

class Client:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Client):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome 
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta: 
    def __init__(self, number, client):
        self._saldo = 0
        self._number = number
        self._agencia = "0007"
        self._client = client
        self._history = History()
    
    @classmethod
    def nova_conta(cls, client, number):
        return cls(number, client)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def number(self):
        return self._number
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def client(self):
        return self._client
    
    @property
    def history(self):
        return self._history
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou, saldo insuficiente. ")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso! ")
            return True
        
        else:
            print("Operação falhou, valor informado é inválido ")

        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Depósito realizado!! ")
        else:
            print("Operação falhou, valor informado inválido!! ")
            return False
        
        return True
    
class ContaCorrente(Conta):
    def __init__(self, number, client, limite=500, limite_saques=3):
        super().__init__(number, client)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len({transacao for transacao in self.historico.transacaoes 
                             if transacao["tipo"] == Saque.__name__})

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("Operação falhou! O valor do sauqe excede o limite. ")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            
        else: 
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.number}
            Titurar:\t{self.client.nome}
        """
    
class History:
    def __init__(self):
        self.transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.history.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.history.adcionar_transacao(self)
