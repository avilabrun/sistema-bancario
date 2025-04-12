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
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = int(input(menu))
    
    if opcao == 1: # Extrato
        print(extrato)

        print(f"Saldo:         R$ {saldo:.2f}\n")

    elif opcao == 2: # Saque
        if numero_saques == LIMITE_SAQUES: # Testa quandidade de saques disponíveis
            print("Número de saques diários excedido.")
        
        else:
            valor_saque = float(input("Informe o valor desejado: "))
            
            if valor_saque <= 0:
                print("Valor informado inválido para operações de saque!")

            else:
                if valor_saque > saldo: # Testa saldo suficente
                    print("Saldo insuficiente para operação")
                
                elif valor_saque > limite: # Testa limite de saque por operação
                    print("Valor informado acima do limite permitido para operações de saque!")

                else: # Realiza saque se todas as condições forem atendidas
                    saldo -= valor_saque # Incrementa saldo
                    numero_saques += 1 # Incrementa saldo
                    extrato += f"Saque:         R$ {valor_saque:.2f}\n" # Registra extrato

    elif opcao == 3: # Depósito
        valor_deposito = int(input("Informe o valor a ser depositado: "))
        if valor_deposito > 0: # Testa valor positivo para depósito
            saldo += valor_deposito # Incrementa saldo
            extrato += f"Depósito:      R$ {valor_deposito:.2f}\n" # Registra extrato
        
        else: # Mensagem de erro para valor de depósito inválido
            print("Valor informado inválido para operação de depósito.")

    elif opcao == 9: # Imprime o saldo atual
        print(f"Saldo:         R$ {saldo:.2f}\n")
    
    elif opcao == 0: # Sair
        print("Obrigado por usar nossos serviços!")
        break

    else:
        print("Opção invalida!\nPor favor insira uma opção válida.")