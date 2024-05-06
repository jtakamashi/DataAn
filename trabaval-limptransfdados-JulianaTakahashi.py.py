import mysql.connector
import beaupy
import os
import json
from datetime import datetime

# Função para limpar o terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def data_atual(data):   # Função para comparar uma data com a data atual
    return datetime.strptime(data, '%Y-%m-%d') > datetime.now()

def conectar_banco_dados():  # Função que permite optimizar o código, assim escuso de em todas a funções por isto e só chamo como argumento
    try:
        conn = mysql.connector.connect(user='root', host='localhost', database='pl01-operacoes-com-sql', port=3306, autocommit=True)
        return conn
    except mysql.connector.Error as e:
        print('\nErro de conexão:', e)
        return None

def ver_curso(conn):   
    try:
        cursorObject = conn.cursor()
        # Visualizar todos os cursos
        query = 'SELECT * FROM Curso'
        cursorObject.execute(query)
        cursos = cursorObject.fetchall()

        if cursos:
            print('\nCursos:')
            for curso in cursos:
                print(f'ID: {curso[0]:<2} - Curso: {curso[1]:<20}🢧  Data de Início: {curso[2]}  |  Data de Fim: {curso[3]}')
        else:
            print('\nNenhum curso encontrado')

    except mysql.connector.Error as e:
        print('\nErro ao visualizar cursos:', e)

    finally:
        cursorObject.close()

def inserir_curso(conn, nome, data_inicio, data_fim):
    cursorObject = None
    try:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
        # Inseri a condição de que os cursos não devem ter menos de 1 mês
        prazo = data_fim - data_inicio
        if prazo.days < 30:
            print('\nErro: A duração do curso deve ser de, no mínimo, 1 mês.')
            return

        # Verificar se a data de início não é a de hoje
        if not data_atual(data_inicio.strftime('%Y-%m-%d')):
            print('\nErro: A data de início não pode ser hoje.')
            return

        cursorObject = conn.cursor()
        # Insere o curso na BD
        query = 'INSERT INTO Curso (nome, data_inicio, data_fim) VALUES (%s, %s, %s)'
        values = (nome, data_inicio, data_fim)
        cursorObject.execute(query, values)

        print(f'\nRegistros inseridos: {cursorObject.rowcount}\n')

    except ValueError:
        print('\nErro: Data inserida em formato inválido. Certifique-se de usar o formato YYYY-MM-DD para as datas.')

    except mysql.connector.Error as e:
        print('\nErro ao inserir curso:', e)

    finally:
        if cursorObject:
            cursorObject.close()

def pesquisar_curso(conn):
    try:
        nome_curso = input('Indique o nome do curso que deseja procurar: ')

        cursorObject = conn.cursor()

        # Consulta o curso pelo nome
        query_curso = 'SELECT * FROM Curso WHERE nome = %s'
        cursorObject.execute(query_curso, (nome_curso,))
        curso = cursorObject.fetchone()

        if curso:
            print('\nDetalhes do Curso:')
            print(f'ID: {curso[0]} - Nome: {curso[1]}  |   Data de Início: {curso[2]}  |  Data de Fim: {curso[3]}')

            # Consultan os formandos inscritos no curso
            query_alunos = 'SELECT f.nome, f.nif FROM Formando f INNER JOIN Matricula m ON f.id = m.formando_id WHERE m.curso_id = %s'
            cursorObject.execute(query_alunos, (curso[0],))
            alunos_inscritos = cursorObject.fetchall()

            if alunos_inscritos:
                print('\nListagem de Formandos Inscritos:')
                for index, aluno in enumerate(alunos_inscritos, start=1):
                    print(f'{index} - {aluno[0]:<20}')
            else:
                print('\nO curso ainda não tem formandos.')
        else:
            print('\nCurso não encontrado.')

    except mysql.connector.Error as e:
        print('\nErro ao pesquisar curso:', e)

    finally:
        cursorObject.close()

def gestao_cursos(conn):  # Menu da gestão dos cursos
    clear_screen()
    while True:
        
        submenu = ['A) Ver Cursos', 'B) Inserir Curso', 'C) Voltar ao Menu']
        print('-'*50)
        print(' '*12 + 'Submenu - Gestão de Cursos:')
        print('-'*50)
        op_sub = beaupy.select(submenu, cursor='🢧', cursor_style='purple', return_index=True)
        if op_sub == 0:
            ver_curso(conn)
        elif op_sub == 1:
            nome = input('Nome do Curso: ')
            data_inicio = input('Data de Início (YYYY-MM-DD): ')
            data_fim = input('Data de Fim (YYYY-MM-DD): ')
            inserir_curso(conn, nome, data_inicio, data_fim)
        elif op_sub == 2:
            clear_screen() 
            break

