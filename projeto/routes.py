from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from database import get_db_connection

def init_routes(app: Flask):

    @app.route("/")
    def home():
        if "user_id" in session:
            return render_template("index.html", usuario=session["user_name"])
        return render_template("index.html")

    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        if request.method == "POST":
            nome = request.form["nome"]
            email = request.form["email"]
            senha = request.form["senha"]

            conn = get_db_connection()
            cursor = conn.cursor()

            try:
                cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)", (nome, email, senha))
                conn.commit()
                flash("Cadastro realizado com sucesso!", "success")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("Erro: O email já está cadastrado.", "danger")
            finally:
                conn.close()

        return render_template("cadastro.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            senha = request.form["senha"]

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
            user = cursor.fetchone()
            conn.close()

            if user:
                session["user_id"] = user["id"]
                session["user_name"] = user["nome"]
                flash("Login realizado com sucesso!", "success")
                return redirect(url_for("perfil"))
            else:
                flash("Email ou senha incorretos!", "danger")

        return render_template("login.html")

    @app.route("/perfil")
    def perfil():
        if "user_id" not in session:
            flash("Você precisa estar logado para acessar essa página.", "warning")
            return redirect(url_for("login"))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nome, email FROM usuarios WHERE id = ?", (session["user_id"],))
        user = cursor.fetchone()
        conn.close()

        return render_template("perfil.html", usuario=user)

    @app.route("/logout")
    def logout():
        session.clear()
        flash("Logout realizado com sucesso!", "info")
        return redirect(url_for("home"))

    @app.route("/membros")
    def membros():
        if "user_id" not in session:
            flash("Você precisa estar logado para acessar essa página.", "warning")
            return redirect(url_for("login"))
    
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, email FROM usuarios")
        users = cursor.fetchall()
        conn.close()
    
        return render_template("membros.html", membros=users)
    