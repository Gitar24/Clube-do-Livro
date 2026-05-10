from flask import Flask, render_template, request, jsonify
import psycopg2
from dbconnection import get_connection

app = Flask(__name__)

@app.route("/interface_cadastrar_livros")
def homepage():
    return render_template("cad_livros.html")

@app.route("/cadastrar_livros", methods=["post"])
def cadastrar_livros():
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
    return render_template("cad_livros.html")

@app.route("/listar_livros", methods=["get"])
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