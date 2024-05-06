import random

def inserir_jogador(filename, nome, vezes_jogadas, vezes_ganhas):
    with open(filename, 'a') as file:
        file.write(f'Nome: {nome} | vezes jogadas: {vezes_jogadas} | Vezes ganhas: {vezes_ganhas} | Media de palpites: 0\n')

def editar_jogador(filename, nome_antigo, novo_nome, novas_vezes_jogou, novas_vezes_ganhou):
    if novas_vezes_jogou < novas_vezes_ganhou:
        print("Erro: O número de vezes jogadas não pode ser menor do que o número de vezes ganhas.")
        return False

    jogador_encontrado = False
    jogadores = []

    with open(filename, 'r') as file:
        linhas = file.readlines()

    with open(filename, 'w') as file:
        for linha in linhas:
            jogador = linha.strip().split('|')
            if jogador[0].strip() == nome_antigo:
                jogadas = novas_vezes_jogou
                ganhas = novas_vezes_ganhou
                file.write(f'Nome: {novo_nome} | vezes jogadas: {jogadas} | Vezes ganhas: {ganhas}\n')
                jogador_encontrado = True
            else:
                file.write(linha)  # Manter as linhas não editadas

    if jogador_encontrado:
        print(f'O jogador "{nome_antigo}" foi editado para "{novo_nome}" com sucesso.')
    else:
        print(f'O jogador "{nome_antigo}" não foi encontrado. Nenhuma alteração foi feita.')

    jogadores = carregar_jogadores(filename)
    return jogadores


def eliminar_jogador(filename, nome):
    jogadores = []
    jogador_encontrado = False

    with open(filename, 'r') as file:
        linhas = file.readlines()

    with open(filename, 'w') as file:
        for linha in linhas:
            jogador = linha.strip().split('|')
            if nome not in jogador[0]:
                file.write(linha)
            else:
                jogador_encontrado = True

    if jogador_encontrado:
        print(f'O jogador "{nome}" foi eliminado com sucesso.')
    else:
        print(f'O jogador "{nome}" não foi encontrado. Nenhuma alteração foi feita.')


def carregar_jogadores(filename):    # <- Atualiza o ficheiro.txt com os dados novos
    jogadores = []
    try:
        with open(filename, 'r') as file:
            for linha in file:
                jogador = linha.strip().split('|')
                nome = jogador[0].strip().split(': ')[1]
                vezes_jogadas = int(jogador[1].strip().split(': ')[1])
                vezes_ganhas = int(jogador[2].strip().split(': ')[1])
                media_palpites = float(jogador[3].strip().split(': ')[1])
                jogadores.append({'nome': nome, 'vezes_jogadas': vezes_jogadas, 'vezes_ganhas': vezes_ganhas, 'media_palpites': media_palpites})
    except FileNotFoundError:
        print(f'O arquivo "{filename}" não existe. Criando um novo arquivo.')
        open(filename, 'w').close()
    return jogadores

def jogar(peso_correto, jogadores, filename):   # <- Alterei também a função para que ao jogar, 
                                                # escolher com quem quer jogar, atualizando assim um jogador de cada vez que joga
    if not jogadores:
        print('Não há jogadores suficientes, insira-os primeiro.')
        return

    print("Jogadores disponíveis:")
    for idx, jogador in enumerate(jogadores):
        print(f"{idx + 1}. {jogador['nome']}")

    while True:
        escolha = input("Escolha o número do jogador que deseja jogar (ou 0 para voltar): ")
        if escolha == '0':
            return
        try:
            escolha_idx = int(escolha) - 1
            if 0 <= escolha_idx < len(jogadores):
                break
            else:
                print("Escolha inválida. Por favor, escolha um número válido ou 0 para voltar.")
        except ValueError:
            print("Escolha inválida. Por favor, escolha um número válido ou 0 para voltar.")

    jogador_escolhido = jogadores[escolha_idx]

    palpite = random.uniform(4.200, 4.350)
    print(f'Palpite de {jogador_escolhido["nome"]}: {palpite:.3f} kg')

    diferenca = abs(palpite - peso_correto)
    print(f'Diferença: {diferenca:.3f} kg')

    jogador_escolhido['vezes_jogadas'] += 1

    if diferenca <= 0.075:
        jogador_escolhido['vezes_ganhas'] += 1
        print(f'{jogador_escolhido["nome"]} ganhou!')

    jogador_escolhido['media_palpites'] = (jogador_escolhido['media_palpites'] * (jogador_escolhido['vezes_jogadas'] - 1) + diferenca) / jogador_escolhido['vezes_jogadas']

    with open(filename, 'w') as file:
        for jogador in jogadores:
            file.write(f'Nome: {jogador["nome"]} | vezes jogadas: {jogador["vezes_jogadas"]} | Vezes ganhas: {jogador["vezes_ganhas"]} | Media de palpites: {jogador["media_palpites"]:.3f}\n')

    print('Jogo concluído. Obrigada pela sua participação!')

