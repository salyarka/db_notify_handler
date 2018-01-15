import os
import unittest
import click

from app.manager import Manager


if os.getenv('APP_CONFIG') == 'dev':
    import coverage

    cov = coverage.coverage(
        branch=True,
        include='app/*',
        omit=[
            'app/__init__.py',
            'app/db/__init__.py'
        ]
    )
    cov.start()


@click.group()
def cli():
    pass


@click.command()
def test():
    """CLI command for tests launch.
    """
    tests = unittest.TestLoader().discover('tests')
    res = unittest.TextTestRunner(verbosity=2).run(tests)
    if res.wasSuccessful():
        exit(0)
    exit(1)


@click.command()
def coverage_test():
    """CLI command tests launch with coverage.
    """
    if os.getenv('APP_CONFIG') != 'dev':
        print('Coverage test is available only in development environment.')
        exit(1)
    tests = unittest.TestLoader().discover('tests')
    res = unittest.TextTestRunner(verbosity=2).run(tests)
    if res.wasSuccessful():
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        cov.erase()
        exit(0)
    exit(1)


@click.command()
def start():
    """CLI command for start app.
    """
    manager = Manager(os.getenv('APP_CONFIG') or 'prod')
    manager.run()

cli.add_command(test)
cli.add_command(start)

if __name__ == '__main__':
    cli()
