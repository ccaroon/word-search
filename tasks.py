from invoke import task


TEST_FILES = (
    "word_search/position.py",
    "word_search/direction.py",
)

@task
def test(ctx):

    for file in TEST_FILES:
        ctx.run(f"python -mdoctest -v {file}")
