from datetime import date, datetime

menu = """
Olá!
Informe o serviço desejado entre as opções:

    1 - Extrato
    2 - Saque
    3 - Depósito
    9 - Saldo
    0 - Sair

=> """

saldo = 0
extrato = ""

mascara_ptbr = '%d/%m/%Y %H:%M'

limite_saque = 500
numero_saques = 0
operacoes = 0

LIMITE_SAQUES_DIARIOS = 3
LIMITE_OPERACOES = 10

while True:

    opcao = int(input(menu))
    
    if opcao == 1: # Extrato
        print("\n************** EXTRATO **************")
        print(extrato)
        print("\n*************************************")
        print(f"Saldo:         R$ {saldo:.2f}\n")
        print("\n*************************************")

    elif opcao == 2: # Saque
        if operacoes >= LIMITE_OPERACOES:
            print("Limite de operações diárias excedido")

        else:
            if numero_saques == LIMITE_SAQUES_DIARIOS: # Testa quandidade de saques disponíveis
                print("Número de saques diários excedido.")
            
            else:
                valor_saque = float(input("Informe o valor desejado: "))
                
                if valor_saque <= 0:
                    print("Valor informado inválido para operações de saque!")

                else:
                    if valor_saque > saldo: # Testa saldo suficente
                        print("Saldo insuficiente para operação")
                    
                    elif valor_saque > limite_saque: # Testa limite de saque por operação
                        print("Valor informado acima do limite permitido para operações de saque!")

                    else: # Realiza saque se todas as condições forem atendidas
                        saldo -= valor_saque # Incrementa saldo
                        numero_saques += 1 # Incrementa saques realizados
                        
                        hora = datetime.now()
                        extrato += f"{hora.strftime(mascara_ptbr)} - Saque:         R$ {valor_saque:.2f}\n" # Registra extrato

                        operacoes += 1 # Incrementa operações realizadas no dia

    elif opcao == 3: # Depósito      
        if operacoes >= LIMITE_OPERACOES:
            print("Limite de operações diárias excedido")

        else:
            valor_deposito = int(input("Informe o valor a ser depositado: "))
            
            if valor_deposito > 0: # Testa valor positivo para depósito
                saldo += valor_deposito # Incrementa saldo

                hora = datetime.now()
                extrato += f"{hora.strftime(mascara_ptbr)} - Depósito:      R$ {valor_deposito:.2f}\n" # Registra extrato

                operacoes += 1 # Incrementa operações realizadas no dia
            
            else: # Mensagem de erro para valor de depósito inválido
                print("Valor informado inválido para operação de depósito.")

    elif opcao == 9: # Imprime o saldo atual
        print(f"Saldo:         R$ {saldo:.2f}\n")
    
    elif opcao == 0: # Sair
        print("Obrigado por usar nossos serviços!")
        break

    else:
        print("Opção invalida!\nPor favor insira uma opção válida.")