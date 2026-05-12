from flask import Flask, render_template, request, jsonify
import psycopg2
from database.dbconnection import get_connection

app = Flask(__name__)
@app.route("/")
def homepage():
    return render_template("/index.html")
    
##########################
### CADASTRO DE LIVROS ###
##########################

@app.route("/cadastrar_livro")
def pagina_cadastrar_livro():
    return render_template("cadastrar_livro.html")

@app.route("/livro", methods=["post"])
def cadastrar_livro():
    dados = request.get_json()

    titulo = dados.get("titulo")
    autor = dados.get("autor")
    genero = dados.get("genero")
    ano_publicacao = dados.get("ano_publicacao")

    if not titulo or not autor or not genero or not ano_publicacao:
        return jsonify({"erro": "todos os campos sao obrigatorio"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("insert into livros(titulo, autor, genero, ano_publicacao) values(%s, %s, %s, %s)", (titulo, autor, genero, ano_publicacao))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": "Livro cadastrado com sucesso!"}), 201

############################
### REGISTRO dos.get("comentario")
    data_conclusao = dados.get("data_conclusao")
    livro_id = dados.get("livro_id")

    if not livro_id or not nota:
        return jsonify({"erro": "livro_id e nota sao obrigatorios"}), 400
    if int(nota) <1 or int(nota) >5:
        return jsonify({"erro": "nota deve ser entre 1 e 5"}), 400

    if comentario == "":
        comentario = None
        
    if data_conclusao == "":
        data_conclusao = None

    conDE LEITURAS ###
############################

@app.route("/registrar_leitura")
def pagina_registrar_leitura():
    return render_template("registrar_leitura.html")

@app.route("/leituras", methods=["post"])
def registrar_leitura():
    dados = request.get_json()
    nota = dados.get("nota")
    comentario = dan = get_connection()
    cur = conn.cursor()
    cur.execute("insert into leituras(nota, comentario, data_conclusao, livro_id) values(%s, %s, %s, %s)", (nota, comentario, data_conclusao, livro_id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": "Leitura registrada com sucesso!"}), 201

#######################
### LISTA DE LIVROS ###
#######################

@app.route("/lista", methods=["get"])
def listar_livros():
    conn = get_connection()
    cur = conn.cursor()
    query = "select l.id, l.titulo, l.autor, l.genero, l.ano_publicacao, le.id from livros l left join leituras le on l.id = le.livro_id"
    cur.execute(query)
    livros = cur.fetchall()
    cur.close()
    conn.close()
    resultado = []
    for livro in livros:
        status_texto = "Nao Lido" if livro[5] is None else "Lido"
        resultado.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "genero": livro[3],
            "ano_publicacao": livro[4],
            "status": status_texto
        })
    return jsonify(resultado), 200

#############################
### LISTA DE LIVROS LIDOS ###
#############################

@app.route("/lidos", methods=["get"])
def listar_livros_lidos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select * from livros l inner join leituras le on l.id = le.livro_id")
    livros_lidos = cur.fetchall()
    cur.close()
    conn.close()
    resultado_lidos = []
    for livro in livros_lidos:
        resultado_lidos.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "genero": livro[3],
            "ano_publicacao": livro[4],
            "status": "Lido"
        })
    return jsonify(resultado_lidos), 200

#################################
### LISTA DE LIVROS NAO LIDOS ###
#################################

@app.route("/nao_lidos", methods=["get"])
def listar_livros_nao_lidos():
    conn = get_connection()
    cur = conn.cursor()
    query = "select * from livros l left join leituras le on l.id = le.livro_id where le.livro_id is null"
    cur.execute(query)
    livros_nao_lidos = cur.fetchall()
    cur.close()
    conn.close()
    resultado_nao_lidos = []
    for livro in livros_nao_lidos:
        resultado_nao_lidos.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "genero": livro[3],
            "ano_publicacao": livro[4],
            "status": "Nao Lido"
        })
    return jsonify(resultado_nao_lidos), 200

##################################
### BUSCAR POR AUTOR E GENERO ###
##################################

@app.route("/buscar", methods=["get"])
def buscar_livros():
    buscar = request.args["buscar"]
    buscar_formatado = f"%{buscar}%"
    conn = get_connection()
    cur = conn.cursor()
    query = "select l.id, l.titulo, l.autor, l.genero, l.ano_publicacao, le.id from livros l left join leituras le on l.id = le.livro_id"
    cur.execute(query, (buscar_formatado, buscar_formatado))
    livros_filtrados = cur.fetchall()
    cur.close()
    conn.close()
    resultado = []
    for livro in livros_filtrados:
        status_texto = "Lido" if livro[5] is not None else "Nao Lido"
        resultado.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "genero": livro[3],
            "ano_publicacao": livro[4],
            "status": status_texto
        })
    return jsonify(resultado), 200

#####################
### RECOMENDACOES ###
#####################

@app.route("/recomendacoes")
def recomendar_livros():
    conn = get_connection()
    cur = conn.cursor()
    query = "select * from livros where (genero, autor) in (select l.genero, l.autor  from livros l join leituras r on l.id = r.livro_id group by l.genero, l.autor  order by avg(r.nota) desc limit 1) and id not in (select livro_id from leituras)"
    cur.execute(query)
    livros_recomendados = cur.fetchall()
    cur.close()
    conn.close()
    resultado = []
    for livro in livros_recomendados:
        resultado.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "genero": livro[3],
            "ano_publicacao": livro[4],
            "status": "Recomendado"
        })
    return jsonify(resultado), 200

if __name__=="__main__":
    app.run()