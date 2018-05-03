import click
from flask_migrate import Migrate
from app import create_app, db

app = create_app('dev_mysql')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db)


@app.cli.command()
def initdb_dev():
    # Creation University
    from app.api.v1.users.models import University
    univ_a = University(code=1, name='에이대학교', domain='auniv.ac.kr')
    univ_b = University(code=2, name='비이대학교', domain='buniv.ac.kr')
    univ_c = University(code=3, name='씨이대학교', domain='cuniv.ac.kr')
    univ_d = University(code=4, name='디이대학교', domain='duniv.ac.kr')
    db.session.add(univ_a)
    db.session.add(univ_b)
    db.session.add(univ_c)
    db.session.add(univ_d)
    db.session.commit()

    # Creation boards
    from app.api.v1.boards.models import Board
    ''' title = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(128), nullable=False)'''
    board_free = Board(title='자유게시판', description='모두의 게시판')
    board_a = Board(title='에이대학교', description='에이 대학교')
    board_b = Board(title='비이대학교', description='비이 대학교')
    board_c = Board(title='씨이대학교', description='씨이 대학교')
    board_d = Board(title='디이대학교', description='디이 대학교')
    db.session.add(board_free)
    db.session.add(board_a)
    db.session.add(board_b)
    db.session.add(board_c)
    db.session.add(board_d)
    db.session.commit()