def ver_formandos(conn):  # Retorna os formandos criados
    try:
        cursorObject = conn.cursor()

        query = 'SELECT * FROM Formando'
        cursorObject.execute(query)
        formandos = cursorObject.fetchall()

        if formandos:
            print('\nFormandos:')
            for formando in formandos:
                print(f'ID: {formando[0]:<2} | Nome: {formando[1]:<20}  |  NIF: {formando[2]}')
        else:
            print('\nNenhum formando encontrado')

    except mysql.connector.Error as e:
        print('\nErro ao visualizar formandos:', e)

    finally:
        cursorObject.close()

def inserirFormando(conn, nome, nif):
    try:
        cursorObject = conn.cursor()

        # Verifica se o formando já está inscrito
        query = 'SELECT * FROM Formando WHERE nif = %s'
        cursorObject.execute(query, (nif,))
        formando = cursorObject.fetchone()

        if formando:
            print('\nFormando já inscrito')
            return None

        # Insere o formando caso não esteja inscrito
        query = 'INSERT INTO Formando (nome, nif) VALUES (%s, %s)'
        values = (nome, nif)
        cursorObject.execute(query, values)

        # Retorna o ID do formando inserido
        return cursorObject.lastrowid

    except mysql.connector.Error as e:
        print('\nErro ao inserir formando:', e)

    finally:
        cursorObject.close()

def inserir_matricular_formando(conn):  # Validação que verifica primeiro se existem cursos para se inscreverem
    try:
        cursorObject = conn.cursor()

        current_date = datetime.now().strftime('%Y-%m-%d')
        query = 'SELECT * FROM Curso WHERE data_inicio > %s'
        cursorObject.execute(query, (current_date,))
        cursos_disponiveis = cursorObject.fetchall()

        if not cursos_disponiveis:
            print('\nNão há cursos disponíveis para matrícula.')
            return

        print(f'\nExistem {len(cursos_disponiveis)} cursos disponíveis:')
        for i, curso in enumerate(cursos_disponiveis, start=1):
            print(f"{i}. {curso[1]:<20} 🢧 Data de Início: {curso[2].strftime('%Y-%m-%d')} | Data de Fim: {curso[3].strftime('%Y-%m-%d')}")

        continuar = input('\nDeseja continuar com a inscrição/matricula? (s/n): ')
        if continuar.lower() != 's':
            return
        #  Caso exista cursos, inserir o NIF
        nif = input('\nDigite o NIF do formando: ')

        query = 'SELECT * FROM Formando WHERE nif = %s'
        cursorObject.execute(query, (nif,))
        formando = cursorObject.fetchone()

        if formando:                   #  Caso exista o NIF na BD, chama a função da matricula, caso não esteja, chama a função de inserir o novo formando.
            print('\nFormando já registrado.')
            matricular_formando_existente(conn, formando)
        else:
            nome = input('Nome do Formando: ')
            formando_id = inserirFormando(conn, nome, nif)
            if formando_id is not None:
                matricular_formando_existente(conn, (formando_id, nome, nif))

    except mysql.connector.Error as e:
        print('\nErro ao verificar formando ou cursos:', e)

def matricular_formando_existente(conn, formando):
    try:
        cursorObject = conn.cursor()

        current_date = datetime.now().strftime('%Y-%m-%d')
        query = 'SELECT * FROM Curso WHERE data_inicio > %s'
        cursorObject.execute(query, (current_date,))
        cursos_disponiveis = cursorObject.fetchall()

        print('Matricule o formando no curso:')
        # Formatação para facilitar a visualização
        cursos_formatados = [
            f"{i}. Curso: {curso[1]:<20} 🢧 Data de Início: {curso[2].strftime('%Y-%m-%d')} | Data de Fim: {curso[3].strftime('%Y-%m-%d')}"
            for i, curso in enumerate(cursos_disponiveis, start=1)
        ]
        selected_index = beaupy.select(cursos_formatados + ['Nenhum Curso'], cursor='🢧', cursor_style='green', return_index=True)

        if selected_index == len(cursos_disponiveis):
            print('Nenhum curso selecionado.')
            return

        curso_id = cursos_disponiveis[selected_index][0]
        # Insere na BD a ligação do Formando com o curso
        query = 'INSERT INTO Matricula (formando_id, curso_id) VALUES (%s, %s)'
        values = (formando[0], curso_id)
        cursorObject.execute(query, values)
        print('Matrícula realizada com sucesso!')

    except mysql.connector.Error as e:
        print('\nErro ao realizar matrícula:', e)

