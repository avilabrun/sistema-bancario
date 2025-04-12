menu = """

Olá!
Informe o serviço desejado entre as opções:

    1 - Extrato
    2 - Saque
    3 - Depósito
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
        print("s")

    elif opcao == 2: # Saque
        valor_saque = float(input("Informe o valor desejado: "))
        

    elif opcao == 3: # Depósito
        valor_deposito = int(input("Informe o valor a ser depositado: "))
        

    elif opcao == 0: # Sair
        print("Obrigado por usar nossos serviços!")
        break

    else:
        print("Opção invalida!\nPor favor insira uma opção válida.")