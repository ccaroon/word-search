from invoke import task


TEST_FILES = (
    "word_search/position.py",
    "word_search/direction.py",
)

@task
def test(ctx):

    for file in TEST_FILES:
        ctx.run(f"python -mdoctest -v {file}")


PEOPLE = {
    # NAME   (THEME, NUDGE-VALUE)
    "bryce": ("christmas", 0.30),
    "cole": ("gingerbread house", 0.0),
    "mason": ("santa claus", -0.25),
    "nathan": ("winter", 0.30)
}
@task
def pdf(ctx, name):
    """
    Generate a Christmas WordSearch for `name` person.
    """
    person_data = PEOPLE.get(name)
    if person_data:
        base_path = f"~/Documents/Christmas-WordSearches/{name}"
        word_list = f"{base_path}/words.txt"
        filler = name
        theme = person_data[0]
        title = " ".join([word.capitalize() for word in theme.split(" ")])
        # theme.capitalize()
        nudge = person_data[1]
        padding = 2
        bg_image = f"{base_path}/background-image.png"
        outfile = f"{base_path}/{name.capitalize()}.pdf"

        ctx.run(f"./generate.py {word_list} --filler {filler} --title '{title}' --padding {padding} --bg-image {bg_image} --output {outfile} --nudge {nudge}")
    else:
        print(f"=> Unknown Person: '{name}'")
