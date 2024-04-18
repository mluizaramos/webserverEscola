from django.shortcuts import render, redirect
from django.http import HttpResponse
from hashlib import sha256
from .models import Professor, Turma, Atividade
from django.db import connection, transaction
from django.contrib import messages
from django.db.utils import IntegrityError


def initial_population():
    print ("Vou Popular")

    cursor = connection.cursor()
    print("aqui kakk")

    # senha="123456"
    # senha_armazenar = sha256(senha.encode()).hexdigest()

    #  professor ---------------------------------------------------------------------------------------------
    # insert_sql_professor = "INSERT INTO App_Escola_professor (nome, email, senha) VALUES"
    # insert_sql_professor = insert_sql_professor + "('Prof. Barak Obama', 'barak.obama@gmail.com', '" + senha_armazenar + "'),"
    # insert_sql_professor = insert_sql_professor + "('Prof. Angela Merkel', 'angela.merkel@gmail.com', '" + senha_armazenar + "'),"
    # insert_sql_professor = insert_sql_professor + "('Prof. Xi Jinping', 'xi.jinping@gmail.com', '" + senha_armazenar + "')"

    # print("Professores inseridos")
    # cursor.execute(insert_sql_professor)
    # transaction.atomic()

    # turma ----------------------------------------------
    # insert_sql_turma = "INSERT INTO App_Escola_turma (nome_turma, id_professor_id) VALUES"
    # insert_sql_turma = insert_sql_turma + "('1o Semestre - Adminstração', 4), "
    # insert_sql_turma = insert_sql_turma + "('2o Semestre - Mecatrônica', 4), "
    # insert_sql_turma = insert_sql_turma + "('3o Semestre - Manufatura', 4)"

    # try:
    #     cursor.execute(insert_sql_turma)
    #     transaction.commit()
    #     print("Atividades inseridas com sucesso.")

    # except IntegrityError as e:
    #     print("Erro ao inserir atividades:", e)
    #     transaction.rollback()

    # print("Turmas inseridas com sucesso.")

    # # Atividade --------------------------------------------
    # insert_sql_atividade = "INSERT INTO App_Escola_atividade (nome_atividade, id_turma_id) VALUES"
    # insert_sql_atividade = insert_sql_atividade + "('Apresentar Fundamentos da Segurança', 250), "
    # insert_sql_atividade = insert_sql_atividade + "('Apresentar Django e DB', 250), "
    # insert_sql_atividade = insert_sql_atividade + "('Apresentar Projetos de IA', 250)"

    # cursor.execute(insert_sql_atividade)
    # transaction.commit()

    # print("Atividades inseridas com sucesso.")

    # print("Populei")

# abrir index--------------------------------------------------------
def abre_index(request):
    dado_pesquisa = 'Obama'
    verifica_populado =  Professor.objects.filter(nome__icontains=dado_pesquisa)

    if len(verifica_populado) == 0:
        print("Não está populado")
        initial_population()
    else:
        print("Achei Obama", verifica_populado)

    return render(request, 'Login.html')

# enviar login --------------------------------------------------------
def enviar_login(request):
    if (request.method == 'POST'):
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
        dados_professor = Professor.objects.filter(email=email).values("nome","senha","id")
        print("Dados do professor ", dados_professor)

        if dados_professor:
            senha = dados_professor[0]
            senha = senha ['senha']
            usuario_logado = dados_professor[0]
            usuario_logado = usuario_logado['nome']
            #return render(request, 'Index.html', {'usuario_logado': usuario_logado})
            print("user log, " , usuario_logado)
            
            if (senha == senha_criptografada):
                # messages.info(request, 'Bem-vindo.')

                id_logado = dados_professor[0]
                id_logado = id_logado['id']
                turmas_do_professor = Turma.objects.filter(id_professor=id_logado)
                print("Turmas do professor:", turmas_do_professor)
                return render(request, 'Cons_Turma_Lista.html', {'usuario_logado': usuario_logado, 'turmas_do_professor':turmas_do_professor, 'id_logado':id_logado})
            
            else:
                messages.info(request, "Usuario ou senha incorretos. Tente novamente")
                return render(request, 'Login.html')
            
        messages.info(request, f'Olá {email}, seja bem-vindo! Percebemos que você é novo por aqui. Complete seu cadastro')
        return render(request, 'Cadastro.html', {'login':email})
    

# confirmar cadastro-------------------------------------------------------------
def confirmar_cadastro(request):
    if (request.method == 'POST'):
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        senha_criptografada = sha256(senha.encode()).hexdigest()
       
        grava_professor = Professor(
            nome=nome,
            email=email,
            senha=senha_criptografada
        )
        grava_professor.save()
        
        return render(request, 'Index.html')


def cad_turmas(request, id_professor):
    usuario_logado = Professor.objects.filter(id=id_professor).values("nome","id")
    usuario_logado = usuario_logado[0]
    usuario_logado = usuario_logado['nome']

    print("user log " , usuario_logado)
        
    return render(request, 'Cad_Turmas.html', {'usuario_logado': usuario_logado, 'id_logado':id_professor})
    

def salvar_turma_nova(request):
    if (request.method == 'POST'):
        nome_turma = request.POST.get('nome_turma')
        id_professor = request.POST.get('id_professor')
        
        professor = Professor.objects.get(id=id_professor)
       
        grava_turma = Turma(
            nome_turma = nome_turma,
            id_professor = professor
        )
        grava_turma.save()
        messages.info(request, 'Turma ' + nome_turma + ' cadastrado com sucesso.')

        return redirect('lista_turma', id_professor=id_professor) #redirect
        

def lista_turma(request, id_professor):
    dados_professor = Professor.objects.filter(id=id_professor).values("nome","id")
    usuario_logado = dados_professor[0]
    usuario_logado = usuario_logado['nome']
    id_logado = dados_professor[0]
    id_logado = id_logado['id']
    turmas_do_professor = Turma.objects.filter(id=id_logado)
        
    return render(request, 'Cons_Turma_Lista.html', {'usuario_logado': usuario_logado, 'turmas_do_professor': turmas_do_professor,'id_logado':id_logado})


#---------------------------------------

def cad_atividade(request, id_turma):
    nome_turma = Turma.objects.get(id=id_turma).nome_turma
    return render(request, 'Cad_Atividade.html', {'nome_turma': nome_turma, 'id_turma': id_turma})

def salvar_atividade_nova(request):
    if request.method == 'POST':
        id_turma = request.POST.get('id_turma')
        nome_atividade = request.POST.get('nome_atividade')
        
        turma = Turma.objects.get(id=id_turma)
       
        grava_atividade = Atividade(
            nome_atividade=nome_atividade,
            id_turma=turma
        )
        grava_atividade.save()
        messages.info(request, f'Atividade {nome_atividade} cadastrada com sucesso.')
        return redirect('lista_atividade', id_turma=id_turma)

def lista_atividade(request, id_turma):
    turma = Turma.objects.get(id=id_turma)
    atividades_da_turma = Atividade.objects.filter(id_turma=turma)
    return render(request, 'Cons_Atividade_Lista.html', {'turma_logada': turma.nome_turma, 'atividades_da_turma': atividades_da_turma, 'id_turma': id_turma})



