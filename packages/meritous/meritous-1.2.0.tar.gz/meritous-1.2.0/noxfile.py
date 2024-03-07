# noxfile.py
import nox
@nox.session(python=["3.10"])
def tests(session):
    session.run("flit", "install", "--deps=all", external=True)
    session.run("pytest", "--cov")