def pesquisar_formando(conn):
    try:
        nif_formando = input('Digite o NIF do formando a pesquisar: ')

        cursorObject = conn.cursor()

        # Consulta o formando pelo NIF
        query_formando = 'SELECT * FROM Formando WHERE nif = %s'
        cursorObject.execute(query_formando, (nif_formando,))
        formando = cursorObject.fetchone()

        if formando:
            print('\nDetalhes do Formando:')
            print(f'ID: {formando[0]} |  Nome: {formando[1]}  |  NIF: {formando[2]}')

            # Consulta os cursos em que o formando está matriculado
            query_cursos = 'SELECT c.nome, c.data_inicio, c.data_fim FROM Curso c INNER JOIN Matricula m ON c.id = m.curso_id WHERE m.formando_id = %s'
            cursorObject.execute(query_cursos, (formando[0],))
            cursos_matriculados = cursorObject.fetchall()

            if cursos_matriculados:
                print('\nCursos Matriculados:')
                for curso in cursos_matriculados:
                    print(f'Nome do Curso: {curso[0]:<20} 🢧  Data de Início: {curso[1]} | Data de Fim: {curso[2]}')
            else:
                print('\nEste formando não está matriculado em nenhum curso.')
        else:
            print('\nFormando não encontrado.')

    except mysql.connector.Error as e:
        print('\nErro ao pesquisar formando:', e)

    finally:
        cursorObject.close()

def gestao_formandos(conn): #  Menu da gestão dos formandos
    clear_screen()
    while True:
        submenu = ['A) Ver Formandos', 'B) Inserir/Matricular Formando', 'C) Voltar ao Menu']
        print('-'*50)
        print(' '*10 + 'Submenu - Gestão de Formandos:')
        print('-'*50)
        op_sub = beaupy.select(submenu, cursor='🢧', cursor_style='purple', return_index=True)
        if op_sub == 0:
            # Chama a função para ver formandos
            ver_formandos(conn)
        elif op_sub == 1:
            # Chama a função para inserir/matricular formandos
            inserir_matricular_formando(conn)
        elif op_sub == 2:
            clear_screen() 
            break
        
def exportar_para_json(conn):
    try:
        cursor = conn.cursor(dictionary=True)

        # Exportar dados da tabela Curso
        cursor.execute('SELECT * FROM Curso')
        cursos = cursor.fetchall()

        for curso in cursos:
            curso['data_inicio'] = curso['data_inicio'].strftime('%Y-%m-%d')
            curso['data_fim'] = curso['data_fim'].strftime('%Y-%m-%d')

        with open('cursos.json', 'w') as file:
            json.dump(cursos, file, indent=4)

        # Exportar dados da tabela Formando
        cursor.execute('SELECT * FROM Formando')
        formandos = cursor.fetchall()

        with open('formandos.json', 'w') as file:
            json.dump(formandos, file, indent=4)

        # Exportar dados da tabela Matricula
        cursor.execute('SELECT * FROM Matricula')
        matriculas = cursor.fetchall()

        with open('matriculas.json', 'w') as file:
            json.dump(matriculas, file, indent=4)

        print('\nDados exportados para arquivos JSON com sucesso!')

    except mysql.connector.Error as e:
        print('\nErro ao exportar dados para JSON:', e)

    finally:
        cursor.close()


def main():
    conn = conectar_banco_dados()
    if conn:
        clear_screen()  # Limpa o terminal antes de mostrar o menu pela primeira vez
        listMenus = ['1 - Gestão de Cursos', '2 - Gestão de Formandos', '3 - Pesquisar Curso', '4 - Pesquisar Formando', '5 - Sair']

        while True:
            print('-'*50)
            print(' '*21 + 'MENU')
            print('-'*50)
            op = beaupy.select(listMenus, cursor='🢧', cursor_style='blue', return_index=True) + 1
            if op == 1:
                gestao_cursos(conn)
            elif op == 2:
                gestao_formandos(conn)
            elif op == 3:
                pesquisar_curso(conn)
            elif op == 4:
                pesquisar_formando(conn)
            elif op == 5:
                clear_screen()
                exportar_para_json(conn)
                print('-'*50)
                print(' '*7 + 'Obrigada por usar o nosso Programa!')
                print('-'*50)
                break

        conn.close()

if __name__ == "__main__":
    main()