def ver_dados_ouvinte(filename, nome):
    try:
        with open(filename, 'r') as file:
            for linha in file:
                jogador = linha.strip().split('|')
                if jogador[0].strip().split(': ')[1] == nome:
                    vezes_jogadas = int(jogador[1].strip().split(': ')[1])
                    vezes_ganhas = int(jogador[2].strip().split(': ')[1])
                    media_palpites = float(jogador[3].strip().split(': ')[1])
                    print(f'Dados do ouvinte {nome}:')
                    print(f'Vezes Jogadas: {vezes_jogadas}')
                    print(f'Vezes Ganhas: {vezes_ganhas}')
                    print(f'Media de palpites: {media_palpites:.3f}')
                    return
        print(f'O ouvinte "{nome}" não foi encontrado.')
    except FileNotFoundError:
        print(f'O arquivo "{filename}" não existe.')

def ver_ranking(filename):                      # Apesar de não termos dado a função lambda, estive a ver no 
                                                #  stackoverflow e foi a forma mais prática que encontrei de realizar o ranking
    try:
        jogadores = carregar_jogadores(filename)
        ranking = sorted(jogadores, key=lambda x: (x['vezes_ganhas'], -x['vezes_jogadas'], -x['media_palpites'], x['nome']), reverse=True)
        print('Ranking de Ouvintes:')
        print('Posição | Nome  | Vezes Jogadas | Vezes Ganhas | Media de palpites')
        print('-' * 70)
        for posicao, jogador in enumerate(ranking, start=1):
            print(f'{posicao:>7} | {jogador["nome"]} | {jogador["vezes_jogadas"]: ^13} | {jogador["vezes_ganhas"]: ^12} | {jogador["media_palpites"]: ^17.3f}')
    except FileNotFoundError:
        print(f'O arquivo "{filename}" não existe.')


def salvar_dados(filename, jogadores):
    with open(filename, 'w') as file:
        for jogador in jogadores:
            nome = jogador['nome']
            vezes_jogadas = jogador['vezes_jogadas']
            vezes_ganhas = jogador['vezes_ganhas']
            media_palpites = jogador['media_palpites']
            file.write(f'Nome: {nome} | vezes jogadas: {vezes_jogadas} | Vezes ganhas: {vezes_ganhas} | Media de palpites: {media_palpites:.3f}\n')
    print(f'Dados gravados com sucesso no arquivo "{filename}".')

def menu():
    filename = 'jogadores.txt'

    while True:
        print('______________________________________________________________________')
        print('                    Bem-Vindo ao Jogo do Saco!')
        print('______________________________________________________________________')
        print('       Neste Jogo,o objetivo é acertar o peso correto do saco.')
        print('                A Nossa margem de hoje é de 150gr!')
        print('              O saco pesa entre os 4,200kg à 4,350kg')
        print('           Escolha uma das opções abaixo e vamos nessa!')
        print('______________________________________________________________________')
        print('[1] - Criar, editar e eliminar ouvintes')
        print('[2] - Veja os dados de um ouvinte!')
        print('[3] - Veja o Ranking')
        print('[4] - Hora de Jogar!')
        print('[5] - Grave o seu ficheiro.')
        print('[0] - Sair')
        print('______________________________________________________________________')

        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            print('[1] - Criar novo ouvinte')
            print('[2] - Editar ouvinte existente')
            print('[3] - Eliminar ouvinte existente')
            sub_opcao = input('Escolha uma sub-opção: ')
            if sub_opcao == '1':
                nome = input('Digite o nome do ouvinte: ')
                jogadores = carregar_jogadores(filename)
                jogadores.append({'nome': nome, 'vezes_jogadas': 0, 'vezes_ganhas': 0, 'media_palpites': 0})
                inserir_jogador(filename, nome, 0, 0)
            elif sub_opcao == '2':
                nome_antigo = input('Digite o nome do ouvinte a ser editado: ')
                novo_nome = input('Digite o novo nome do ouvinte: ')
                novas_vezes_jogou = int(input('Digite o número de vezes jogadas: '))
                novas_vezes_ganhou = int(input('Digite o número de vezes ganhas: '))
                jogadores = editar_jogador(filename, nome_antigo, novo_nome, novas_vezes_jogou, novas_vezes_ganhou)
            elif sub_opcao == '3':
                nome = input('Digite o nome do ouvinte a ser eliminado: ')
                eliminar_jogador(filename, nome)
            else:
                print('Opção inválida.')
        elif opcao == '2':
            nome = input('Digite o nome do ouvinte: ')
            ver_dados_ouvinte(filename, nome)
        elif opcao == '3':
            ver_ranking(filename)
        elif opcao == '4':
            jogadores = carregar_jogadores(filename)
            peso_correto = random.uniform(4.200, 4.350)   # <-  Peso escolhido de forma random
            jogar(peso_correto, jogadores, filename)
        elif opcao == '5':
            filename = input('Digite o nome do arquivo: ')
            salvar_dados(filename, jogadores)
        elif opcao == '0':
            salvar_dados(filename, jogadores)
            print('OBRIGADA PELA SUA PARTICIPAÇÃO!')
            return
        else:
            print('ERRO - OPÇÃO INVÁLIDA')

menu()
