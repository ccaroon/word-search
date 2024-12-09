from invoke import task


TEST_FILES = (
    "word_search/position.py",
)

@task
def test(ctx):

    for file in TEST_FILES:
        ctx.run(f"python -mdoctest {file}")
