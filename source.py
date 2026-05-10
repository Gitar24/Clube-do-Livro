from flask import Flask, render_template, request, jsonify
import psycopg2
from dbconnection import get_connection

app = Flask(__name__)

##########################
### CADASTRO DE LIVROS ###
##########################

@app.route("/cadastrar_livro")
def pagina_cadastrar_livro():
    return render_template("cadastrar_livro.html")

@app.route("/livros", methods=["post"])
def cadastrar_livro():
    titulo = request.form["titulo"]
    autor = request.form["autor"]
    genero = request.form["genero"]
    ano_publicacao = request.form["ano_publicacao"]
        
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("insert into livros(titulo, autor, genero, ano_publicacao) values(%s, %s, %s, %s)", (titulo, autor, genero, ano_publicacao))
    conn.commit()
    cur.close()
    conn.close()
    return render_template("cadastrar_livro.html")

############################
### REGISTRO DE LEITURAS ###
############################

@app.route("/registrar_leitura")
def pagina_registrar_leitura():
    return render_template("registrar_leitura.html")

@app.route("/leituras", methods=["post"])
def registrar_leitura():
    print(request.form)
    nota = request.form["nota"]
    comentario = request.form["comentario"]
    data_conclusao = request.form["data_conclusao"]
    livro_id = request.form["livro_id"]
        
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("insert into leituras(nota, comentario, data_conclusao, livro_id) values(%s, %s, %s, %s)", (nota, comentario, data_conclusao, livro_id))
    conn.commit()
    cur.close()
    conn.close()
    return render_template("registrar_leitura.html")

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
    return jsonify(resultado)

if __name__=="__main__":
    app.run()