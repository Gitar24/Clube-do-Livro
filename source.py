from flask import Flask, render_template, request, jsonify
import psycopg2
from dbconnection import get_connection

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
        return jsonify({"erro": "todos os campos sao obrigatorios"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("insert into livros(titulo, autor, genero, ano_publicacao) values(%s, %s, %s, %s)", (titulo, autor, genero, ano_publicacao))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensagem": "Livro cadastrado com sucesso!"}), 201

############################
### REGISTRO DE LEITURAS ###
############################

@app.route("/registrar_leitura")
def pagina_registrar_leitura():
    return render_template("registrar_leitura.html")

@app.route("/leituras", methods=["post"])
def registrar_leitura():
    dados = request.get_json()

    nota = dados.get("nota")
    comentario = dados.get("comentario")
    data_conclusao = dados.get("data_conclusao")
    livro_id = dados.get("livro_id")

    if not nota or not livro_id:
        return jsonify({"erro": "livro_id e nota sao obrigatórios"}), 400
 
    if int(nota) < 1 or int(nota) > 5:
        return jsonify({"erro": "a nota deve ser entre 1 e 5"}), 400

    conn = get_connection()
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
    cur.execute("select * from livros")
    livros = cur.fetchall()
    cur.close()
    conn.close()
    resultado = []
    for livro in livros:
        resultado.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "genero": livro[3]
        })
    return jsonify(resultado), 200

#############################
### LISTA DE LIVROS LIDOS ###
#############################

@app.route("/lidos", methods=["get"])
def listar_livros_lidos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select * from livros as a inner join leituras as b on a.id = b.livro_id")
    livros_lidos = cur.fetchall()
    cur.close()
    conn.close()
    resultado_lidos = []
    for livro in livros_lidos:
        resultado_lidos.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "genero": livro[3]
        })
    return jsonify(resultado_lidos), 200

#################################
### LISTA DE LIVROS NAO LIDOS ###
#################################

@app.route("/nao_lidos", methods=["get"])
def listar_livros_nao_lidos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select * from livros as a left join leituras as b on a.id = b.livro_id where b.livro_id is null")
    livros_nao_lidos = cur.fetchall()
    cur.close()
    conn.close()
    resultado_nao_lidos = []
    for livro in livros_nao_lidos:
        resultado_nao_lidos.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "genero": livro[3]
        })
    return jsonify(resultado_nao_lidos), 200

##################################
### FILTRAR POR AUTOR E GENERO ###
##################################

@app.route("/buscar", methods=["get"])
def buscar_livros():
    buscar = request.args["buscar"]
    buscar_formatado = f"%{buscar}%"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("select * from livros where autor ILIKE (%s) or genero ILIKE (%s)", (buscar_formatado, buscar_formatado))
    livros_filtrados = cur.fetchall()
    cur.close()
    conn.close()
    resultado = []
    for livro in livros_filtrados:
        resultado.append({
            "id": livro[0],
            "titulo": livro[1],
            "autor": livro[2],
            "genero": livro[3]
        })
    return jsonify(resultado), 200

if __name__=="__main__":
    app.run()