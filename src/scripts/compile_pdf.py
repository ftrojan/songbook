from typeset import utils


name = "all_of_me"
profile = utils.get_profile(name)
print(profile)
utils.create_pdf(name, profile)
