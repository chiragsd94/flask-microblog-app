from flask import Blueprint, render_template, redirect, url_for


from app.extension import db
from app.models import Article
from app.forms import ArticleForm

router = Blueprint("article_route", __name__, template_folder="templates")


@router.route("/")
def index():
    articles = Article.query.all()
    return render_template("home.html", articles=articles)


@router.route("/create", methods=["GET", "POST"])
def create():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data, content=form.content.data)
        db.session.add(article)
        db.session.commit()
        return redirect(url_for("article_route.index"))
    return render_template("create.html", form=form)


@router.route("/article/<int:article_id>")
def article_detail(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template("article_detail.html", article=article)


@router.route("/article/<int:article_id>/edit", methods=["GET", "POST"])
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    form = ArticleForm(obj=article)
    if form.validate_on_submit():
        form.populate_obj(article)
        db.session.commit()
        return redirect(url_for("article_route.article_detail", article_id=article.id))
    return render_template("edit_article.html", form=form, article=article)


@router.route("/article/<int:article_id>/delete", methods=["POST"])
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for("article_route.index"))


@router.route("/about")
def about():
    return render_template("about.html")
